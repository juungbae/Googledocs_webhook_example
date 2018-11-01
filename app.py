from flask import Flask, request, render_template
from sqlalchemy import Column, String, Enum, DateTime
from sqlalchemy.ext.declarative import declarative_base
import enum
from datetime import datetime
from uuid import uuid4
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy_session import flask_scoped_session


app = Flask(__name__, static_url_path='')
uri = 'mysql+pymysql://hack:1234@localhost/hack'
engine = create_engine(uri)
session_factory = sessionmaker(bind=engine)
Base = declarative_base()
session = flask_scoped_session(session_factory, app)


class Type(enum.Enum):
    person = "Person"
    team = "Team"


class Logs(Base):
    __tablename__ = "logs"
    id = Column(String(32), primary_key=True)
    type = Column(Enum(Type), nullable=False)
    timestamp = Column(DateTime, default=datetime.now, nullable=False)

    def __init__(self, type):
        self.id = str(uuid4()).replace('-', '')
        self.type = type


@app.route("/webhook", methods=['POST'])
def webhook_counter():
    payload = request.form.get('payload')
    payload = json.loads(payload)
    type = payload['type']

    obj = Logs(type)
    session.add(obj)
    session.commit()

    return "{ \"message\" : \"success\"}"


@app.route("/")
def current():
    query_result = session.query(Logs).all()
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
    app.run(port=8901, debug=True)
