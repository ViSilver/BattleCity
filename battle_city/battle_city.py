from PyQt5.QtWidgets import (QApplication, QWidget, QMainWindow, QFrame,
                             QWidget, QVBoxLayout, QDesktopWidget, QHBoxLayout,
                             QMessageBox)
from PyQt5.QtGui import (QPainter, QColor)
from PyQt5.QtCore import (Qt, QBasicTimer, pyqtSignal, QSize)
import sys
import time
import _thread


class UI_BattleCity(QMainWindow):
    def __init__(self):
        super().__init__()
        self.field = Field(self)
        self.setupUi(self)
        self.show()
        # self.field.show()

    def setupUi(self, BattleCity):
        BattleCity.setObjectName('BattleCity')
        self.resize(241, 240)

        self.centralWidget = self.field

        self.setMinimumSize(QSize(240, 240))
        self.center()
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.centralWidget)

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())/2,
            (screen.height()-size.height())/2)


class Field(QFrame):
    def __init__(self, parent=None):
        super(Field, self).__init__(parent)
        self.initField()
        self.colors = self.getColors()
        self.battleMap = BattleMap()
        self.events = {}
        _thread.start_new_thread(self.start_loop, ())
        self.square_width = self.squareWidth()
        self.square_height = self.squareHeight()

    def initField(self):
        self.timer = QBasicTimer()
        self.setFocusPolicy(Qt.StrongFocus)
        self.setMinimumSize(QSize(240, 240))
        self.setMaximumSize(QSize(240, 240))

    @staticmethod
    def getColors():
        colors = {}
        colors[1] = 0xEEEEEE
        colors[2] = 0x505050
        colors[3] = 0xAAAAAA
        return colors

    def squareWidth(self):
        return self.contentsRect().width() // BattleMap.width

    def squareHeight(self):
        return self.contentsRect().height() // BattleMap.height

    def paintEvent(self, event):
        painter = QPainter(self)
        rect = self.contentsRect()

        fieldTop = rect.bottom() - BattleMap.height * self.square_height

        for i in range(BattleMap.height):
            for j in range(BattleMap.width):
                self.drawSquare(painter, rect.left() + j * self.square_width,
                                fieldTop + i * self.square_height,
                                self.battleMap.grid[i][j])

    def drawSquare(self, painter, x, y, type):
        color = QColor(self.colors[type])
        painter.fillRect(x, y,
                         self.square_width,
                         self.square_height,
                         color)

    def keyPressEvent(self, event):
        if 'keyPressEvent' in self.events.keys():
            self.events['keyPressEvent'].append(event)
        else:
            self.events['keyPressEvent'] = [event]
        return
        # self.update()

        # for bullet in self.battleMap.bullets:
        #     bullet.move(bullet.orientation)
        #
        # key = event.key()
        #
        # if key == Qt.Key_Up:
        #     self.make_move('up')
        # elif key == Qt.Key_Down:
        #     self.make_move('down')
        # elif key == Qt.Key_Right:
        #     self.make_move('right')
        # elif key == Qt.Key_Left:
        #     self.make_move('left')
        # elif key == Qt.Key_Space:
        #     self.battleMap.activeTank.shoot()
        # else:
        #     super(Field, self).keyPressEvent(event)

        # self.update()

    def make_move(self, direction):
        self.battleMap.move(direction)

    def start_loop(self):
        while True:
            start = time.time()

            self.process_input()
            self.update()

            time.sleep(start + 0.015 - time.time())

    def process_input(self):
        for bullet in self.battleMap.bullets:
                bullet.move(bullet.orientation)

        for event_key in self.events:
            event = self.events[event_key]

            if event_key == 'keyPressEvent':
                for ev in event:
                    ev = event.pop()
                    key = ev.key()

                    if key == Qt.Key_Up:
                        self.make_move('up')
                    elif key == Qt.Key_Down:
                        self.make_move('down')
                    elif key == Qt.Key_Right:
                        self.make_move('right')
                    elif key == Qt.Key_Left:
                        self.make_move('left')
                    elif key == Qt.Key_Space:
                        self.battleMap.activeTank.shoot()
                    else:
                        # super(Field, self).keyPressEvent(event)
                        pass


class BattleMap(object):
    height = 30
    width = 30

    def __init__(self):
        self.grid = list()
        self.clear()
        # self.activeCell = (5, 5)
        self.bullets = []
        self.activeTank = Tank(self)
        # self.figures.append(self.activeTank)

    def clear(self):
        self.grid = [list(range(self.height)) for x in range(self.width)]
        self.grid = [list(map(lambda x: 3, row)) for row in self.grid]

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
        else:
            pass


class Figure(object):
    def __init__(self, map):
        self.topLeft = [0, 0]
        self.width = 1
        self.height = 1
        self.grid = []
        self.orientation = 'up'
        self.map = map

    def bottomRight(self):
        return (self.topLeft[0] + self.width,
                self.topLeft[1] + self.height)

    def setPosition(self, pos):
        self.topLeft = pos

    def rotateClockwise(self):
        grid_copy = [list(range(self.height)) for x in range(self.width)]
        for i in range(self.width):
            for j in range(self.height):
                grid_copy[j][self.width - i - 1] = self.grid[i][j]
        self.grid = grid_copy
        self.connectToMap()

    def connectToMap(self):
        for i in range(self.width):
            for j in range(self.height):
                self.map.grid[j + self.topLeft[0]][i + self.topLeft[1]] = self.grid[j][i]

    def clear(self):
        for i in range(self.width):
            for j in range(self.height):
                self.map.grid[j + self.topLeft[0]][i + self.topLeft[1]] = 3


class Bullet(Figure):
    def __init__(self, map):
        super().__init__(map)
        self.grid = [[1]]
        self.new = True

    def move(self, direction):
        # Check how many steps are needed to rotate the figure
        if not self.new:
            self.clear()
        else:
            self.new = False

        if direction == 'up' and self.topLeft[0] > 0:
            self.topLeft[0] -= 1
        elif direction == 'down' and self.topLeft[0] + self.width < self.map.height:
            self.topLeft[0] += 1
        elif direction == 'left' and self.topLeft[1] > 0:
            self.topLeft[1] -= 1
        elif direction == 'right' and self.topLeft[1] + self.width < self.map.width:
            self.topLeft[1] += 1
        else:
            self.map.bullets.remove(self)
            return
        self.connectToMap()


class Tank(Figure):
    def __init__(self, map):
        super().__init__(map)
        self.height = 3
        self.width = 3
        self.makeTank()

    def makeTank(self):
        self.grid = [list(range(self.height)) for x in range(self.width)]
        self.grid = [list(map(lambda x: 1, row)) for row in self.grid]
        self.grid[0][0] = 3
        self.grid[0][2] = 3
        self.grid[2][1] = 3
        self.connectToMap()

    def goUp(self):
        self.orientation = 'up'
        self.grid = [list(map(lambda x: 1, row)) for row in self.grid]
        self.grid[0][0] = 3
        self.grid[0][2] = 3
        self.grid[2][1] = 3
        self.connectToMap()

    def goDown(self):
        self.orientation = 'down'
        self.grid = [list(map(lambda x: 1, row)) for row in self.grid]
        self.grid[0][1] = 3
        self.grid[2][2] = 3
        self.grid[2][0] = 3
        self.connectToMap()

    def goLeft(self):
        self.orientation = 'left'
        self.grid = [list(map(lambda x: 1, row)) for row in self.grid]
        self.grid[0][0] = 3
        self.grid[1][2] = 3
        self.grid[2][0] = 3
        self.connectToMap()

    def goRight(self):
        self.orientation = 'right'
        self.grid = [list(map(lambda x: 1, row)) for row in self.grid]
        self.grid[1][0] = 3
        self.grid[0][2] = 3
        self.grid[2][2] = 3
        self.connectToMap()

    def move(self, direction):
        # Check how many steps are needed to rotate the figure
        self.clear()
        if direction == 'up' and self.topLeft[0] > 0:
            self.topLeft[0] = self.topLeft[0] - 1
        elif direction == 'down' and self.topLeft[0] + self.width < self.map.height:
            self.topLeft[0] = self.topLeft[0] + 1
        elif direction == 'left' and self.topLeft[1] > 0:
            self.topLeft[1] = self.topLeft[1] - 1
        elif direction == 'right' and self.topLeft[1] + self.width < self.map.width:
            self.topLeft[1] = self.topLeft[1] + 1
        else:
            pass
        self.connectToMap()

    def shoot(self):
        bullet = Bullet(self.map)
        bullet.orientation = self.orientation
        if self.orientation == 'up':
            bullet.topLeft = [self.topLeft[0], self.topLeft[1] + 1]
        elif self.orientation == 'down':
            bullet.topLeft = [self.topLeft[0] + 2, self.topLeft[1] + 1]
        elif self.orientation == 'left':
            bullet.topLeft = [self.topLeft[0] + 1, self.topLeft[1]]
        elif self.orientation == 'right':
            bullet.topLeft = [self.topLeft[0] + 1, self.topLeft[1] + 2]
        self.map.bullets.append(bullet)


if __name__ == '__main__':
    app = QApplication([])
    battle_city = UI_BattleCity()
    sys.exit(app.exec_())
