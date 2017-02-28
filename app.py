#!/usr/bin/env python

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
@app.route('/home')
def index():
	return render_template("index.html")

@app.route('/learnmore')
def learnmore():
	return render_template("learnmore.html")

@app.route('/collegevalue')
def cllegevalue():
	return render_template("collegevalue.html")

@app.route('/forum', methods=['GET', 'POST'])
def forum():

	if request.method == 'GET':
		posts = database.getPosts()
		print posts
		return render_template("forum.html",comments=posts)
	else:
		print request.form 
		return render_template("forum.html",comments=database.getPosts())



def main():
	app.debug = True
	app.run(host='0.0.0.0', port=8000)


if __name__ == '__main__':
	main()
	pass
