#!/usr/bin/env python

"""Present the form to the user and collect input"""

import wx

class MainFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1)
        self.panel = CollapsibleForm(self)
        self.Show(True)
    

class CollapsibleForm(wx.Panel):
    """A Frame  with several collapsible sections that contain
    parts of the form"""
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)

        ## contents of the panel
         # title at top
         # button at bottom
         # collpasible panes in between
        self.title = wx.StaticText(self, label="Fill in the values")
        
        self.cp1 = wx.CollapsiblePane(self, label='Demographics',
                                      style=wx.CP_DEFAULT_STYLE|wx.CP_NO_TLW_RESIZE)
        self.make_pane_content(self.cp1.GetPane())
        
        self.btn = wx.Button(self, label='Press me')

        self._layout()
        self._setbindings()

        self.Show(True)
        
    def _layout(self):
        """Layout the controls using sizers"""
        sizer = wx.BoxSizer(wx.VERTICAL)

        sizer.Add(self.title, 0, wx.ALL, 25)
        sizer.Add(self.cp1, 0, wx.RIGHT|wx.LEFT|wx.EXPAND, 25)
        sizer.Add(self.btn, 0, wx.ALL, 25)

        self.SetSizer(sizer)


    def _setbindings(self):
        """All the bindings will be set up here"""
        self.Bind(wx.EVT_COLLAPSIBLEPANE_CHANGED, self.on_panechanged, self.cp1)
        

    def on_panechanged(self, event):
        self.Layout()
        
        
    def make_pane_content(self, pane):
        """Put in the contents of the pane"""
        namelbl = wx.StaticText(pane, -1, "Name")
        name = wx.TextCtrl(pane, -1, "")

        agelbl = wx.StaticText(pane, -1, "Age")
        age = wx.TextCtrl(pane, -1, "")

        sizer = wx.FlexGridSizer(cols=2, hgap=5, vgap=5)
        sizer.AddGrowableCol(1)
        sizer.Add(namelbl, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(name, 0, wx.EXPAND)
        sizer.Add(agelbl, 0 , wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(age, 0, wx.EXPAND)

        pane.SetSizer(sizer)
        


if __name__ == '__main__':
    app = wx.App()
    f = MainFrame(None)
    app.MainLoop()
