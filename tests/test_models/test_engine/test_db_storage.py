#!/usr/bin/python3
"""Contains the TestDBStorageDocs and TestDBStorage classes """

from datetime import datetime
import inspect
import models
from models import storage
from models.engine import db_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.review import Review
from models.place import Place
from models.state import State
from models.user import User
import os
import json
import pep8
import unittest
import MySQLdb
DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))

"""
@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                 'db_storage test not supported')
class TestDBStorage(unittest.TestCase):
    '''testing dbstorage engine'''
    def test_new_and_save(self):
        '''testing  the new and save methods'''
        db = MySQLdb.connect(user=os.getenv('HBNB_MYSQL_USER'),
                             host=os.getenv('HBNB_MYSQL_HOST'),
                             passwd=os.getenv('HBNB_MYSQL_PWD'),
                             port=3306,
                             db=os.getenv('HBNB_MYSQL_DB'))
        new_user = User(**{'first_name': 'jack',
                           'last_name': 'bond',
                           'email': 'jack@bond.com',
                           'password': '12345'})
        cur = db.cursor()
        cur.execute('SELECT COUNT(*) FROM users')
        old_count = cur.fetchall()
        cur.close()
        db.close()
        new_user.save()
        db = MySQLdb.connect(user=os.getenv('HBNB_MYSQL_USER'),
                             host=os.getenv('HBNB_MYSQL_HOST'),
                             passwd=os.getenv('HBNB_MYSQL_PWD'),
                             port=3306,
                             db=os.getenv('HBNB_MYSQL_DB'))
        cur = db.cursor()
        cur.execute('SELECT COUNT(*) FROM users')
        new_count = cur.fetchall()
        self.assertEqual(new_count[0][0], old_count[0][0] + 1)
        cur.close()
        db.close()

    def test_new(self):
        """ New object is correctly added to database """
        t_new = User(
            email='john2020@gmail.com',
            password='password',
            first_name='John',
            last_name='Zoldyck'
        )
        self.assertFalse(t_new in storage.all().values())
        t_new.save()
        self.assertTrue(t_new in storage.all().values())
        db_c = MySQLdb.connect(
            host=os.getenv('HBNB_MYSQL_HOST'),
            port=3306,
            user=os.getenv('HBNB_MYSQL_USER'),
            passwd=os.getenv('HBNB_MYSQL_PWD'),
            db=os.getenv('HBNB_MYSQL_DB')
        )
        cursor = db_c.cursor()
        cursor.execute('SELECT * FROM users WHERE id="{}"'.format(t_new.id))
        result = cursor.fetchone()
        self.assertTrue(result is not None)
        self.assertIn('john2020@gmail.com', result)
        self.assertFalse('password' in result)
        self.assertIn('John', result)
        self.assertIn('Zoldyck', result)
        cursor.close()
        db_c.close()

    def test_delete(self):
        """ Object is correctly deleted from database """
        new = User(
            email='john2020@gmail.com',
            password='password',
            first_name='John',
            last_name='Zoldyck'
        )
        obj_key = 'User.{}'.format(new.id)
        db_c = MySQLdb.connect(
            host=os.getenv('HBNB_MYSQL_HOST'),
            port=3306,
            user=os.getenv('HBNB_MYSQL_USER'),
            passwd=os.getenv('HBNB_MYSQL_PWD'),
            db=os.getenv('HBNB_MYSQL_DB')
        )
        new.save()
        self.assertTrue(new in storage.all().values())
        cursor = db_c.cursor()
        cursor.execute('SELECT * FROM users WHERE id="{}"'.format(new.id))
        result = cursor.fetchone()
        self.assertTrue(result is not None)
        self.assertIn('john2020@gmail.com', result)
        self.assertFalse('password' in result)
        self.assertIn('John', result)
        self.assertIn('Zoldyck', result)
        self.assertIn(obj_key, storage.all(User).keys())
        new.delete()
        self.assertNotIn(obj_key, storage.all(User).keys())
        cursor.close()
        db_c.close()

    def test_reload(self):
        """ Tests the reloading of the database session """
        db_c = MySQLdb.connect(
            host=os.getenv('HBNB_MYSQL_HOST'),
            port=3306,
            user=os.getenv('HBNB_MYSQL_USER'),
            passwd=os.getenv('HBNB_MYSQL_PWD'),
            db=os.getenv('HBNB_MYSQL_DB')
        )
        cursor = db_c.cursor()
        cursor.execute(
            'INSERT IGNORE INTO users(id, created_at, updated_at, email, pa' +
            'ssword, first_name, last_name) ' +
            'VALUES(%s, %s, %s, %s, %s, %s, %s);',
            [
                '4445-by-me',
                str(datetime.now()),
                str(datetime.now()),
                'ben_pike@yahoo.com',
                'pass',
                'Benjamin',
                'Pike',
            ]
        )
        self.assertNotIn('User.4445-by-me', storage.all())
        db_c.commit()
        storage.reload()
        self.assertIn('User.4445-by-me', storage.all())
        cursor.execute('DELETE FROM users WHERE id=\'4445-by-me\'')
        db_c.commit()
        storage.reload()
        cursor.close()
        db_c.close()

    def test_save(self):
        """ object is successfully saved to database """
        t_new = User(
            email='john2020@gmail.com',
            password='password',
            first_name='John',
            last_name='Zoldyck'
        )
        db_c = MySQLdb.connect(
            host=os.getenv('HBNB_MYSQL_HOST'),
            port=3306,
            user=os.getenv('HBNB_MYSQL_USER'),
            passwd=os.getenv('HBNB_MYSQL_PWD'),
            db=os.getenv('HBNB_MYSQL_DB')
        )
        cursor = db_c.cursor()
        cursor.execute('SELECT * FROM users WHERE id="{}"'.format(t_new.id))
        result = cursor.fetchone()
        cursor.execute('SELECT COUNT(*) FROM users;')
        old_cnt = cursor.fetchone()[0]
        self.assertTrue(result is None)
        self.assertFalse(t_new in storage.all().values())
        t_new.save()
        dbc1 = MySQLdb.connect(
            host=os.getenv('HBNB_MYSQL_HOST'),
            port=3306,
            user=os.getenv('HBNB_MYSQL_USER'),
            passwd=os.getenv('HBNB_MYSQL_PWD'),
            db=os.getenv('HBNB_MYSQL_DB')
        )
        cursor1 = dbc1.cursor()
        cursor1.execute('SELECT * FROM users WHERE id="{}"'.format(t_new.id))
        result = cursor1.fetchone()
        cursor1.execute('SELECT COUNT(*) FROM users;')
        new_cnt = cursor1.fetchone()[0]
        self.assertFalse(result is None)
        self.assertEqual(old_cnt + 1, new_cnt)
        self.assertTrue(t_new in storage.all().values())
        cursor1.close()
        dbc1.close()
        cursor.close()
        db_c.close()
"""
    def test_count(self):
        """Tests the count method"""
        initial_count = len(storage.all())
        initial_user_count = len(storage.all(User))
        method_count = storage.count()
        user_count = storage.count(User)
        self.assertEqual(initial_count, method_count)
        self.assertEqual(user_count, initial_user_count)
        t_new = User(
            email='bohn2020@gmail.com',
            password='password',
            first_name='John',
            last_name='Zoldyck'
        )
        db_c = MySQLdb.connect(
            host=os.getenv('HBNB_MYSQL_HOST'),
            port=3306,
            user=os.getenv('HBNB_MYSQL_USER'),
            passwd=os.getenv('HBNB_MYSQL_PWD'),
            db=os.getenv('HBNB_MYSQL_DB')
        )
        t_new.save()
        db_c.close()
        self.assertTrue(t_new in storage.all().values())
        method_count = storage.count()
        user_count = storage.count(User)
        self.assertEqual(initial_count + 1, method_count)
        self.assertEqual(initial_user_count + 1, user_count)

    def test_get(self):
        """Tests for the get method"""
        T_new = State(
            id='oboy',
            name='lagos',
            email='bohn2020@gmail.com',
            password='password',
            first_name='John',
            last_name='Zoldyck'
        )
        db_c = MySQLdb.connect(
            host=os.getenv('HBNB_MYSQL_HOST'),
            port=3306,
            user=os.getenv('HBNB_MYSQL_USER'),
            passwd=os.getenv('HBNB_MYSQL_PWD'),
            db=os.getenv('HBNB_MYSQL_DB')
        )
        if 'State.' + T_new.id not in storage.all().keys():
            T_new.save()
            self.assertTrue(T_new in storage.all().values())
        db_c.close()
        hold = storage.get(State, T_new.id)
        self.assertEqual(T_new.id, hold.id)
