import types

CONTROLLER_CONNECTED = 1541
CONTROLLER_DISCONNECTED = 1542
CONTROLLER_BUTTON_UP = 1540
CONTROLLER_BUTTON_DOWN = 1539
CONTROLLER_DPAD_EVENT = 1538
XBOX_BUTTON = 10
SHARE_BUTTON = 11
WINDOWS_BUTTON = 6
OPTIONS_BUTTON = 7
DPAD_TOP_BUTTON = 1
DPAD_LEFT_BUTTON = -1
DPAD_RIGHT_BUTTON = 1
DPAD_BOTTOM_BUTTON = -1

EVENT_XBOX_BUTTON_DOWN = 0
EVENT_XBOX_BUTTON_UP = 1
EVENT_XBOX_BUTTON_LONG_PRESS = 2

XboxControllerVibrator = types.SimpleNamespace()
XboxControllerVibrator.LEFT = 1
XboxControllerVibrator.RIGHT = 2

WELCOME_PATTERN_VIBRATION = [(XboxControllerVibrator.RIGHT, 500),
                             (XboxControllerVibrator.LEFT, 200),
                             (XboxControllerVibrator.RIGHT, 500),
                             (XboxControllerVibrator.LEFT, 200)]

GAME_SELECT_PATTERN_VIBRATION = [(XboxControllerVibrator.RIGHT, 100),
                             (XboxControllerVibrator.LEFT, 200),
                             (XboxControllerVibrator.RIGHT, 100),
                             (XboxControllerVibrator.LEFT, 200)]
