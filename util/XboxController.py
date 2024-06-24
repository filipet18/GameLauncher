import time
import pygame
from util.XboxControllerConstants import *
from util.Game import GameSettings
from PyQt5.QtCore import QTimer
from queue import Queue


class XboxController:
    def __init__(self, gameSettings: GameSettings, controllerListenerCallback, longPressCallback):
        self.initialTime = 0
        self.joystick: pygame.joystick.JoystickType = 0
        self.Vibrator: XboxControllerVibrator = 0

        self.xboxControllerListener = XboxControllerListener(self, controllerListenerCallback)
        self.xboxControllerLongPress = XboxControllerLongPress(self, longPressCallback)

        pygame.init()
        pygame.joystick.init()
        self.initController()

    def initController(self):
        self.joystick = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
        self.Vibrator = XboxControllerVibrator(self.joystick)

    def update(self):
        event = pygame.event.wait(50)
        if event.type == CONTROLLER_CONNECTED:
            self.xboxControllerListener.onConnected()
        elif event.type == CONTROLLER_DISCONNECTED:
            self.xboxControllerListener.onDisconnected()
        elif event.type == CONTROLLER_DPAD_EVENT:
            self.xboxControllerListener.onDirPadEvent(event.value[0], event.value[1])
        elif event.type == CONTROLLER_BUTTON_DOWN:
            self.initialTime = time.time()
            self.xboxControllerLongPress.onStart(event)
        elif event.type == CONTROLLER_BUTTON_UP:
            self.xboxControllerLongPress.onCancel()
            if (time.time() - self.initialTime) < 1:
                self.xboxControllerListener.onButtonClick(event)


class XboxControllerListener:

    def __init__(self, controller: XboxController, callback):
        self.controller: XboxController = controller
        self.callback: XboxControllerListener = callback

    def onConnected(self):
        self.controller.initController()

        if self.callback is not None:
            self.callback.onConnected()

    def onDisconnected(self):
        if self.callback is not None:
            self.callback.onDisconnected()

    def onXboxButtonClick(self):
        if self.callback is not None:
            self.callback.onXboxButtonClick()

    def onShareButtonClick(self):
        if self.callback is not None:
            self.callback.onShareButtonClick()

    def onWindowsButtonClick(self):
        if self.callback is not None:
            self.callback.onWindowsButtonClick()

    def onDirPadEvent(self, padEventX, padEventY):
        if self.callback is not None:
            self.callback.onDirPadEvent(padEventX, padEventY)

    def onOptionsButtonClick(self):
        if self.callback is not None:
            self.callback.onOptionsButtonClick()

    def onButtonClick(self, event):
        if event.button == XBOX_BUTTON:
            self.onXboxButtonClick()
        elif event.button == SHARE_BUTTON:
            self.onShareButtonClick()
        elif event.button == WINDOWS_BUTTON:
            self.onWindowsButtonClick()
        elif event.button == OPTIONS_BUTTON:
            self.onOptionsButtonClick()
        elif self.callback is not None:
            self.callback.onButtonClick(event)


class XboxControllerLongPress:
    PRESS_DURATION = 1500

    def __init__(self, controller: XboxController, callback):
        self.controller: XboxController = controller
        self.callback: XboxControllerLongPress = callback
        self.initialTime = 0

    def onLongPress(self):
        return #TODO
        if self.initialTime == 0:
            return
        self.initialTime = 0

        if self.callback is not None:
            self.callback.onLongPress()

    def onStart(self, event):
        if event.button != XBOX_BUTTON:
            return
        self.initialTime = time.time()
        QTimer.singleShot(self.PRESS_DURATION, lambda: self.onLongPress())

        if self.callback is not None:
            self.callback.onStart(event)

    def onCancel(self):
        if self.initialTime == 0:
            return
        self.initialTime = 0

        if self.callback is not None:
            self.callback.onCancel()


class XboxControllerVibrator:
    LEFT = 1
    RIGHT = 2
    queue = Queue()

    def __init__(self, joystick: list):
        if len(joystick) > 0:
            self.joystick: pygame.joystick.JoystickType = joystick[0]

    def nextVibration(self):
        vibration = XboxControllerVibrator.queue.get()
        if vibration[0] == XboxControllerVibrator.LEFT:
            self.vibrateLeft(vibration[1])

        if vibration[0] == XboxControllerVibrator.RIGHT:
            self.vibrateRight(vibration[1])

    def vibrateSequentially(self, pattern):
        for index, vibration in enumerate(pattern):
            XboxControllerVibrator.queue.put(vibration)
            QTimer.singleShot(vibration[1] * index, lambda: self.nextVibration())

    def vibrateLeft(self, duration):
        self.joystick.rumble(1, 0, duration)

    def vibrateRight(self, duration):
        self.joystick.rumble(0, 1, duration)
