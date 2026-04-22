from flask import Flask, jsonify, request, render_template
from app.database import criar_tabela, inserir_log, buscar_logs, limpar_logs_antigos, buscar_logs_after_id
import threading
import time
import os
from datetime import datetime

app = Flask(__name__)

CAMPOS_OBRIGATORIOS = {"timestamp", "level", "message", "service"}

@app.before_request
def limpeza_data():
    limpar_logs_antigos()

criar_tabela()

@app.route('/logs', methods=['GET'])
def get_logs():
    data     = request.args.get('date')
    after_id = request.args.get('after_id', type=int)
    limit    = int(request.args.get('limit', 50))
    offset   = int(request.args.get('offset', 0))

    if after_id is not None:
        return jsonify(buscar_logs_after_id(after_id))

    return jsonify(buscar_logs(data, limit, offset))


@app.route('/logs', methods=['POST'])
def post_log():
    dados = request.get_json()

    if not dados:
        return jsonify({"erro": "Body vazio ou não é JSON"}), 400

    campos_faltando = CAMPOS_OBRIGATORIOS - dados.keys()
    if campos_faltando:
        return jsonify({"erro": f"Campos faltando: {campos_faltando}"}), 400

    timestamp = dados["timestamp"]

    try:
        datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")

    except ValueError:
        return jsonify({"erro": "timestamp inválido"}), 400

    level_validos = ["INFO", "ERROR", "WARNING", "DEBUG"]

    level = dados["level"]
    level = level.strip().upper()

    if level not in level_validos:
        return jsonify({"erro": "level inválido"}), 400

    dados["level"] = level

    inserir_log(dados)
    return jsonify({"status": "ok"}), 201


@app.route('/')
def home():
    return render_template('index.html')


if __name__ == "__main__":
    port  = int(os.getenv("PORT", 5000))
    debug = os.getenv("DEBUG", "false").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug)