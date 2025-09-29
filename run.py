#!/usr/bin/env python3
"""
🚀 LAUNCHER - Sistema de Informações Financeiras

Execute este arquivo para iniciar o sistema completo
"""

import sys
import os

# Adiciona o diretório atual ao path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

def main():
    print("💼 SISTEMA DE INFORMAÇÕES FINANCEIRAS")
    print("=" * 50)
    print("📺 Similar à tela Bloomberg que você viu!")
    print("=" * 50)
    print()
    
    print("🎯 Opções disponíveis:")
    print("1. 🌐 Dashboard Web (web/run_web.py) - NOVO!")
    print("2. 🚀 Sistema Completo (financial_collector.py)")
    print("3. 💱 Apenas Câmbio (examples/exemplo_cambio.py)")
    print("4. 📈 Apenas Bolsa (examples/exemplo_bolsa.py)")
    print("5. 🎮 Exemplos Interativos (examples/exemplo_completo.py)")
    print("6. 📚 Ver documentação (README.md)")
    print("0. ❌ Sair")
    print()
    
    while True:
        try:
            escolha = input("Digite sua opção (0-6): ").strip()
            
            if escolha == "0":
                print("👋 Obrigado por usar o sistema!")
                break
                
            elif escolha == "1":
                print("🌐 Iniciando dashboard web...")
                exec(open('web/run_web.py').read())
                
            elif escolha == "2":
                print("🚀 Iniciando sistema completo...")
                from financial_collector import main as run_collector
                run_collector()
                
            elif escolha == "3":
                print("💱 Executando exemplos de câmbio...")
                exec(open('examples/exemplo_cambio.py').read())
                
            elif escolha == "4":
                print("📈 Executando exemplos da bolsa...")
                exec(open('examples/exemplo_bolsa.py').read())
                
            elif escolha == "5":
                print("🎮 Abrindo menu de exemplos...")
                from examples.exemplo_completo import menu_exemplos
                menu_exemplos()
                
            elif escolha == "6":
                print("📚 Abrindo documentação...")
                if os.name == 'nt':  # Windows
                    os.system('notepad README.md')
                else:  # Linux/Mac
                    os.system('cat README.md')
                    
            else:
                print("❌ Opção inválida! Tente novamente.")
                continue
                
            input("\n⏎ Pressione Enter para voltar ao menu...")
            print("\n" + "="*50 + "\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 Sistema encerrado pelo usuário!")
            break
        except Exception as e:
            print(f"\n❌ Erro: {e}")
            print("🔄 Voltando ao menu...\n")

if __name__ == "__main__":
    main()