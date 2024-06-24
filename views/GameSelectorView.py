from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QSequentialAnimationGroup, QPropertyAnimation, QMargins
from PyQt5.QtGui import QPixmap, QColor

from util.Dimensions import Dimensions
from util.Game import Game, GameList
from views.ViewGroup import ViewGroup, LayerImageView


class GameSelectorView(ViewGroup):
    def __init__(self, launcherView):
        super().__init__(ViewGroup.HORIZONTAL)
        self.launcherView = launcherView
        self.setAlignment(Qt.AlignLeft | Qt.AlignBottom)
        self.setContentsMargins(int(launcherView.defaultPadding / 2), int(launcherView.defaultPadding / 2), int(launcherView.defaultPadding / 2), int(launcherView.defaultPadding / 2))
        self.setChildPadding(int(launcherView.defaultPadding / 3))
        self.currentGameIndex = 0
        self.animator = QSequentialAnimationGroup()

        self.lastPlayedGame = GameHeaderView(self.launcherView)
        self.lastPlayedGame.getOverlay().setEnabled(True)
        self.addView(self.lastPlayedGame)

        self.gameViewList = []

    def __refreshCurrentGameIndex(self, dirX):
        self.currentGameIndex = self.currentGameIndex + dirX
        if self.currentGameIndex < 0:
            self.currentGameIndex = len(self.gameViewList) - 1

        if self.currentGameIndex >= len(self.gameViewList):
            self.currentGameIndex = 0

    def show(self):
        for gameView in self.gameViewList:
            self.animator.addAnimation(gameView.getOpacityAnimatorFrom(1.0, 100))
        self.animator.start()

    def hideImmediately(self):
        self.animator.stop()
        for animation in self.animator.children():
            self.animator.removeAnimation(animation)

        for gameView in self.gameViewList:
            gameView.animateOpacityTo(0.0, 50)

    def hide(self):
        self.animator.stop()
        for animation in self.animator.children():
            self.animator.removeAnimation(animation)

        for gameView in self.gameViewList:
            gameView.animateOpacityTo(0.0, 200)

    def getCurrentGameView(self):
        return self.gameViewList[self.currentGameIndex]

    def setGameList(self, gameList: GameList):
        self.removeAllViews()
        self.gameViewList.clear()
        self.gameViewList.append(self.lastPlayedGame)
        self.lastPlayedGame.setGame(gameList.getLastPlayedGame())

        for game in gameList:
            gameView = GameCoverView(self.launcherView)
            gameView.setGame(game)
            gameView.setPixmap(game.getCover())
            self.addView(gameView)
            self.gameViewList.append(gameView)

    def reset(self):
        self.gameViewList[self.currentGameIndex].getOverlay().setEnabled(False)
        self.currentGameIndex = 0
        self.gameViewList[self.currentGameIndex].getOverlay().setEnabled(True)

        self.launcherView.onGameSelected(self.gameViewList[self.currentGameIndex].getGame())

    def setLastPlayedGame(self, lastPlayedGame: Game):
        self.lastPlayedGame.setPixmap(lastPlayedGame.getHeader())

    def inputHorizontal(self, dirEventX):
        self.gameViewList[self.currentGameIndex].getOverlay().setEnabled(False)
        self.__refreshCurrentGameIndex(dirEventX)
        self.gameViewList[self.currentGameIndex].getOverlay().setEnabled(True)

        self.launcherView.onGameSelected(self.gameViewList[self.currentGameIndex].getGame())


class GameView(LayerImageView):
    def __init__(self, launcherView):
        super().__init__()
        self.game = None

        self.setOpacity(0.0)

        self.getOverlay().setBorderWidth(3)
        self.getOverlay().setBorderRadius(launcherView.corners)
        self.getOverlay().setBorderColor(QColor(255, 255, 255))
        self.getOverlay().setBorderStyle(self.getOverlay().OUTSET)
        self.getOverlay().setEnabled(False)

    def setGame(self, game: Game):
        self.game = game

    def getGame(self):
        return self.game


class GameCoverView(GameView):
    def __init__(self, launcherView):
        super().__init__(launcherView)

        self.width = Dimensions.getFrom(launcherView.windowWidth, 0.1069)
        self.height = Dimensions.getFrom(launcherView.windowHeight, 0.5882)

        self.setAlignment(Qt.AlignTop)
        self.setSize(self.width, self.height)
        self.setFixedSize(self.width, self.height)
        self.setRoundCorners(launcherView.corners)

    def setPixmap(self, pixmap: QPixmap):
        pixmap = pixmap.scaledToWidth(self.width, Qt.TransformationMode.SmoothTransformation)
        super().setPixmap(pixmap)


class GameHeaderView(GameView):
    def __init__(self, launcherView):
        super().__init__(launcherView)

        self.width = Dimensions.getFrom(launcherView.windowWidth, 0.2673)
        self.height = Dimensions.getFrom(launcherView.windowHeight, 0.5882)

        self.setAlignment(Qt.AlignCenter)
        self.setSize(self.width, self.height)
        self.setFixedSize(self.width, self.height)
        self.setRoundCorners(launcherView.corners)

    def setPixmap(self, pixmap: QPixmap):
        pixmap = pixmap.scaledToHeight(self.height, Qt.TransformationMode.SmoothTransformation)
        super().setPixmap(pixmap)
