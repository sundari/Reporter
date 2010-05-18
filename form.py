#!/usr/bin/env python

"""Present the form to the user and collect input"""

import wx
import sys
import yaml


class Collector(wx.Frame):
    def __init__(self, parent, fields_file):
        """Read the file containing fields,
        display the controls, collect the information
        and return values as dictionary"""
        wx.Frame.__init__(self, parent, -1, 'Fill in the values', size=(450, 300))
        self.fields_file = fields_file
        scroll=wx.ScrolledWindow(self,-1)
        self.scroll=scroll
        #panel=wx.Panel(scroll,-1)

        self.panel = wx.Panel(scroll, -1)
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        self.fields = self.get_fields()

        fgs = wx.FlexGridSizer(len(self.fields)+1, 2, 2, 2)
        fgs.AddMany(self.make_widget_list(self.fields))
        fgs.AddGrowableCol(1, 1)
        hbox.Add(fgs, 1, wx.ALL | wx.EXPAND, 15)
        self.panel.SetSizer(hbox)

        self.panel.SetAutoLayout(True)
        self.panel.Layout()
        self.panel.Fit()
        
        self.unit=20
        width,height=self.panel.GetSizeTuple()
        
        scroll.SetScrollbars(self.unit, self.unit, width/self.unit, height/self.unit)
        # if (width>600): width=600
        # if (height>800): height=800
        # print width, height
        #self.SetSize((width,height))
        #self.panel.SetSize((360, 500))

        self.CreateStatusBar()
        self.Centre()
        self.MakeModal(True)
        self.Show(True)

    def get_fields(self):
        """Read the fields file and use yaml to load the fields"""
        fields = yaml.load(open(self.fields_file))
        return fields

    def read_values(self):
        """read the values from each control"""
        field_values = {}

        for ct in range(len(self.fields)):
            label = self.fields[ct][0]
            widget = self.widgets[ct]

            field_values[label] = widget.GetValue()

        print field_values
        
    def focusGain(self,event):
        """part of scrolled window functionality"""
        w=self.FindWindowById(event.GetId())
        x,y=w.GetPositionTuple()
        hx,hy=w.GetSizeTuple()
        cx,cy=self.scroll.GetClientSizeTuple()
        sx,sy=self.scroll.GetViewStart()
        sx=sx*20
        sy=sy*20

        if (y<sy):
            self.scroll.Scroll(0,y/self.unit)
        if (x<sx):
            self.scroll.Scroll(0,-1)
        if ((x+sx)>cx):
            self.scroll.Scroll(0,-1)
        if ((y+hy-sy)>cy):
            self.scroll.Scroll(0,y/self.unit)

        event.Skip()


    def make_widgetlist(self, fields):
        """From the field list, make a list of widgets
        which can be directly passed to the constructor for
        flexgridsizer"""
        self.labels = []
        self.widgets = []

        for i in range(len(fields)):
            f = fields[i]
            self.labels.append(wx.StaticText(self.panel, -1, f[0],
                                             style=wx.ALIGN_CENTER_VERTICAL))
            widget_type = f[1]
            if widget_type == 'text':
                self.widgets.append(wx.TextCtrl(self.panel, -1))
            elif widget_type == 'spin':
                self.widgets.append(wx.SpinCtrl(self.panel, -1,
                                                min=f[2], max=f[3], initial=f[4]))
            elif widget_type == 'combo':
                self.widgets.append(wx.ComboBox(self.panel, -1, choices=f[2]))

        done_button = wx.Button(self.panel, -1, "Done")
        quit_button = wx.Button(self.panel, wx.ID_EXIT, "Quit")

        done_button.Bind(wx.EVT_BUTTON, self.OnDone)
        quit_button.Bind(wx.EVT_BUTTON, self.OnQuit)
        self.Bind(wx.EVT_CLOSE, self.OnQuit)

        widget_list = []
        for l, w in zip(self.labels, self.widgets):
            widget_list.append((l))
            widget_list.append((w, 1, wx.EXPAND))

            wx.EVT_SET_FOCUS(w,self.focusGain)
            
        widget_list += [(done_button), (quit_button)]

        return widget_list
        
    def OnDone(self, event):
        self.get_values()

    def OnQuit(self, event):
        sys.exit(0)
        

if __name__ == "__main__":
    # test values
    fields_file = 'input_fields.yaml'
    app = wx.App()
    Collector(None, fields_file)
    app.MainLoop()
