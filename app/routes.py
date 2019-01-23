# -*- coding:utf-8 -*-
from flask import redirect, url_for
from app import app, g_herb_type
from app import views

#加载全局数据
views.load_g_data()
#print(g_herb_type)

@app.route('/favicon.ico')
def favicon():
    return redirect(url_for('static', filename='favicon.ico'), code=301)

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    return views.index()

@app.route('/initdb')
def initdb():
    return views.initdb()

@app.errorhandler(404)
def page_not_found(e):
    return redirect('/index')
