from util.Game import Game, GameList, GameSettings
from util.XboxController import XboxController
from util.XboxControllerConstants import *
from views.LauncherView import (LauncherView, expandStep)
from views.ToastView import ToastView

#VARIABLE'S
xboxController: XboxController
launcherView: LauncherView
gameSettings: GameSettings
toastView: ToastView


def onCreate():
    global gameSettings, xboxController, launcherView, toastView

    gameSettings = GameSettings()
    xboxController = XboxController(gameSettings, ControllerListener(), ControllerLongPress())
    launcherView = LauncherView(gameSettings, LauncherViewGameSelect())
    toastView = ToastView(gameSettings)

    while True:
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
        # xboxController.Vibrator.vibrateSequentially(WELCOME_PATTERN_VIBRATION)

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

    @staticmethod
    def onWindowsButtonClick():
        toastView.expand()
        pass

    @staticmethod
    def onOptionsButtonClick():
        toastView.collapse()
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


if __name__ == "__main__": onCreate()
