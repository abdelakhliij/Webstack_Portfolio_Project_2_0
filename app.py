from flask import Flask, request, jsonify, render_template
import json
import os

app = Flask(__name__)

SCORES_FILE = 'scores.json'


if not os.path.exists(SCORES_FILE):
    with open(SCORES_FILE, 'w') as f:
        json.dump([], f)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/save-score', methods=['POST'])
def save_score():
    data = request.get_json()
    username = data.get('username')
    score = data.get('score')

    if not username or not isinstance(score, int) or score > 100:
        return jsonify({'error': 'Invalid data'}), 400

    with open(SCORES_FILE, 'r+') as f:
        scores = json.load(f)
        scores.append({'username': username, 'score': score})
        f.seek(0)
        json.dump(scores, f, indent=2)

    return jsonify({'message': 'Score saved'}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

