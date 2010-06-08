"""The main controller for the reports.
On the one hand it interfaces with the database
to retrieve old records and store new ones.
On the other hand it interfaces with the form to
collect information to insert in a new record"""

import os
from buzhug import Base

class ReportManager():
    def __init__(self, db_path):
        """db_path is full path to the database"""
        self.db_path = db_path
        
        if os.path.exists(db_path):
            self.open_db()
        else:
            pass # TODO: create db without fields, then get fields and update them
        
        
    def populate_db(self, fields):
        """Populate a new empty db with fields
        fields is a tuple of tuples with the inner tuples
        specifying each field
        eg: (("Name", str), ("Age", int))"""
        fields.reverse()
        print fields
        for field in fields:
            print 'field', field
            self.db.add_field(*field)

    
    def open_db(self):
        """open an existing database or create a new one"""
        self.db = Base(self.db_path)

        try:
            self.db.open() # if pre-existing
        except IOError:
            self.db.create()

            
    def close_db(self):
        """close the database"""
        self.db.close()


    def get_index(self, index_fields):
        """Get data from db to create an index.
        index_fields are the fields for creating the index
        return list of tuples"""
        indices = []
        for field in index_fields: #terrible hack, only works for strings
            indices.append(f[0].lstrip('-').rstrip('\n') for f in self.db.select([field]))

        return zip(*indices)

    def insert_record(self, record):
        """Insert a record into the database.
        record is a tuple of the fields."""
        self.db.insert(*record)


    def dump(self):
        """dump all the database records"""
        for rec in self.db:
            print rec
            
        
def db_tests(path):
    """Create a db in the path, and test it"""
    manager = ReportManager(path)
    
    print 'Creating db'
    manager.open_db()

    print 'populating db'
    manager.populate_db([("Name", str), ("Age", int), ("Sex", str)])

    print 'insert record'
    reca = (("Raja", 37, "Male"))
    recb = (("Rajan", 38, "Male"))
    recc = (("Rajee", 39, "Female"))

    manager.insert_record(reca)
    manager.insert_record(recb)
    manager.insert_record(recc)

    # debug
    print manager.db.keys()
    print manager.db.field_names
    print manager.db.select(['Name'])
    
    print 'get index'
    print manager.get_index(('Name', 'Age'))

    print 'dump data'
    print manager.dump()


if __name__ == '__main__':
    db_tests('/data/tmp/testdb')
