import sys
import random
from PySide2.QtCore import *
from PySide2.QtWidgets import *

RULES_TEXT = "Все цифры в зашифрованном числе различные.\n" \
             "Число не может начинаться с нуля.\n" \
             "Если цифры в вашем числе совпали с задуманным, то они 'Быки'.\n" \
             "Одинаковые цифры на разных позициях - это 'Коровы'.\n" \
             "В верхней области экрана выводится кол-во 'Быков' и 'Коров' в вашем числе.\n" \
             "Вы можете узнать больше на: https://en.wikipedia.org/wiki/Bulls_and_Cows."

WHOAMI = "Меня зовут Дмитрий, я - создатель этого предложения.\n" \
         "Мои контакты:\n" \
         "https://vk.com/dm_sut - VK\n" \
         "s21v_sutyy@179.ru - электронная почта\n" \
         "\n" \
         "ВСЕ ПРАВА ЗАЩИЩЕНЫ"

LB_TEXT = "Вы были достаточно хороши, чтобы попасть в нашу таблице лидеров!\n" \
          "Все, что нужно сделать - ввести ваше имя"

NOBODY_TEXT = "Пока что в таблице лидеров нет имен, но мы недеемся, что Вы это исправите!"

EULA = ("БЛА " * 100 + '\n') * 100


def MyKey(a):
    return int(a[0])


def num_of_digits(n):
    if isinstance(n, int):
        return len(set(str(n)))
    return len(set(n))


def is_correct_data(s):
    return s.isdigit() and num_of_digits(s) == 4 and (10 ** 3 <= int(s) and int(s) < 10 ** 4)


def bulls_cows_count(n, k):
    coins = len(set(str(n)) & set(str(k)))
    bulls = 0
    while n:
        if k % 10 == n % 10:
            bulls += 1
        n //= 10
        k //= 10
    return (bulls, coins - bulls)


def nums_names(s):
    ret = []
    line = []
    curr_s = ''
    for c in s:
        if c == ' ' and len(line) == 0:
            line.append(curr_s)
            curr_s = ''
        elif c == '\n':
            line.append(curr_s)
            ret.append(line)
            line = []
            curr_s = ''
        else:
            curr_s += c
    return ret


class MyGame(QObject):
    for_user = Signal(str)

    def __init__(self):
        QObject.__init__(self)
        self.__game_num = random.randint(1000, 9999)
        while num_of_digits(self.__game_num) != 4:
            self.__game_num = random.randint(1000, 9999)
        print(self.__game_num)
        self.__user_num = 0
        self.__user_data = ""
        self.__steps = 0
        self.__game_solved = False

    def setValue(self, value):
        self.__user_data = value

    def check(self):
        if not is_correct_data(self.__user_data):
            self.for_user.emit("Введенная строка некорректна, прочите условие еще раз!")
            return

        if self.__user_num != int(self.__user_data):
            self.__steps += 1
            self.__user_num = int(self.__user_data)
        bulls, cows = bulls_cows_count(self.__game_num, self.__user_num)
        if (self.__user_num == self.__game_num):
            self.win()
        else:
            self.for_user.emit('{} "Быков", {} "Коров"'.format(bulls, cows))
        self.__user_data = 0
        TextLine.setText("")

    def new_game(self):
        self.__game_num = random.randint(1000, 9999)
        while num_of_digits(self.__game_num) != 4:
            self.__game_num = random.randint(1000, 9999)
        print(self.__game_num)
        self.__user_num = 0
        self.__user_data = ""
        self.__steps = 0
        self.__game_solved = False

    def give_up(self):
        self.for_user.emit("Повезет в другой раз!\nВаше число: {}".format(self.__game_num))
        self.__game_solved = True
        RestartButton.setText("Новая игра")
        TextLine.setEnabled(False)
        CheckButton.setEnabled(False)

    def win(self):
        self.for_user.emit("Поздравляем!\nПобеда!\nЧисло попыток: {}".format(self.__steps))
        self.__game_solved = True
        RestartButton.setText("Новая игра")
        CheckButton.setEnabled(False)
        TextLine.setEnabled(False)
        self.leaders()

    def leaders(self):
        try:
            f = open("leaderboard.txt", "r")
            lb = nums_names(f.read())
            f.close()
            if len(lb) < 5 or int(lb[-1][0]) > self.__steps:
                name, status = QInputDialog.getText(None, "LeaderBoard", LB_TEXT)
                if status:
                    f = open("leaderboard.txt", "w")
                    lb.append([str(self.__steps), name])
                    lb.sort(key=MyKey)
                    for i in range(min(5, len(lb))):
                        f.write(lb[i][0] + ' ' + lb[i][1] + '\n')
        except FileNotFoundError:
            f = open("leaderboard.txt", "w")
            name, status = QInputDialog.getText(None, "LeaderBoard", LB_TEXT)
            f.write(str(self.__steps) + ' ' + name + '\n')
            f.close()


    def show_leader_board(self):
        mb = QMessageBox()
        try:
            f = open("leaderboard.txt", "r")
            lines = nums_names(f.read())
            f.close()
        except FileNotFoundError:
            lines = []
        if len(lines) == 0:
            mb.setText(NOBODY_TEXT)
        else:
            board_text = ''
            for i in range(len(lines)):
                board_text += "{} место - {}: {} попыток\n".format(i + 1, lines[i][1], lines[i][0])
            for i in range(5 - len(lines)):
                board_text += "{} место - еще не занято\n".format(len(lines) + i + 1)
            mb.setText(board_text)
        mb.exec()


    def restart(self):
        if self.__game_solved:
            self.for_user.emit("")
            CheckButton.setEnabled(True)
            TextLine.setEnabled(True)
            TextLine.setText("")
            RestartButton.setText("Give up")
            self.new_game()
        else:
            self.give_up()


app = QApplication(sys.argv)
Window = QMainWindow()
Window.setWindowTitle("Bulls and cows")
Window.setFixedSize(260, 235)
TextLine = QLineEdit(Window)
TextLine.setGeometry(40, 75, 180, 30)
CheckButton = QPushButton("Проверить", Window)
CheckButton.setGeometry(40, 110, 85, 30)
RestartButton = QPushButton("Сдаться", Window)
RestartButton.setGeometry(135, 110, 85, 30)
ForUser = QLabel(Window)
ForUser.setGeometry(40, 20, 200, 40)
ShowLeaderBoard = QPushButton("Лучшие игроки", Window)
ShowLeaderBoard.setGeometry(40, 145, 180, 20)

RulesButton = QPushButton("Правила", Window)
RulesButton.setGeometry(40, 170, 180, 20)
RulesShow = QMessageBox()
RulesShow.setWindowTitle("The Rules")
RulesShow.setText(RULES_TEXT)

CreatorButton = QPushButton("Про создателя", Window)
CreatorButton.setGeometry(40, 195, 180, 20)
CreatorShow = QMessageBox()
CreatorShow.setWindowTitle("IcensQ")
CreatorShow.setText(WHOAMI)

Game = MyGame()

RulesButton.clicked.connect(RulesShow.exec)
CreatorButton.clicked.connect(CreatorShow.exec)
TextLine.textChanged.connect(Game.setValue)
CheckButton.clicked.connect(Game.check)
ShowLeaderBoard.clicked.connect(Game.show_leader_board)
Game.for_user.connect(ForUser.setText)
RestartButton.clicked.connect(Game.restart)

Window.show()
app.exec_()