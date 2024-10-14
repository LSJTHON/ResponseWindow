from flask import Flask, render_template, url_for, redirect  #Flask 모듈
import dht as d                                              #온습도 센서 모듈
import gas as g                                              #가스센서 모듈
import motor as m
import pymysql
import RPi.GPIO as GPIO
import time
GPIO.setup(4, GPIO.IN, GPIO.PUD_UP)
a = True

def init():
    temp = d.temp() #온도 측정
    humi = d.humi() #습도 측정
    gas = g.gas()   #가스 측정
    return temp, humi, gas

def manual_Control(set2):
    if set2 == 1:
        m.motor('open')
        return "열림"
    
    elif set2 == 0:
        m.motor('close')
        return '닫힘'

@app.route('/')
def home():
    while True:
        temp, humi, gas = restart()
        return render_template("hello.html", temp = temp, gas = gas, humi = humi result = "수동", result2 = "닫힘")

@app.route('/<int:set1>/<int:set2>')
def set_mode(set1,set2):
    if set1 == 1:

        result2 = manual_Control(set2)
        result = '자동'
        onoff = 'disabled'
        a = True
        restart()
        post()
        select()
        if (rows[i][0] >= 30.0 or rows[i][1] <= 30 or GPIO.input(4) == GPIO.HIGH):
                time.sleep(2)
            if a != True:
                m.motor('open')
                a = True
        elif (rows[i][0] <= 26.0 or rows[i][1] > 30):
            if a != False:
                m.motor('close')
            a = False
        i = i+1
        return render_template('hello.html',rows = rows,
                                result=result,result2 = result2, onoff = onoff)
    elif set1 == 0:
        result2 = manual_Control(set2)
        result = '수동'
        if set2 == 0:
            m.motor('close')
        elif set2 == 1:
            m.motor('open')
        onoff = ''
        return render_template('hello.html',rows = rows,
                               result=result,result2 = result2, onoff = onoff)
    return 0

def con():
    return pymysql.connect(host = 'swc.mysql.pythonanywhere-services.com',
                           user = 'swc', password = 'swcswcsw',
                           db = 'swc$default', charset = 'utf8')

def create_table():
    con = con()
    con.execute('create table table(float temp, float humi, float gas)')
    con.close()

def select():
    con = con()
    cur = con.cursor()
    cur.execute('select * from table')
    rows = cur.fetchall()
    con.close()

@app.route('/post', methods = ['post', 'get'])
def post():
    if request.method == 'post':
        item = request.form['id']
 
        try:
            con = con()
            cur = con.cursor()
            cur.execute('insert into table (temp, humi, gas) values (%f, %f, %f)', (temp, humi, gas))
            con.commit()
            msg = ''
        except:
            con.rollback()
            msg = ''
        finally:
            con.close()
