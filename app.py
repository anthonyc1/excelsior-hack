#!/usr/bin/env python

#Website created by Anthony Chan
#anthonychan0123@gmail.com

#Website created by Shaan Sheikh
#shaansweb.com | shaansweb@gmail.com

import os
from datetime import datetime
import flask
from flask import Flask,render_template,request, redirect, flash, session,url_for,send_from_directory, Response
from dbfunctions import AuthDatabase



app = Flask(__name__)


database = AuthDatabase('exel.db')
app.secret_key = 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'


@app.route('/')
@app.route('/index')
def index():
	return render_template("index.html")

@app.route('/learnmore')
def learnmore():
	return render_template("learnmore.html")

@app.route('/contact')
def contact():
	return render_template("contact.html")

@app.route('/mentorship')
def mentorship():
	return render_template("mentorship.html")

@app.route('/collegevalue')
def collegevalue():
	return render_template("collegevalue.html")

@app.route('/elgibility')
def elgibility():
	return render_template("elgibility.html")

@app.route('/sunycuny')
def sunycuny():
	return render_template("sunycuny.html")

@app.route('/forum', methods=['GET', 'POST'])
def forum():

	if request.method == 'GET':
		posts = database.getPosts()
		replies = database.getComments()
		print replies
		return render_template("forum.html",comments=posts,replies=replies)
	else:
		database.insertPost(request.form['addTitle'],request.form['addComment'])

		return render_template("forum.html",comments=database.getPosts(),replies=database.getComments())



def main():
	app.debug = True
	app.run(host='0.0.0.0', port=8000)


if __name__ == '__main__':
	main()
	pass
