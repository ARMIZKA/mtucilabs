import requests
from flask import Flask, render_template, request, redirect
import psycopg2
from KEYS import dbpass
app = Flask(__name__)
conn = psycopg2.connect(database="db_registr",
                        user="postgres",
                        password=dbpass,
                        host="localhost",
                        port="5432")

cursor = conn.cursor()


@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form.get("login"):
            username = request.form.get('username')
            password = request.form.get('password')
            user_exist = False
            password_exist = False
            if username == '':
                user_exist = True
            if password == '':
                password_exist = True
            try:
                cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s",
                               (str(username), str(password)))
                records = list(cursor.fetchall())
                return render_template('account.html', full_name=records[0][1], login=records[0][2],
                                       password=records[0][3])
            except IndexError:
                return render_template('login.html', error=True, password_exist=password_exist, user_exist=user_exist)
        elif request.form.get("registration"):
            return redirect("/registration/")
    return render_template('login.html')


@app.route('/registration/', methods=['POST', 'GET'])
def registration():
    name_exist = False
    login_exist = False
    password_exist = False
    if request.method == 'POST':

        name = request.form.get('name')
        user_login = request.form.get('login')
        password = request.form.get('password')

        if name == '':
            name_exist = True
        if password == '':
            login_exist = True
        if password == '':
            password_exist = True

        if name_exist or login_exist or password_exist:
            return render_template('registration.html', name_exist=name_exist, login_exist=login_exist,
                                   password_exist=password_exist, coincidence=False)
        else:
            cursor.execute('SELECT * FROM service.users WHERE login = %s ;', [str(user_login)])
            records = list(cursor.fetchall())
            if records:
                return render_template('registration.html', name_exist=name_exist, login_exist=login_exist,
                                       password_exist=password_exist, coincidence=True)
            else:
                cursor.execute('INSERT INTO service.users (full_name, login, password) VALUES (%s, %s, %s);',
                               (str(name), str(user_login), str(password)))
                conn.commit()
                return redirect('/login/')
    return render_template('registration.html', name_exist=name_exist, login_exist=login_exist,
                           password_exist=password_exist, coincidence=False)