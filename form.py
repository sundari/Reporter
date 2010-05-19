#!/usr/bin/env python

"""Present the form to the user and collect input"""

import wx
import yaml

class Form(wx.Frame):
    def __init__(self, parent, fields_file):
        wx.Frame.__init__(self, parent, -1)
        self.panel = FormPanel(self, fields_file)
        self.Show(True)

    def collect_values(self):
        """collect all the values from the different collapsible panels"""
        self.vals = {}
        for pane in self.panels.panes:
            self.vals.update(pane.get_values())

class FormPanel(wx.Panel):
    """A Frame  with several collapsible sections that contain
    parts of the form"""
    def __init__(self, parent, fields_file):
        wx.Panel.__init__(self, parent, -1)

        ## contents of the panel
         # title at top
         # button at bottom
         # collpasible panes in between
        self.title = wx.StaticText(self, label="Fill in the values")
        
        # self.cp1 = wx.CollapsiblePane(self, label='Demographics',
        #                               style=wx.CP_DEFAULT_STYLE|wx.CP_NO_TLW_RESIZE)
        # Panes will be constructed from yaml file
        self.panes = []
        self.construct_panes(fields_file)
        #self.make_pane_content(self.cp1.GetPane())
        
        self.btn = wx.Button(self, label='Press me')

        self._layout()

        self.Show(True)
        
    def _layout(self):
        """Layout the controls using sizers"""
        sizer = wx.BoxSizer(wx.VERTICAL)

        sizer.Add(self.title, 0, wx.ALL, 25)

        for cp in self.panes:
            sizer.Add(cp, 0, wx.RIGHT|wx.LEFT|wx.EXPAND, 25)

        sizer.Add(self.btn, 0, wx.ALL, 25)

        self.SetSizer(sizer)


    def on_panechanged(self, event):
        print 'laying out'
        self.Layout()

    def construct_panes(self, fields_file):
       """Read the fields file and use the data to construct the
       collapsible panes"""
       fields_data = yaml.load_all(open(fields_file))
       for pane_data in fields_data:
           self.panes.append(Pane(self, pane_data))
       self.Layout()

class Pane(wx.CollapsiblePane):
    """Individual collapsible pane which can construct the controls,
    build the pane and read the values out"""
    def __init__(self, parent, pane_data):
        """pane_data is the data defining the controls in the form of
        a dictionary read from the yaml file"""
        self.panel = parent
        
        self.name = pane_data.keys()[0]
        self.pane_data = pane_data[self.name]

        wx.CollapsiblePane.__init__(self, parent, label=self.name,
                                    style=wx.CP_DEFAULT_STYLE|wx.CP_NO_TLW_RESIZE)
        widget_list =  self.make_content()

        self.Bind(wx.EVT_COLLAPSIBLEPANE_CHANGED, self.on_collapse_state_changed)

        #widget_list = []
        self.make_layout(widget_list)


    def on_collapse_state_changed(self, event):
        print 'state changed'
        self.panel.on_panechanged(event)
        self.panel.Layout()

    def make_content(self):
       """Put in the contents of the given pane based on the data.
       Data is a dict with index as keys and a list describing the
       widget as the value. See form_fields.yaml for examples.

       Pane content that is constructed are a widgetlist to go into the
       sizer, list of labels and list of controls"""
       self.labels = []
       self.control_labels = []
       self.controls = []
       self.pane = self.GetPane()
       
       # Use indices for looping as dict does not preserve order
       for i in range(len(self.pane_data)):
           control_data = self.pane_data[i]
           label = control_data[0]
           control_type = control_data[1]

           # keep a list of labels
           self.labels.append(self.name + '_' + label)

           # statictext label
           self.control_labels.append(wx.StaticText(self.pane, -1, label,
                                            style=wx.ALIGN_CENTER_VERTICAL))

           # control
           if control_type == 'text':
               self.controls.append(wx.TextCtrl(self.pane, -1))
           elif control_type == 'spin':
               self.controls.append(wx.SpinCtrl(self.pane, -1,
                                    min=control_data[2], max=control_data[3],
                                                initial=control_data[4]))
           elif control_type == 'combo':
               self.controls.append(wx.ComboBox(self.pane, -1, choices=control_data[2]))
               self.controls[-1].SetValue(control_data[3])

       # buttons
       self.done_button = wx.Button(self.pane, -1, "Done")
       self.dummy_button = wx.Button(self.pane, -1, "Dummy")
       self.done_button.Bind(wx.EVT_BUTTON, self.on_done)

       # make widget list - keep as loop so any additional steps can be added
       widget_list = []
       for l, c in zip(self.control_labels, self.controls):
           widget_list.append(l)
           widget_list.append((c, 1, wx.EXPAND))

       widget_list += [(self.done_button, 0 ,wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL),
                       (self.dummy_button, 0 ,wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)]
       return widget_list

    
    def make_layout(self, widget_list):
        """Put in the contents of the pane"""
        # namelbl = wx.StaticText(pane, -1, "Name:")
        # name = wx.TextCtrl(pane, -1, "")
        # agelbl = wx.StaticText(pane, -1, "Age:")
        # age = wx.TextCtrl(pane, -1, "")
        
        fsizer = wx.FlexGridSizer(cols=2, hgap=5, vgap=5)
        fsizer.AddGrowableCol(1)
        # fsizer.Add(namelbl, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        # fsizer.Add(name, 0, wx.EXPAND)
        # fsizer.Add(agelbl, 0 , wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        # fsizer.Add(age, 0, wx.EXPAND)
        fsizer.AddMany(widget_list)
        self.pane.SetSizer(fsizer)

    def on_done(self, event):
        self.get_values()

    def get_values(self):
        """Read all the values"""
        vals = {}
        for label, control in zip(self.labels, self.controls):
            vals[label] = control.GetValue()

        print vals
            
        
if __name__ == '__main__':
    app = wx.App()
    f = Form(None, 'form_fields.yaml')
    app.MainLoop()
