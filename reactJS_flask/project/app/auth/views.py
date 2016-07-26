# -*- coding: utf8 -*-

from . import auth
from flask import render_template

@auth.route('/login', methods=['get', 'post'])
def login():
	return render_template('auth/login.html')