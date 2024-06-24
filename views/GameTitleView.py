from PyQt5.QtWidgets import QLabel, QGraphicsOpacityEffect
from PyQt5.QtCore import Qt, QPropertyAnimation

from util.Game import Game
from util.Dimensions import Dimensions
from views.ViewGroup import ViewGroup, ImageView


class GameTitle(ViewGroup):
    def __init__(self, launcherView):
        super().__init__(ViewGroup.HORIZONTAL)
        self.setChildPadding(int(launcherView.defaultPadding / 3))
        self.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.setContentsMargins(launcherView.windowPadding, int(launcherView.defaultPadding), launcherView.defaultPadding, launcherView.defaultPadding)
        self.setOpacity(0.0)

        iconSize = Dimensions.getFrom(launcherView.windowWidth, 0.0250)

        self.icon = ImageView()
        self.icon.setSize(iconSize, iconSize)
        self.icon.setFixedSize(iconSize, iconSize)
        self.icon.setScaledContents(True)
        self.addView(self.icon)

        self.title = QLabel()
        palette = self.title.palette()
        palette.setColor(self.title.foregroundRole(), Qt.white)
        font = self.title.font()
        font.setFamily("Poppins Medium")
        font.setPixelSize(Dimensions.getFrom(launcherView.defaultPadding, 0.8))

        self.setPalette(palette)
        self.title.setFont(font)
        self.addView(self.title)

    def setCurrentGame(self, game: Game):
        self.icon.setPixmap(game.getIcon())
        self.title.setText(game.getName())

    def show(self):
        self.animateOpacityTo(1.0, 300)

    def hideImmediately(self):
        self.animateOpacityTo(0.0, 50)

    def hide(self):
        self.animateOpacityTo(0.0, 300)

