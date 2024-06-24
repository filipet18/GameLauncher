import types
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QSize
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QColor, QResizeEvent, QPalette, QFont

from util.Game import GameSettings
from util.String import String
from util.Dimensions import Dimensions
from views.ViewGroup import ViewGroup, View, ImageView

expandStep = types.SimpleNamespace()
expandStep.COLLAPSED = 0
expandStep.EXPANDED = 1
expandStep.BUSY = 2


class BackgroundView(View):
    def __init__(self, toastView):
        super().__init__()
        self.setBorderRadius(toastView.windowHeight / 2)
        self.setBorderColor(QColor(0, 255, 0, 255))
        self.setBackgroundColor(QColor(0, 0, 0, 255))
        self.setBorderWidth(2)
        self.setBorderStyle(View.INSET)
        self.setEnabled(True)


class XboxIcon(ImageView):
    def __init__(self, toastView):
        super().__init__()

        padding = Dimensions.getFrom(toastView.windowHeight, 0.1250)
        self.setPixmap(QPixmap("res/xbox"))
        self.setScaledContents(True)
        self.setFixedSize(toastView.windowHeight, toastView.windowHeight)
        self.setContentsMargins(padding, padding, padding, padding)
        
        
class TextView(ViewGroup):
    def __init__(self, toastView):
        super().__init__(ViewGroup.VERTICAL)

        self.toastView = toastView
        self.setOpacity(0.0)
        self.setAlignment(Qt.AlignHCenter)

        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Foreground, Qt.white)
        font = QFont()
        font.setFamily("Poppins")
        font.setPixelSize(17)

        self.title = QLabel(String.CONTROLLER_CONNECTED)
        self.title.setPalette(palette)
        self.title.setFont(font)
        self.addView(self.title)

        font.setPixelSize(10)
        font.setFamily("Poppins Medium")

        self.pressToPlay = QLabel(String.PRESS_TO_PLAY)
        self.pressToPlay.setPalette(palette)
        self.pressToPlay.setFont(font)
        self.addView(self.pressToPlay)

    def resizeEvent(self, event: QResizeEvent):
        super().resizeEvent(event)

        x = int((event.size().width() - self.pressToPlay.fontMetrics().boundingRect(self.pressToPlay.text()).width()) / 2)
        self.pressToPlay.setGeometry(x, self.pressToPlay.geometry().top(), self.pressToPlay.fontMetrics().boundingRect(self.pressToPlay.text()).width(), self.pressToPlay.geometry().height())


class ToastView:
    def __init__(self, gameSettings: GameSettings):
        self.gameSettings = gameSettings
        self.screen = gameSettings.getScreen()

        self.windowPadding = Dimensions.getFrom(self.screen.size().height(), 0.0231)
        self.collapsedSize = Dimensions.getFrom(self.screen.size().height(), 0.0781)
        self.expandedSize = Dimensions.getFrom(self.screen.size().width(), 0.2562)

        self.windowHeight = self.collapsedSize
        self.windowWidth = self.collapsedSize
        self.padding = Dimensions.getFrom(self.windowHeight, 0.1250)
        self.expandStep = expandStep.COLLAPSED

        self.window = ToastView.Parent(self)
        self.__initLayout()

        self.animator = QPropertyAnimation(self.window, b"size")
        self.animator.setDuration(500)
        self.animator.setEasingCurve(QEasingCurve.OutBack)

    def __initLayout(self):
        self.textView = TextView(self)
        self.window.addView(self.textView)

        self.__xboxIcon = XboxIcon(self)
        self.window.addView(self.__xboxIcon)

        self.__background = BackgroundView(self)
        self.window.addView(self.__background)

    def expand(self):
        if self.expandStep == expandStep.COLLAPSED:
            self.animator.stop()
            if self.expandStep == expandStep.COLLAPSED:
                self.animator.setEasingCurve(QEasingCurve.OutBack)
                self.animator.setEndValue(QSize(self.expandedSize, self.windowHeight))
                self.expandStep = expandStep.EXPANDED
            self.textView.animateOpacityTo(1.0, 300)
            self.animator.start()

            self.expandStep = expandStep.EXPANDED

    def collapse(self):
        if self.expandStep == expandStep.EXPANDED:
            self.animator.stop()
            if self.expandStep == expandStep.EXPANDED:
                self.animator.setEasingCurve(QEasingCurve.InBack)
                self.animator.setEndValue(QSize(self.collapsedSize, self.collapsedSize))
                self.expandStep = expandStep.COLLAPSED
                self.textView.animateOpacityTo(0.0, 300)
            self.animator.start()

            self.expandStep = expandStep.COLLAPSED

    class Parent(ViewGroup):
        def __init__(self, toastView):
            super().__init__(ViewGroup.NONE)

            self.textView = None

            self.toastView = toastView
            self.setScreen(toastView.screen)
            self.setRoundCorners(toastView.windowHeight / 2)
            self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnBottomHint)
            self.setInitialSize(toastView.collapsedSize, toastView.collapsedSize)
            self.setGeometry(toastView.windowPadding, toastView.windowPadding, toastView.windowWidth, toastView.windowHeight)
            self.setAttribute(Qt.WA_TranslucentBackground)
            self.show()

        def addView(self, view: QWidget):
            super().addView(view)
            if type(view) is TextView:
                self.textView = view

        def resizeEvent(self, event: QResizeEvent):
            if self.textView is not None:
                x = self.toastView.collapsedSize
                y = self.toastView.padding
                self.toastView.textView.setGeometry(x, y, event.size().width() - x - int(self.toastView.windowHeight / 2), event.size().height() - (y * 2))
