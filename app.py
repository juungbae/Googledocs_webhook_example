from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
import enum
from datetime import datetime
from uuid import uuid4
import json


app = Flask(__name__, static_url_path='')
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'mysql+pymysql://hack:1234@localhost/hack'
db = SQLAlchemy(app)


class Type(enum.Enum):
    person = "Person"
    team = "Team"


class Logs(db.Model):
    id = db.Column(db.String(32), primary_key=True)
    type = db.Column(db.Enum(Type), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now, nullable=False)

    def __init__(self, type):
        self.id = str(uuid4()).replace('-', '')
        self.type = type


@app.route("/webhook", methods=['POST'])
def webhook_counter():
    payload = request.form.get('payload')
    payload = json.loads(payload)
    type = payload['type']

    obj = Logs(type)
    db.session.add(obj)
    db.session.commit()

    return "{ \"message\" : \"success\"}"


@app.route("/")
def current():
    query_result = db.session.query(Logs).all()
    obj = {
        "Person": 0,
        "Team": 0
    }

    for i in query_result:
        obj[i.type.value] = obj[i.type.value] + 1

    now = datetime.now()
    datestring = now.strftime("%Y년 %m월 %d일 ")
    datestring += ("이른" if now.hour < 12 else "늦은")
    datestring += now.strftime(" %I시 %M분 %S초")

    return render_template(
            'index.html', person=obj['Person'], team=obj['Team'],
            current=datestring, all=(obj['Person']+obj['Team']))


if __name__ == "__main__":
    db.create_all()
    app.run(port=8901, debug=True)
