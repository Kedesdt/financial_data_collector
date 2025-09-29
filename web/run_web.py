#!/usr/bin/env python3
"""
🌐 LAUNCHER WEB - Dashboard Financeiro

Execute este arquivo para iniciar o servidor web
"""

import os
import sys
import webbrowser
import time
from threading import Timer

# Adiciona o diretório pai ao path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)


def open_browser():
    """Abre o navegador após 2 segundos"""
    webbrowser.open("http://localhost:5000")


def main():
    print("🌐 DASHBOARD FINANCEIRO WEB")
    print("=" * 50)
    print("🚀 Iniciando servidor Flask...")
    print("📊 Interface moderna com dados em tempo real")
    print("🔄 WebSockets para atualizações automáticas")
    print("📱 Responsivo para mobile e desktop")
    print("=" * 50)

    # Programa abertura do navegador
    Timer(3.0, open_browser).start()

    try:
        # Importa e executa a aplicação
        from app import app, socketio

        print("✅ Servidor iniciado com sucesso!")
        print("🌐 Dashboard: http://localhost:5000")
        print("🔗 API: http://localhost:5000/api/data")
        print()
        print("💡 Pressione Ctrl+C para parar")
        print("🔄 O navegador abrirá automaticamente...")
        print("=" * 50)

        # Inicia servidor Flask com SocketIO
        socketio.run(
            app, debug=False, host="0.0.0.0", port=5000, allow_unsafe_werkzeug=True
        )

    except KeyboardInterrupt:
        print("\n👋 Servidor encerrado pelo usuário!")
    except Exception as e:
        print(f"\n❌ Erro ao iniciar servidor: {e}")
        input("⏎ Pressione Enter para sair...")


if __name__ == "__main__":
    main()
