#-*- coding:utf-8 -*-
#----------------------------------------
# Purpose: 用于子类化wxPython的窗口控件
#  Author: puwow
#   CDate: 2017.11.06
#----------------------------------------

import wx
from wx.py.editwindow import EditWindow

class EditDialog( wx.Dialog ):
    #编辑器
    def __init__( self, parent=None, id=-1, title='编辑工具', pos=wx.DefaultPosition, size=(800,600), style=wx.DEFAULT_DIALOG_STYLE, name="edit" ):
        wx.Dialog.__init__( self, parent=parent, id=id, title=title, pos=pos, size=size, style=style, name=name )
        self.edit = edit = EditWindow( self )
        edit.setDisplayLineNumbers(True)
        with open("TreeData.xml") as fp:
            edit.SetText( fp.read())
    def SetReadOnly( self, flag=True ):
        self.edit.SetReadOnly(flag)


if __name__ == '__main__':
    app = wx.App()
    dialog = EditDialog()
    dialog.CenterOnParent()
    ret = dialog.ShowModal()
    if ret == wx.ID_CANCEL:
        dialog.Destroy()
    app.MainLoop()
