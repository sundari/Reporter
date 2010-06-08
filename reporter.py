"""The main controller for the reports.
On the one hand it interfaces with the database
to retrieve old records and store new ones.
On the other hand it interfaces with the form to
collect information to insert in a new record"""

import os
import UserDict
from sqlite3 import dbapi2 as sqlite
from buzhug import Base

#import os,os.path,UserDict


class DataBase(UserDict.DictMixin):
    """Modified from http://sebsauvage.net/python/snyppets/index.html#dbdict.
    a dictionary-like object using sqlite"""
    def __init__(self, db_filename):
        self.db_filename = db_filename
        if not os.path.isfile(self.db_filename):
            self.con = sqlite.connect(self.db_filename)
            self.con.execute("create table data (key PRIMARY KEY,value)")
        else:
            self.con = sqlite.connect(self.db_filename)
   
    def __getitem__(self, key):
        row = self.con.execute("select value from data where key=?",(key,)).fetchone()
        if not row: raise KeyError
        return row[0]
   
    def __setitem__(self, key, item):
        if self.con.execute("select key from data where key=?",(key,)).fetchone():
            self.con.execute("update data set value=? where key=?",(item,key))
        else:
            self.con.execute("insert into data (key,value) values (?,?)",(key, item))
        self.con.commit()
              
    def __delitem__(self, key):
        if self.con.execute("select key from data where key=?",(key,)).fetchone():
            self.con.execute("delete from data where key=?",(key,))
            self.con.commit()
        else:
             raise KeyError
            
    def keys(self):
        return [row[0] for row in self.con.execute("select key from data").fetchall()]


    
class ReportManager():
    def __init__(self, db_path):
        """db_path is full path to the database"""
        self.db_path = db_path
        self.db = DataBase(db_path)        
            

    def get_index(self, index_fields):
        """Get data from db to create an index.
        index_fields are the fields for creating the index
        return list of tuples"""
        index_field_vals = []
        for field in index_fields: 
            index_field_vals.append([self.db[x][field] for x in range(len(self.db))])
            
        return zip(*index_field_vals)

    def insert_record(self, record_dict):
        """Insert a record into the database.
        record_dict is a dict
        eg: {'Name': 'Raja', 'Age': 39}"""
        # find last key
        try:
            last_key = max(self.db.keys())
        except ValueError: # empty dict
            last_key = -1

        # insert this record
        self.db[last_key+1] = record_dict


    def dump(self):
        """dump all the database records"""
        for rec in self.db:
            print rec
            
        
def db_tests(path):
    """Create a db in the path, and test it"""
    print 'Creating db'
    manager = ReportManager(path)

    print 'insert record'
    reca = {'Name': 'Raja', 'Age': 38, 'Sex':'M'}
    recb = {'Name': 'Rajan', 'Age': 39, 'Sex':'M'}
    recc = {'Name': 'Rajee', 'Age': 48, 'Sex':'F'}

    manager.insert_record(reca)
    manager.insert_record(recb)
    manager.insert_record(recc)

    # debug
    print manager.db.keys()
    
    print 'get index'
    print manager.get_index(('Name', 'Age'))

    print 'dump data'
    print manager.dump()


if __name__ == '__main__':
    db_tests('/data/tmp/testdb')
    
