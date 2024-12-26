from flask import Flask, render_template
import subprocess
from pymongo import MongoClient

app = Flask(__name__)

mongo_client = MongoClient("mongodb://localhost:27017/")
db = mongo_client["twitter_trends"]
collection = db["trending_topics"]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_script')
def run_script():
    try:
        subprocess.run(["python", "selenium_script.py"], check=True)

        last_record = collection.find().sort("_id", -1).limit(1)
        last_record = list(last_record)  

        if not last_record:
            return render_template('no_records.html')

        last_record = last_record[0]
        return render_template('results.html', record=last_record)

    except subprocess.CalledProcessError as e:
        return render_template('error.html', error_message=str(e))

if __name__ == '__main__':
    app.run(debug=True)
