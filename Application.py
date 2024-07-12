import json
import sys
import winreg
from os.path import isfile
from pathlib import Path

from varname import nameof


class String:
    def __init__(self, context):
        self.context = context
        self.SELECT_YOUR_GAME_FOLDER = "Selecione sua pasta de jogos"
        self.CONTROLLER_CONNECTED = "Controle Conectado"
        self.CONNECTED = "Conectado"
        self.DISCONNECTED = "Desconectado"
        self.PRESS = "Aperte"
        self.TO_PLAY = "para jogar"
        self.PRESS_TO_PLAY = "Pressione para jogar"
        self.STARTING_GAME = "Iniciando jogo"

        if isfile(self.__getPath()):
            self.__loadStringsFile()
        self.__saveStringsFile()

    def __getPath(self):
        return str(self.context.getRootPath()) + "\\strings.config"

    def __loadStringsFile(self):
        with open(self.__getPath(), "r", encoding="UTF-8") as file:
            jsonBuffer = json.loads(file.read())

        try:
            self.SELECT_YOUR_GAME_FOLDER    = jsonBuffer[nameof(self.SELECT_YOUR_GAME_FOLDER)]
            self.CONTROLLER_CONNECTED       = jsonBuffer[nameof(self.CONTROLLER_CONNECTED)]
            self.CONNECTED                  = jsonBuffer[nameof(self.CONNECTED)]
            self.DISCONNECTED               = jsonBuffer[nameof(self.DISCONNECTED)]
            self.PRESS                      = jsonBuffer[nameof(self.PRESS)]
            self.TO_PLAY                    = jsonBuffer[nameof(self.TO_PLAY)]
            self.PRESS_TO_PLAY              = jsonBuffer[nameof(self.PRESS_TO_PLAY)]
            self.STARTING_GAME              = jsonBuffer[nameof(self.STARTING_GAME)]
        except KeyError:
            pass

    def __saveStringsFile(self):
        jsonBuffer = json.loads("{}")
        jsonBuffer.update({nameof(self.SELECT_YOUR_GAME_FOLDER):   self.SELECT_YOUR_GAME_FOLDER})
        jsonBuffer.update({nameof(self.CONTROLLER_CONNECTED):      self.CONTROLLER_CONNECTED})
        jsonBuffer.update({nameof(self.CONNECTED):                 self.CONNECTED})
        jsonBuffer.update({nameof(self.DISCONNECTED):              self.DISCONNECTED})
        jsonBuffer.update({nameof(self.PRESS):                     self.PRESS})
        jsonBuffer.update({nameof(self.TO_PLAY):                   self.TO_PLAY})
        jsonBuffer.update({nameof(self.PRESS_TO_PLAY):             self.PRESS_TO_PLAY})
        jsonBuffer.update({nameof(self.STARTING_GAME):             self.STARTING_GAME})

        with open(self.__getPath(), "w", encoding="UTF-8") as file:
            json.dump(jsonBuffer, file, ensure_ascii=False, indent=4)


class Context:
    def __init__(self, context=None):
        if context is None:
            self.__rootPath = Path(sys.executable).parent
            self.__string = String(self)
        else:
            self.__rootPath = context.getRootPath()
            self.__string = context.getString()

    def getString(self):
        return self.__string

    def getRootPath(self):
        return self.__rootPath


class WindowsSetup:
    def __init__(self):
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_WRITE)
        winreg.SetValueEx(key, "XBOXController", 0, winreg.REG_SZ, '"{}"'.format(sys.executable))
        winreg.CloseKey(key)


if __name__ == "__main__":
    from GameLauncher import GameLauncher

    windowsSetup = WindowsSetup()
    appContext = Context()

    gameLauncher = GameLauncher(appContext)
    gameLauncher.onCreate()

    while True:
        gameLauncher.onLoop()
