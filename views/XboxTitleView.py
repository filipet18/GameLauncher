from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from views.ViewGroup import ViewGroup, ImageView
from util.String import String


class XboxTitle(ViewGroup):
    def __init__(self, launcherView):
        super().__init__(ViewGroup.HORIZONTAL)

        self.setChildPadding(int(launcherView.defaultPadding / 2))
        self.setAlignment(Qt.AlignRight | Qt.AlignTop)
        self.setContentsMargins(launcherView.defaultPadding, launcherView.defaultPadding, launcherView.defaultPadding, launcherView.defaultPadding)
        self.setOpacity(0.0)

        self.title = QLabel()
        self.title.setText(String.PRESS_TO_PLAY)
        self.title.setAlignment(Qt.AlignRight | Qt.AlignCenter)

        palette = self.title.palette()
        palette.setColor(self.title.foregroundRole(), Qt.white)
        font = self.title.font()
        font.setFamily("Poppins Medium")
        font.setPixelSize(int(launcherView.defaultPadding / 3))

        self.setPalette(palette)
        self.title.setFont(font)
        self.addView(self.title)

        self.icon = ImageView()
        self.icon.setPixmap(QPixmap("res/xboxIcon.png"))
        self.icon.setSize(48, 48)
        self.icon.setFixedSize(48, 48)
        self.icon.setScaledContents(True)
        self.addView(self.icon)

    def show(self):
        self.animateOpacityTo(1.0, 300)

    def hideImmediately(self):
        self.animateOpacityTo(0.0, 50)

    def hide(self):
        self.animateOpacityTo(0.0, 300)
