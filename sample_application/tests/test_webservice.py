from flask.ext.testing import TestCase
from flask import url_for, request
import unittest
from sample_application.models import Base
from sample_application import app
import json
import os
from mock import mock

class TestServices(TestCase):
    '''Tests that each route is an http response'''

    def create_app(self):
        '''Start the wsgi application'''
        a = app.create_app(**{
               'SQLALCHEMY_DATABASE_URI': 'sqlite://',
               'SQLALCHEMY_ECHO': False,
               'TESTING': True,
               'PROPAGATE_EXCEPTIONS': True,
               'TRAP_BAD_REQUEST_ERRORS': True
            })
        Base.metadata.bind = a.db.session.get_bind()
        Base.metadata.create_all()
        return a


    def tearDown(self):
        unittest.TestCase.tearDown(self)
        Base.metadata.drop_all()
        self.app.db = None


    def test_date(self):
        # if you want to know the urls: print self.app.url_map
        
        r = self.client.post(url_for('sample_application.date', date='2018-09-10 20:15:57'))
        self.assertEqual(r.status_code,200)
        assert r.json == {u'date': u'2018-09-10T20:15:57+00:00'}
    
        r = self.client.get(url_for('sample_application.date', date='2018-09-10 20:15:57'))
        self.assertEqual(r.status_code,200)
        assert r.json == {u'date': u'2018-09-10T20:15:57+00:00'}
    
        r = self.client.get(url_for('sample_application.date'))
        self.assertEqual(r.status_code,200)
        assert 'date' in r.json
        
if __name__ == '__main__':
  unittest.main()
