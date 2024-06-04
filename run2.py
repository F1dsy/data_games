from flask import Flask, render_template, request, jsonify
import os
import random
import csv
#import cv2
try:
    import app.GETDATA
except:
    import GETDATA

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        path = "static/"
        files=os.listdir(path)
        d=random.choice(files)
        return render_template("index.html", flag=d)
    else:
        data = GETDATA.getRandomCountry()
        vej = request.form["flag"]
        for d in data:
            if d['filnavn'] == vej:
                country_name = d['land']
                break
            else:
                country_name = "Not found yet"

        if request.form["guess"] == country_name:
            result = "That's correct!"
        else:
            result = f"That's wrong, it's {country_name}. Jonas would have guessed that"
        
        path = "static/"
        files=os.listdir(path)
        d=random.choice(files)
        return render_template("index.html", flag=d, result=result)



if __name__ == '__main__':
    app.run(host='0.0.0.0')