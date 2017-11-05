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
from simple import SimpleMaven
from control import EditDialog

TREE_DATA_XML=os.path.join(os.getcwd(),"TreeData.xml")
__version__='v1.0.0'
print TREE_DATA_XML
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

        box = wx.BoxSizer( wx.HORIZONTAL )
        box.Add( self.tree, -1, wx.EXPAND|wx.ALL, 3 )
        box.Add( self.html, 2, wx.EXPAND|wx.RIGHT|wx.TOP|wx.BOTTOM, 3 )
        self.SetSizer( box )

        #创建SimpleMaven对象，加载TreeData.xml文件
        self.simpleMaven = SimpleMaven()
        wx.CallAfter( self.DataInit, controls=self.tree )

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


if __name__ == '__main__':
    app = wx.App()
    frame = MainFrame(parent=None, size=(960,640), style=wx.DEFAULT_FRAME_STYLE)
    frame.CenterOnParent()
    frame.Show()
    app.SetTopWindow(frame)
    app.MainLoop()
