# -*- coding:utf-8 -*-
from flask import render_template, request, flash
from flask import redirect, url_for
from app import gdb, g_herb_type, models
import app.utils as utils
import datetime

def index():
    res = request.args
    module = res.get('m', 'index').lower()
    action = res.get('a', 'index').lower()
    print(module,action)
    vObj = eval('V'+module+'()')
    if vObj:
        func = getattr(vObj, action, None)
        if func:
            return func(module, action)
    return redirect('/index')

def initdb():
    tool = models.DbTools()
    tool.init()
    tool.importHerbs()
    #tool.testData()
    return 'init database finish'

def load_g_data():
    query = gdb.session.query(models.MHerbType)
    herb_types = query.all()
    for row in herb_types:
        g_herb_type[row.c_id]=row.c_name

    return True

#########################################################
### View Index
class Vindex(object):
    def index(self, module, action):
        param = ''
        template = module + '_' + action + ".html"
        return render_template(template, data=param)

class Vconfig(object):
    def index(self, module, action):
        query = gdb.session.query(models.MConfig)
        param = query.all()
        template = module + '_' + action + ".html"
        return render_template(template, data=param)
    def update(self, module, action):
        dw = request.values.get('default_weight', '15')
        dc = request.values.get('default_count', '4')
        dg = request.values.get('default_gain', '5')
        pu = request.values.get('price_unit', 'kg')
        #print(dw,dc,dg,pu)
        if dw=='' or dc=='' or dg=='':
            flash('配置项不能为空')
            return redirect('/index?m=config')
        models.MConfig.query.filter_by(c_name='default_weight').update({'c_value':dw})
        models.MConfig.query.filter_by(c_name='default_count').update({'c_value':dc})
        models.MConfig.query.filter_by(c_name='default_gain').update({'c_value':dg})
        models.MConfig.query.filter_by(c_name='price_uint').update({'c_value':pu})
        gdb.session.commit()
        flash('配置已经保存')
        return redirect('/index?m=config')
    def optimize(self, module, action):
        flash('数据库优化完成')
        return redirect('/index?m=config')

#########################################################
### View Herb
class Vherb(object):
    def index(self, module, action):
        page = request.args.get('page', 1, type=int)
        search = request.values.get('search', '')

        if search.encode('utf-8').isalpha():
            query = models.MHerb.query.filter(models.MHerb.c_py.like("%$"+search+"%"))
        else:
            query = models.MHerb.query.filter(models.MHerb.c_name.like("%"+search+"%"))
        pagination = query.paginate(page, 8, error_out=False)
        posts = pagination.items

        template = module + '_' + action + ".html"
        return render_template(template, data=posts, pagination=pagination, 
            herbtype=g_herb_type, search=search)
    def form(self, module, action):
        id = request.values.get('id', 0)
        search = request.values.get('search', '')
        if id==0:   #new
            param = 'new'
        else:
            query = models.MHerb.query.filter(models.MHerb.c_id==id)
            param = query.first()
        template = module + '_' + action + ".html"
        return render_template(template, data=param, herbtype=g_herb_type, search=search)
    def new(self, module, action):
        hn = request.values.get('herb_name', '')
        ht = request.values.get('herb_type', 0)
        hp = request.values.get('herb_price', 0)
        hg = request.values.get('herb_gain', 0)
        if hg=='':
            hg = 0
        h = models.MHerb(hn,ht,hp,hg)
        gdb.session.add(h)
        gdb.session.commit()
        return redirect('/index?m=herb&search='+hn)
    def save(self, module, action):
        hid = request.values.get('id', 0)
        hn = request.values.get('herb_name', '')
        hpy = utils.getPinyin(hn)
        ht = request.values.get('herb_type', 0)
        hp = request.values.get('herb_price', 0)
        hg = request.values.get('herb_gain', 0)
        if hn=='' or hp=='':
            flash('药品信息不能为空')
            return redirect('/index?m=herb&a=form&id='+hid)
        if hg=='':
            hg = 0
        herb = models.MHerb.query.filter_by(c_id=hid)
        herb.update({ 'c_name':hn, 'c_py':hpy, 'c_type':ht, 'c_price':hp, 'c_gain':hg })
        gdb.session.commit()
        flash('药品信息已经保存')
        return redirect('/index?m=herb&a=form&id='+hid)
    def delete(self, module, action):
        id = request.values.get('id', 0)
        herb = models.MHerb.query.filter_by(c_id=id)
        herb.delete()
        gdb.session.commit()
        return redirect('/index?m=herb')

#########################################################
### View Cure
class Vcure(object):
    def index(self, module, action):
        page = request.args.get('page', 1, type=int)
        search = request.values.get('search', '')

        if search.isdigit():
            query = models.MPatient.query.filter(models.MPatient.c_id==search)
        elif search.encode('utf-8').isalpha():
            query = models.MPatient.query.filter(models.MPatient.c_py.like("%$"+search+"%"))
        else:
            query = models.MPatient.query.filter(models.MPatient.c_name.like("%"+search+"%"))
        pagination = query.paginate(page, 8, error_out=False)
        posts = pagination.items

        template = module + '_' + action + ".html"
        return render_template(template, data=posts, pagination=pagination, search=search)

    def form(self, module, action):
        id = request.values.get('id', 0)
        search = request.values.get('search', '')
        if id==0:   #new
            param = 'new'
        else:
            query = models.MPatient.query.filter(models.MPatient.c_id==id)
            param = query.first()
        template = module + '_' + action + ".html"
        return render_template(template, data=param, search=search)
    def new(self, module, action):
        pn = request.values.get('cure_name', '')
        pa = request.values.get('cure_age', 0)
        ps = request.values.get('cure_sex', '')
        pi = request.values.get('cure_info', '')
        p = models.MPatient(pn, pa, ps, pi)
        gdb.session.add(p)
        gdb.session.commit()
        return redirect('/index?m=cure&search='+pn)
    def save(self, module, action):
        pid = request.values.get('id', 0)
        pn = request.values.get('cure_name', '')
        ppy = utils.getPinyin(pn)
        pa = request.values.get('cure_age', 0)
        ps = request.values.get('cure_sex', '')
        pi = request.values.get('cure_info', '')
        if pn=='' or pa==0:
            flash('药品信息不能为空')
            return redirect('/index?m=cure&a=form&id='+pid)
        patient = models.MPatient.query.filter_by(c_id=pid)
        patient.update({ 'c_name':pn, 'c_py':ppy, 'c_age':pa, 'c_sex':ps, 'c_info':pi })
        gdb.session.commit()
        flash('患者信息已经保存')
        return redirect('/index?m=cure&a=form&id='+pid)
    def delete(self, module, action):
        id = request.values.get('id', 0)
        patient = models.MPatient.query.filter_by(c_id=id)
        patient.delete()
        gdb.session.commit()
        return redirect('/index?m=cure')
    def list(self, module, action):
        id = request.values.get('id', 0)
        query = models.MPatient.query.filter_by(c_id=id)
        pa = query.first()
        ps = models.MPrescription.query.filter_by(c_petient_id=id)
        
        template = module + '_' + action + ".html"
        return render_template(template, data=ps, patient=pa)
    def step1(self, module, action):
        pid = request.values.get('pid', 0)
        query = models.MPatient.query.filter_by(c_id=pid)
        pa = query.first() 

        query = gdb.session.query(models.MHerb)
        herbs = query.all()
        herb_lists = []
        tmp = []
        
        tmp.append(1)
        old_type = 1
        for herb in herbs:
            if old_type < herb.c_type:
                herb_lists.append(tmp)
                tmp = []
                tmp.append(herb.c_type)
                old_type = herb.c_type
            tmp.append(herb)


        template = module + '_' + action + ".html"
        return render_template(template, data=herb_lists, patient=pa, 
            herbtype=g_herb_type)  
            
#########################################################
### View Take
class Vtake(object):
    def index(self, module, action):
        param = ''
        template = module + '_' + action + ".html"
        return render_template(template, data=param)

#########################################################
### View Fang
class Vfang(object):
    def index(self, module, action):
        page = request.args.get('page', 1, type=int)
        search = request.values.get('search', '')
        ##test git
        if search.encode('utf-8').isalpha():
            query = models.MFang.query.filter(models.MFang.c_py.like("%$"+search+"%"))
        else:
            query = models.MFang.query.filter(models.MFang.c_name.like("%"+search+"%"))
        pagination = query.paginate(page, 5, error_out=False)
        posts = pagination.items

        template = module + '_' + action + ".html"
        return render_template(template, data=posts, pagination=pagination, search=search)
    def new(self, module, action):
        query = gdb.session.query(models.MHerb)
        herbs = query.all()
        type_lists = []
        tmp = []
        for herb in herbs:
            if len(type_lists) < herb.c_type:
                tmp = []
                tmp.append(herb.c_type)
                type_lists.append(tmp)
            index = herb.c_type -1
            tmp = type_lists[index]
            tmp.append(herb)
            type_lists[index] = tmp

        template = module + '_' + action + ".html"
        return render_template(template, data=type_lists, herbtype=g_herb_type)

#########################################################
### View Query
class Vquery(object):
    def index(self, module, action):
        today = datetime.datetime.now()
        param = today.strftime('%Y-%m-%d')
        template = module + '_' + action + ".html"
        return render_template(template, data=param)