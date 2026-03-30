from flask import Flask, jsonify, request
import json

app = Flask(__name__)

aqv_logs = "./data/logs.jsonl"


def ler_logs():

    logs = []

    try:
        with open(aqv_logs, "r", encoding="utf-8") as f:
            for linha in f:
                if linha.strip():
                    logs.append(json.loads(linha))

    except FileNotFoundError:
        pass

    return logs

def formatar_logs():
    logs = ler_logs()

    logs_formatados = []

    for log in logs:

        logs_format = {
            "timestamp": log["timestamp"],
            "level": log["level"],
            "message": log["message"].strip(),
            "service": log["service"]
        }

        logs_formatados.append(logs_format)

    return logs_formatados


@app.route('/logs', methods=['GET'])
def get_logs():
    logs = formatar_logs()
    return jsonify(logs)

app.run()