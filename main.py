
import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QMainWindow, QFrame
from PyQt5.QtWidgets import QVBoxLayout, QLabel
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

    vx = 300 # pixels / sec
    vy = 30

    def __init__(self,x,y,delta_ms):
        super().__init__()
        self.x = int(x / 2)
        self.y = int(y / 2)
        self.delta_ms = delta_ms


    def update_ball(self):
        self.x = int(self.x + self.vx * self.delta_ms / 1000)
        self.y = int(self.y + self.vy * self.delta_ms / 1000)

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

        # self.layout = QVBoxLayout(self)
        # self.layout.addWidget(QLabel('Cunt'))
        # self.layout.addWidget(QFrame())
        # self.setLayout(self.layout)


        self.p1 = Paddle(self.width, self.height)
        self.p2 = Paddle(0, self.height)
        self.ball = Ball(self.width, self.height, self.dt)
 
        self.init_window()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.timer_callback)
        self.timer.start(self.dt)

    def timer_callback(self):

        is_contact1 =  self.p1.draw_paddle().intersected(self.ball.draw_ball())
        is_contact2 =  self.p2.draw_paddle().intersected(self.ball.draw_ball())

        if self.ball.y + self.ball.radius > self.height:
            self.ball.vy = -self.ball.vy
        elif self.ball.y - self.ball.radius < 0:
            self.ball.vy = -self.ball.vy

        if is_contact1 or is_contact2:
            self.ball.vx = -self.ball.vx

        self.ball.update_ball()
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

        if event.key() == Qt.Key.Key_Q:
            sys.exit()

        self.update()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()

    sys.exit(app.exec_())