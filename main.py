from flask import Flask
from flask import url_for
from flask import render_template
# from flask import flash
# from flask import request
from get_id import *
import random
import urllib
import urllib.request
import re


app = Flask(__name__)


@app.route('/')
def index():
	return render_template('index.html')


@app.route('/video')
def video():
	id = get_new_video()
	return render_template('video.html', id=id)

with app.test_request_context():
	print(url_for('index'))
	print(url_for('video'))
	print(url_for('static', filename='style.css'))


def get_new_video():
	with open("keywords.txt") as kw:
		keywords = kw.read().splitlines()
	return view_limit(50, keywords)


def view_limit(limit, keywords):
	with open("filter.txt") as fil:
		filter = fil.read().splitlines()
	while True:
		randkeyword = random.choice(keywords)
		validids = get_id(randkeyword)
		try:
			if len(validids) == 0:
				continue
		except TypeError:
			continue
		tryid = random.choice(validids)
		url = 'http://gdata.youtube.com/feeds/api/videos/' + tryid
		try:
			title, views = test_connection(url)
		except TypeError:
			continue
		if title is None or title == [] or views is None or views == []:
			continue
		elif any(f.lower() in title[0].lower() for f in filter):
			continue
		elif views < limit:
			return tryid


# Tries connection and returns view count (if the id is valid)
def test_connection(url):
	try:
		sock = urllib.request.urlopen(url).read().decode("utf-8")
		titlepatt = re.compile("<title[^>]*>(.*?)</title>")
		viewpatt = re.compile("viewCount='(.*?)'/>")
		title = titlepatt.findall(sock)
		views = viewpatt.findall(sock)
		if views == [] or views is None:
			return(title, 0)
		else:
			return(title, int(views[0]))
	except Exception:
		pass


def get_id(searchquery):
	gdataurl = "http://gdata.youtube.com/feeds/api/videos?q="
	try:
		sock = urllib.request.urlopen(gdataurl + searchquery).read().decode("utf-8")
		idatt = re.compile("/v/(.*?)\?")
		foundid = idatt.findall(sock)
		return foundid
	except Exception:
		pass


if __name__ == '__main__':
	app.run()
