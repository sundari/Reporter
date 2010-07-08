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
    """The database holding the records.
    This is a dictionary with keys made of a unique hash
    and vals being a dict that has all the values for
    each variable for that record.
    eg:
    {
    'uniq_hash1':{'Name':'Raja', 'Age':38},
    'uniq_hash2':{'Name':'Rajesh', 'Age':38}
    }
    """
    def __init__(self, db_path, index_keys):
        """db_path is full path to the database.
        index_keys is a list of the keys that will
        be used to make the index view"""
        self.db_path = db_path
        # Note that open will create a new db if it does not exist
        self.db = shelve.open(db_path)
        self.index_keys = index_keys

    def get_index(self):
        """Get data from db to create an index.
        index_fields are the fields for creating the index
        return list of tuples"""
        index_field_vals = []
        
        for field in self.index_keys:
            index_field_vals.append([self.db[rec][field] for rec in self.db])

        vals = zip(*index_field_vals)

        return vals
    
    def insert_record(self, record):
        """Insert a record into the database.
        The key for each record is a unique id
        constructed by joining all the index elements.
        record is a dict
        eg: {'Name': 'Raja', 'Age': 39}"""
        unique_id = ''.join([str(record[k]) for k in self.index_keys])
        
        # insert this record
        self.db[unique_id] = record


    def delete_record(self, rec_id):
        """Delete record corresponsing to record_id"""
        del self.db[rec_id]

    def dump(self):
        """dump all the database records"""
        for rec in self.db: 
            print rec

    def to_csv(self, fields, filename):
        """export the database to a csv file.
        fields is a tuple of header corresponding
        to the dictionary keys"""
        # string format for each row
        row_format = '%s,' * len(fields) + '\n'

        print 'fields', fields
        with open(filename, 'w') as f:
            # header row
            f.write(row_format % fields)
            # record per row
            for record in self.db:
                f.write(row_format % tuple([self.db[record][key]
                                            for key in fields]))
            
            
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
        self.record_display.InsertColumn(0, 'Name', width=120)
        self.record_display.InsertColumn(1, 'Age', width=30)
        self.record_display.InsertColumn(2, 'Sex', width=60)
        self.record_display.InsertColumn(3, 'Procedure Date', 100)

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
        
        self.vbox.Add(self.hbox1, 6, wx.EXPAND, 10)
        self.vbox.Add(self.hbox2, 1, wx.ALL, 10)

        self._build_menubar()
        
        self._set_bindings()

        # instantiate the db
        self.index_keys = ['Demographics_Name', 'Demographics_Age',
                           'Demographics_Sex', 'Demographics_Date of Procedure']
        self.db = ReportDatabase('/data/tmp/testdb', self.index_keys)
        
        self.rec_summary = self.db.get_index()

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

        # convert to string coz unicode object does not work
        selected_record_key = str(''.join([self.record_display.GetItem(
                    selected_record, x).GetText()
                    for x in range(len(self.index_keys))]))

        rec = self.db.db[selected_record_key]
        f = Form(self, 'report_docs/form_fields.yaml', selected_record_key)
        f.set_values(rec)


    def remove_record(self, event):
        """Remove selected record from the database"""
        selected_record = self.record_display.GetFirstSelected()
        if selected_record == -1: # none selected
            return

        db_key = self.rec_summary[selected_record][-1]
        #self.db.delete_record()
        #self.record_display.DeleteItem(2)

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
        #self.db.to_csv(self.index_keys, '/data/tmp/dump.csv')

        self.db.db.close()
        
        sys.exit(0)
        
    def show_records(self, records):
        """Populate the listctrl with record summaries.
        records is a list of tuples"""
        self.record_display.itemDataMap = records

        #self.record_display.ClearAll()
        for rec in records:
            self.record_display_append(rec)


    def record_display_append(self, rec):
        """add the rec to display"""
        index = self.record_display.InsertStringItem(sys.maxint, rec[0])
        self.record_display.SetStringItem(index, 1, str(rec[1]))
        self.record_display.SetStringItem(index, 2, rec[2])
        self.record_display.SetStringItem(index, 3, rec[3])
        #self.record_display.SetStringItem(index, 4, rec[4])
        self.record_display.SetItemData(index, index)
            
            
    def new_record(self, event):
        """Create a new record"""
        f = Form(self, 'report_docs/form_fields.yaml')

    def insert_record(self):
        """Insert the record into the database.
        Will be triggered from the form"""
        self.db.insert_record(self.record)

        rec_summary = [self.record[k] for k in self.index_keys]
        self.record_display_append(rec_summary)
        #self.show_records()

    def update_record(self, id):
        """Update the record with given id"""
        self.db.db[id] = self.record
        #TODO: update the record display
        

if __name__ == '__main__':
    app = wx.App()
    rep = Reporter(None, -1, 'EP Reports')
    app.MainLoop()

    
