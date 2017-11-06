#-*- coding:utf-8 -*-
#----------------------------------------
# Purpose: 主函数+主框架
#  Author: puwow
#   CDate: 2017.11.05
#----------------------------------------

import os
import wx
import wx.html
import markdown
import logging
from wx.py.editwindow import EditWindow
from simple import SimpleMaven
from control import EditDialog,MyLogHandler

TREE_DATA_XML=os.path.join(os.getcwd(),"TreeData.xml")
__version__='v1.0.0'
class MainFrame( wx.Frame ):
    #主框架类
    def __init__( self, parent=None, title=u'简单Maven', pos=wx.DefaultPosition, \
            size=(800,600), style=wx.DEFAULT_FRAME_STYLE^wx.RESIZE_BORDER, name='mainFrame' ):
        wx.Frame.__init__( self, parent=parent, title=title, pos=pos, size=size, \
                style=style, name=name )

        self.SetBackgroundColour("gray")
        self.createStatusBar()
        self.createMenuBar()

        self.tree = wx.TreeCtrl( self, id=wx.NewId(), size=(300,-1), style=wx.TR_HAS_BUTTONS|wx.TR_LINES_AT_ROOT )
        self.tree.SetBackgroundColour("light gray")

        self.html = wx.html.HtmlWindow(self)
        self.html.SetHTMLBackgroundColour("medium goldenrod")

        self.log = EditWindow( self )
        #self.log.SetReadOnly(True)
        self.log.setDisplayLineNumbers(True)
        handler = MyLogHandler( "root", control=self.log )
        logging.getLogger().setLevel(logging.INFO)
        logging.getLogger().addHandler(handler)

        vbox = wx.BoxSizer( wx.VERTICAL )
        box = wx.BoxSizer( wx.HORIZONTAL )
        box.Add( self.tree, -1, wx.EXPAND|wx.RIGHT, 3 )
        box.Add( self.html, 2, wx.EXPAND, 3 )
        vbox.Add( box, 5, wx.EXPAND|wx.ALL, 3 )
        vbox.Add( self.log, 1, wx.EXPAND|wx.RIGHT|wx.LEFT|wx.BOTTOM, 3 ) 
        self.SetSizer( vbox )

        #创建SimpleMaven对象，加载TreeData.xml文件
        self.simpleMaven = SimpleMaven()
        wx.CallAfter( self.DataInit, controls=self.tree )

        self.Bind( wx.EVT_TREE_ITEM_RIGHT_CLICK, self.OnTreeRightClick, self.tree )
        self.Bind( wx.EVT_TREE_SEL_CHANGED, self.OnTreeChanged, self.tree )

    def createStatusBar( self ):
        #创建状态栏
        statusBar = self.CreateStatusBar(3)
        statusBar.SetStatusWidths([-1,-2,-3])
        statusBar.SetStatusText(__version__, 0 )
        statusBar.SetStatusText(__file__, 1 )
    def createMenuBar( self ):
        menuBar = wx.MenuBar()
        #工具菜单
        menuTool = wx.Menu()
        edit_tree_data = menuTool.Append(wx.MenuItem( menuTool, id=wx.NewId(), text="文件预览", helpString="查看TreeData.xml文件" ) )
        self.Bind( wx.EVT_MENU, self.OnEditTreeData, edit_tree_data )
        menuBar.Append(menuTool, "&工具" )

        self.SetMenuBar(menuBar)
    #事件处理
    def OnTreeChanged( self, event ):
        if event.GetItem() == event.GetEventObject().GetRootItem():
            with open( "README.md" ) as fp:
                self.html.SetPage(markdown.markdown(fp.read().decode("UTF-8")))
        else:
            self.html.SetPage( event.GetEventObject().GetItemData(event.GetItem()) )
            logging.info(event.GetEventObject().GetItemData(event.GetItem()) )
    def OnEditTreeData( self, event ):
        parentSize=self.GetClientSize()
        edit = EditDialog(self, size=(parentSize[0]*0.8,parentSize[1]*0.8), title="文件预览")
        edit.SetReadOnly()
        edit.CenterOnParent()
        ret = edit.ShowModal()
        if ret == wx.ID_CANCEL:
            edit.Destroy()
    def DataInit( self, controls=None ):
        if controls is not None:
            if isinstance(controls, wx.TreeCtrl):
                self.simpleMaven.parseTree( controls, xmlFile=TREE_DATA_XML )
        with open( "README.md" ) as fp:
            txt = markdown.markdown(fp.read().decode("UTF-8"))
            self.html.SetPage(txt)
    def OnTreeRightClick( self, event ):
        if not hasattr( self, "addNodeId" ):
            self.addNodeId = wx.NewId()
            self.removeNodeId = wx.NewId()
            self.changeNodeId = wx.NewId()
            self.Bind( wx.EVT_MENU, self.OnAddNode, id=self.addNodeId )
            self.Bind( wx.EVT_MENU, self.OnRemoveNode, id=self.removeNodeId )
            self.Bind( wx.EVT_MENU, self.OnChangeNode, id=self.changeNodeId )
        menu = wx.Menu()
        menu.Append( wx.MenuItem(menu, id=self.addNodeId, text="添加子节点") )
        menu.Append( wx.MenuItem(menu, id=self.removeNodeId, text="删除子节点") )
        menu.Append( wx.MenuItem(menu, id=self.changeNodeId, text="修改字节点") )
        self.PopupMenu( menu, event.GetPoint() )
        menu.Destroy()
    def OnAddNode( self, event ):
        print self.tree.GetSelection()
    def OnRemoveNode( self, event ):
        pass
    def OnChangeNode( self, event ):
        pass

if __name__ == '__main__':
    app = wx.App()
    frame = MainFrame(parent=None, size=(960,640), style=wx.DEFAULT_FRAME_STYLE)
    frame.CenterOnParent()
    frame.Show()
    app.SetTopWindow(frame)
    app.MainLoop()
