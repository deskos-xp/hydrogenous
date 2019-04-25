#! /usr/bin/env python3

import os,json
from datetime import datetime
import time
import sqlite3

class handler:
    sql_type='SQLite3'
    def __init__(me,self):
        me.cursor=None
        me.db=None
        me.parent=self
        print(self.main['dbName'])
    def disconnect(me):
        pass
