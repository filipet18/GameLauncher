import glob
import json
import pathlib
import subprocess
import sys
import os
import ctypes
import psutil
from os.path import isfile, isdir, exists
from tkinter.filedialog import askdirectory

from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPixmap, QFontMetrics, QColor, QResizeEvent
from PyQt5.QtWidgets import *

from views.ViewGroup import ViewGroup, ImageView
from util.String import String
from util.Dimensions import Dimensions

LAST_PLAYED_GAME = "lastPlayedGame"
GAME_PATH = "gamePath"
SETTINGS_CONFIG = "settings.config"


class GameObserverView(ViewGroup):
    def __init__(self, launcherView):
        super().__init__(ViewGroup.NONE)
        self.launcherView = launcherView
        self.setContentsMargins(0, 0, 0, launcherView.defaultPadding)

        self.setOpacity(0.0)

        iconSize = Dimensions.getFrom(launcherView.windowWidth, 0.0250)

        self.icon = ImageView()
        self.icon.setPixmap(QPixmap("res/xboxIcon.png"))
        self.icon.setSize(iconSize, iconSize)
        self.icon.setFixedSize(iconSize, iconSize)
        self.icon.setScaledContents(True)
        self.addView(self.icon)

        self.title = QLabel()
        self.title.setText(String.STARTING_GAME)
        self.title.setAlignment(Qt.AlignHCenter)
        self.title.setContentsMargins(0, 0, 0, 0)

        palette = self.title.palette()
        palette.setColor(self.title.foregroundRole(), Qt.white)
        font = self.title.font()
        font.setFamily("Poppins Medium")
        font.setPixelSize(int(launcherView.defaultPadding / 3))

        self.title.setMaximumHeight(self.title.fontMetrics().boundingRect(self.title.text()).height() * 2)
        self.title.setMaximumWidth(self.title.fontMetrics().boundingRect(self.title.text()).width() * 2)
        self.title.setPalette(palette)
        self.title.setFont(font)
        self.addView(self.title)

    def resizeEvent(self, event: QResizeEvent):
        left = int((event.size().width() - self.title.width()) / 2)
        top = int(event.size().height() - self.title.height() - self.contentsMargins().bottom())
        self.title.setGeometry(left, top, left + self.title.width(), top + self.title.height())

        left = int((event.size().width() - self.icon.width()) / 2)
        top = int(self.title.geometry().top() - self.contentsMargins().bottom() - (self.launcherView.windowPadding / 2))
        self.icon.setGeometry(left, top, left + self.icon.width(), top + self.icon.height())

    def show(self):
        self.animateOpacityTo(1.0, 300)

    def hideImmediately(self):
        self.animateOpacityTo(0.0, 50)

    def hide(self):
        self.animateOpacityTo(0.0, 300)


class GameObserver:
    def __init__(self):
        self.gameRunning = False
        self.process = psutil.Process()

    def startGame(self, game):
        if not self.gameRunning:
            os.startfile(game.getShortcut())
            self.gameRunning = True

    def update(self):
        if self.gameRunning:
            children = self.process.children(recursive=False)
            self.gameRunning = len(children) > 0


class Game:
    def __init__(self, settings, path: str):
        self.__settings = settings
        self.__path = path.replace("\\", "/")
        self.__path = path.replace("//", "/")
        self.__name = self.__path.split("/")[1]

    def setName(self, name: str):
        self.__name = name

    def launch(self):
        self.__settings.setLastPlayedGame(self)
        self.__settings.getGameObserver().startGame(self)

    def getPath(self):
        return self.__path

    def getName(self):
        return self.__name

    def getShortcut(self):
        return self.__path + "/resources/shortcut"

    def getBackground(self):
        return QPixmap(self.__path + "/resources/background")

    def getHeader(self):
        return QPixmap(self.__path + "/resources/header")

    def getCover(self):
        return QPixmap(self.__path + "/resources/cover")

    def getIcon(self):
        return QPixmap(self.__path + "/resources/icon")

    def getLogo(self):
        return QPixmap(self.__path + "/resources/logo")


class GameList(list):
    def __init__(self):
        super().__init__()
        self.lastPlayedGame: Game = None

    def setLastPlayedGame(self, game):
        self.lastPlayedGame = game

    def getLastPlayedGame(self):
        return self.lastPlayedGame


class GameSettings:
    def __init__(self):
        self.__app = QApplication([])
        self.__gamePath = None
        self.__gameList = GameList()
        self.__gameObserver = GameObserver()

        if self.isSetupFinished():
            self.init()

    @staticmethod
    def __createDefault():
        jsonBuffer = json.loads("{}")
        jsonBuffer[LAST_PLAYED_GAME] = ""
        jsonBuffer[GAME_PATH] = ""

        file = open(SETTINGS_CONFIG, "w", encoding="UTF-8")
        file.write(json.dumps(jsonBuffer))
        file.close()

    def __write(self, value: json):
        if not exists(SETTINGS_CONFIG):
            self.__createDefault()

        file = open(SETTINGS_CONFIG, "w", encoding="UTF-8")
        file.write(json.dumps(value))
        file.close()

    def __read(self):
        if not exists(SETTINGS_CONFIG):
            self.__createDefault()

        file = open(SETTINGS_CONFIG, "r", encoding="UTF-8")
        jsonBuffer = json.loads(file.read())
        file.close()
        return jsonBuffer

    def init(self):
        self.__gameList.clear()

        self.__gamePath = self.__read()[GAME_PATH]
        self.__gameList.setLastPlayedGame(Game(self, self.__read()[LAST_PLAYED_GAME]))
        for gameFolder in os.listdir(self.__gamePath):
            gamePath = self.__gamePath + gameFolder
            if exists(gamePath + "/resources"):
                game = Game(self, gamePath)
                if game.getName() == self.__gameList.getLastPlayedGame().getName():
                    continue

                self.__gameList.append(game)

    def getScreen(self):
        return self.__app.screens()[1]

    def getApp(self):
        return self.__app

    def getGameObserver(self):
        return self.__gameObserver

    def getGameList(self):
        return self.__gameList

    def isSetupFinished(self):
        return len(self.__read()[GAME_PATH]) > 0

    def startSetup(self):
        if self.isSetupFinished():
            return

        self.__gamePath = askdirectory(title=String.SELECT_YOUR_GAME_FOLDER)
        if len(self.__gamePath) == 0:
            self.__gamePath = None
            return

        for gameFolder in os.listdir(self.__gamePath):
            gamePath = self.__gamePath + gameFolder
            if exists(gamePath + "/resources"):
                self.__gameList.append(Game(self, gamePath))

        self.setGamePath(self.__gamePath)
        self.setLastPlayedGame(self.__gameList[0])

    def setGamePath(self, path):
        self.__gamePath = path
        jsonBuffer = self.__read()
        jsonBuffer[GAME_PATH] = path
        self.__write(jsonBuffer)

    def setLastPlayedGame(self, game: Game):
        self.getGameList().setLastPlayedGame(game)
        jsonBuffer = self.__read()
        jsonBuffer[LAST_PLAYED_GAME] = game.getPath()
        self.__write(jsonBuffer)
        self.init()

    def getLastPlayedGame(self):
        if not isdir(self.lastPlayedGame.getPath()):
            self.setLastPlayedGame(self[0])
        return self.lastPlayedGame

    def update(self):
        self.__gameObserver.update()
