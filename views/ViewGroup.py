import json

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QStackedLayout, QSizePolicy, QLabel, QGraphicsOpacityEffect, QGraphicsColorizeEffect
from PyQt5.QtCore import Qt, QRectF, QPropertyAnimation, QTimer
from PyQt5.QtGui import QPainterPath, QRegion, QShowEvent, QPixmap, QColor, QScreen


class View(QLabel):
    INSET = "inset"
    OUTSET = "outset"

    def __init__(self):
        super().__init__()

        self.__overlayStyleSheet = {}
        self.setBackgroundColor(QColor(0, 0, 0, 0))

    def __getStyleSheet(self):
        styleSheet = json.dumps(self.__overlayStyleSheet)
        styleSheet = styleSheet.replace('",', '";')
        styleSheet = styleSheet.replace('"', '')
        styleSheet = styleSheet.replace('{', '')
        styleSheet = styleSheet.replace('}', '')

        return styleSheet

    def setBorderWidth(self, border: int):
        self.__overlayStyleSheet["border-width"] = "{}px".format(border)
        self.setStyleSheet(self.__getStyleSheet())

    def setBorderColor(self, color: QColor):
        self.__overlayStyleSheet["border-color"] = "rgba({},{},{},{})".format(color.red(), color.green(), color.blue(), color.alpha())
        self.setStyleSheet(self.__getStyleSheet())

    def setBorderStyle(self, style):
        self.__overlayStyleSheet["border-style"] = style
        self.setStyleSheet(self.__getStyleSheet())

    def setBorderRadius(self, radius):
        self.__overlayStyleSheet["border-radius"] = "{}px".format(int(radius))
        self.setStyleSheet(self.__getStyleSheet())

    def setBackgroundColor(self, color: QColor):
        self.__overlayStyleSheet["background"] = "rgba({},{},{},{})".format(color.red(), color.green(), color.blue(), color.alpha())
        self.setStyleSheet(self.__getStyleSheet())

    def setEnabled(self, enabled):
        if enabled:
            self.setStyleSheet(self.__getStyleSheet())
        else:
            self.setStyleSheet("")


class ViewGroup(QWidget):
    NONE = 0
    VERTICAL = 1
    HORIZONTAL = 2

    def __init__(self, orientation):
        super().__init__()
        self.__initialWidth = None
        self.__initialHeight = None
        self.__effect = None
        self.__opacityAnimator = None
        self.__cornersRadius = 0
        self.__rectF = QRectF()
        self.__path = QPainterPath()
        self.__targetScreen: QScreen = None

        if orientation == ViewGroup.VERTICAL:
            self.__layoutParent = QVBoxLayout(self)
        elif orientation == ViewGroup.HORIZONTAL:
            self.__layoutParent = QHBoxLayout(self)
        else:
            self.__layoutParent = QStackedLayout(self)
            self.__layoutParent.setStackingMode(QStackedLayout.StackingMode.StackAll)

        self.__layoutParent.setContentsMargins(0, 0, 0, 0)
        self.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        self.setLayout(self.__layoutParent)

    def setRoundCorners(self, radius):
        self.__cornersRadius = radius

    def setSize(self, width, height):
        self.__rectF.setWidth(width)
        self.__rectF.setHeight(height)

    def setOpacity(self, opacity: float):
        if self.graphicsEffect() is None:
            self.__effect = QGraphicsOpacityEffect(self)
            self.__effect.setOpacity(opacity)
            self.setGraphicsEffect(self.__effect)

            self.__opacityAnimator = QPropertyAnimation(self.__effect, b"opacity")
        else:
            self.__effect.setOpacity(opacity)

    def getOpacityAnimatorFrom(self, targetOpacity: float, duration):
        if self.__opacityAnimator is None:
            self.__opacityAnimator = QPropertyAnimation(self.__effect, b"opacity")

        self.__opacityAnimator.setDuration(duration)
        self.__opacityAnimator.setStartValue(self.__effect.opacity())
        self.__opacityAnimator.setEndValue(targetOpacity)

        return self.__opacityAnimator

    def getOpacityAnimator(self):
        return self.__opacityAnimator

    def animateOpacityTo(self, targetOpacity: float, duration):
        if self.__opacityAnimator is None:
            self.__opacityAnimator = QPropertyAnimation(self.__effect, b"opacity")

        self.__opacityAnimator.stop()
        self.__opacityAnimator.setDuration(duration)
        self.__opacityAnimator.setStartValue(self.__effect.opacity())
        self.__opacityAnimator.setEndValue(targetOpacity)
        self.__opacityAnimator.start()

    def setInitialSize(self, width, height):
        self.__initialWidth = width
        self.__initialHeight = height

    def setBackgroundColor(self, color):
        self.setStyleSheet("background-color: {}".format(color))

    def setAlignment(self, alignment: Qt.Alignment):
        self.__layoutParent.setAlignment(alignment)

    def setChildPadding(self, padding):
        self.__layoutParent.setSpacing(padding)

    def addView(self, view: QWidget):
        self.__layoutParent.addWidget(view)

    def removeAllViews(self):
        for index in range(self.__layoutParent.count()):
            self.__layoutParent.itemAt(index).widget().deleteLater()

    def setScreen(self, screen: QScreen):
        self.__targetScreen = screen

    def showEvent(self, event: QShowEvent):
        if self.__targetScreen is not None:
            self.move(self.__targetScreen.geometry().left() + self.geometry().left(), self.__targetScreen.geometry().top() + self.geometry().top())

        if self.__initialWidth is None:
            self.__initialWidth = int(self.__rectF.width())

        if self.__initialHeight is None:
            self.__initialHeight = int(self.__rectF.height())

        self.resize(self.__initialWidth, self.__initialHeight)

        self.__path.clear()
        self.__path.addRoundedRect(self.__rectF, self.__cornersRadius, self.__cornersRadius)
        self.setMask(QRegion(self.__path.toFillPolygon().toPolygon()))


class ImageView(ViewGroup):
    def __init__(self):
        super().__init__(ViewGroup.NONE)

        self.image = QLabel()
        self.addView(self.image)

    def setPixmap(self, pixmap: QPixmap):
        self.image.setPixmap(pixmap)

    def setScaledContents(self, scaled):
        self.image.setScaledContents(scaled)

    def setAlignment(self, alignment: Qt.Alignment):
        super().setAlignment(alignment)
        self.image.setAlignment(alignment)


class LayerImageView(ViewGroup):
    def __init__(self):
        super().__init__(ViewGroup.NONE)

        self.overlay = View()
        self.addView(self.overlay)

        self.middle = ViewGroup(ViewGroup.NONE)
        self.addView(self.middle)

        self.imageView = ImageView()
        self.addView(self.imageView)

    def getOverlay(self):
        return self.overlay

    def getMiddle(self):
        return self.middle

    def getImageView(self):
        return self.imageView

    def setPixmap(self, pixmap: QPixmap):
        self.imageView.setPixmap(pixmap)

    def setScaledContents(self, scaled):
        self.imageView.setScaledContents(scaled)

    def setAlignment(self, alignment: Qt.Alignment):
        self.imageView.setAlignment(alignment)
