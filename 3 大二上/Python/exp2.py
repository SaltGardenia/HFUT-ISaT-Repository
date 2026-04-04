import sys
import random
import string
import re
from collections import Counter, defaultdict
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit,
                             QSpinBox, QGroupBox, QMessageBox, QListWidget, QSplitter)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class CustomSet:
    """自定义集合类"""
    def __init__(self, elements=None):
        self.elements = set(elements) if elements else set()

    def union(self, other):
        """并集"""
        return CustomSet(self.elements.union(other.elements))

    def intersection(self, other):
        """交集"""
        return CustomSet(self.elements.intersection(other.elements))

    def difference(self, other):
        """差集"""
        return CustomSet(self.elements.difference(other.elements))

    def __str__(self):
        return str(self.elements)

class StringStatsTab(QWidget):
    """随机字符统计标签页"""
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.generated_string = ""

    def init_ui(self):
        layout = QVBoxLayout()

        # 生成随机字符串区域
        generate_group = QGroupBox("生成随机字符串")
        generate_layout = QVBoxLayout()

        self.generate_btn = QPushButton("生成1000个随机字符")
        self.generate_btn.clicked.connect(self.generate_random_string)

        self.string_display = QTextEdit()
        self.string_display.setMaximumHeight(100)
        self.string_display.setPlaceholderText("生成的随机字符串将显示在这里...")

        generate_layout.addWidget(self.generate_btn)
        generate_layout.addWidget(QLabel("生成的字符串:"))
        generate_layout.addWidget(self.string_display)
        generate_group.setLayout(generate_layout)

        # 统计方法区域
        stats_group = QGroupBox("字符统计方法")
        stats_layout = QHBoxLayout()

        # 方法1：使用Counter
        method1_layout = QVBoxLayout()
        method1_btn = QPushButton("方法1：使用collections.Counter")
        method1_btn.clicked.connect(self.method1_counter)
        self.method1_result = QTextEdit()
        self.method1_result.setMaximumHeight(150)

        method1_layout.addWidget(method1_btn)
        method1_layout.addWidget(self.method1_result)

        # 方法2：使用字典
        method2_layout = QVBoxLayout()
        method2_btn = QPushButton("方法2：使用字典手动统计")
        method2_btn.clicked.connect(self.method2_dict)
        self.method2_result = QTextEdit()
        self.method2_result.setMaximumHeight(150)

        method2_layout.addWidget(method2_btn)
        method2_layout.addWidget(self.method2_result)

        stats_layout.addLayout(method1_layout)
        stats_layout.addLayout(method2_layout)
        stats_group.setLayout(stats_layout)

        layout.addWidget(generate_group)
        layout.addWidget(stats_group)
        self.setLayout(layout)

    def generate_random_string(self):
        """生成1000个随机字符"""
        characters = string.ascii_letters + string.digits + string.punctuation
        self.generated_string = ''.join(random.choice(characters) for _ in range(1000))
        self.string_display.setText(self.generated_string)
        self.method1_result.clear()
        self.method2_result.clear()

    def method1_counter(self):
        """方法1：使用Counter统计"""
        if not self.generated_string:
            QMessageBox.warning(self, "错误", "请先生成随机字符串")
            return

        counter = Counter(self.generated_string)
        result = "方法1：使用collections.Counter\n\n"
        result += f"总字符数: {len(self.generated_string)}\n"
        result += f"不同字符数: {len(counter)}\n\n"
        result += "字符出现次数统计:\n"

        # 显示前20个最常出现的字符
        for char, count in counter.most_common(20):
            result += f"'{char}': {count}次\n"

        if len(counter) > 20:
            result += f"\n... 还有{len(counter)-20}个其他字符"

        self.method1_result.setText(result)

    def method2_dict(self):
        """方法2：使用字典手动统计"""
        if not self.generated_string:
            QMessageBox.warning(self, "错误", "请先生成随机字符串")
            return

        char_count = {}
        for char in self.generated_string:
            char_count[char] = char_count.get(char, 0) + 1

        result = "方法2：使用字典手动统计\n\n"
        result += f"总字符数: {len(self.generated_string)}\n"
        result += f"不同字符数: {len(char_count)}\n\n"
        result += "字符出现次数统计:\n"

        # 按出现次数排序
        sorted_chars = sorted(char_count.items(), key=lambda x: x[1], reverse=True)
        for char, count in sorted_chars[:20]:
            result += f"'{char}': {count}次\n"

        if len(char_count) > 20:
            result += f"\n... 还有{len(char_count)-20}个其他字符"

        self.method2_result.setText(result)

class SetOperationsTab(QWidget):
    """集合操作标签页"""
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # 输入区域
        input_group = QGroupBox("输入集合")
        input_layout = QHBoxLayout()

        setA_layout = QVBoxLayout()
        setA_layout.addWidget(QLabel("集合A (用逗号分隔):"))
        self.setA_input = QLineEdit()
        self.setA_input.setText("1,2,3,4,5")
        setA_layout.addWidget(self.setA_input)

        setB_layout = QVBoxLayout()
        setB_layout.addWidget(QLabel("集合B (用逗号分隔):"))
        self.setB_input = QLineEdit()
        self.setB_input.setText("4,5,6,7,8")
        setB_layout.addWidget(self.setB_input)

        input_layout.addLayout(setA_layout)
        input_layout.addLayout(setB_layout)
        input_group.setLayout(input_layout)

        # 操作按钮
        btn_group = QGroupBox("操作方法")
        btn_layout = QHBoxLayout()

        system_btn = QPushButton("系统集合类操作")
        system_btn.clicked.connect(self.system_set_operations)

        custom_btn = QPushButton("自定义集合类操作")
        custom_btn.clicked.connect(self.custom_set_operations)

        btn_layout.addWidget(system_btn)
        btn_layout.addWidget(custom_btn)
        btn_group.setLayout(btn_layout)

        # 结果显示
        result_group = QGroupBox("操作结果")
        result_layout = QHBoxLayout()

        self.system_result = QTextEdit()
        self.custom_result = QTextEdit()

        result_layout.addWidget(QLabel("系统类结果:"))
        result_layout.addWidget(self.system_result)
        result_layout.addWidget(QLabel("自定义类结果:"))
        result_layout.addWidget(self.custom_result)
        result_group.setLayout(result_layout)

        layout.addWidget(input_group)
        layout.addWidget(btn_group)
        layout.addWidget(result_group)
        self.setLayout(layout)

    def parse_set_input(self, text):
        """解析集合输入"""
        try:
            elements = [x.strip() for x in text.split(',') if x.strip()]
            return set(elements)
        except:
            return set()

    def system_set_operations(self):
        """系统集合类操作"""
        setA = self.parse_set_input(self.setA_input.text())
        setB = self.parse_set_input(self.setB_input.text())

        if not setA or not setB:
            QMessageBox.warning(self, "错误", "请输入有效的集合元素")
            return

        result = f"集合A: {setA}\n"
        result += f"集合B: {setB}\n\n"
        result += f"并集 (A ∪ B): {setA.union(setB)}\n"
        result += f"交集 (A ∩ B): {setA.intersection(setB)}\n"
        result += f"差集 (A - B): {setA.difference(setB)}\n"
        result += f"差集 (B - A): {setB.difference(setA)}\n"
        result += f"对称差集: {setA.symmetric_difference(setB)}"

        self.system_result.setText(result)

    def custom_set_operations(self):
        """自定义集合类操作"""
        setA = self.parse_set_input(self.setA_input.text())
        setB = self.parse_set_input(self.setB_input.text())

        if not setA or not setB:
            QMessageBox.warning(self, "错误", "请输入有效的集合元素")
            return

        customA = CustomSet(setA)
        customB = CustomSet(setB)

        result = f"集合A: {customA}\n"
        result += f"集合B: {customB}\n\n"
        result += f"并集 (A ∪ B): {customA.union(customB)}\n"
        result += f"交集 (A ∩ B): {customA.intersection(customB)}\n"
        result += f"差集 (A - B): {customA.difference(customB)}\n"
        result += f"差集 (B - A): {customB.difference(customA)}"

        self.custom_result.setText(result)

class NestedListTab(QWidget):
    """嵌套列表标签页"""
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # 输入参数区域
        param_group = QGroupBox("生成参数")
        param_layout = QHBoxLayout()

        n_layout = QVBoxLayout()
        n_layout.addWidget(QLabel("列表元素数量 (n):"))
        self.n_input = QSpinBox()
        self.n_input.setRange(1, 20)
        self.n_input.setValue(5)
        n_layout.addWidget(self.n_input)

        m_layout = QVBoxLayout()
        m_layout.addWidget(QLabel("字符串最大长度 (m):"))
        self.m_input = QSpinBox()
        self.m_input.setRange(1, 10)
        self.m_input.setValue(5)
        m_layout.addWidget(self.m_input)

        param_layout.addLayout(n_layout)
        param_layout.addLayout(m_layout)

        self.generate_btn = QPushButton("生成嵌套列表")
        self.generate_btn.clicked.connect(self.generate_nested_list)
        param_layout.addWidget(self.generate_btn)

        param_group.setLayout(param_layout)

        # 结果显示区域
        result_group = QGroupBox("结果")
        result_layout = QVBoxLayout()

        self.original_result = QTextEdit()
        self.original_result.setMaximumHeight(120)
        self.original_result.setPlaceholderText("原始嵌套列表将显示在这里...")

        self.sorted_result = QTextEdit()
        self.sorted_result.setMaximumHeight(120)
        self.sorted_result.setPlaceholderText("按字符串长度排序的结果将显示在这里...")

        result_layout.addWidget(QLabel("原始嵌套列表:"))
        result_layout.addWidget(self.original_result)
        result_layout.addWidget(QLabel("按字符串长度降序排列:"))
        result_layout.addWidget(self.sorted_result)
        result_group.setLayout(result_layout)

        layout.addWidget(param_group)
        layout.addWidget(result_group)
        self.setLayout(layout)

    def generate_random_string(self, max_length):
        """生成随机字符串"""
        length = random.randint(1, max_length)
        chars = string.ascii_letters + string.digits
        return ''.join(random.choice(chars) for _ in range(length))

    def generate_nested_list(self):
        """生成嵌套列表"""
        n = self.n_input.value()
        m = self.m_input.value()

        # 生成嵌套列表
        nested_list = []
        for i in range(n):
            sublist_size = random.randint(1, 5)  # 每个子列表1-5个元素
            sublist = [self.generate_random_string(m) for _ in range(sublist_size)]
            nested_list.append(sublist)

        # 显示原始列表
        original_text = "原始嵌套列表:\n"
        for i, sublist in enumerate(nested_list):
            original_text += f"  子列表{i+1}: {sublist}\n"

        self.original_result.setText(original_text)

        # 展平列表并排序
        flat_list = [item for sublist in nested_list for item in sublist]
        sorted_list = sorted(flat_list, key=len, reverse=True)

        # 显示排序结果
        sorted_text = "按字符串长度降序排列:\n"
        for item in sorted_list:
            sorted_text += f"  '{item}' (长度: {len(item)})\n"

        self.sorted_result.setText(sorted_text)

class ListSlicingTab(QWidget):
    """列表切片标签页"""
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # 输入区域
        input_group = QGroupBox("输入列表")
        input_layout = QVBoxLayout()

        input_layout.addWidget(QLabel("输入整数列表 (用逗号分隔):"))
        self.list_input = QLineEdit()
        self.list_input.setText("1,2,3,4,5,6,7,8,9,10")
        input_layout.addWidget(self.list_input)

        self.generate_btn = QPushButton("生成随机列表")
        self.generate_btn.clicked.connect(self.generate_random_list)
        input_layout.addWidget(self.generate_btn)

        input_group.setLayout(input_layout)

        # 操作区域
        operation_group = QGroupBox("列表操作")
        operation_layout = QVBoxLayout()

        self.operate_btn = QPushButton("执行列表操作")
        self.operate_btn.clicked.connect(self.perform_list_operations)

        self.result_display = QTextEdit()

        operation_layout.addWidget(self.operate_btn)
        operation_layout.addWidget(self.result_display)
        operation_group.setLayout(operation_layout)

        layout.addWidget(input_group)
        layout.addWidget(operation_group)
        self.setLayout(layout)

    def generate_random_list(self):
        """生成随机列表"""
        n = random.randint(5, 15)
        random_list = [random.randint(1, 100) for _ in range(n)]
        self.list_input.setText(','.join(map(str, random_list)))

    def parse_list_input(self):
        """解析列表输入"""
        try:
            text = self.list_input.text()
            elements = [int(x.strip()) for x in text.split(',') if x.strip()]
            return elements
        except ValueError:
            QMessageBox.warning(self, "错误", "请输入有效的整数列表")
            return None

    def perform_list_operations(self):
        """执行列表操作"""
        original_list = self.parse_list_input()
        if original_list is None:
            return

        result = f"原始列表: {original_list}\n\n"

        # 1. 包含原列表所有元素的新列表
        new_list = original_list.copy()
        result += f"1. 新列表 (复制): {new_list}\n\n"

        # 2. 逆序列表
        reversed_list = original_list[::-1]
        result += f"2. 逆序列表: {reversed_list}\n\n"

        # 3. 偶数位置元素列表 (索引为偶数的位置)
        even_positions = original_list[::2]  # 从0开始，步长为2
        result += f"3. 偶数位置元素 (索引0,2,4...): {even_positions}\n\n"

        # 4. 其他切片操作示例
        first_half = original_list[:len(original_list)//2]
        second_half = original_list[len(original_list)//2:]
        result += f"4. 前半部分: {first_half}\n"
        result += f"5. 后半部分: {second_half}\n\n"

        # 5. 每隔一个元素取一个
        every_other = original_list[::2]
        result += f"6. 每隔一个元素: {every_other}"

        self.result_display.setText(result)

class TupleGeneratorTab(QWidget):
    """元组生成器标签页"""
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # 参数输入区域
        param_group = QGroupBox("生成参数")
        param_layout = QHBoxLayout()

        n_layout = QVBoxLayout()
        n_layout.addWidget(QLabel("元素数量 (n):"))
        self.n_input = QSpinBox()
        self.n_input.setRange(1, 50)
        self.n_input.setValue(10)
        n_layout.addWidget(self.n_input)

        m_layout = QVBoxLayout()
        m_layout.addWidget(QLabel("最大值 (m):"))
        self.m_input = QSpinBox()
        self.m_input.setRange(1, 1000)
        self.m_input.setValue(100)
        m_layout.addWidget(self.m_input)

        param_layout.addLayout(n_layout)
        param_layout.addLayout(m_layout)

        self.generate_btn = QPushButton("生成并过滤元组")
        self.generate_btn.clicked.connect(self.generate_and_filter_tuple)
        param_layout.addWidget(self.generate_btn)

        param_group.setLayout(param_layout)

        # 结果显示区域
        result_group = QGroupBox("生成结果")
        result_layout = QVBoxLayout()

        self.original_result = QTextEdit()
        self.original_result.setMaximumHeight(100)
        self.original_result.setPlaceholderText("原始元组将显示在这里...")

        self.filtered_result = QTextEdit()
        self.filtered_result.setMaximumHeight(100)
        self.filtered_result.setPlaceholderText("过滤后的元组将显示在这里...")

        result_layout.addWidget(QLabel("原始元组 (生成器推导式):"))
        result_layout.addWidget(self.original_result)
        result_layout.addWidget(QLabel("过滤后元组 (去掉偶数):"))
        result_layout.addWidget(self.filtered_result)
        result_group.setLayout(result_layout)

        layout.addWidget(param_group)
        layout.addWidget(result_group)
        self.setLayout(layout)

    def generate_and_filter_tuple(self):
        """生成并过滤元组"""
        n = self.n_input.value()
        m = self.m_input.value()

        # 使用生成器推导式生成元组
        tuple_generator = (random.randint(1, m) for _ in range(n))
        original_tuple = tuple(tuple_generator)

        # 过滤掉偶数
        filtered_tuple = tuple(x for x in original_tuple if x % 2 != 0)

        # 显示结果
        self.original_result.setText(
            f"原始元组 ({len(original_tuple)}个元素):\n{original_tuple}\n\n"
            f"生成器推导式代码:\n"
            f"tuple_generator = (random.randint(1, {m}) for _ in range({n}))"
        )

        self.filtered_result.setText(
            f"过滤后元组 ({len(filtered_tuple)}个元素):\n{filtered_tuple}\n\n"
            f"过滤代码:\n"
            f"filtered_tuple = tuple(x for x in original_tuple if x % 2 != 0)"
        )

class WordCountTab(QWidget):
    """单词统计标签页"""
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # 输入区域
        input_group = QGroupBox("输入文本")
        input_layout = QVBoxLayout()

        self.text_input = QTextEdit()
        self.text_input.setMaximumHeight(100)
        self.text_input.setPlaceholderText("请输入英文文本...")
        self.text_input.setText("I love China and I love programming")

        self.count_btn = QPushButton("统计单词频率")
        self.count_btn.clicked.connect(self.count_words)

        input_layout.addWidget(self.text_input)
        input_layout.addWidget(self.count_btn)
        input_group.setLayout(input_layout)

        # 结果显示区域
        result_group = QGroupBox("统计结果")
        result_layout = QVBoxLayout()

        self.result_display = QTextEdit()

        result_layout.addWidget(self.result_display)
        result_group.setLayout(result_layout)

        layout.addWidget(input_group)
        layout.addWidget(result_group)
        self.setLayout(layout)

    def count_words(self):
        """统计单词频率"""
        text = self.text_input.toPlainText().strip()
        if not text:
            QMessageBox.warning(self, "错误", "请输入文本")
            return

        # 转换为小写并分割单词
        words = text.lower().split()

        # 统计单词频率
        word_count = {}
        for word in words:
            # 去除标点符号
            clean_word = re.sub(r'[^\w\s]', '', word)
            if clean_word:
                word_count[clean_word] = word_count.get(clean_word, 0) + 1

        # 显示结果
        result = "单词出现次数统计:\n\n"
        for word, count in sorted(word_count.items()):
            result += f"{word}: {count}\n"

        result += f"\n总单词数: {len(words)}"
        result += f"\n不同单词数: {len(word_count)}"

        self.result_display.setText(result)

class RegexTab(QWidget):
    """正则表达式标签页"""
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # 输入区域
        input_group = QGroupBox("输入英文文本")
        input_layout = QVBoxLayout()

        self.text_input = QTextEdit()
        self.text_input.setMaximumHeight(100)
        self.text_input.setPlaceholderText("请输入英文文本...")
        self.text_input.setText("The cat and the dog ran but the fox jumped over the box")

        self.find_btn = QPushButton("查找3字母单词")
        self.find_btn.clicked.connect(self.find_three_letter_words)

        input_layout.addWidget(self.text_input)
        input_layout.addWidget(self.find_btn)
        input_group.setLayout(input_layout)

        # 方法选择区域
        method_group = QGroupBox("查找方法")
        method_layout = QHBoxLayout()

        self.regex_btn = QPushButton("使用正则表达式findall")
        self.regex_btn.clicked.connect(lambda: self.find_three_letter_words("regex"))

        self.split_btn = QPushButton("使用split方法")
        self.split_btn.clicked.connect(lambda: self.find_three_letter_words("split"))

        method_layout.addWidget(self.regex_btn)
        method_layout.addWidget(self.split_btn)
        method_group.setLayout(method_layout)

        # 结果显示区域
        result_group = QGroupBox("查找结果")
        result_layout = QVBoxLayout()

        self.result_display = QTextEdit()

        result_layout.addWidget(self.result_display)
        result_group.setLayout(result_layout)

        layout.addWidget(input_group)
        layout.addWidget(method_group)
        layout.addWidget(result_group)
        self.setLayout(layout)

    def find_three_letter_words(self, method="regex"):
        """查找3字母单词"""
        text = self.text_input.toPlainText().strip()
        if not text:
            QMessageBox.warning(self, "错误", "请输入文本")
            return

        if method == "regex":
            # 方法1：使用正则表达式findall
            pattern = r'\b[a-zA-Z]{3}\b'
            three_letter_words = re.findall(pattern, text)
            method_name = "正则表达式findall方法"
            code_example = "re.findall(r'\\b[a-zA-Z]{3}\\b', text)"
        else:
            # 方法2：使用split方法
            words = text.split()
            three_letter_words = [word for word in words if len(word.strip(".,!?;:\"'")) == 3]
            method_name = "split方法"
            code_example = "[word for word in text.split() if len(word.strip('.,!?;:\\\"\\'')) == 3]"

        # 显示结果
        result = f"使用方法: {method_name}\n\n"
        result += f"找到的3字母单词 ({len(three_letter_words)}个):\n"

        if three_letter_words:
            for i, word in enumerate(three_letter_words, 1):
                result += f"{i}. '{word}'\n"
        else:
            result += "未找到3字母单词\n"

        result += f"\n代码示例:\n{code_example}"

        self.result_display.setText(result)

class MainWindow(QMainWindow):
    """主窗口"""
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Python数据结构与算法验证系统')
        self.setGeometry(100, 100, 900, 800)

        # 创建标签页
        self.tab_widget = QTabWidget()

        # 添加各个标签页
        self.string_stats_tab = StringStatsTab()
        self.set_operations_tab = SetOperationsTab()
        self.nested_list_tab = NestedListTab()
        self.list_slicing_tab = ListSlicingTab()
        self.tuple_generator_tab = TupleGeneratorTab()
        self.word_count_tab = WordCountTab()
        self.regex_tab = RegexTab()

        self.tab_widget.addTab(self.string_stats_tab, "随机字符统计")
        self.tab_widget.addTab(self.set_operations_tab, "集合操作")
        self.tab_widget.addTab(self.nested_list_tab, "嵌套列表")
        self.tab_widget.addTab(self.list_slicing_tab, "列表切片")
        self.tab_widget.addTab(self.tuple_generator_tab, "元组生成器")
        self.tab_widget.addTab(self.word_count_tab, "单词统计")
        self.tab_widget.addTab(self.regex_tab, "正则表达式")

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
    font = QFont("Microsoft YaHei", 9)
    app.setFont(font)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()