from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QLabel

from util.Game import Game
from views.ViewGroup import ViewGroup, ImageView


class BackgroundView(ViewGroup):
    def __init__(self, launcherView):
        super().__init__(ViewGroup.NONE)
        self.launcherView = launcherView
        self.currentGame = None
        self.setSize(launcherView.windowWidth, launcherView.windowHeight)
        self.setRoundCorners(20)

        self.overlay = QLabel()
        self.overlay.setStyleSheet("background: rgb(0, 0, 0, 100);")
        self.overlay.setScaledContents(False)
        self.overlay.setAlignment(Qt.AlignCenter)
        self.addView(self.overlay)

        self.gameForeground = ImageView()
        self.gameForeground.setScaledContents(False)
        self.gameForeground.setAlignment(Qt.AlignCenter)
        self.gameForeground.setOpacity(1.0)
        self.gameForeground.getOpacityAnimator().finished.connect(self.onAnimationFinish)
        self.addView(self.gameForeground)

        self.gameBackground = ImageView()
        self.gameBackground.setScaledContents(False)
        self.gameBackground.setAlignment(Qt.AlignCenter)
        self.addView(self.gameBackground)

    def __getBackgroundFrom(self, game: Game):
        pixmap = game.getBackground()
        pixmap = pixmap.scaledToWidth(self.launcherView.windowWidth, Qt.TransformationMode.SmoothTransformation)
        return pixmap

    def getCurrentGame(self):
        return self.currentGame

    def setLastPlayedGame(self, lastPlayedGame: Game):
        pixmap = self.__getBackgroundFrom(lastPlayedGame)
        self.gameBackground.setPixmap(pixmap)
        self.gameForeground.setPixmap(pixmap)

    def onAnimationFinish(self):
        pixmap = self.__getBackgroundFrom(self.currentGame)
        self.gameBackground.setPixmap(pixmap)
        self.gameForeground.setPixmap(pixmap)
        self.gameForeground.setOpacity(1.0)

    def applyBackground(self, game: Game):
        if self.currentGame.getName() == game.getName():
            pixmap = self.__getBackgroundFrom(game)
            self.gameBackground.setPixmap(pixmap)
            self.gameForeground.animateOpacityTo(0.0, 250)

    def setCurrentGame(self, game: Game):
        currentValue = self.gameForeground.getOpacityAnimator().currentValue()
        if currentValue is not None and currentValue > 0:
            QTimer.singleShot(250, lambda: self.setCurrentGame(game))
            return

        QTimer.singleShot(250, lambda: self.applyBackground(game))
        self.currentGame = game
