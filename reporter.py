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

    
class ReportDatabase():
    def __init__(self, db_path):
        """db_path is full path to the database"""
        self.db_path = db_path
        self.db = shelve.open(db_path)        

    def get_index(self, index_fields):
        """Get data from db to create an index.
        index_fields are the fields for creating the index
        return list of tuples"""
        index_field_vals = []
        for field in index_fields: 
            index_field_vals.append([self.db[str(x)][field]
                                     for x in range(len(self.db))])
            
        vals = zip(*index_field_vals)

        record_summary = {}
        for i in range(len(vals)):
            record_summary[i] = vals[i]

        return record_summary

    
    def insert_record(self, record_dict):
        """Insert a record into the database.
        record_dict is a dict
        eg: {'Name': 'Raja', 'Age': 39}"""
        # find last id
        try:
            last_id = max([int(x) for x in self.db.ids()])
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
        wx.Frame.__init__(self, parent, id, title, size=(400, 600))

        self.hbox = wx.BoxSizer(wx.HORIZONTAL)
        panel = wx.Panel(self, -1)

        self.records = AutoWidthListCtrl(panel)
        self.records.InsertColumn(0, 'Name', width=120)
        self.records.InsertColumn(1, 'Age', width=30)
        self.records.InsertColumn(2, 'Sex', width=60)
        self.records.InsertColumn(3, 'Procedure Date', 100)

        self.hbox.Add(self.records, 1, wx.ALL|wx.EXPAND, 10)

        # instantiate the db
        self.db = ReportDatabase('/data/tmp/testdb')
        rec_summary = self.db.get_index(('Name', 'Age', 'Sex', 'Date'))
        self.show_records(rec_summary)

        panel.SetSizer(self.hbox)
        self.Centre()
        self.Show(True)
        
    def show_records(self, records):
        """Populate the listctrl with record summaries.
        records is a list of tuples"""
        self.records.itemDataMap = records
        for i in range(len(records)):
            rec = records[i]
            index = self.records.InsertStringItem(sys.maxint, rec[0])
            self.records.SetStringItem(index, 1, str(rec[1]))
            self.records.SetStringItem(index, 2, rec[2])
            self.records.SetStringItem(index, 3, rec[3])
            self.records.SetItemData(index, i)





            
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

    
