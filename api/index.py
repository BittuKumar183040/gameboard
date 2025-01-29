from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from sqlalchemy import text

load_dotenv()

app = Flask(__name__)

database_user = os.getenv('DATABASE_USER')
password = os.getenv('PASSWORD')
host = os.getenv('HOST')
port = os.getenv('PORT')
database_name = os.getenv('DATABASE_NAME')

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{database_user}:{password}@{host}:{port}/{database_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

db = SQLAlchemy(app)

@app.route('/')
def home():
    appIntegrated = [{
        "scoreboard":["flappybird", "snake"],
        'url':"/scoreboard/<scoreboard>"
    }]
    return appIntegrated

class Scoreboard(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255))
    score = db.Column(db.Integer)
    website = db.Column(db.String(255))


@app.route('/status')
def status():
    try:
        result = db.session.execute(text('SELECT 1'))
        db.session.commit()
        return {"status":"active", "database":"Database Connected Successfully."}
    except Exception as e:
        return f"Error connecting to the database: {str(e)}"

@app.route('/scoreboard', methods=['POST'])
def add_score():
    try:
        data = request.get_json()
        print(data)
        username = data.get('username')
        score = data.get('score')
        website = data.get('website')

        if not username or not score or not website:
            return jsonify({"error": "Missing required fields: username, score, website"}), 400

        new_score = Scoreboard(username=username, score=score, website=website)
        db.session.add(new_score)
        db.session.commit()

        return jsonify({
            "message": "Data inserted successfully",
            "data": {
                "username": new_score.username,
                "score": new_score.score,
                "website": new_score.website
            }
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/scoreboard/<website>')
def scoreboard(website):
    try:
        query = text("SELECT * FROM scoreboard WHERE website = :website order by score DESC Limit 10")
        result = db.session.execute(query, {'website':website})
        rows = result.fetchall()
        data = []
        for row in rows:
            data.append({'username': row[1], 'score': row[2]})
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)})