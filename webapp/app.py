#!/Users/andersaarvikBC/PycharmProjects/webdl/bin/python

from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

from webdl import webdl
from webdl import db

s = db.session()

@app.route("/")
def main():
    websites = list()

    results = s.execute(db.select([db.Website]))

    for result in results:
        info = {
            'id': result.id,
            'url': result.url,
            'last_modified': result.last_modified
        }

        websites.append(info)

    return render_template('main.html', websites=websites)

@app.route("/logs")
def logs():
    logs = list()

    results = s.execute(db.select([db.Log]))

    for result in results:
        info = {
            'id': result.id,
            'website_id': result.website_id,
            'type': result.type,
            'output': result.output,
            'timestamp': result.timestamp
        }

        logs.append(info)

    return render_template('logs.html', logs=logs)

@app.route("/options")
def options():
    options = list()

    results = s.execute(db.select([db.Options]))

    for result in results:
        info = {
            'id': result.id,
            'option': result.option,
            'option_type': result.option_type,
            'option_value': result.option_value
        }

        options.append(info)

    return render_template('options.html', options=options)

@app.route("/local_website", methods=['GET'])
def local_website():
    return app.send_static_file('local_websites/%s/%s/index.html' % (request.args.get('local_website'), request.args.get('local_website')))

if __name__ == "__main__":
    app.debug = True
    app.run()
