from flask import Flask, redirect, render_template, request, url_for
import helpers
import os
import sys
from analyzer import Analyzer

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():

    screen_name = request.args.get("screen_name", "").lstrip("@")       # validate screen_name
    if not screen_name:
        return redirect(url_for("index"))

    positives = os.path.join(sys.path[0], "positive-words.txt")         # absolute paths to lists
    negatives = os.path.join(sys.path[0], "negative-words.txt")

    analyzer = Analyzer(positives, negatives)                           # instantiate analyzer
    
    tweets = helpers.get_user_timeline(screen_name, 100)                # get screen_name's most recent 100 tweets
    
    if tweets == None:                                                  # return to index if screen_name doesn't exist
        return redirect(url_for("index"))
        
    positive, negative, neutral = 0, 0, 0                               # create positive, negative and neutral count

    for tweet in tweets:                                                # analyze each tweet & increase corresponding sentimen count
        score = analyzer.analyze(tweet)
        if score > 0.0:
            positive += 1
        elif score < 0.0:
            negative += 1
        else:
            neutral += 1

    chart = helpers.chart(positive, negative, neutral)                  # generate chart

    return render_template("search.html", chart=chart, screen_name=screen_name)         # render results
