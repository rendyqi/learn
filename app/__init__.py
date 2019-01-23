# -*- coding:utf-8 -*-
from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
import os.path
from app.tools import pinyin
#import sys
#print (sys.path)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a very secret string'

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database/rendy.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'True'

# 全局数据库对象
gdb = SQLAlchemy(app)

# 全局拼音对象
gpy = pinyin.PinYin()
gpy.load_dict()

#全局变量
g_herb_type = {'0':'未知类型'}