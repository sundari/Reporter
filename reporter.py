"""The main controller for the reports.
On the one hand it interfaces with the database
to retrieve old records and store new ones.
On the other hand it interfaces with the form to
collect information to insert in a new record"""

#import os
import sys
import wx
from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin, ColumnSorterMixin
import shelve
from form import Form
from mako.template import Template
import subprocess

#################
ID_NEW = wx.NewId()
ID_EDIT = wx.NewId()
ID_REMOVE = wx.NewId()
ID_PREF = wx.NewId()
ID_QUIT = wx.NewId()


class ReportDatabase():
    def __init__(self, db_path):
        """db_path is full path to the database"""
        self.db_path = db_path
        self.db = shelve.open(db_path)        

    def get_index(self, index_fields):
        """Get data from db to create an index.
        index_fields are the fields for creating the index
        return list of tuples"""
        index_field_vals = [range(len(self.db))] # first value will be the id
        # getting pretty hackish
        for field in index_fields: 
            index_field_vals.append([self.db[str(x)][field]
                                     for x in range(self.get_max_id())
                                     if str(x) in self.db.keys()])
            
        vals = zip(*index_field_vals)

        record_summary = {}
        for i in range(len(vals)):
            record_summary[i] = vals[i]

        return record_summary


    def get_max_id(self):
        """Get the maximum id"""
        return max([int(x) for x in self.db.keys()])

    
    def insert_record(self, record_dict):
        """Insert a record into the database.
        record_dict is a dict
        eg: {'Name': 'Raja', 'Age': 39}"""
        # find last id
        try:
            last_id = max([int(x) for x in self.db.keys()])
        except ValueError: # empty dict
            last_id = -1

        # insert this record
        self.db[str(last_id+1)] = record_dict


    def delete_record(self, rec_id):
        """Delete record corresponsing to record_id"""
        del self.db[rec_id]

    def dump(self):
        """dump all the database records"""
        for rec in self.db: 
            print rec


            
class AutoWidthListCtrl(wx.ListCtrl, ListCtrlAutoWidthMixin, ColumnSorterMixin):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT)
        ListCtrlAutoWidthMixin.__init__(self)
        ColumnSorterMixin.__init__(self, 4)

    def GetListCtrl(self):
        return self

        
            
class Reporter(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(460, 600))

        self.hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        
        panel = wx.Panel(self, -1)
        
        # listcontrol
        self.record_display = AutoWidthListCtrl(panel)
        self.record_display.InsertColumn(0, 'No.', width=30)
        self.record_display.InsertColumn(1, 'Name', width=120)
        self.record_display.InsertColumn(2, 'Age', width=30)
        self.record_display.InsertColumn(3, 'Sex', width=60)
        self.record_display.InsertColumn(4, 'Procedure Date', 100)

        # buttons
        #self.view_button = wx.Button(panel, -1, 'View Record')
        self.edit_button = wx.Button(panel, -1,  'Edit Record')
        self.new_button = wx.Button(panel, -1, 'New Record')
        self.remove_button = wx.Button(panel, -1, 'Remove Record')
        self.report_button = wx.Button(panel, -1, 'Make Report')
        #self.update_button = wx.Button(panel, -1, 'Update Report')
        
        self.hbox1.Add(self.record_display, 1, wx.ALL|wx.EXPAND, 10)
        #self.hbox2.Add(self.view_button, 1, wx.ALL, 10)
        self.hbox2.Add(self.new_button, 1, wx.ALL, 5)
        self.hbox2.Add(self.edit_button, 1, wx.ALL, 5)
        self.hbox2.Add(self.remove_button, 1, wx.ALL, 5)
        #self.hbox2.Add(self.update_button, 1, wx.ALL, 10)
        self.hbox2.Add(self.report_button, 1, wx.ALL, 5)
        
        self.vbox.Add(self.hbox1, 5, wx.EXPAND, 5)
        self.vbox.Add(self.hbox2, 1, wx.ALL, 5)

        self._build_menubar()
        
        self._set_bindings()
        # instantiate the db
        self.db = ReportDatabase('/data/tmp/testdb')
        self.rec_summary = self.db.get_index(
            ('Demographics_Name', 'Demographics_Age',
             'Demographics_Sex', 'Demographics_Date of Procedure'))

        self.show_records(self.rec_summary)
        self.record = {} #active record in memory

        panel.SetSizer(self.vbox)
        self.Centre()
        self.Show(True)

    def _build_menubar(self):
        """Build the menu bar"""
        self.MenuBar = wx.MenuBar()

        file_menu = wx.Menu()
        file_menu.Append(ID_NEW, "&New Record","Create a new record")
        file_menu.Append(ID_EDIT, "&Edit Record", "Edit an existing record")
        file_menu.Append(ID_REMOVE, "&Remove Record", "Remove existing record")
        file_menu.Append(ID_QUIT, "&Quit","Quit the program")
   
        edit_menu = wx.Menu()
        edit_menu.Append(ID_PREF, "Preferences", "Edit preferences")
        
        self.MenuBar.Append(file_menu, "&File")
        self.MenuBar.Append(edit_menu, "&Edit")
        
        self.SetMenuBar(self.MenuBar)

    def _set_bindings(self):
        """All the bindings"""
        self.Bind(wx.EVT_CLOSE, self.on_quit)
        self.new_button.Bind(wx.EVT_BUTTON, self.new_record)
        self.edit_button.Bind(wx.EVT_BUTTON, self.load_and_edit_record)
        self.remove_button.Bind(wx.EVT_BUTTON, self.remove_record)
        self.report_button.Bind(wx.EVT_BUTTON, self.render_report)

        self.Bind(wx.EVT_MENU, self.new_record, id=ID_NEW)
        self.Bind(wx.EVT_MENU, self.load_and_edit_record, id=ID_EDIT)
        self.Bind(wx.EVT_MENU, self.on_quit, id=ID_QUIT)
        
        #self.update_button.Bind(wx.EVT_BUTTON, self.update_record)

    def load_and_edit_record(self, event):
        """Load the selected record into a form for editing"""
        selected_record = self.record_display.GetFirstSelected()
        if selected_record == -1: # none selected
            return

        self.edit_id = str(self.record_display.GetItem(selected_record, 0).GetText())

        rec = self.db.db[self.edit_id]
        f = Form(self, 'report_docs/form_fields.yaml', self.edit_id)
        f.set_values(rec)


    def remove_record(self, event):
        """Remove selected record from the database"""
        selected_record = self.record_display.GetFirstSelected()
        if selected_record == -1: # none selected
            return
        
        self.db.delete_record(str(selected_record))
        

    def render_report(self, event):
        """Render selected record as a pdf"""
        #TODO: refactor to avoid repetition
        selected_record = self.record_display.GetFirstSelected()
        if selected_record == -1: # none selected
            return

        id = str(self.record_display.GetItem(selected_record, 0).GetText())

        rec = self.db.db[id]

        report_template = Template(filename='report_docs/ep_report_template.rst')
        rep = report_template.render(vals = rec)

        reportfile = 'report_docs/report.rst'
        with open(reportfile, 'w') as fi:
            fi.write(rep)
        self.write_pdf(rep)
    
    def write_pdf(self, report_rst):
        """report rst is the rst text for the report.
        Format that using rst2pdf to create pdf"""
        pdffile = 'report_docs/report.pdf'

        ### Need to process paths !!! ## TODO:
        subprocess.Popen(['rst2pdf', '-s', '/data/Dropbox/programming/EP_report2/report_docs/ep_report.sty', '/data/Dropbox/programming/EP_report2/report_docs/report.rst'])
        subprocess.Popen(['evince', '/data/Dropbox/programming/EP_report2/report_docs/report.pdf'])
        
        
    def on_quit(self, event):
        """Close the db properly"""
        self.db.db.close()
        sys.exit(0)
        
    def show_records(self, records):
        """Populate the listctrl with record summaries.
        records is a list of tuples"""
        self.record_display.itemDataMap = records

        #self.record_display.ClearAll()
        for ind in range(len(records)):
            rec = records[ind]
            self.record_display_append(rec, ind)


    def record_display_append(self, rec, ind):
        """add the rec to display"""
        index = self.record_display.InsertStringItem(sys.maxint, str(rec[0]))
        self.record_display.SetStringItem(index, 1, rec[1])
        self.record_display.SetStringItem(index, 2, str(rec[2]))
        self.record_display.SetStringItem(index, 3, rec[3])
        self.record_display.SetStringItem(index, 4, rec[4])
        self.record_display.SetItemData(index, ind)
            
            
    def new_record(self, event):
        """Create a new record"""
        f = Form(self, 'report_docs/form_fields.yaml')

    def insert_record(self):
        """Insert the record into the database.
        Will be triggered from the form"""
        self.db.insert_record(self.record)

        new_id = len(self.rec_summary)
        #self.record_display.ClearAll()
        #TODO: just append to rec_summary
        rec_summary = [self.record[k] for k in ['Demographics_Name',
                      'Demographics_Age', 'Demographics_Sex',
                      'Demographics_Date of Procedure']]
        rec_summary = [new_id] + rec_summary
        self.record_display_append(rec_summary, new_id)
        #self.show_records()
        #self.db.close()

    def update_record(self, id):
        """Update the record with given id"""
        self.db.db[id] = self.record
        #TODO: update the record display
        
def db_tests(path):
    """Create a db in the path, and test it"""
    print 'Creating db'
    manager = ReportDatabase(path)
 
    print 'insert record'
    reca = {'Name': 'Raja', 'Age': 38, 'Sex':'M'}
    recb = {'Name': 'Rajan', 'Age': 39, 'Sex':'M'}
    recc = {'Name': 'Rajee', 'Age': 48, 'Sex':'F'}

    manager.insert_record(reca)
    manager.insert_record(recb)
    manager.insert_record(recc)

    # debug
    print manager.db.ids()
    
    print 'get index'
    print manager.get_index(('Name', 'Age'))

    print 'dump data'
    print manager.dump()


if __name__ == '__main__':
    app = wx.App()
    rep = Reporter(None, -1, 'Records')
    app.MainLoop()

    
