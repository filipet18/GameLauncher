from util.Game import Game, GameSettings
from util.XboxController import XboxController
from util.XboxControllerConstants import *
from views.LauncherView import (LauncherView, expandStep)
from views.ToastView import ToastView
from Application import Context

# VARIABLE'S
xboxController: XboxController
launcherView: LauncherView
gameSettings: GameSettings
toastView: ToastView


class GameLauncher(Context):
    def onCreate(self):
        global gameSettings, xboxController, launcherView, toastView
        gameSettings = GameSettings(self)
        xboxController = XboxController(gameSettings, ControllerListener(), ControllerLongPress())
        launcherView = LauncherView(gameSettings, LauncherViewGameSelect())
        toastView = ToastView(self, gameSettings)

    def onLoop(self):
        xboxController.update()
        launcherView.update()
        gameSettings.update()


class LauncherViewGameSelect:
    @staticmethod
    def onGameSelected(game: Game):
        xboxController.Vibrator.vibrateSequentially(GAME_SELECT_PATTERN_VIBRATION)
        launcherView.launchGame(game)


class ControllerLongPress:
    @staticmethod
    def onLongPress():
        if launcherView.getExpandStep() == expandStep.EXPANDED:
            launcherView.onXboxButtonEvent(EVENT_XBOX_BUTTON_LONG_PRESS)

    @staticmethod
    def onStart(event):
        if launcherView.getExpandStep() == expandStep.EXPANDED:
            launcherView.onXboxButtonEvent(EVENT_XBOX_BUTTON_DOWN)

    @staticmethod
    def onCancel():
        if launcherView.getExpandStep() == expandStep.EXPANDED:
            launcherView.onXboxButtonEvent(EVENT_XBOX_BUTTON_UP)


class ControllerListener:
    @staticmethod
    def onConnected():
        toastView.expand()
        xboxController.Vibrator.vibrateSequentially(WELCOME_PATTERN_VIBRATION)

    @staticmethod
    def onDisconnected():
        toastView.collapse()
        launcherView.collapse()

    @staticmethod
    def onXboxButtonClick():
        if not gameSettings.isSetupFinished():
            gameSettings.startSetup()
            return

        if launcherView.getExpandStep() != expandStep.BUSY:
            launcherView.expand()

    @staticmethod
    def onShareButtonClick():
        launcherView.collapse()
        pass

    @staticmethod
    def onWindowsButtonClick():
        pass

    @staticmethod
    def onOptionsButtonClick():
        pass

    @staticmethod
    def onDirPadEvent(padEventX, padEventY):
        if (launcherView.getExpandStep() == expandStep.COLLAPSED
                or launcherView.getExpandStep() == expandStep.BUSY):
            return

        if padEventX < 0:
            xboxController.Vibrator.vibrateLeft(100)
        elif padEventX > 0:
            xboxController.Vibrator.vibrateRight(100)

        launcherView.inputDirPadEvent(padEventX, padEventY)

    @staticmethod
    def onButtonClick(event):
        print("onButtonClick", event)
