from sqlite3 import IntegrityError
import sqlite3, pathlib, os

PROHIBITED = ['matplotlib_code']
database = 'database.sql'

OFFSET = 0 # NOTE in case the data path needs to be changed

class Mock:

    def connect(self, database):
        return self

    def execute(self, a, b):
        pass

    def commit(self):
        pass

    def IntegrityError(self):
        pass

    def executescript(self, script):
        pass

    def __enter__(self):
        return self

    def __exit__(self, a, b, c):
        pass

def hierarchy(root, directory):
    with sqlite3.connect(database) as db:
        try:
            assert directory not in PROHIBITED
            path = os.path.join(root, directory).split(os.sep)
            if path[3 + OFFSET] == directory:
                sql = 'INSERT INTO category VALUES (?);'
                db.execute(sql, (path[3 + OFFSET],))
            else:
                sql = 'INSERT INTO subject VALUES (?, ?);'
                db.execute(sql, (path[4 + OFFSET], path[3 + OFFSET]))
            db.commit()
        except AssertionError as prohibited:
            return
        except IntegrityError as ok:
            return #NOTE Tuple already exists.

def content(root, fname, data):
    sql = 'INSERT INTO {} VALUES (?, ?, ?);'
    name = str(pathlib.Path(fname).stem)
    url = os.path.join(root, fname)[19 + OFFSET:]
    sub = url.split(os.sep)[1]
    try:
        assert fname not in data
        assert pathlib.Path(fname).suffix == '.jpg'
        name, _ = name.split('_')[0], name.split('_')[1]
        sql = sql.format('plot')
    except IndexError:
        sql = sql.format('theorem')
    except AssertionError:
        return
    values = (name, url, sub)
    print(values) #TODO
    with sqlite3.connect(database) as db:
        db.execute(sql, values)
        db.commit()

def populate(verbose=False):
    
    # Create tables if they do not exist
    with sqlite3.connect(database) as db, open('tables.sql') as TABLES:
        db.executescript(TABLES.read())
        db.commit()
            
    # Find out what is in the database already (prevents duplication)
    with sqlite3.connect(database) as db:

        theorems, plots = set(), set()

        if not verbose:
            theorems = {theorem[0].split(os.sep)[-1
                ] for theorem in db.execute(
                'SELECT url FROM theorem;').fetchall()
                }
        
            plots = {plot[0].split(os.sep)[-1
                ] for plot in db.execute(
                'SELECT url FROM plot;').fetchall()
                }

    data = theorems | plots # all content in the database
  
    home = os.path.join('.', 'application', 'data')

    for root, directories, fnames in os.walk(home):
        
        for directory in directories:
            if verbose: print(f'HIERARCHY: {os.path.join(root, directory)}')
            else: hierarchy(root, directory)
       
        for fname in fnames:
            if verbose: print(f'CONTENT: {os.path.join(root, fname)}')
            else: content(root, fname, data)

if __name__ == '__main__':
    # test / trace paths
    sqlite3 = Mock()
    populate(verbose=True)
