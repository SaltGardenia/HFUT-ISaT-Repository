import sys
import random
import math
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit,
                             QSpinBox, QGroupBox, QMessageBox, QProgressBar)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QPalette, QColor

# 猜数字游戏的线程
class GuessNumberThread(QThread):
    result_signal = pyqtSignal(str)

    def __init__(self, game_type, target=None, guess=None, max_attempts=5):
        super().__init__()
        self.game_type = game_type
        self.target = target
        self.guess = guess
        self.max_attempts = max_attempts

    def run(self):
        if self.game_type == "branch":
            self.run_branch_game()
        elif self.game_type == "loop":
            self.run_loop_game()

    def run_branch_game(self):
        if self.guess == self.target:
            self.result_signal.emit("right! 恭喜你猜对了！")
        elif self.guess > self.target:
            self.result_signal.emit(f"too large! 游戏结束，正确答案是: {self.target}")
        else:
            self.result_signal.emit(f"too small! 游戏结束，正确答案是: {self.target}")

    def run_loop_game(self):
        # 这个在GUI中通过按钮点击处理
        pass

# 数学函数工具类
class MathFunctions:
    @staticmethod
    def fibonacci_less_than_n(n):
        """计算斐波那契数列中小于参数n的所有值"""
        if n <= 0:
            return []
        elif n == 1:
            return [0]

        fib_sequence = [0, 1]
        while True:
            next_fib = fib_sequence[-1] + fib_sequence[-2]
            if next_fib >= n:
                break
            fib_sequence.append(next_fib)

        return fib_sequence

    @staticmethod
    def sieve_of_eratosthenes(n):
        """利用筛选法求小于n的所有素数"""
        if n <= 2:
            return []

        is_prime = [True] * n
        is_prime[0] = is_prime[1] = False

        for i in range(2, int(math.sqrt(n)) + 1):
            if is_prime[i]:
                for j in range(i*i, n, i):
                    is_prime[j] = False

        primes = [i for i in range(2, n) if is_prime[i]]
        return primes

    @staticmethod
    def is_palindrome(s):
        """判断字符串是否是回文"""
        cleaned = ''.join(c.lower() for c in s if c.isalnum())
        return cleaned == cleaned[::-1]

    @staticmethod
    def random_list_stats(n, min_val=1, max_val=100):
        """生成随机列表并返回平均值和大于平均值的元素"""
        random_list = [random.randint(min_val, max_val) for _ in range(n)]
        average = sum(random_list) / len(random_list)
        above_avg = [x for x in random_list if x > average]

        return (average, tuple(above_avg)), random_list

    @staticmethod
    def calculate_workday_effort():
        """计算工作日需要努力的程度"""
        daily_effort = 1.01
        total_with_daily = daily_effort ** 365

        def yearly_growth(workday_effort):
            weeks = 52
            extra_day = 1

            total_growth = 1.0
            for week in range(weeks):
                for _ in range(5):
                    total_growth *= workday_effort
                for _ in range(2):
                    total_growth *= 0.99

            total_growth *= workday_effort
            return total_growth

        low, high = 1.01, 1.1
        precision = 1e-8

        while high - low > precision:
            mid = (low + high) / 2
            if yearly_growth(mid) < total_with_daily:
                low = mid
            else:
                high = mid

        required_effort = (low + high) / 2
        return required_effort

    @staticmethod
    def find_max_overlap(s1, s2):
        """查找两个字符串首尾交叉的最大子串长度"""
        find_overlap = lambda x, y: [i for i in range(min(len(x), len(y)), 0, -1)
                                     if x[-i:] == y[:i]]

        overlaps = find_overlap(s1, s2)
        max_overlap = overlaps[0] if overlaps else 0

        if max_overlap > 0:
            result = s1 + s2[max_overlap:]
        else:
            result = s1 + s2

        return max_overlap, result

# 猜数字游戏标签页
class GuessNumberTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.loop_target = None
        self.loop_attempts = 0
        self.max_loop_attempts = 5

    def init_ui(self):
        layout = QVBoxLayout()

        # 分支结构游戏
        branch_group = QGroupBox("1. 分支结构猜数字游戏")
        branch_layout = QVBoxLayout()

        self.branch_target = random.randint(1, 100)
        branch_info = QLabel(f"系统已生成1-100的随机数，你有1次猜测机会")
        self.branch_input = QSpinBox()
        self.branch_input.setRange(1, 100)
        self.branch_input.setValue(50)

        branch_btn = QPushButton("猜数字")
        branch_btn.clicked.connect(self.play_branch_game)

        self.branch_result = QTextEdit()
        self.branch_result.setMaximumHeight(100)

        branch_layout.addWidget(branch_info)
        branch_layout.addWidget(QLabel("你的猜测:"))
        branch_layout.addWidget(self.branch_input)
        branch_layout.addWidget(branch_btn)
        branch_layout.addWidget(QLabel("结果:"))
        branch_layout.addWidget(self.branch_result)
        branch_group.setLayout(branch_layout)

        # 循环结构游戏
        loop_group = QGroupBox("2. 循环结构猜数字游戏")
        loop_layout = QVBoxLayout()

        self.start_loop_btn = QPushButton("开始新游戏")
        self.start_loop_btn.clicked.connect(self.start_loop_game)

        loop_info = QLabel("点击开始游戏后，你有5次猜测机会")
        self.loop_input = QSpinBox()
        self.loop_input.setRange(1, 100)
        self.loop_input.setValue(50)
        self.loop_input.setEnabled(False)

        self.loop_guess_btn = QPushButton("猜数字")
        self.loop_guess_btn.clicked.connect(self.play_loop_game)
        self.loop_guess_btn.setEnabled(False)

        self.loop_attempts_label = QLabel("剩余次数: 0")
        self.loop_result = QTextEdit()
        self.loop_result.setMaximumHeight(150)

        loop_layout.addWidget(self.start_loop_btn)
        loop_layout.addWidget(loop_info)
        loop_layout.addWidget(QLabel("你的猜测:"))
        loop_layout.addWidget(self.loop_input)
        loop_layout.addWidget(self.loop_guess_btn)
        loop_layout.addWidget(self.loop_attempts_label)
        loop_layout.addWidget(QLabel("游戏过程:"))
        loop_layout.addWidget(self.loop_result)
        loop_group.setLayout(loop_layout)

        layout.addWidget(branch_group)
        layout.addWidget(loop_group)
        self.setLayout(layout)

    def play_branch_game(self):
        guess = self.branch_input.value()
        if guess == self.branch_target:
            result = "right! 恭喜你猜对了！"
        elif guess > self.branch_target:
            result = f"too large! 游戏结束，正确答案是: {self.branch_target}"
        else:
            result = f"too small! 游戏结束，正确答案是: {self.branch_target}"

        self.branch_result.setText(result)

    def start_loop_game(self):
        self.loop_target = random.randint(1, 100)
        self.loop_attempts = 0
        self.max_loop_attempts = 5
        self.loop_input.setEnabled(True)
        self.loop_guess_btn.setEnabled(True)
        self.loop_attempts_label.setText(f"剩余次数: {self.max_loop_attempts}")
        self.loop_result.clear()
        self.loop_result.append("游戏开始！请输入你的猜测。")

    def play_loop_game(self):
        if self.loop_target is None:
            return

        guess = self.loop_input.value()
        self.loop_attempts += 1
        remaining = self.max_loop_attempts - self.loop_attempts

        if guess == self.loop_target:
            self.loop_result.append(f"第{self.loop_attempts}次: {guess} -> right! 恭喜你猜对了！")
            self.loop_input.setEnabled(False)
            self.loop_guess_btn.setEnabled(False)
        elif guess > self.loop_target:
            self.loop_result.append(f"第{self.loop_attempts}次: {guess} -> too large!")
        else:
            self.loop_result.append(f"第{self.loop_attempts}次: {guess} -> too small!")

        self.loop_attempts_label.setText(f"剩余次数: {remaining}")

        if remaining == 0 and guess != self.loop_target:
            self.loop_result.append(f"游戏结束！正确答案是: {self.loop_target}")
            self.loop_input.setEnabled(False)
            self.loop_guess_btn.setEnabled(False)

class FunctionTab(QWidget):
    """函数结构标签页"""
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # 斐波那契数列
        fib_group = QGroupBox("(1) 斐波那契数列")
        fib_layout = QHBoxLayout()
        fib_input_layout = QVBoxLayout()

        self.fib_input = QSpinBox()
        self.fib_input.setRange(1, 1000)
        self.fib_input.setValue(50)
        self.fib_calc_btn = QPushButton("计算")
        self.fib_calc_btn.clicked.connect(self.calculate_fibonacci)
        self.fib_result = QTextEdit()
        self.fib_result.setMaximumHeight(80)

        fib_input_layout.addWidget(QLabel("输入n值:"))
        fib_input_layout.addWidget(self.fib_input)
        fib_input_layout.addWidget(self.fib_calc_btn)
        fib_layout.addLayout(fib_input_layout)
        fib_layout.addWidget(self.fib_result)
        fib_group.setLayout(fib_layout)

        # 筛选法求素数
        prime_group = QGroupBox("(2) 筛选法求素数")
        prime_layout = QHBoxLayout()
        prime_input_layout = QVBoxLayout()

        self.prime_input = QSpinBox()
        self.prime_input.setRange(2, 1000)
        self.prime_input.setValue(30)
        self.prime_calc_btn = QPushButton("计算素数")
        self.prime_calc_btn.clicked.connect(self.calculate_primes)
        self.prime_result = QTextEdit()
        self.prime_result.setMaximumHeight(80)

        prime_input_layout.addWidget(QLabel("输入自然数:"))
        prime_input_layout.addWidget(self.prime_input)
        prime_input_layout.addWidget(self.prime_calc_btn)
        prime_layout.addLayout(prime_input_layout)
        prime_layout.addWidget(self.prime_result)
        prime_group.setLayout(prime_layout)

        # 回文判断
        palindrome_group = QGroupBox("(3) 回文判断")
        palindrome_layout = QHBoxLayout()
        palindrome_input_layout = QVBoxLayout()

        self.palindrome_input = QLineEdit()
        self.palindrome_input.setText("A man a plan a canal Panama")
        self.palindrome_btn = QPushButton("判断回文")
        self.palindrome_btn.clicked.connect(self.check_palindrome)
        self.palindrome_result = QTextEdit()
        self.palindrome_result.setMaximumHeight(60)

        palindrome_input_layout.addWidget(QLabel("输入字符串:"))
        palindrome_input_layout.addWidget(self.palindrome_input)
        palindrome_input_layout.addWidget(self.palindrome_btn)
        palindrome_layout.addLayout(palindrome_input_layout)
        palindrome_layout.addWidget(self.palindrome_result)
        palindrome_group.setLayout(palindrome_layout)

        # 随机列表统计
        stats_group = QGroupBox("(4) 随机列表统计")
        stats_layout = QHBoxLayout()
        stats_input_layout = QVBoxLayout()

        self.stats_input = QSpinBox()
        self.stats_input.setRange(1, 20)
        self.stats_input.setValue(5)
        self.stats_btn = QPushButton("生成并统计")
        self.stats_btn.clicked.connect(self.generate_stats)
        self.stats_result = QTextEdit()
        self.stats_result.setMaximumHeight(100)

        stats_input_layout.addWidget(QLabel("列表长度:"))
        stats_input_layout.addWidget(self.stats_input)
        stats_input_layout.addWidget(self.stats_btn)
        stats_layout.addLayout(stats_input_layout)
        stats_layout.addWidget(self.stats_result)
        stats_group.setLayout(stats_layout)

        # 工作日努力程度
        effort_group = QGroupBox("(5) 工作日努力程度计算")
        effort_layout = QVBoxLayout()

        self.effort_btn = QPushButton("计算所需努力程度")
        self.effort_btn.clicked.connect(self.calculate_effort)
        self.effort_result = QTextEdit()
        self.effort_result.setMaximumHeight(120)

        effort_layout.addWidget(QLabel("计算每周工作5天，休息2天的情况下，要达到每天努力1%的效果需要多大的努力程度"))
        effort_layout.addWidget(self.effort_btn)
        effort_layout.addWidget(self.effort_result)
        effort_group.setLayout(effort_layout)

        layout.addWidget(fib_group)
        layout.addWidget(prime_group)
        layout.addWidget(palindrome_group)
        layout.addWidget(stats_group)
        layout.addWidget(effort_group)
        self.setLayout(layout)

    def calculate_fibonacci(self):
        n = self.fib_input.value()
        result = MathFunctions.fibonacci_less_than_n(n)
        self.fib_result.setText(f"小于{n}的斐波那契数列:\n{result}")

    def calculate_primes(self):
        n = self.prime_input.value()
        result = MathFunctions.sieve_of_eratosthenes(n)
        self.prime_result.setText(f"小于{n}的所有素数:\n{result}")

    def check_palindrome(self):
        text = self.palindrome_input.text()
        is_pal = MathFunctions.is_palindrome(text)
        result = "是回文字符串" if is_pal else "不是回文字符串"
        self.palindrome_result.setText(f"'{text}'\n{result}")

    def generate_stats(self):
        n = self.stats_input.value()
        (average, above_avg), random_list = MathFunctions.random_list_stats(n, 1, 100)
        self.stats_result.setText(
            f"生成的随机列表: {random_list}\n"
            f"平均值: {average:.2f}\n"
            f"大于平均值的元素: {above_avg}"
        )

    def calculate_effort(self):
        effort = MathFunctions.calculate_workday_effort()
        daily_increase = (effort - 1) * 100
        self.effort_result.setText(
            f"每天努力1%一年的效果: 37.78倍\n\n"
            f"工作日需要努力的程度:\n"
            f"• 每日增长率: {effort:.6f}\n"
            f"• 相当于每天努力: {daily_increase:.4f}%\n"
            f"• 说明: 工作日需要更加努力才能弥补休息日的退步"
        )

class LambdaTab(QWidget):
    """Lambda表达式标签页"""
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        group = QGroupBox("Lambda表达式 - 字符串交叉连接")
        main_layout = QVBoxLayout()

        # 输入区域
        input_layout = QHBoxLayout()
        left_input_layout = QVBoxLayout()
        right_input_layout = QVBoxLayout()

        left_input_layout.addWidget(QLabel("第一个字符串:"))
        self.str1_input = QLineEdit()
        self.str1_input.setText("1234")
        left_input_layout.addWidget(self.str1_input)

        right_input_layout.addWidget(QLabel("第二个字符串:"))
        self.str2_input = QLineEdit()
        self.str2_input.setText("2347")
        right_input_layout.addWidget(self.str2_input)

        input_layout.addLayout(left_input_layout)
        input_layout.addLayout(right_input_layout)

        # 按钮
        self.calc_btn = QPushButton("计算交叉连接")
        self.calc_btn.clicked.connect(self.calculate_overlap)

        # 结果显示
        self.result_display = QTextEdit()
        self.result_display.setMaximumHeight(150)

        # 示例
        example_group = QGroupBox("示例")
        example_layout = QVBoxLayout()
        example_text = QTextEdit()
        example_text.setPlainText(
            "示例1: '1234' 和 '2347' -> 最大交叉: 3, 连接结果: '12347'\n"
            "示例2: 'hello' 和 'world' -> 最大交叉: 1, 连接结果: 'helloworld'\n"
            "示例3: 'abc' 和 'def' -> 最大交叉: 0, 连接结果: 'abcdef'"
        )
        example_text.setMaximumHeight(100)
        example_layout.addWidget(example_text)
        example_group.setLayout(example_layout)

        main_layout.addLayout(input_layout)
        main_layout.addWidget(self.calc_btn)
        main_layout.addWidget(QLabel("计算结果:"))
        main_layout.addWidget(self.result_display)
        main_layout.addWidget(example_group)

        group.setLayout(main_layout)
        layout.addWidget(group)
        self.setLayout(layout)

    def calculate_overlap(self):
        str1 = self.str1_input.text()
        str2 = self.str2_input.text()

        if not str1 or not str2:
            QMessageBox.warning(self, "输入错误", "请输入两个字符串")
            return

        max_overlap, connected = MathFunctions.find_max_overlap(str1, str2)

        self.result_display.setText(
            f"字符串1: '{str1}'\n"
            f"字符串2: '{str2}'\n"
            f"最大交叉子串长度: {max_overlap}\n"
            f"连接结果: '{connected}'\n\n"
            f"Lambda表达式说明:\n"
            f"find_overlap = lambda x, y: [i for i in range(min(len(x), len(y)), 0, -1) if x[-i:] == y[:i]]"
        )

class MainWindow(QMainWindow):
    """主窗口"""
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Python编程问题验证系统')
        self.setGeometry(100, 100, 800, 700)

        # 创建标签页
        self.tab_widget = QTabWidget()

        # 添加各个标签页
        self.guess_tab = GuessNumberTab()
        self.function_tab = FunctionTab()
        self.lambda_tab = LambdaTab()

        self.tab_widget.addTab(self.guess_tab, "猜数字游戏")
        self.tab_widget.addTab(self.function_tab, "函数结构")
        self.tab_widget.addTab(self.lambda_tab, "Lambda表达式")

        self.setCentralWidget(self.tab_widget)

        # 设置样式
        self.apply_styles()

    def apply_styles(self):
        """应用样式"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QTabWidget::pane {
                border: 1px solid #C2C7CB;
                background-color: white;
            }
            QTabBar::tab {
                background-color: #E1E1E1;
                border: 1px solid #C4C4C3;
                padding: 8px 20px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: #4CAF50;
                color: white;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #CCCCCC;
                border-radius: 5px;
                margin-top: 1ex;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            QPushButton {
                background-color: #4CAF50;
                border: none;
                color: white;
                padding: 8px 16px;
                text-align: center;
                font-size: 14px;
                margin: 4px 2px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
            QTextEdit {
                border: 1px solid #CCCCCC;
                border-radius: 3px;
                padding: 5px;
                background-color: #FAFAFA;
            }
            QLineEdit, QSpinBox {
                padding: 5px;
                border: 1px solid #CCCCCC;
                border-radius: 3px;
            }
        """)

def main():
    app = QApplication(sys.argv)

    # 设置应用程序字体
    font = QFont("Microsoft YaHei", 10)
    app.setFont(font)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()