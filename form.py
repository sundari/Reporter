#!/usr/bin/env python

"""
Framework for creating reports using a template and user input.

Template is a mako template with variables.
A separate file lists the variables and the wx control
required to get user input (see input_fields.yaml)

The input fields file is loaded using yaml. Based on this,
the controls are created and presented to the user. Once the user
has entered the values, mako is used to render the template and create
an rst document. This is converted to pdf using rst2pdf"""


##
# Author: Raja Selvaraj <rajajs@gmail.com>
# License: GPL
##

# #ToDo:
# 1. Collapse other panes when one pane is opened  -------------- Done
# 2. Bulleted or Enumerated lists must ignore empty items ------- Done
# 3. None at top of each pdf page
# 4. Widget for multline text
# 5. Correctly use rst2pdf from python
# 6. Paths for all files to be calculated


import wx
import yaml
from mako.template import Template
from rst2pdf.createpdf import RstToPdf

class Form(wx.Frame):
    def __init__(self, parent, fields_file):
        wx.Frame.__init__(self, parent, -1, size=(600, 800))
        self.panel = FormPanel(self, fields_file)

        self.panel.print_button.Bind(wx.EVT_BUTTON, self.collect_values)
        
        self.Show(True)

    def collect_values(self, event):
        """collect all the values from the different collapsible panels"""
        self.vals = {}
        for pane in self.panel.panes:
            self.vals.update(pane.get_values())

        #print self.vals

        report_template = Template(filename='report_docs/ep_report_template.rst')
        rep = report_template.render(vals = self.vals)
        #print rep
        #reportfile = 'report_docs/report.rst'
        # with open(reportfile, 'w') as fi:
        #     fi.write(rep)
        self.write_pdf(rep)

    def write_pdf(self, report_rst):
        """report rst is the rst text for the report.
        Format that using rst2pdf to create pdf"""
        rsttopdf = RstToPdf(stylesheets=['/data/Dropbox/programming/EP_report2/report_docs/ep_report.sty'])
        rsttopdf.createPdf(text=report_rst, output='report_docs/report.pdf')
            
class FormPanel(wx.Panel):
    """A Frame  with several collapsible sections that contain
    parts of the form"""
    def __init__(self, parent, fields_file):
        wx.Panel.__init__(self, parent, -1)

        ## contents of the panel
         # title at top
         # button at bottom
         # collpasible panes in between
        self.title = wx.StaticText(self, label="EP Report")
        self.title.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
        
        # Panes will be constructed from yaml file
        self.panes = []
        self.construct_panes(fields_file)
        #self.make_pane_content(self.cp1.GetPane())
        
        self.print_button = wx.Button(self, label='Print report')

        self._layout()

        self.Show(True)
        
    def _layout(self):
        """Layout the controls using sizers"""
        sizer = wx.BoxSizer(wx.VERTICAL)

        sizer.Add(self.title, 0, wx.ALL, 25)

        for cp in self.panes:
            sizer.Add(cp, 0, wx.RIGHT|wx.LEFT|wx.EXPAND, 25)

        sizer.Add(self.print_button, 0, wx.ALL, 25)

        self.SetSizer(sizer)

    def construct_panes(self, fields_file):
       """Read the fields file and use the data to construct the
       collapsible panes"""
       fields_data = yaml.load_all(open(fields_file))
       for pane_data in fields_data:
           self.panes.append(Pane(self, pane_data))
       self.Layout()

    def on_pane_changed(self, event):
        """When a pane uncollapses, make sure other panes are collapsed"""
        active_pane = event.EventObject
        if not event.GetCollapsed():
            for pane in self.panes:
                pane.Collapse(pane != active_pane)
                

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
        self.panel.on_pane_changed(event)
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

           elif control_type == 'multitext':
               self.controls.append(wx.TextCtrl(self.pane, -1,
                                                style=wx.TE_MULTILINE))

           elif control_type == 'spin':
               self.controls.append(wx.SpinCtrl(self.pane, -1,
                                    min=control_data[2], max=control_data[3],
                                                initial=control_data[4]))

           elif control_type == 'combo':
               self.controls.append(wx.ComboBox(self.pane, -1, choices=control_data[2]))
               self.controls[-1].SetValue(control_data[3])


       # make widget list - keep as loop so any additional steps can be added
       widget_list = []
       for l, c in zip(self.control_labels, self.controls):
           widget_list.append(l)
           widget_list.append((c, 1, wx.EXPAND))

       return widget_list

    
    def make_layout(self, widget_list):
        """Put in the contents of the pane"""
        fsizer = wx.FlexGridSizer(cols=2, hgap=5, vgap=5)
        fsizer.AddGrowableCol(1)
        fsizer.AddMany(widget_list)

        # border
        border = wx.BoxSizer(wx.HORIZONTAL)
        border.Add(fsizer, 1, wx.EXPAND|wx.ALL, 10)
        
        self.pane.SetSizer(border)


    def get_values(self):
        """Read all the values"""
        vals = {}
        for label, control in zip(self.labels, self.controls):
            vals[label] = control.GetValue()
        return vals
        
if __name__ == '__main__':
    app = wx.App()
    f = Form(None, 'report_docs/form_fields.yaml')
    app.MainLoop()
