import os
from flask import Flask,Blueprint,request,jsonify,render_template
from flask_sqlalchemy import SQLAlchemy
import pymysql
import hashlib
import random
import datetime
import pymssql
from flask_mail import Mail, Message
import time
import requests
import json

def Md5(res):
    print(res)
    md = hashlib.md5()  # 构造一个md5
    md.update(res.encode(encoding='utf-8'))
    # 加密
    print(md.hexdigest().upper())
    return md.hexdigest().upper()

app=Flask(__name__)
app.config['JSON_AS_ASCII'] = False
@app.route('/search')
def search():
    # zidian= json.load(requests.data)
    # data=zidian['med']
    data=(request.args.get('data'))
    conn = pymysql.connect(host='124.220.156.129', user='med', password='8ZDYwGcLJTM8YxMY', db='med')
    cur = conn.cursor()
    sql="select * from med where med like '"+"{}".format(data)+"%' limit 10"
    print(sql)
    cur.execute(sql)
    u=cur.fetchall()
    conn.commit()
    conn.close()
    result={}
    result['msg']='right'
    result['data']=u
    return result











@app.route('/avv')
def avv():
    conn = pymysql.connect(host='118.178.241.96', user='patients', password='LiwZ5eHyksRtpDJf', db='patients')
    cur = conn.cursor()
    sql3 = "DROP VIEW b"
    cur.execute(sql3)
    conn.close()
    return "delete"


@app.route('/disease/<keyword>')
def add(keyword):
    keyword = keyword[keyword.index("=") + 1:]
    print(keyword)
    conn=pymysql.connect(host='118.178.241.96',user='patients',password='LiwZ5eHyksRtpDJf',db='patients')
    cur=conn.cursor()
    sql1='''CREATE VIEW b AS SELECT med1,COUNT(med1) AS num FROM human WHERE(HumanSign IN '''+keyword +''') GROUP BY med1 UNION SELECT med2,COUNT(med2) AS num FROM human WHERE(HumanSign IN '''+keyword +''') GROUP BY med2 UNION SELECT med3,COUNT(med3) AS num FROM human WHERE(HumanSign IN '''+keyword +''') GROUP BY med3 UNION SELECT med4,COUNT(med4) AS num FROM human WHERE(HumanSign IN '''+keyword +''') GROUP 
    BY med4 UNION SELECT med5,COUNT(med5) AS num FROM human WHERE(HumanSign IN '''+keyword +''') GROUP BY med5 UNION SELECT med6,COUNT(med6) AS num FROM human WHERE(HumanSign IN '''+keyword +''') GROUP BY med6 UNION SELECT med7,COUNT(med7) AS num FROM human WHERE(HumanSign IN '''+keyword +''') GROUP BY med7'''
    print(sql1)
    cur.execute(sql1)
    sql2 = "SELECT med1 FROM b ORDER BY num DESC LIMIT 5"
    cur.execute(sql2)
    u=cur.fetchall()
    sql3 = "DROP VIEW b"
    cur.execute(sql3)
    a = []
    for i in range(5):
        sql4 = "SELECT element FROM med WHERE med='" + "{}".format(u[i][0]) + "'"
        print(sql4)
        cur.execute(sql4)
        v=cur.fetchall()
        a.append(v)
        print(v)
    conn.close()
    json_dict = {
        "values":u,
        "neirong":a
    }
    return jsonify(json_dict)
@app.route('/a')
def index():
    return "hey"

@app.route('/searchmed/<keyword>')
def searchmed(keyword):
    conn = pymysql.connect(host='118.178.241.96', user='patients', password='LiwZ5eHyksRtpDJf', db='patients')
    cur = conn.cursor()
    keyword = keyword[ keyword.index("=")+1:]
    print(keyword)
    sql="SELECT element FROM med WHERE med='"+"{}".format(keyword) + "'"
    sql2="UPDATE med SET sum=sum+1 WHERE med=\""+"{}".format(keyword) + "\""
    print(sql2)
    cur.execute(sql)
    u1 = cur.fetchall()
    cur.execute(sql2)
    conn.commit()
    conn.close()
    json_dict = {
        "values": u1[0]
    }
    return jsonify(json_dict)

@app.route('/paixv')
def paixv():
    conn = pymysql.connect(host='124.220.156.129', user='med', password='8ZDYwGcLJTM8YxMY', db='med')
    cur = conn.cursor()
    sql = "SELECT med FROM med ORDER BY sum DESC LIMIT 8"
    cur.execute(sql)
    u = cur.fetchall()
    print(u)
    conn.close()
    json_dict = {
        "values1": u
    }
    return jsonify(json_dict)






if __name__=="__main__":
    app.run(port=5000)



