
from flask import Flask, jsonify
from flask_restx import Api, Resource, reqparse
from flask_mongoengine import MongoEngine
# from mongoengine import StringField
from src.transform import shorten
import logging

app = Flask(__name__)
app.logger.setLevel(logging.INFO)
app.config.SWAGGER_UI_DOC_EXPANSION = 'list'
app.config["MONGODB_SETTINGS"] = {
    'db': 'my_db'
}
db = MongoEngine(app)

class Url(db.Document):
    short_url = db.StringField()
    long_url = db.StringField()
    def to_json(self):
        return {
            "short_url": self.short_url,
            "long_url": self.long_url
        }
    
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument("long_url", type=str, help="URL you want to shortened")

get_parser = reqparse.RequestParser()
get_parser.add_argument("short_url", type=str, help="URL you want to return to full length")

@api.route('/url', methods=["PUT", "GET"])
class TinyURL(Resource):
    @api.expect(parser)
    def put(self):
        args = parser.parse_args()
        long_url = args.get("long_url") 

        short_url = shorten(long_url)
        url = Url(short_url=short_url, long_url=long_url)
        url.save()
        return jsonify(url.to_json())
    

    @api.expect(get_parser)
    def get(self):
        args = get_parser.parse_args()
        short_url = args.get("short_url")
        long_url = Url.objects(short_url=short_url).first()
        
        if not long_url:
            return jsonify({"error": "url not found"})

        else:
            return jsonify(long_url.to_json().get("long_url"))



if __name__ == "__main__":
    app.run(debug=1)