from flask import Flask, jsonify, request, render_template
from database import criar_tabela, inserir_log, buscar_logs, limpar_logs_antigos, buscar_logs_after_id
import threading
import time

app = Flask(__name__)

CAMPOS_OBRIGATORIOS = {"timestamp", "level", "message", "service"}

# limpeza automática a cada 24h
def limpeza_automatica():
    while True:
        time.sleep(86400)  # 24h em segundos
        limpar_logs_antigos()
        print("Limpeza de logs antigos executada")

threading.Thread(target=limpeza_automatica, daemon=True).start()
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

    inserir_log(dados)
    return jsonify({"status": "ok"}), 201


@app.route('/')
def home():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)