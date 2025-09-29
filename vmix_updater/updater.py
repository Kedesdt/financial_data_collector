import os
import json
import threading
import time
import requests
from urllib.parse import quote
import queue
import traceback

PATH_1 = "Z:\\GC\\gc_1.txt"
PATH_2 = "Z:\\GC\\gc_2.txt"
PATH_3 = "Z:\\GC\\gc_3.txt"

LIMITE = 70  # Limite de caracteres para o texto

# Instâncias globais dos updaters
updater_1 = None
updater_2 = None
updater_3 = None


def load_config():
    """Carrega configurações"""
    try:
        if os.path.exists("vmix_updater/config.json"):
            with open("vmix_updater/config.json", "r", encoding="utf-8") as f:
                return json.load(f)
    except:
        pass

    # Configurações padrão
    return {
        "ip": "10.13.22.82",
        "porta": "8088",
        "title": "GC_TARJA",
        "text_1": "TextBlock1.Text",
        "text_2": "TextBlock2.Text",
        "text_3": "Ticker1.Text",
    }


def start_updaters():
    global updater_1, updater_2, updater_3

    config = load_config()

    if updater_1 is None or not updater_1.is_alive():
        updater_1 = ApiUpdater(
            updater_id="updater_1",
            path_in="phrases_1.json",
            path_out=PATH_1,
            name_1=config["title"],
            name=config["text_1"],
        )
        updater_1.start()

    if updater_2 is None or not updater_2.is_alive():
        updater_2 = ApiUpdater(
            updater_id="updater_2",
            path_in="phrases_2.json",
            path_out=PATH_2,
            name_1=config["title"],
            name=config["text_2"],
        )
        updater_2.start()

    if updater_3 is None or not updater_3.is_alive():
        updater_3 = ApiUpdater(
            updater_id="updater_3",
            path_in="phrases_3.json",
            path_out=PATH_3,
            name_1=config["title"],
            name=config["text_3"],
            caractere_limite=300,  # Ticker pode ter mais caracteres
        )
        updater_3.start()


def stop_updaters():
    global updater_1, updater_2, updater_3
    if updater_1:
        updater_1.stop()
    if updater_2:
        updater_2.stop()
    if updater_3:
        updater_3.stop()


def send_phrase_directly(ip, porta, title, field_name, text):
    """Envia uma frase específica diretamente"""
    encoded_text = quote(text)
    url = f"http://{ip}:{porta}/API?Function=SetText&Input={title}&SelectedName={field_name}&Value={encoded_text}"
    print(url)
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        print(f"Frase enviada com sucesso: {text}")
        return True
    except requests.RequestException as e:
        print(f"Erro ao enviar frase para {url}: {e}")
        return False


class ApiUpdater(threading.Thread):

    def __init__(
        self,
        phrases=[],
        default_time=10,
        name_1="GC_TARJA",
        name="Message.Text",
        caractere_limite=LIMITE,
    ):
        threading.Thread.__init__(self)
        self.phrases = phrases
        self.default_time = default_time
        self.running = True
        self.mode = "auto"
        self.index = 0
        self.current = ""
        self.name_1 = name_1
        self.name = name
        self.caractere_limite = caractere_limite
        self.daemon = True
        self.queue = queue.Queue()
        self.config = load_config()

    def run(self):

        while self.running:
            try:
                data = self.queue.get(timeout=30)
                if data:
                    print(f"Enviando dados para API: {data}")
                    for key in data["cambio"].keys():
                        if key in self.config.keys():
                            send_phrase_directly(
                                self.config["ip"],
                                self.config["porta"],
                                self.config["title"],
                                self.config[key]["name"],
                                key,
                            )
                            for field in data["cambio"][key].keys():
                                if field == "rate":
                                    send_phrase_directly(
                                        self.config["ip"],
                                        self.config["porta"],
                                        self.config["title"],
                                        self.config[key]["value"],
                                        f"{data['cambio'][key][field]:.4f}",
                                    )
                                elif field == "change":
                                    send_phrase_directly(
                                        self.config["ip"],
                                        self.config["porta"],
                                        self.config["title"],
                                        self.config[key]["diff"],
                                        f"{data['cambio'][key][field]:+.4f}",
                                    )
                                elif field == "change_percent":
                                    send_phrase_directly(
                                        self.config["ip"],
                                        self.config["porta"],
                                        self.config["title"],
                                        self.config[key]["perc"],
                                        f"{data['cambio'][key][field]:+.2f}%",
                                    )
                            send_phrase_directly(
                                self.config["ip"],
                                self.config["porta"],
                                self.config["title"],
                                self.config["IBOV"]["name"],
                                "IBOVESPA",
                            )
                            send_phrase_directly(
                                self.config["ip"],
                                self.config["porta"],
                                self.config["title"],
                                self.config["IBOV"]["value"],
                                f"{data["bolsa"]['IBOV']['price']:+.2f}",
                            )
                            arrow = "↑" if data["bolsa"]["IBOV"]["price"] >= 0 else "↓"
                            send_phrase_directly(
                                self.config["ip"],
                                self.config["porta"],
                                self.config["title"],
                                self.config["IBOV"]["diff"],
                                f"{arrow}{data["bolsa"]['IBOV']['change']:+.2f}",
                            )
                            send_phrase_directly(
                                self.config["ip"],
                                self.config["porta"],
                                self.config["title"],
                                self.config["IBOV"]["perc"],
                                f"{data["bolsa"]['IBOV']['change_percent']:+.2f}%",
                            )
                    self.queue.task_done()

            except Exception as e:
                # traceback.print_exc()
                print(f"Erro no APIupdater: {e}")
                time.sleep(1)
        print(f"Terminado APIupdater")

    def stop(self):
        self.running = False

    def send(self, ip, porta, name, text):
        """Envia uma mensagem para a API do Vmix."""
        if len(text) <= self.caractere_limite:
            encoded_text = quote(text)
            url = f"http://{ip}:{porta}/API?Function=SetText&Input={self.name_1}&SelectedName={self.name}&Value={encoded_text}"

            # print(f"Enviando para {url}")

            try:
                response = requests.get(url, timeout=5)
                response.raise_for_status()
            except requests.RequestException as e:
                print(f"Erro ao enviar mensagem para {url}: {e}")


def apply_config_to_updaters(config):
    """Aplica configurações aos updaters"""

    # Atualizar configurações da classe ApiUpdater
    ApiUpdater.ip = config["ip"]
    ApiUpdater.porta = config["porta"]
    ApiUpdater.name_1 = config["title"]

    # Aplicar configurações específicas se os updaters estiverem rodando
    global updater_1, updater_2, updater_3

    if updater_1 and updater_1.is_alive():
        updater_1.name_1 = config["title"]
        updater_1.name = config["text_1"]

    if updater_2 and updater_2.is_alive():
        updater_2.name_1 = config["title"]
        updater_2.name = config["text_2"]

    if updater_3 and updater_3.is_alive():
        updater_3.name_1 = config["title"]
        updater_3.name = config["text_3"]


def get_updaters_status():
    """Retorna o status atual de todos os updaters"""
    global updater_1, updater_2, updater_3

    status = {}
    for i, updater in enumerate([updater_1, updater_2, updater_3], 1):
        if updater:
            status[i] = {
                "mode": updater.mode,
                "running": updater.running,
                "current_phrase_index": updater.index,
            }
        else:
            status[i] = {"mode": "auto", "running": False, "current_phrase_index": 0}

    return status
