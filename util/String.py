import types
import json
from os.path import isfile

STRING_FILE = "strings.config"

String = types.SimpleNamespace()
String.SELECT_YOUR_GAME_FOLDER = "Selecione sua pasta de jogos"
String.CONNECTED = "Conectado"
String.DISCONNECTED = "Desconectado"
String.PRESS = "Aperte"
String.TO_PLAY = "para jogar"
String.PRESS_TO_PLAY = "Pressione para jogar"
String.STARTING_GAME = "Iniciando jogo"


def loadStringsFile():
    with open(STRING_FILE, "r", encoding="UTF-8") as string:
        jsonBuffer = json.loads(string.read())

    try: String.SELECT_YOUR_GAME_FOLDER = jsonBuffer["SELECT_YOUR_GAME_FOLDER"]
    except KeyError: pass

    try: String.CONNECTED = jsonBuffer["CONNECTED"]
    except KeyError: pass

    try: String.DISCONNECTED = jsonBuffer["DISCONNECTED"]
    except KeyError: pass

    try: String.PRESS = jsonBuffer["PRESS"]
    except KeyError: pass

    try: String.TO_PLAY = jsonBuffer["TO_PLAY"]
    except KeyError: pass

    try: String.PRESS_TO_PLAY = jsonBuffer["PRESS_TO_PLAY"]
    except KeyError: pass

    try: String.STARTING_GAME = jsonBuffer["STARTING_GAME"]
    except KeyError: pass


def saveStringsFile():
    jsonBuffer = json.loads("{}")
    jsonBuffer.update({'SELECT_YOUR_GAME_FOLDER': String.SELECT_YOUR_GAME_FOLDER})
    jsonBuffer.update({'CONNECTED': String.CONNECTED})
    jsonBuffer.update({'DISCONNECTED': String.DISCONNECTED})
    jsonBuffer.update({'PRESS': String.PRESS})
    jsonBuffer.update({'TO_PLAY': String.TO_PLAY})
    jsonBuffer.update({'PRESS_TO_PLAY': String.PRESS_TO_PLAY})
    jsonBuffer.update({'STARTING_GAME': String.STARTING_GAME})

    with open(STRING_FILE, "w", encoding="UTF-8") as string:
        json.dump(jsonBuffer, string, ensure_ascii=False, indent=4)


if isfile(STRING_FILE):
    loadStringsFile()
saveStringsFile()
