
from database import Database


import sqlite3
import os
import glob

__all__ = ['AuthDatabase']


class AuthDatabase(Database):

    def getPosts(self):
        return self._execute('SELECT * FROM Posts')


    def insertPost(self,title,post):
        self._execute('INSERT INTO Posts(postTitle, post) VALUES (?,?);',(title,post))

    def getComments(self):
        return self._execute('SELECT * FROM Comments')

    

