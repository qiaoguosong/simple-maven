#-*- coding:utf-8 -*-

import os
import wx
from simple import SimpleMaven

TREE_DATA_XML=os.path.join(os.getcwd(),"TreeData.xml")
__version__='v1.0.0'
print TREE_DATA_XML
class MainFrame( wx.Frame ):
    #主框架类
    def __init__( self, parent=None, title=u'简单Maven', pos=wx.DefaultPosition, \
            size=(800,600), style=wx.DEFAULT_FRAME_STYLE^wx.RESIZE_BORDER, name='mainFrame' ):
        wx.Frame.__init__( self, parent=parent, title=title, pos=pos, size=size, \
                style=style, name=name )

        self.createStatusBar()
        self.createMenuBar()

        self.tree = wx.TreeCtrl( self, id=wx.NewId(), style=wx.TR_HAS_BUTTONS|wx.TR_LINES_AT_ROOT )
        self.panel = wx.Panel( self, -1 )

        box = wx.BoxSizer( wx.HORIZONTAL )
        box.Add( self.tree, 1, wx.EXPAND|wx.ALL, 3 )
        box.Add( self.panel, 2, wx.EXPAND|wx.ALL, 3 )
        self.SetSizer( box )

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
        self.SetMenuBar(menuBar)
    def DataInit( self, controls=None ):
        if controls is not None:
            if isinstance(controls, wx.TreeCtrl):
                self.simpleMaven.parseTree( controls, xmlFile=TREE_DATA_XML )


if __name__ == '__main__':
    app = wx.App()
    frame = MainFrame(parent=None)
    frame.CenterOnParent()
    frame.Show()
    app.SetTopWindow(frame)
    app.MainLoop()
