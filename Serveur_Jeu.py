from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)
SCORES_FILE = 'scores.json'
SECRET_KEY = 'elgkezopgjsiprtezl432R_aàr"_"343SE3reyt"yèé&e'  # À modifier et garder privé
@app.before_request
def limiter_ip():
    if request.remote_addr not in ['192.168.72.55', '127.168.72.57']:
        return "Accès refusé", 403
# Initialiser fichier
if not os.path.exists(SCORES_FILE):
    with open(SCORES_FILE, 'w') as f:
        json.dump([], f)

@app.route('/get_scores', methods=['GET'])
def get_scores():
    with open(SCORES_FILE, 'r') as f:
        scores = json.load(f)
    return jsonify(scores)

@app.route('/post_score', methods=['POST'])
def post_score():
    data = request.json
    if not data:
        return jsonify({'error': 'Aucune donnée reçue'}), 400

    # Vérifie la clé
    if data.get('key') != SECRET_KEY:
        return jsonify({'error': 'Clé invalide'}), 403

    # Vérifie les données minimales
    name = data.get('name')
    score = data.get('score')
    if not isinstance(name, str) or not isinstance(score, (int, float)):
        return jsonify({'error': 'Données invalides'}), 400

    # Enregistre
    with open(SCORES_FILE, 'r') as f:
        scores = json.load(f)

    scores.append({'name': name, 'score': score})

    with open(SCORES_FILE, 'w') as f:
        json.dump(scores, f)

    return jsonify({'status': 'OK'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

