import sqlite3, pathlib, os

PROHIBITED = ['matplotlib_code']
database = 'database.sql'

def hierarchy(root, directory):
    with sqlite3.connect(database) as db:
        try:
            assert directory not in PROHIBITED
            path = os.path.join(root, directory).split(os.sep)
            if path[4] == directory:
                sql = 'INSERT INTO category VALUES (?);'
                db.execute(sql, (path[4],))
            else:
                sql = 'INSERT INTO subject VALUES (?, ?);'
                db.execute(sql, (path[5], path[4]))
            db.commit()
        except AssertionError as prohibited:
            return
        except sqlite3.IntegrityError as ok:
            return #NOTE Tuple already exists.

def content(root, fname, data):
    sql = 'INSERT INTO {} VALUES (?, ?, ?);'
    name = str(pathlib.Path(fname).stem)
    url = os.path.join(root, fname)[21:]
    sub = url.split(os.sep)[2]
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

def populate():
    
    # Create tables if they do not exist
    with sqlite3.connect(database) as db, open('tables.sql') as TABLES:
        db.executescript(TABLES.read())
        db.commit()
            
    # Find out what is in the database already (prevents duplication)
    with sqlite3.connect(database) as db:        
        
        theorems = {theorem[0].split(os.sep)[-1
            ] for theorem in db.execute(
            'SELECT url FROM theorem;').fetchall()
            }
        
        plots = {plot[0].split(os.sep)[-1
            ] for plot in db.execute(
            'SELECT url FROM plot;').fetchall()
            }

    data = theorems | plots # all content in the database
  
    home = os.path.join('.', 'application', 'static', 'data')

    for root, directories, fnames in os.walk(home):
        
        for directory in directories:
            hierarchy(root, directory)
       
        for fname in fnames:
            content(root, fname, data)
