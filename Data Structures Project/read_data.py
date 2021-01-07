#Data Structures Project
#By Jamal Uddin Ahamed
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 00:11:47 2020

@author: Jamal
"""
import sys
import csv
import os
#from database import Base,Accounts,Customers,Users,CustomerLog,Transactions
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_bcrypt import Bcrypt
from flask import Flask
app = Flask(__name__)
engine = create_engine('sqlite:///database.db',connect_args={'check_same_thread': False},echo=True)
#Base.metadata.bind = engine
db = scoped_session(sessionmaker(bind=engine))
bcrypt = Bcrypt(app)

passw = 'userpass'
passw_hash = bcrypt.generate_password_hash(passw).decode('utf-8')
usern = "employee"
result = db.execute("SELECT * FROM users WHERE id = :u", {"u": usern}).fetchone()
print(bcrypt.check_password_hash(result['password'], passw))
print(passw_hash)
print(result["password"])