import sys
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from math import cos, sin, pi, atan2, sqrt


types = ["Кривая Коха", "Кривая Миньковского", "Кривая Серпинского"]
angle1 = atan2(sqrt(3) / 4, 3 / 2)
angle2 = atan2(sqrt(3) / 4, 1 / 2)
Koch_size = 5
X, Y = 400, 400


def angle_vec(alpha):
    return QPointF(cos(alpha), sin(alpha))


def rotation_point(p, angle):
    angle *= -1
    new_x = p.x() * cos(angle) - p.y() * sin(angle)
    new_y = p.y() * cos(angle) + p.x() * sin(angle)
    return QPointF(new_x, new_y)


def mink_x(n):
    ans, k = 0, 1
    for i in range(n):
        ans += k
        k /= 4
    return ans


class MyWidget(QWidget):
    curr_n = Signal(int)

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setMinimumSize(300, 300)
        self.__n = 0
        self.__mode = 0

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        if types[self.__mode] == "Кривая Коха":
            self.koch_preparing(painter)
        elif types[self.__mode] == "Кривая Серпинского":
            self.sierpinski_preparing(painter)
        else:
            self.minkowski_preparing(painter)
        painter.end()

    def set_n(self, n):
        self.__n = n
        self.repaint()
        self.curr_n.emit(n)

    def set_mode(self, k):
        self.set_n(0)
        self.__mode = k
        self.repaint()

    def koch_preparing(self, painter):
        X = self.width()
        Y = self.height()
        centre = QPointF(X / 2, Y / 2)
        v1, v2 = angle_vec(angle1), angle_vec(pi - angle1)
        k = min((X - 5) / 2 / v1.x(), (Y - 5) / 2 / v1.y())
        p1, p2 = centre + v1 * k, centre + v2 * k
        self.koch(self.__n, p1, p2, painter)

    def koch(self, n, p1, p2, painter):
        if n == 0:
            painter.drawLine(p1, p2)
        else:
            q1 = p1 * 2 / 3 + p2 * 1 / 3
            q2 = p1 * 1 / 3 + p2 * 2 / 3
            q3 = q1 + rotation_point(q2 - q1, -pi / 3)
            self.koch(n - 1, p1, q1, painter)
            self.koch(n - 1, q1, q3, painter)
            self.koch(n - 1, q3, q2, painter)
            self.koch(n - 1, q2, p2, painter)

    def sierpinski_preparing(self, painter):
        X = self.width()
        Y = self.height()
        centre = QPointF(X / 2, Y / 2)
        v1, v2 = angle_vec(angle2), angle_vec(pi - angle2)
        k = min((X - 5) / 2 / v1.x(), (Y - 5) / 2 / v1.y())
        p1, p2, p3 = centre + v1 * k, centre + v2 * k, centre + QPointF(0, -v1.y()) * k
        self.sierpinski(self.__n, p1, p2, p3, painter)

    def sierpinski(self, n, p1, p2, p3, painter):
        if (n == 0):
            painter.drawLine(p1, p2)
            painter.drawLine(p1, p3)
            painter.drawLine(p2, p3)
        else:
            q1, q2, q3 = (p1 + p3) / 2, (p2 + p3) / 2, (p1 + p2) / 2
            self.sierpinski(n - 1, q1, q2, p3, painter)
            self.sierpinski(n - 1, p1, q3, q1, painter)
            self.sierpinski(n - 1, q3, q2, p2, painter)

    def minkowski_preparing(self, painter):
        X = self.width()
        Y = self.height()
        centre = QPointF(X / 2, Y / 2)
        leng = min(X - 5, (Y - 5) / (2 / 3)) / 2
        p1, p2 = centre - QPointF(leng, 0), centre + QPointF(leng, 0)
        self.minkowski(self.__n, p1, p2, painter)

    def minkowski(self, n, p1, p2, painter):
        if n == 0:
            painter.drawLine(p1, p2)
        else:
            v1 = (p2 - p1) / 4
            v2 = rotation_point(v1, pi / 2)
            q1 = p1 + v1
            q2 = q1 + v2
            q3 = q2 + v1
            q4 = q3 - v2
            q5 = q4 - v2
            q6 = q5 + v1
            q7 = q6 + v2
            self.minkowski(n - 1, p1, q1, painter)
            self.minkowski(n - 1, q1, q2, painter)
            self.minkowski(n - 1, q2, q3, painter)
            self.minkowski(n - 1, q3, q4, painter)
            self.minkowski(n - 1, q4, q5, painter)
            self.minkowski(n - 1, q5, q6, painter)
            self.minkowski(n - 1, q6, q7, painter)
            self.minkowski(n - 1, q7, p2, painter)

app = QApplication(sys.argv)
Window = QWidget()
Window.setWindowTitle("Curve")
Window.resize(X, Y)
Widget = MyWidget(Window)
Spin = QSpinBox(Window)
Spin.setMaximum(7)
Spin.valueChanged.connect(Widget.set_n)
ComboBox = QComboBox(Window)
ComboBox.addItems(types)
ComboBox.currentIndexChanged.connect(Widget.set_mode)
Widget.curr_n.connect(Spin.setValue)

Layout = QVBoxLayout()
hor_layout = QHBoxLayout()
hor_layout.addWidget(ComboBox, 2)
hor_layout.addWidget(Spin, 1)
Layout.addLayout(hor_layout)
Layout.addWidget(Widget, 1)

Window.setLayout(Layout)
Window.show()
app.exec_()