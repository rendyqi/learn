# -*- coding:utf-8 -*-
import os.path
from app import gdb
import app.utils as utils

class MHerb(gdb.Model):
    __tablename__ = 't_herbs'
    c_id = gdb.Column(gdb.Integer, primary_key=True)
    c_name = gdb.Column(gdb.String(10))
    c_py = gdb.Column(gdb.String(50))
    c_type = gdb.Column(gdb.Integer)
    c_price = gdb.Column(gdb.Float)
    c_gain = gdb.Column(gdb.Float)
    c_stock = gdb.Column(gdb.Integer)

    def __init__(self, p_name, p_type, p_price=0.0, p_gain=0, p_stock=0):
        self.c_name = p_name
        self.c_py = utils.getPinyin(p_name)
        self.c_type = p_type
        self.c_price = p_price
        self.c_gain = p_gain
        self.c_stock = p_stock

    def __repr__(self):
        return '<Herb %s>' % self.c_name

class MHerbType(gdb.Model):
    __tablename__ = 't_herbtypes'
    c_id = gdb.Column(gdb.Integer, primary_key=True)
    c_name = gdb.Column(gdb.String(10), unique=True)

    def __init__(self, p_name):
        self.c_name = p_name

    def __repr__(self):
        return '<HerbType %s>' % self.c_name

class MPatient(gdb.Model):
    __tablename__ = 't_patients'
    c_id = gdb.Column(gdb.Integer, primary_key=True)
    c_name = gdb.Column(gdb.String(10))
    c_py = gdb.Column(gdb.String(50))
    c_age = gdb.Column(gdb.Integer)
    c_sex = gdb.Column(gdb.String(1))
    c_info = gdb.Column(gdb.String(50))

    def __init__(self, p_name, p_age, p_sex, p_info=''):
        self.c_name = p_name
        self.c_py = utils.getPinyin(p_name)
        self.c_age = p_age
        self.c_sex = p_sex
        self.c_info = p_info

    def __repr__(self):
        return '<Patient %s>' % self.name

class MFang(gdb.Model):
    __tablename__ = 't_fangs'
    c_id = gdb.Column(gdb.Integer, primary_key=True)
    c_name = gdb.Column(gdb.String(10), unique=True)
    c_py = gdb.Column(gdb.String(50))
    c_content = gdb.Column(gdb.Text)

    def __init__(self, p_name, p_content):
        self.c_name = p_name
        self.c_py = utils.getPinyin(p_name)
        self.c_contentc_age = p_content

    def __repr__(self):
        return '<Fang %s>' % self.name

class MPrescription(gdb.Model):
    __tablename__ = 't_prescriptions'
    c_id = gdb.Column(gdb.Integer, primary_key=True)
    c_doctor = gdb.Column(gdb.String(10))
    c_petient_id = gdb.Column(gdb.Integer)
    c_date = gdb.Column(gdb.DateTime)
    c_time = gdb.Column(gdb.DateTime)
    c_content = gdb.Column(gdb.Text)
    c_count = gdb.Column(gdb.Integer)
    c_price = gdb.Column(gdb.Float)
    c_money = gdb.Column(gdb.Float)
    c_take = gdb.Column(gdb.Integer)

    def __init__(self, p_doctor, p_petient_id, p_date, p_time,\
                p_content, p_count=4, p_price=0.0, p_money=0.0, p_take=0):
        self.c_doctor = p_doctor
        self.c_petient_id = p_petient_id
        self.c_date = p_date
        self.c_time = p_time
        self.c_content = p_content
        self.c_count = p_count
        self.c_price = p_price
        self.c_money = p_money
        self.c_take = p_take

    def __repr__(self):
        return '<Prescription %s>' % (self.c_doctor+self.c_petient_id+self.c_date+self.c_time)

class MUser(gdb.Model):
    __tablename__ = 't_users'
    c_id = gdb.Column(gdb.Integer, primary_key=True)
    c_name = gdb.Column(gdb.String(10), unique=True)
    c_py = gdb.Column(gdb.String(50))
    c_pwd = gdb.Column(gdb.String(32))
    c_permission = gdb.Column(gdb.Integer)

    def __init__(self, p_name, p_pwd, p_permission):
        self.c_name = p_name
        self.c_py = utils.getPinyin(p_name)
        self.c_pwd = p_pwd
        self.c_permission = p_permission

    def __repr__(self):
        return '<User %s>' % self.name

class MConfig(gdb.Model):
    __tablename__ = 't_config'
    c_name = gdb.Column(gdb.String(10), primary_key=True)
    c_value = gdb.Column(gdb.String(10))

    def __init__(self, p_name, p_value):
        self.c_name = p_name
        self.c_value = p_value

    def __repr__(self):
        return '<Config %s>' % self.c_name

################################################################    

class AllQuery(object):
    def q_herb(self):
        # query = gdb.session.query(Herb, Patient)
        # query = query.filter(Herb.id == Patient.id)
        #query = gdb.session.query(MHerb)
        #return query.all()
        pass
    def q_patient(self):
        # query = gdb.session.query(Herb, Patient)
        # query = query.filter(Herb.id == Patient.id)
        #query = gdb.session.query(Patient)
        #return query.all()
        pass

class DbTools(object):
    @classmethod
    def init(cls):
        gdb.drop_all()
        gdb.create_all()

        cfg = []
        cfg.append(MConfig('default_weight','15'))
        cfg.append(MConfig('default_count','4'))
        cfg.append(MConfig('default_gain','5'))
        cfg.append(MConfig('price_uint','kg'))
        for c in cfg:
            gdb.session.add(c)
        gdb.session.commit()

    @classmethod
    def testData(cls):
        p = MPatient('rendy',30,'男')
        p1 = MPatient('齐文凌',30,'男')
        gdb.session.add(p)
        gdb.session.add(p1)
        u = MUser('rendy', '123', 1)
        gdb.session.add(u)
        gdb.session.commit()

    def importHerbs(cls):
        herbtype = 0
        basedir = os.path.abspath(os.path.dirname(__file__))
        herbf = os.path.join(basedir, 'extdata/zyherbs.txt')
        fp = open(herbf, 'r', encoding='UTF-8')
        line = fp.readline()
        while line:
            if line.strip()=='' :
                line = fp.readline()
                continue
            line = line.strip('\n')
            if line[:1]==' ' :
                line = line.strip()
                h = MHerb(line, herbtype, 100.0)
                gdb.session.add(h)      
                #print("herb %s"%line)
            else:
                ht = MHerbType(line)
                gdb.session.add(ht)
                herbtype += 1
                #print("type %s"%line)
            line = fp.readline()
        gdb.session.commit()   
        fp.close()
        return True



if __name__ == "__main__":
    test = DbTools()
    test.importHerbs()