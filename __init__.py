#This is the file that contains back-end code of project. It runs the algorithm from compute.py and sends data to html, renders template to html in front-end
from flask import Flask, request, session, render_template, flash, redirect
import os.path
from pathlib import Path
from flask import jsonify, redirect, url_for
from wtforms import Form, BooleanField, TextField, PasswordField, validators
from datetime import datetime
import compute 
import json

app = Flask(__name__)
app.secret_key = b'\x9e\x02\xc2<W!A\xf8\xe2\x169:v\x97lC'

def convert_keys_to_string(dictionary):
    """Recursively converts dictionary keys to strings."""
    if not isinstance(dictionary, dict):
        return dictionary
    return dict((str(k), convert_keys_to_string(v)) 
        for k, v in dictionary.items())

@app.route('/app2/', methods = ["GET", "POST"])
@app.route('/', methods = ["GET", "POST"])
def app2():
	print("In app2")
	data = {}
	bname = ""
	get_bname = request.args.get("bname")
	if request.method == "POST":
		bname = request.form['restaurant']
		print("bname", bname)
		fileName = bname + ".json"
		with open('./reviews/' + fileName) as f:
			data = json.load(f)
	
		return render_template("index1.html", dic=data, restaurant=bname, app="app2")
	elif get_bname != None:
		print("Searching......")
		bname = get_bname
		print("bname", bname)
		fileName = bname + ".json"
		with open('./reviews/' + fileName) as f:
			data = json.load(f)
		return render_template("index1.html", dic=data, restaurant=bname, app="app2")
	
	return render_template("index1.html", dic=data, restaurant=bname, app="app2")

@app.route('/app1/', methods = ["GET", "POST"])
def app1():
	print("In app1")
	bname = ""
	dic = {}
	get_bname = request.args.get("bname")
	if request.method == "POST":
		print("Searching......")
		bname = request.form['restaurant']
		print("bname", bname)
		dic = compute.main(bname, top_three=True)
		print(len(dic.keys()))
		num_items = len(dic.keys())
		return render_template("index.html", restaurant=bname, dic=(dic), num=num_items, displayLoad="none", displayRes="block", app="app1")
	elif get_bname != None:
		print("Searching......")
		bname = get_bname
		print("bname", bname)
		dic = compute.main(bname, top_three=True)
		print(len(dic.keys()))
		num_items = len(dic.keys())
		return render_template("index.html", restaurant=bname, dic=(dic), num=num_items, displayLoad="none", displayRes="block", app="app1")
	
	return render_template("index.html", restaurant=bname, dic=(dic), displayLoad="none", displayRes="none", app="app1")

@app.route('/redirecter/', methods = ["GET", "POST"])
def redirecter():
	dic = {}
	if request.method == "GET":
		bname = request.args.get("bname")
		caption = request.args.get("caption")
		item, score = compute.getItem(bname, caption)
		print(score)
		if score < 0.6:
			url = 'https://www.yelp.com/menu/' + bname
			return redirect(url, code=303)
		else:
			url = 'https://www.yelp.com/menu/' + bname + '/item/' + item
			print(url)
			return redirect(url, code=303)
	
	return render_template("index.html", dic=(dic), displayLoad="none", displayRes="none", app="app1")

if __name__ == "__main__":
	app.run()
