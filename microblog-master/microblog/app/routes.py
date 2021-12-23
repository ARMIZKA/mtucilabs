# -*- coding: utf-8 -*-
from flask import render_template, request
from app import app

user = {'username': 'Dear Friend '}
posts = [
    {
        'author': {'username': 'Arthas'},
        'body': 'Your soul shall be mine!'
    },
    {
        'author': {'username': 'Alex'},
        'body': 'Waasup!'
    },
    {
        'author': {'username': 'ZXZXZX'},
        'body': 'QWQWQW'
    }
]


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home', user=user, posts=posts)


@app.route('/dict', methods=['post'])
def dict():
    nickname = str(request.form.get("nickname"))
    message = str(request.form.get("message"))

    posts.append({
        'author': {'username': nickname},
        'body': message
    })

    return render_template('index.html', title='Home', user=user, posts=posts)