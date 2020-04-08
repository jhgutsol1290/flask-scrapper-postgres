import os

from flask import Flask, jsonify, request, Response
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields

from controllers.controller import (PerformSearch,
                                    Validator)

# Init app
app = Flask(__name__)

ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/scrapper'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://pwdcwdvbeoleep:52f788cceed84b92903381949f0f16acd190089904d939981f897929003f959e@ec2-34-197-212-240.compute-1.amazonaws.com:5432/d6fh5a24mu20mb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Initialize db
db = SQLAlchemy(app)
# Initialize ma
ma = Marshmallow(app)

# Models


class Input(db.Model):
    __tablename__ = 'input'
    id = db.Column(db.Integer, primary_key=True)
    input_query = db.Column(db.String(200), unique=True)
    scrappers = db.relationship('Scrapper', backref='input')


class Scrapper(db.Model):
    __tablename__ = 'scrapper'
    id = db.Column(db.Integer, primary_key=True)
    reference = db.Column(db.String(200))
    rating = db.Column(db.Float)
    content = db.Column(db.Text())
    input_id = db.Column(db.Integer, db.ForeignKey('input.id'))

# Serializers


class ScrapperSchema(ma.Schema):
    class Meta:
        fields = ('reference', 'rating', 'content',)


scrappers_schema = ScrapperSchema(many=True)

# Utilities for saving data and searching keywords


def save_data(data: list, keywords: list) -> None:
    keywords = sorted(keywords)
    keywords = ' '.join(keywords)
    input_to_save = Input(input_query=keywords)
    db.session.add(input_to_save)
    db.session.commit()
    for item in data:
        scrapper_to_save = Scrapper(
            reference=item['reference'], rating=item['rating'], content=item['content'], input=input_to_save)
        db.session.add(scrapper_to_save)
        db.session.commit()


def search_keywords(keywords: list) -> object:
    keywords = sorted(keywords)
    input_to_search = ' '.join(keywords)
    input_exists = Input.query.filter_by(input_query=input_to_search).first()
    if input_exists:
        return input_exists
    return None

# Defining routes
@app.route('/api/news', methods=['POST'])
def api_news():
    keywords = request.json['keywords']
    validator = Validator()
    validated_request = validator.validate_request(keywords)
    if not validated_request:
        message = {"mensaje": "Parámetros Incorrectos. Intente de nuevo"}
        resp = jsonify(message)
        resp.status_code = 500
        return resp
    try:
        existing_input = search_keywords(keywords)
        if existing_input is not None:
            scrappers = Scrapper.query.filter_by(input_id=existing_input.id).all()
            data = scrappers_schema.dump(scrappers)
            resp = jsonify({"mensaje": "Registros recuperados de DB correctamente", "news": data})            
        else:
            search = PerformSearch()
            data = search.perform_search(keywords)
            save_data(data, keywords)
            resp = jsonify({"mensaje": "Registros recuperados correctamente", "news": data})
        resp.status_code = 200
        return resp
    except Exception as e:
        message = {"mensaje": f"Parámetros Incorrectos. Intente de nuevo. Error: {e}"}
        resp = jsonify(message)
        resp.status_code = 500
        return resp


# Run server
if __name__ == '__main__':
    app.run(debug=True)
