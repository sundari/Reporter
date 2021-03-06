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
# 3. None at top of each pdf page                        -------- Done
# 4. Widget for multline text ----------------------------------- Done
# 5. Correctly use rst2pdf from python 
# 6. Paths for all files to be calculated
# 7. widget for date                              --------------- Done
# 8. widget with combobox and one field for custom entry
# 9. form - under ablation - rhythm
# 10. Canned recommendations                      --------------- Done
# 11. Modify getvalue for datepicker
# 12. Change bullet lists to look better without indent
# 13. Empty cover page                            --------------  Done
# 14. Edited record must replace, not become new
# 15. Summary, conclusions are centred - check style file


import subprocess
import wx
import yaml
from mako.template import Template
#from rst2pdf.createpdf import RstToPdf

class Form(wx.Frame):
    def __init__(self, parent, fields_file, id=-1):
        """fields_file is the file to use to construct fields.
        id is required when we are updating / editing.
        id of -1 means it is a new form"""
        wx.Frame.__init__(self, parent, -1, size=(600, 700))
        self.panel = FormPanel(self, fields_file)
        self.parent = parent
        self.id = id

        self.panel.print_button.Bind(wx.EVT_BUTTON, self.collect_values)
        self.panel.insert_button.Bind(wx.EVT_BUTTON, self.insert_record)
        self.panel.update_button.Bind(wx.EVT_BUTTON, self.update_record)

        if id == -1:
            self.panel.update_button.Enable(False)
        
        self.panel.panes[0].Collapse(False)
        self.Show(True)
        

    def collect_values(self, event):
        """collect all the values from the different collapsible panels"""
        self.vals = {}
        for pane in self.panel.panes:
            self.vals.update(pane.get_values())


    def render_report(self):
        """render the report as a pdf"""
        report_template = Template(filename='report_docs/ep_report_template.rst')
        rep = report_template.render(vals = self.vals)

        reportfile = 'report_docs/report.rst'
        with open(reportfile, 'w') as fi:
            fi.write(rep)
        self.write_pdf(rep)
        

    def insert_record(self, event):
        """insert the values into the database.
        The parent must be ReportManager"""
        self.collect_values(None)
        self.parent.record = self.vals
        self.parent.insert_record()
        self.Destroy()

    def update_record(self, event):
        """Update the record that has been opened for editing"""
        self.collect_values(None)
        self.parent.record = self.vals
        self.parent.update_record(self.id)
        self.Destroy()

        
    def write_pdf(self, report_rst):
        """report rst is the rst text for the report.
        Format that using rst2pdf to create pdf"""
        pdffile = 'report_docs/report.pdf'

        ### Need to process paths !!! ## TODO:
        subprocess.Popen(['rst2pdf', '-s', '/data/Dropbox/programming/EP_report2/report_docs/ep_report.sty', '/data/Dropbox/programming/EP_report2/report_docs/report.rst'])
        subprocess.Popen(['evince', '/data/Dropbox/programming/EP_report2/report_docs/report.pdf'])
        

    def set_values(self, vals):
        """Fill in the form according to the dict vals"""
        labels = []
        controls = []

        for pane in self.panel.panes:
            labels += pane.labels
            controls += pane.controls
        
        for label, control in zip(labels, controls):
            control.SetValue(vals[label])
        
            
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
        self.insert_button = wx.Button(self, label = 'Insert new record')
        self.update_button = wx.Button(self, label= 'Update record')
        
        self._layout()

        self.Show(True)
        
    def _layout(self):
        """Layout the controls using sizers"""
        sizer = wx.BoxSizer(wx.VERTICAL)
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        sizer.Add(self.title, 0, wx.ALL, 25)

        for cp in self.panes:
            sizer.Add(cp, 0, wx.RIGHT|wx.LEFT|wx.EXPAND, 25)

        button_sizer.Add(self.insert_button, 0, wx.ALL, 25)
        button_sizer.Add(self.update_button, 0, wx.ALL, 25)
        button_sizer.Add(self.print_button, 0, wx.ALL, 25)
        
        sizer.Add(button_sizer, 0 ,wx.ALL)
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

        # set focus on first control in the active pane
        active_pane.controls[0].SetFocus()
                

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


    def without_parentheses(self, label_str):
        """Remove terminal text within parentheses
        >>> without_parentheses(self, "test(within)")
            "test"
        """
        opening_brace_pos = label_str.find('(')

        if opening_brace_pos == -1:
            return label_str
        
        return label_str[:opening_brace_pos].strip()

    
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
           self.labels.append(self.name + '_' +
                              self.without_parentheses(label))

           # statictext label
           self.control_labels.append(wx.StaticText(self.pane, -1, label,
                                            style=wx.ALIGN_CENTER_VERTICAL))

           # control
           if control_type == 'text':
               self.controls.append(wx.TextCtrl(self.pane, -1))
               try:
                   self.controls[-1].SetValue(control_data[2])
               except IndexError:
                   pass # no default value

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

           elif control_type == 'date':
               self.controls.append(wx.DatePickerCtrl(self.pane, -1,
                                    style=wx.TAB_TRAVERSAL))


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
