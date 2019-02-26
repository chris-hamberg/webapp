from collections import namedtuple
from requests_oauthlib import OAuth1
import sqlite3

database = 'database.sql'

class ORM:

    PROHIBIT = ('query')

    @classmethod
    def query(cls, **where):
        sql = f'SELECT * FROM {cls.__tablename__};'
        with sqlite3.connect(database) as db:

            schema = db.execute(
                    f'PRAGMA table_info({cls.__tablename__});'
                    ).fetchall()
            
            attributes = ''
            for attribute in schema:
                attributes += attribute[1] + ' '
            attributes = attributes.rstrip()
            NameSpace = namedtuple(cls.__name__, attributes)

            data = list()
            for row in db.execute(sql):
                data.append(NameSpace(*row))

            if where:
                predicate = list(where.keys())[0]
                value = where[predicate]
                data = list(filter(
                    lambda i: getattr(i, predicate) == value, 
                    data
                    ))

            return data

    def __repr__(self):
        return self.name

class Category(ORM):

    __tablename__ = 'category'

    def __init__(self, name):
        self.name = name

    @classmethod
    def query(cls, **where): return super().query(**where)

class Subject(ORM):

    __tablename__ = 'subject'

    def __init__(self, name, category):
        self.name = name
        self.category = category

    @classmethod
    def query(cls, **where): return super().query(**where)

class Theorem(ORM):

    __tablename__ = 'theorem'

    def __init__(self, name, url, subject):
        self.name = name
        self.url = url
        self.subject = subject

    @classmethod
    def query(cls, **where): return super().query(**where)

class Plot(ORM):

    __tablename__ = 'plot'

    def __init__(self, name, url, subject):
        self.name = name
        self.url = url
        self.subject = subject

    @classmethod
    def query(cls, **where): return super().query(**where)

class User:

    def __init__(self, email):
        self.email = email
        self.query()

    def get_id(self):
        return self.email

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def query(self):
        try:
            sql = ('SELECT api_key, api_secret, access_token, token_secret'
                  f'FROM users WHERE email="{self.email}";')
            with sqlite3.connect(database) as db:
                data = db.execute(sql).fetchone()[0]
            self.api_key = data[0]
            self.api_secret = data[1]
            self.access_token = data[2]
            self.token_secret = data[3]
        except sqlite3.OperationalError as no_OAuth:
            pass

    @classmethod
    def password(cls, email):
        sql = f'SELECT salt, hash FROM users WHERE email="{email}"'
        with sqlite3.connect(database) as db:
            data = db.execute(sql).fetchone()
        try:
            return {'salt':data[0], 'hash':data[1]}
        except TypeError as NoneType:
            return None

def dynamic_join(stub):
    '''
    A special handler for dynamic routing, the controller route
    '''
    NameSpace = namedtuple('Theorem', 'name, theorem, plot, subject')
    
    sql = '''SELECT theorem.name, theorem.url, plot.url, theorem.subject
    FROM theorem LEFT JOIN plot USING (name);'''
    with sqlite3.connect(database) as db:
        data = db.execute(sql).fetchall()

    return list(
           filter(lambda i: i.subject == f'{stub}', 
           map(lambda d: NameSpace(d[0], d[1], d[2], d[3]), data
               )))
