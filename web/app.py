"""
Aplicação Web Flask para Dashboard Financeiro
Exibe dados de câmbio e bolsa em tempo real
"""

import sys
import os
from datetime import datetime
import json
import threading
import time

# Adiciona o diretório pai ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit

from financial_collector import FinancialDataCollector

# Configuração do Flask
app = Flask(__name__)
app.config["SECRET_KEY"] = "financial_dashboard_secret_key_2025"
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Instância global do coletor
collector = FinancialDataCollector()
collector.update_interval = 30  # 30 segundos

# Dados globais atualizados
current_data = {}
last_update = None


def update_data_background():
    """Thread para atualizar dados em background"""
    global current_data, last_update

    while True:
        try:
            print(f"🔄 Atualizando dados... {datetime.now().strftime('%H:%M:%S')}")

            # Coleta novos dados
            new_data = collector.collect_all_data()
            current_data = new_data
            last_update = datetime.now()

            # Envia via WebSocket para todos os clientes conectados
            socketio.emit(
                "data_update", {"data": new_data, "timestamp": last_update.isoformat()}
            )

            print(f"✅ Dados atualizados e enviados via WebSocket")

        except Exception as e:
            print(f"❌ Erro na atualização: {e}")

        time.sleep(collector.update_interval)


# Inicia thread de atualização em background
update_thread = threading.Thread(target=update_data_background, daemon=True)
update_thread.start()


@app.route("/")
def dashboard():
    """Página principal do dashboard"""
    return render_template("dashboard.html")


@app.route("/api/data")
def get_data():
    """API endpoint para obter dados financeiros"""
    try:
        if not current_data:
            # Se não há dados, coleta uma vez
            data = collector.collect_all_data()
        else:
            data = current_data

        return jsonify(
            {
                "success": True,
                "data": data,
                "last_update": last_update.isoformat() if last_update else None,
                "server_time": datetime.now().isoformat(),
            }
        )
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/cambio")
def get_cambio():
    """API endpoint específico para dados de câmbio"""
    try:
        cambio_data = collector.cambio_api.get_all_rates()
        return jsonify(
            {
                "success": True,
                "data": cambio_data,
                "timestamp": datetime.now().isoformat(),
            }
        )
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/bolsa")
def get_bolsa():
    """API endpoint específico para dados da bolsa"""
    try:
        bolsa_data = collector.bolsa_api.get_all_indices()
        return jsonify(
            {
                "success": True,
                "data": bolsa_data,
                "timestamp": datetime.now().isoformat(),
            }
        )
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/summary")
def get_summary():
    """API endpoint para resumo executivo"""
    try:
        if current_data:
            summary = collector.get_summary(current_data)
        else:
            data = collector.collect_all_data()
            summary = collector.get_summary(data)

        return jsonify(
            {
                "success": True,
                "summary": summary,
                "timestamp": datetime.now().isoformat(),
            }
        )
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@socketio.on("connect")
def handle_connect():
    """Quando um cliente se conecta via WebSocket"""
    print(f"🔌 Cliente conectado: {request.sid}")

    # Envia dados atuais imediatamente
    if current_data:
        emit(
            "data_update",
            {
                "data": current_data,
                "timestamp": (
                    last_update.isoformat()
                    if last_update
                    else datetime.now().isoformat()
                ),
            },
        )


@socketio.on("disconnect")
def handle_disconnect():
    """Quando um cliente se desconecta"""
    print(f"🔌 Cliente desconectado: {request.sid}")


@socketio.on("request_update")
def handle_request_update():
    """Cliente solicita atualização manual"""
    try:
        data = collector.collect_all_data()
        emit("data_update", {"data": data, "timestamp": datetime.now().isoformat()})
        print(f"📱 Atualização manual enviada para {request.sid}")
    except Exception as e:
        emit("error", {"message": str(e)})


if __name__ == "__main__":
    print("🚀 Iniciando Dashboard Financeiro Web")
    print("=" * 50)
    print("📊 Dashboard: http://localhost:5000")
    print("🔗 API Dados: http://localhost:5000/api/data")
    print("💱 API Câmbio: http://localhost:5000/api/cambio")
    print("📈 API Bolsa: http://localhost:5000/api/bolsa")
    print("=" * 50)
    print("💡 Pressione Ctrl+C para parar")
    print()

    # Coleta dados iniciais
    print("🔄 Coletando dados iniciais...")
    try:
        current_data = collector.collect_all_data()
        last_update = datetime.now()
        print("✅ Dados iniciais carregados!")
    except Exception as e:
        print(f"⚠️ Erro ao carregar dados iniciais: {e}")

    # Inicia servidor
    socketio.run(app, debug=True, host="0.0.0.0", port=5000)
