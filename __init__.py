from flask import Flask, request, session, render_template, flash, redirect
import os.path
from pathlib import Path
from flask import jsonify, redirect, url_for
from wtforms import Form, BooleanField, TextField, PasswordField, validators
from datetime import datetime
import compute 
import json
#from pprint import pprint


app = Flask(__name__)
app.secret_key = b'\x9e\x02\xc2<W!A\xf8\xe2\x169:v\x97lC'

def convert_keys_to_string(dictionary):
    """Recursively converts dictionary keys to strings."""
    if not isinstance(dictionary, dict):
        return dictionary
    return dict((str(k), convert_keys_to_string(v)) 
        for k, v in dictionary.items())

app.route('/app1', methods = ["GET", "POST"])
@app.route('/', methods = ["GET", "POST"])
def app1():
	print("app1")
	data = {}
	bname = ""
	if request.method == "POST":
		bname = request.form['restaurant']
		print("bname", bname)
		fileName = bname + ".json"
		with open('./reviews/' + fileName) as f:
			data = json.load(f)
	
		#reviews = data["reviews"]
		return render_template("index1.html", dic=data, restaurant=bname)
	
	return render_template("index1.html", dic=data, restaurant=bname)

@app.route('/app2', methods = ["GET", "POST"])
def app2():
	print("app2")
	dic = {}
	if request.method == "POST":
		print("Searching......")
		bname = request.form['restaurant']
		print("bname", bname)
		dic = compute.main(bname, True)
		print(dic)
		return render_template("index.html", dic=(dic), displayLoad="none", displayRes="block")
	
	return render_template("index.html", dic=(dic), displayLoad="none", displayRes="none")

@app.route('/redirecter/', methods = ["GET", "POST"])
def redirecter():
	dic = {}
	
	if request.method == "GET":
		bname = request.args.get("bname")
		caption = request.args.get("caption")
		item = compute.getItem(bname, caption).lower()
		item = item.replace(" ", "-")
		url = 'https://www.yelp.com/menu/' + bname + '/item/' + item
		print(url)
		return redirect(url, code=303)
	
	return render_template("index.html", dic=(dic), displayLoad="none", displayRes="none")

if __name__ == "__main__":
	app.run()
