
import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QPainter, QBrush, QPen
from PyQt5.QtCore import Qt, QTimer, QRect

class Paddle(QWidget):
    height = 75
    width = 10

    increment = 10 

    def __init__(self,x,y):
        super().__init__()

        if x == 0:
            self.x = int(x) + self.width
        else:
            self.x = int(x) - self.width
        
        self.y = int(y/2)

        self.upper_bound = y
        self.lower_bound = 0

    def draw_paddle(self):
        return QRect(self.x,self.y,self.width,self.height)

    def move_up(self):
        if self.y - self.increment >= self.lower_bound:
            self.y = self.y - self.increment

    def move_down(self):
        if self.y + self.increment + self.height <= self.upper_bound:
            self.y = self.y + self.increment

class Ball(QWidget):
    radius = 20

    vx = 0 # pixels / sec
    vy = 0

    def __init__(self,x,y,delta_ms):
        super().__init__()
        self.x = int(x/2)
        self.y = int(y/2)
        self.delta_s = delta_ms 
        self.vx = y * self.delta_s


    def update_ball(self):
        self.x = int(self.x + self.vx * self.delta_s)
        print(self.x)

        # self.x = int(self.x + self.vx * self.delta_ms)

    def draw_ball(self):
        return QRect(self.x,self.y,self.radius,self.radius)


class Window(QMainWindow):
    dt = 50

    def __init__(self):
        super().__init__()
 
        self.title = "Pong Game"
        self.top = 100
        self.left = 100
        self.width = 680
        self.height = 500

        self.p1 = Paddle(self.width,self.height)
        self.p2 = Paddle(0,self.height)
        self.ball = Ball(self.width,self.height,self.dt)
 
        self.init_window()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.ball.update_ball)
        self.timer.timeout.connect(self.timer_callback)
        self.timer.start(self.dt)

    def timer_callback(self):
        self.update()

    def init_window(self):
        # self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.show()

    def paintEvent(self, event):
        painter = QPainter(self)

        painter.setBrush(Qt.black);
        painter.drawEllipse(self.ball.draw_ball())
        painter.drawRect(self.p1.draw_paddle())
        painter.drawRect(self.p2.draw_paddle())

    def keyPressEvent(self, event):

        if event.key() == Qt.Key.Key_Up:
            self.p1.move_up()
        
        if event.key() == Qt.Key.Key_Down:
            self.p1.move_down()
        
        if event.key() == Qt.Key.Key_W:
            self.p2.move_up()
        
        if event.key() == Qt.Key.Key_S:
            self.p2.move_down()

        self.update()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()

    sys.exit(app.exec_())