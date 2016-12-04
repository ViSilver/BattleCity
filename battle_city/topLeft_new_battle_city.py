import sys
import math

from PyQt5.QtCore import QPointF, QRect, QRectF, Qt, QTimer, QSize
from PyQt5.QtGui import (QBrush, QColor, QFont, QLinearGradient, QPainter,
        QPen, QSurfaceFormat)
from PyQt5.QtWidgets import (QApplication, QGridLayout, QLabel, QOpenGLWidget,
        QWidget, QDesktopWidget)


class Helper(object):
    def __init__(self):
        self.background = QBrush(QColor(0xAAAAAA))

    def paint(self, painter, event, elapsed, battleMap):
        painter.fillRect(event.rect(), self.background)
        color = QColor(0x333333)

        for bullet in battleMap.bullets:
            painter.fillRect(bullet.topLeft[1], bullet.topLeft[0],
                         bullet.width,
                         bullet.height,
                         color)

        self.draw_tank(battleMap.activeTank, painter)

    def draw_tank(self, tank, painter):
        color = QColor(0x333333)

        painter.fillRect(tank.topLeft[1],
                         tank.topLeft[0],
                         tank.width,
                         tank.height,
                         color)

        color = QColor(0xAAAAAA)

        if tank.orientation == 'up':
            painter.fillRect(tank.topLeft[1],
                             tank.topLeft[0],
                             8, 6, color)

            painter.fillRect(tank.topLeft[1] + 11,
                             tank.topLeft[0],
                             8, 6, color)

            painter.fillRect(tank.topLeft[1] + 7,
                             tank.topLeft[0] + 22,
                             5, 5, color)

        elif tank.orientation == 'down':
            painter.fillRect(tank.topLeft[1],
                             tank.topLeft[0] + 21,
                             8, 6, color)

            painter.fillRect(tank.topLeft[1] + 11,
                             tank.topLeft[0] + 21,
                             8, 6, color)

            painter.fillRect(tank.topLeft[1] + 7,
                             tank.topLeft[0],
                             5, 5, color)

        elif tank.orientation == 'left':
            painter.fillRect(tank.topLeft[1],
                             tank.topLeft[0],
                             6, 8, color)

            painter.fillRect(tank.topLeft[1],
                             tank.topLeft[0] + 11,
                             6, 8, color)

            painter.fillRect(tank.topLeft[1] + 22,
                             tank.topLeft[0] + 7,
                             5, 5, color)

        elif tank.orientation == 'right':
            painter.fillRect(tank.topLeft[1] + 22,
                             tank.topLeft[0],
                             6, 8, color)

            painter.fillRect(tank.topLeft[1] + 22,
                             tank.topLeft[0] + 11,
                             6, 8, color)

            painter.fillRect(tank.topLeft[1],
                             tank.topLeft[0] + 7,
                             5, 5, color)


class Widget(QWidget):
    def __init__(self, helper, parent):
        super(Widget, self).__init__(parent)
        self.helper = helper
        self.battleMap = BattleMap()
        self.elapsed = 0
        self.setMinimumSize(QSize(BattleMap.width, BattleMap.height))

    def animate(self):
        for bullet in self.battleMap.bullets:
            bullet.move(bullet.orientation, self.battleMap)
        self.elapsed = (self.elapsed + self.sender().interval()) % 1000
        self.repaint()

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        self.helper.paint(painter, event, self.elapsed, self.battleMap)
        painter.end()

    def make_move(self, direction):
        self.battleMap.move(direction)


class BattleMap(object):
    width = 240
    height = 240

    def __init__(self):
        self.bullets = []
        self.activeTank = Tank()

    def move(self, direction):
        if direction == 'up':
            if (direction == self.activeTank.orientation):
                self.activeTank.move('up')
            else:
                self.activeTank.goUp()
        elif direction == 'down':
            if (direction == self.activeTank.orientation):
                self.activeTank.move('down')
            else:
                self.activeTank.goDown()
        elif direction == 'left':
            if (direction == self.activeTank.orientation):
                self.activeTank.move('left')
            else:
                self.activeTank.goLeft()
        elif direction == 'right':
            if (direction == self.activeTank.orientation):
                self.activeTank.move('right')
            else:
                self.activeTank.goRight()


class Figure(object):
    def __init__(self):
        # topLeft = [y, x]
        self.width = 1
        self.height = 1
        self.center = [1, 1]
        self.orientation = 'up'
        self.topLeft = [0, 0]

    def bottomRight(self):
        return (self.topLeft[0] + self.width,
                self.topLeft[1] + self.height)

    def setPosition(self, pos):
        self.topLeft = pos


class Bullet(Figure):
    def __init__(self):
        super().__init__()
        self.new = True
        self.height = 3
        self.width = 3
        self.hheight = self.height // 2 + 1
        self.hwidth = self.width // 2 + 1
        self.center[0] = self.hwidth
        self.center[1] = self.hheight

    def move(self, direction, battleMap):
        print(direction)
        if direction == 'up' and self.topLeft[0] - 3 > 0:
            self.topLeft[0] -= 3
        elif direction == 'down' and self.topLeft[0] + 3 < BattleMap.height:
            self.topLeft[0] += 3
        elif direction == 'left' and self.topLeft[1] - 3 > 0:
            self.topLeft[1] -= 3
        elif direction == 'right' and self.topLeft[1] + 3 < BattleMap.width:
            self.topLeft[1] += 3
        else:
            battleMap.bullets.remove(self)


class Tank(Figure):
    height = 27
    width = 19

    def __init__(self):
        super().__init__()
        self.height = Tank.height
        self.width = Tank.width
        self.hheight = Tank.height//2 + 1
        self.hwidth = Tank.width//2 + 1
        self.center[0] = self.hwidth
        self.center[1] = self.hheight

    def rotate(self):
        tmp = self.height
        self.height = self.width
        self.width = tmp

    def goUp(self):
        print(self.center)
        self.orientation = 'up'
        self.height = Tank.height
        self.width = Tank.width

    def goDown(self):
        print(self.center)
        self.orientation = 'down'
        self.height = Tank.height
        self.width = Tank.width

    def goLeft(self):
        print(self.center)
        self.orientation = 'left'
        self.height = Tank.width
        self.width = Tank.height

    def goRight(self):
        print(self.center)
        self.orientation = 'right'
        self.height = Tank.width
        self.width = Tank.height

    def move(self, direction):
        delta = None
        if direction == 'up' and self.topLeft[0] > 2:
            self.topLeft[0] -= 3
        elif direction == 'down' and self.topLeft[0] + 2 + self.height < BattleMap.height:
            self.topLeft[0] += 3
        elif direction == 'left' and self.topLeft[1] > 2:
            self.topLeft[1] -= 3
        elif direction == 'right' and self.topLeft[1] + 2 + self.width < BattleMap.width:
            self.topLeft[1] += 3

    def shoot(self, battleMap):
        bullet = Bullet()
        bullet.orientation = self.orientation
        if self.orientation == 'up':
            bullet.topLeft = [self.topLeft[0], self.topLeft[1] + self.width/2 - 1]
        elif self.orientation == 'down':
            bullet.topLeft = [self.topLeft[0] + 8, self.topLeft[1] + self.width/2 - 1]
        elif self.orientation == 'left':
            bullet.topLeft = [self.topLeft[0] + self.height/2 - 1, self.topLeft[1]]
        elif self.orientation == 'right':
            bullet.topLeft = [self.topLeft[0] + self.height/2 - 1, self.topLeft[1] + 6]
        battleMap.bullets.append(bullet)


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()

        self.setWindowTitle("2D Painting on Native Widgets")

        helper = Helper()
        self.native = Widget(helper, self)

        layout = QGridLayout()
        layout.addWidget(self.native, 0, 0)
        self.setLayout(layout)

        timer = QTimer(self)
        timer.timeout.connect(self.native.animate)
        timer.start(15)

        self.center()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())/2,
            (screen.height()-size.height())/2)

    def keyPressEvent(self, event):
        key = event.key()

        if key == Qt.Key_Up:
            self.native.make_move('up')
        elif key == Qt.Key_Down:
            self.native.make_move('down')
        elif key == Qt.Key_Right:
            self.native.make_move('right')
        elif key == Qt.Key_Left:
            self.native.make_move('left')
        elif key == Qt.Key_Space:
            self.native.battleMap.activeTank.shoot(self.native.battleMap)


if __name__ == '__main__':

    app = QApplication(sys.argv)

    # fmt = QSurfaceFormat()
    # fmt.setSamples(4)
    # QSurfaceFormat.setDefaultFormat(fmt)

    window = Window()
    window.show()
    sys.exit(app.exec_())
