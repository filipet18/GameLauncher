from PyQt5.QtCore import Qt, QPropertyAnimation, QSize, QEasingCurve, QTimer
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor, QPixmap, QScreen

from tkinter.filedialog import askdirectory

from util.Dimensions import *
from util.Game import GameList, Game, GameObserverView, GameSettings
from util.XboxControllerConstants import *
from views.BackgroundView import BackgroundView
from views.GameSelectorView import GameSelectorView
from views.GameTitleView import GameTitle
from views.ViewGroup import ViewGroup
from views.XboxTitleView import XboxTitle

expandStep = types.SimpleNamespace()
expandStep.COLLAPSED = 0
expandStep.EXPANDED = 1
expandStep.BUSY = 2


# noinspection PyUnresolvedReferences
class LauncherView:
    def __init__(self, gameSettings: GameSettings, gameSelectCallback):
        self.gameSettings = gameSettings
        self.app = QApplication([])
        self.gameSelectCallback = OnGameSelectListener(gameSelectCallback)
        self.screen = self.app.screens()[1]

        self.defaultPadding = Dimensions.getFrom(self.screen.size().height(), 0.0462)
        self.windowPadding = int(self.defaultPadding / 2)
        self.windowHeight = Dimensions.getFrom(self.screen.size().height(), 0.4166)
        self.windowWidth = self.screen.size().width() - (self.windowPadding * 2)

        self.expandStep = expandStep.COLLAPSED
        self.isLayoutInit = False

        self.window = ViewGroup(ViewGroup.NONE)
        self.window.setScreen(self.screen)
        self.window.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.window.setInitialSize(self.windowWidth, 0)
        self.window.setGeometry(self.windowPadding, self.windowPadding, self.windowWidth, self.windowHeight)
        self.window.setAttribute(Qt.WA_TranslucentBackground)

        self.animator = QPropertyAnimation(self.window, b"size")
        self.animator.finished.connect(lambda: self.__onAnimationFinish(self.animator.endValue()))
        self.animator.setDuration(500)
        self.animator.setEasingCurve(QEasingCurve.OutBack)

        self.__gameObserverView = None
        self.__xboxTitle = None
        self.__gameTitle = None
        self.__gameSelector = None
        self.__backgroundView = None

    def __onAnimationFinish(self, size: QSize):
        if size.height() == self.windowHeight:
            self.__xboxTitle.show()
            self.__gameTitle.show()
            self.__gameSelector.show()
        else:
            self.__gameSelector.reset()

    def __refreshResources(self):
        gameList = self.gameSettings.getGameList()
        self.__backgroundView.setLastPlayedGame(gameList.getLastPlayedGame())
        self.__gameSelector.setLastPlayedGame(gameList.getLastPlayedGame())
        self.__gameSelector.setGameList(gameList)
        self.__gameTitle.setCurrentGame(gameList.getLastPlayedGame())

    def initLayout(self):
        self.isLayoutInit = True

        self.__gameObserverView = GameObserverView(self)
        self.window.addView(self.__gameObserverView)

        self.__xboxTitle = XboxTitle(self)
        self.window.addView(self.__xboxTitle)

        self.__gameTitle = GameTitle(self)
        self.window.addView(self.__gameTitle)

        self.__gameSelector = GameSelectorView(self)
        self.window.addView(self.__gameSelector)

        self.__backgroundView = BackgroundView(self)
        self.window.addView(self.__backgroundView)

        self.__refreshResources()
        self.window.show()

    def expand(self):
        if not self.isLayoutInit:
            self.initLayout()

        if self.getExpandStep() == expandStep.COLLAPSED:
            self.animator.stop()
            if self.expandStep == expandStep.COLLAPSED:
                self.animator.setEndValue(QSize(self.windowWidth, self.windowHeight))
                self.expandStep = expandStep.EXPANDED
            self.animator.start()

            self.expandStep = expandStep.EXPANDED

    def collapse(self):
        if self.getExpandStep() == expandStep.EXPANDED:
            self.__xboxTitle.hideImmediately()
            self.__gameTitle.hideImmediately()
            self.__gameSelector.hideImmediately()
            self.__gameObserverView.hideImmediately()

            self.animator.stop()
            if self.expandStep == expandStep.EXPANDED:
                self.animator.setEndValue(QSize(self.windowWidth, 0))
                self.expandStep = expandStep.COLLAPSED
            self.animator.start()

            self.expandStep = expandStep.COLLAPSED

    def resetAndCollapse(self):
        self.expandStep = expandStep.EXPANDED
        self.collapse()
        self.__refreshResources()

    def launchGame(self, game: Game):
        if self.getExpandStep() == expandStep.EXPANDED:
            self.__xboxTitle.hide()
            self.__gameTitle.hide()
            self.__gameSelector.hide()
            self.__gameObserverView.show()
            game.launch()
            QTimer.singleShot(2000, lambda: self.resetAndCollapse())
            self.expandStep = expandStep.BUSY

    def getExpandStep(self):
        return self.expandStep

    def inputDirPadEvent(self, dirEventX, dirEventY):
        if dirEventX != 0:
            self.__gameSelector.inputHorizontal(dirEventX)

    def onGameSelected(self, game: Game):
        self.__backgroundView.setCurrentGame(game)
        self.__gameTitle.setCurrentGame(game)

    def onXboxButtonEvent(self, event):
        if event == EVENT_XBOX_BUTTON_DOWN:
            self.gameSelectCallback.onGameSelected(self.__gameSelector.getCurrentGameView().getGame())

        if event == EVENT_XBOX_BUTTON_UP:
            pass

        if event == EVENT_XBOX_BUTTON_LONG_PRESS:
            print("LONG")

    def update(self):
        if not self.isLayoutInit:
            return

        if self.__backgroundView.getCurrentGame() is None or self.__gameSelector.getCurrentGameView().getGame() is None:
            return

        if self.__gameSelector.getCurrentGameView().getGame().getName() != self.__backgroundView.getCurrentGame().getName():
            self.__backgroundView.setCurrentGame(self.__gameSelector.getCurrentGameView().getGame())


class OnGameSelectListener:
    def __init__(self, callback):
        self.callback = callback

    def onGameSelected(self, game: Game):
        if self.callback is not None:
            self.callback.onGameSelected(game)
