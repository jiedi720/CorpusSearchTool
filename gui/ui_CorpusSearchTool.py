# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'CorpusSearchToolueUrKP.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QGridLayout,
    QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QMainWindow, QMenu, QMenuBar, QProgressBar,
    QPushButton, QSizePolicy, QStatusBar, QTabWidget,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_CorpusSearchTool(object):
    def setupUi(self, CorpusSearchTool):
        if not CorpusSearchTool.objectName():
            CorpusSearchTool.setObjectName(u"CorpusSearchTool")
        CorpusSearchTool.resize(1000, 800)
        CorpusSearchTool.setMinimumSize(QSize(1000, 800))
        CorpusSearchTool.setMaximumSize(QSize(1300, 800))
        self.actionlight = QAction(CorpusSearchTool)
        self.actionlight.setObjectName(u"actionlight")
        self.actionDark = QAction(CorpusSearchTool)
        self.actionDark.setObjectName(u"actionDark")
        self.centralwidget = QWidget(CorpusSearchTool)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_6 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setSpacing(15)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(10, 3, 10, -1)
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.ReadPathLabel = QLabel(self.centralwidget)
        self.ReadPathLabel.setObjectName(u"ReadPathLabel")
        font = QFont()
        font.setPointSize(10)
        self.ReadPathLabel.setFont(font)

        self.horizontalLayout_2.addWidget(self.ReadPathLabel)

        self.ReadPathInput = QLineEdit(self.centralwidget)
        self.ReadPathInput.setObjectName(u"ReadPathInput")
        self.ReadPathInput.setMinimumSize(QSize(400, 30))
        self.ReadPathInput.setMaximumSize(QSize(16777215, 30))
        self.ReadPathInput.setStyleSheet(u"border-radius: 7px;\n"
"padding-left: 5px;")

        self.horizontalLayout_2.addWidget(self.ReadPathInput)

        self.ReadPath = QHBoxLayout()
        self.ReadPath.setSpacing(5)
        self.ReadPath.setObjectName(u"ReadPath")
        self.ReadPathSet = QPushButton(self.centralwidget)
        self.ReadPathSet.setObjectName(u"ReadPathSet")
        self.ReadPathSet.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ReadPathSet.sizePolicy().hasHeightForWidth())
        self.ReadPathSet.setSizePolicy(sizePolicy)
        self.ReadPathSet.setMinimumSize(QSize(30, 30))
        self.ReadPathSet.setMaximumSize(QSize(30, 30))
        self.ReadPathSet.setStyleSheet(u"/* \u6309\u94ae\u9ed8\u8ba4\u6837\u5f0f */\n"
"QPushButton {\n"
"    color: white;\n"
"    border-radius: 8px;\n"
"    border: 1px solid #bfc1c8; \n"
"}\n"
"\n"
"/* \u60ac\u6d6e\u7279\u6548 */\n"
"QPushButton[theme=\"light\"]:hover {\n"
"    background-color: #a0a0a0; /* \u989c\u8272\u6bd4\u9ed8\u8ba4\u7a0d\u4eae */\n"
"}\n"
"\n"
"QPushButton[theme=\"dark\"]:hover {\n"
"    background-color: #DEDEDE;  /* \u989c\u8272\u6bd4\u9ed8\u8ba4\u7a0d\u4eae */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    /* 1. \u5411\u4e0b\u63a8\u6587\u5b57 */\n"
"    padding-top: 4px; \n"
"    /* 2. \u540c\u65f6\u51cf\u5c11\u5e95\u90e8\uff0c\u786e\u4fdd\u5185\u90e8\u6709\u6548\u7a7a\u95f4\u9ad8\u5ea6\u4e0d\u53d8 */\n"
"    padding-bottom: 0px; \n"
"    /* 3. \u5f3a\u5236\u5185\u5bb9\u6c34\u5e73\u5782\u76f4\u5c45\u4e2d\uff0c\u9632\u6b62\u5bf9\u9f50\u65b9\u5f0f\u5e72\u6270 */\n"
"    text-align: center;\n"
"}")
        icon = QIcon()
        icon.addFile(u"../../Qt_Widgets_Designer/icons/refresh.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.ReadPathSet.setIcon(icon)
        self.ReadPathSet.setIconSize(QSize(20, 20))

        self.ReadPath.addWidget(self.ReadPathSet)

        self.ReadPathSelect = QPushButton(self.centralwidget)
        self.ReadPathSelect.setObjectName(u"ReadPathSelect")
        self.ReadPathSelect.setMinimumSize(QSize(30, 30))
        self.ReadPathSelect.setMaximumSize(QSize(30, 30))
        self.ReadPathSelect.setStyleSheet(u"/* \u6309\u94ae\u9ed8\u8ba4\u6837\u5f0f */\n"
"QPushButton {\n"
"    color: white;\n"
"    border-radius: 8px;\n"
"    border: 1px solid #bfc1c8; \n"
"}\n"
"\n"
"/* \u60ac\u6d6e\u7279\u6548 */\n"
"QPushButton[theme=\"light\"]:hover {\n"
"    background-color: #a0a0a0; /* \u989c\u8272\u6bd4\u9ed8\u8ba4\u7a0d\u4eae */\n"
"}\n"
"\n"
"QPushButton[theme=\"dark\"]:hover {\n"
"    background-color: #DEDEDE;  /* \u989c\u8272\u6bd4\u9ed8\u8ba4\u7a0d\u4eae */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    /* 1. \u5411\u4e0b\u63a8\u6587\u5b57 */\n"
"    padding-top: 4px; \n"
"    /* 2. \u540c\u65f6\u51cf\u5c11\u5e95\u90e8\uff0c\u786e\u4fdd\u5185\u90e8\u6709\u6548\u7a7a\u95f4\u9ad8\u5ea6\u4e0d\u53d8 */\n"
"    padding-bottom: 0px; \n"
"    /* 3. \u5f3a\u5236\u5185\u5bb9\u6c34\u5e73\u5782\u76f4\u5c45\u4e2d\uff0c\u9632\u6b62\u5bf9\u9f50\u65b9\u5f0f\u5e72\u6270 */\n"
"    text-align: center;\n"
"}")
        icon1 = QIcon()
        icon1.addFile(u"../icons/search2.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.ReadPathSelect.setIcon(icon1)
        self.ReadPathSelect.setIconSize(QSize(20, 20))

        self.ReadPath.addWidget(self.ReadPathSelect)

        self.ReadPathOpen = QPushButton(self.centralwidget)
        self.ReadPathOpen.setObjectName(u"ReadPathOpen")
        sizePolicy.setHeightForWidth(self.ReadPathOpen.sizePolicy().hasHeightForWidth())
        self.ReadPathOpen.setSizePolicy(sizePolicy)
        self.ReadPathOpen.setMinimumSize(QSize(30, 30))
        self.ReadPathOpen.setMaximumSize(QSize(30, 30))
        self.ReadPathOpen.setStyleSheet(u"/* \u6309\u94ae\u9ed8\u8ba4\u6837\u5f0f */\n"
"QPushButton {\n"
"    color: white;\n"
"    border-radius: 8px;\n"
"    border: 1px solid #bfc1c8; \n"
"}\n"
"\n"
"/* \u60ac\u6d6e\u7279\u6548 */\n"
"QPushButton[theme=\"light\"]:hover {\n"
"    background-color: #a0a0a0; /* \u989c\u8272\u6bd4\u9ed8\u8ba4\u7a0d\u4eae */\n"
"}\n"
"\n"
"QPushButton[theme=\"dark\"]:hover {\n"
"    background-color: #DEDEDE;  /* \u989c\u8272\u6bd4\u9ed8\u8ba4\u7a0d\u4eae */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    /* 1. \u5411\u4e0b\u63a8\u6587\u5b57 */\n"
"    padding-top: 4px; \n"
"    /* 2. \u540c\u65f6\u51cf\u5c11\u5e95\u90e8\uff0c\u786e\u4fdd\u5185\u90e8\u6709\u6548\u7a7a\u95f4\u9ad8\u5ea6\u4e0d\u53d8 */\n"
"    padding-bottom: 0px; \n"
"    /* 3. \u5f3a\u5236\u5185\u5bb9\u6c34\u5e73\u5782\u76f4\u5c45\u4e2d\uff0c\u9632\u6b62\u5bf9\u9f50\u65b9\u5f0f\u5e72\u6270 */\n"
"    text-align: center;\n"
"}")
        icon2 = QIcon()
        icon2.addFile(u"../../Qt_Widgets_Designer/icons/open-folder2.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.ReadPathOpen.setIcon(icon2)
        self.ReadPathOpen.setIconSize(QSize(20, 20))

        self.ReadPath.addWidget(self.ReadPathOpen)


        self.horizontalLayout_2.addLayout(self.ReadPath)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.corpus_tab_widget = QTabWidget(self.centralwidget)
        self.corpus_tab_widget.setObjectName(u"corpus_tab_widget")
        self.corpus_tab_widget.setMinimumSize(QSize(520, 150))
        self.corpus_tab_widget.setMaximumSize(QSize(16777215, 999))
        self.corpus_tab_widget.setFont(font)
        self.corpus_tab_widget.setStyleSheet(u"/* \u6574\u4f53\u5bb9\u5668\u7f8e\u5316 */\n"
"QTabWidget[theme=\"light\"]::pane {\n"
"    background-color: #DEDEDE;   \n"
"    border-radius: 10px;            \n"
"    border-top-left-radius: 0px;   \n"
"    border-top-right-radius: 0px;  \n"
"    top: 0px;                     \n"
"}\n"
"\n"
"QTabWidget[theme=\"dark\"]::pane {\n"
"    background-color: #9e9e9e;    \n"
"    border-radius: 10px;            \n"
"    border-top-left-radius: 0px;   \n"
"    border-top-right-radius: 0px;  \n"
"    top: 0px;                     \n"
"}\n"
"\n"
"/* \u6240\u6709\u6807\u7b7e\uff08\u9ed8\u8ba4\u8272\uff09\uff1a\u9ec4\u8272 */\n"
"/* \u6ce8\u610f\uff1a\u8fd9\u91cc\u4f5c\u4e3a\u9ed8\u8ba4\u503c\uff0c\u4f1a\u88ab first \u548c last \u8986\u76d6 */\n"
"QTabBar::tab { \n"
"    color: rgb(0, 0, 0);\n"
"    background-color: #FFC209;\n"
"    padding: 2px 1px;/*\u8bbe\u7f6e\u6807\u7b7e\u6587\u5b57\u4e0e\u6807\u7b7e\u8fb9\u6846\u4e4b\u95f4\u7684\u7559\u767d\u533a\u57df */\n"
"    min-width: 150px; /*\u8bbe\u7f6e\u6807\u7b7e\u7684"
                        "\u6700\u5c0f\u5bbd\u5ea6 */\n"
"    margin-right: 1px; /* \u9ed8\u8ba4\u4fdd\u7559\u8fb9\u8ddd\u7528\u4e8e\u91cd\u53e0 */\n"
"    /* \u6838\u5fc3\u4fee\u6539\uff1a\u5206\u522b\u8bbe\u7f6e\u56db\u4e2a\u89d2\u7684\u5f27\u5ea6 \u987a\u5e8f\u4e3a\uff1a\u5de6\u4e0a, \u53f3\u4e0a, \u53f3\u4e0b, \u5de6\u4e0b */\n"
"    border-top-left-radius: 10px;  \n"
"    border-top-right-radius: 10px; \n"
"    border-bottom-left-radius: 1px;\n"
"    border-bottom-right-radius: 1px;\n"
"}\n"
"\n"
"/* \u9009\u4e2d\u72b6\u6001 */\n"
"QTabBar::tab:selected {\n"
"    font-weight: bold;\n"
"    color: rgb(255, 255, 255);\n"
"    background-color: #7953B1;\n"
"    /* 3. \u8fd9\u91cc\u7684 margin-top \u8bbe\u4e3a 0\uff0c\u914d\u5408\u57fa\u7840\u6001\u7684 2px\uff0c\u5b9e\u73b0\u76f8\u5bf9\u5347\u8d77\u6548\u679c */\n"
"    margin-top: 0px; \n"
"    /* \u518d\u6b21\u660e\u786e\u5706\u89d2\uff0c\u786e\u4fdd\u4e0d\u88ab\u9ed8\u8ba4\u6837\u5f0f\u8986\u76d6 */\n"
"    border-top-left-radius: 9px;\n"
"    border-top-right-radius: 9px;\n"
"}")
        self.english_tab = QWidget()
        self.english_tab.setObjectName(u"english_tab")
        self.verticalLayout_7 = QVBoxLayout(self.english_tab)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setSpacing(10)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setSpacing(8)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.english_keyword_label = QLabel(self.english_tab)
        self.english_keyword_label.setObjectName(u"english_keyword_label")
        self.english_keyword_label.setMinimumSize(QSize(43, 0))
        self.english_keyword_label.setMaximumSize(QSize(43, 30))
        font1 = QFont()
        font1.setPointSize(10)
        font1.setBold(True)
        font1.setHintingPreference(QFont.PreferNoHinting)
        self.english_keyword_label.setFont(font1)

        self.horizontalLayout_6.addWidget(self.english_keyword_label)

        self.english_keyword_combo = QComboBox(self.english_tab)
        self.english_keyword_combo.addItem("")
        self.english_keyword_combo.addItem("")
        self.english_keyword_combo.addItem("")
        self.english_keyword_combo.addItem("")
        self.english_keyword_combo.setObjectName(u"english_keyword_combo")
        self.english_keyword_combo.setMinimumSize(QSize(100, 30))
        self.english_keyword_combo.setMaximumSize(QSize(100, 30))
        self.english_keyword_combo.setFont(font)
        self.english_keyword_combo.setStyleSheet(u"/* 1. \u4e0b\u62c9\u6846\u4e3b\u4f53\uff08\u4fdd\u6301\u4f60\u539f\u6765\u7684\uff09 */\n"
"QComboBox {\n"
"    color: #333333;\n"
"    background-color: #F2F2F2;        \n"
"    border: 1px solid #B5B5B5;\n"
"    border-radius: 9px;\n"
"    padding: 1px 10px;\n"
"}\n"
"\n"
"/* \u60ac\u6d6e\u4e0e\u6fc0\u6d3b\u72b6\u6001 */\n"
"QComboBox:hover {\n"
"    border: 2px solid #7953B1;       \n"
"}\n"
"\n"
"/* 2. \u4e0b\u62c9\u5217\u8868\u5bb9\u5668 */\n"
"QComboBox QAbstractItemView {\n"
"    border: 1px solid #7953B1;\n"
"    border-radius: 9px;\n"
"    background-color: #F2F2F2;\n"
"    outline: 0px;  /* \u79fb\u9664\u865a\u7ebf\u6846 */\n"
"}\n"
"\n"
"/* 3. \u6bcf\u4e00\u4e2a\u9009\u9879\u7684\u6837\u5f0f */\n"
"QComboBox QAbstractItemView::item {\n"
"    color: black;\n"
"    height: 30px; /* \u589e\u52a0\u9ad8\u5ea6\uff0c\u5706\u89d2\u624d\u597d\u770b */\n"
"    padding-left: 10px;\n"
"}\n"
"\n"
"/* 4. \u9009\u4e2d\u9879\u7684\u6837\u5f0f */\n"
"QComboBox QAbstractItemView::item:selected {\n"
"    background-co"
                        "lor: #7953B1;\n"
"    color: white;\n"
"    /* \u5982\u679c\u60f3\u8ba9\u9009\u4e2d\u7684\u9ad8\u4eae\u5757\u4e5f\u6709\u5706\u89d2\uff0c\u53ef\u4ee5\u52a0\u4e0b\u9762\u8fd9\u53e5 */\n"
"    border-radius: 5px; \n"
"}\n"
"\n"
"/*\u79fb\u9664\u4e0b\u62c9\u7bad\u5934 */\n"
"QComboBox::drop-down {\n"
"    width: 0px;                         /* \u5c06\u4e0b\u62c9\u533a\u57df\u5bbd\u5ea6\u8bbe\u4e3a0 */\n"
"    border: none;                       /* \u79fb\u9664\u53ef\u80fd\u5b58\u5728\u7684\u5206\u5272\u7ebf */\n"
"}\n"
"QComboBox::down-arrow {\n"
"    image: none;                        /* \u660e\u786e\u4e0d\u663e\u793a\u4efb\u4f55\u56fe\u6807 */\n"
"}")

        self.horizontalLayout_6.addWidget(self.english_keyword_combo)

        self.english_keyword_edit = QLineEdit(self.english_tab)
        self.english_keyword_edit.setObjectName(u"english_keyword_edit")
        self.english_keyword_edit.setMinimumSize(QSize(130, 30))
        self.english_keyword_edit.setMaximumSize(QSize(500, 30))
        self.english_keyword_edit.setStyleSheet(u"border-radius: 7px;\n"
"padding-left: 5px;")

        self.horizontalLayout_6.addWidget(self.english_keyword_edit)

        self.english_lemma_label = QLabel(self.english_tab)
        self.english_lemma_label.setObjectName(u"english_lemma_label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.english_lemma_label.sizePolicy().hasHeightForWidth())
        self.english_lemma_label.setSizePolicy(sizePolicy1)
        self.english_lemma_label.setMinimumSize(QSize(43, 0))
        self.english_lemma_label.setMaximumSize(QSize(43, 30))
        self.english_lemma_label.setFont(font1)

        self.horizontalLayout_6.addWidget(self.english_lemma_label)

        self.english_lemma_display = QLabel(self.english_tab)
        self.english_lemma_display.setObjectName(u"english_lemma_display")
        self.english_lemma_display.setMinimumSize(QSize(200, 30))
        self.english_lemma_display.setMaximumSize(QSize(16777215, 30))
        self.english_lemma_display.setFont(font)
        self.english_lemma_display.setStyleSheet(u"/* \u9ed8\u8ba4\u6837\u5f0f (\u4f60\u7684\u57fa\u7840\u6837\u5f0f) */\n"
"QFrame {\n"
"    color: rgb(0, 0, 0);\n"
"    background-color: #f0f0f0;\n"
"    border: 2px solid #7953B1;\n"
"    border-radius: 9px;\n"
"    padding: 5px 15px;\n"
"}")
        self.english_lemma_display.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_6.addWidget(self.english_lemma_display)

        self.horizontalLayout_6.setStretch(2, 1)
        self.horizontalLayout_6.setStretch(4, 1)

        self.verticalLayout_4.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setSpacing(8)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.english_lemmalist_label = QLabel(self.english_tab)
        self.english_lemmalist_label.setObjectName(u"english_lemmalist_label")
        sizePolicy1.setHeightForWidth(self.english_lemmalist_label.sizePolicy().hasHeightForWidth())
        self.english_lemmalist_label.setSizePolicy(sizePolicy1)
        self.english_lemmalist_label.setMinimumSize(QSize(43, 0))
        self.english_lemmalist_label.setMaximumSize(QSize(43, 30))
        self.english_lemmalist_label.setFont(font1)

        self.horizontalLayout_8.addWidget(self.english_lemmalist_label)

        self.english_lemmalist_display = QLabel(self.english_tab)
        self.english_lemmalist_display.setObjectName(u"english_lemmalist_display")
        self.english_lemmalist_display.setMinimumSize(QSize(300, 70))
        self.english_lemmalist_display.setMaximumSize(QSize(16777215, 70))
        self.english_lemmalist_display.setFont(font)
        self.english_lemmalist_display.setStyleSheet(u"/* \u9ed8\u8ba4\u6837\u5f0f (\u4f60\u7684\u57fa\u7840\u6837\u5f0f) */\n"
"QFrame {\n"
"    color: rgb(0, 0, 0);\n"
"    background-color: #f0f0f0;\n"
"    border: 1px solid #7953B1;\n"
"    border-radius: 9px;\n"
"}")
        self.english_lemmalist_display.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)

        self.horizontalLayout_8.addWidget(self.english_lemmalist_display)


        self.verticalLayout_4.addLayout(self.horizontalLayout_8)


        self.verticalLayout_7.addLayout(self.verticalLayout_4)

        self.corpus_tab_widget.addTab(self.english_tab, "")
        self.korean_tab = QWidget()
        self.korean_tab.setObjectName(u"korean_tab")
        self.verticalLayout_3 = QVBoxLayout(self.korean_tab)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(8)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.korean_keyword_label = QLabel(self.korean_tab)
        self.korean_keyword_label.setObjectName(u"korean_keyword_label")
        self.korean_keyword_label.setMinimumSize(QSize(43, 0))
        self.korean_keyword_label.setMaximumSize(QSize(43, 30))
        self.korean_keyword_label.setFont(font1)

        self.horizontalLayout_3.addWidget(self.korean_keyword_label)

        self.korean_keyword_combo = QComboBox(self.korean_tab)
        self.korean_keyword_combo.addItem("")
        self.korean_keyword_combo.addItem("")
        self.korean_keyword_combo.setObjectName(u"korean_keyword_combo")
        self.korean_keyword_combo.setMinimumSize(QSize(100, 30))
        self.korean_keyword_combo.setMaximumSize(QSize(100, 30))
        self.korean_keyword_combo.setFont(font)
        self.korean_keyword_combo.setStyleSheet(u"/* 1. \u4e0b\u62c9\u6846\u4e3b\u4f53\uff08\u4fdd\u6301\u4f60\u539f\u6765\u7684\uff09 */\n"
"QComboBox {\n"
"    color: #333333;\n"
"    background-color: #F2F2F2;        \n"
"    border: 1px solid #B5B5B5;\n"
"    border-radius: 9px;\n"
"    padding: 1px 10px;\n"
"}\n"
"\n"
"/* \u60ac\u6d6e\u4e0e\u6fc0\u6d3b\u72b6\u6001 */\n"
"QComboBox:hover {\n"
"    border: 2px solid #7953B1;       \n"
"}\n"
"\n"
"/* 2. \u4e0b\u62c9\u5217\u8868\u5bb9\u5668 */\n"
"QComboBox QAbstractItemView {\n"
"    border: 1px solid #7953B1;\n"
"    border-radius: 9px;\n"
"    background-color: #F2F2F2;\n"
"    outline: 0px;  /* \u79fb\u9664\u865a\u7ebf\u6846 */\n"
"}\n"
"\n"
"/* 3. \u6bcf\u4e00\u4e2a\u9009\u9879\u7684\u6837\u5f0f */\n"
"QComboBox QAbstractItemView::item {\n"
"    color: black;\n"
"    height: 30px; /* \u589e\u52a0\u9ad8\u5ea6\uff0c\u5706\u89d2\u624d\u597d\u770b */\n"
"    padding-left: 10px;\n"
"}\n"
"\n"
"/* 4. \u9009\u4e2d\u9879\u7684\u6837\u5f0f */\n"
"QComboBox QAbstractItemView::item:selected {\n"
"    background-co"
                        "lor: #7953B1;\n"
"    color: white;\n"
"    /* \u5982\u679c\u60f3\u8ba9\u9009\u4e2d\u7684\u9ad8\u4eae\u5757\u4e5f\u6709\u5706\u89d2\uff0c\u53ef\u4ee5\u52a0\u4e0b\u9762\u8fd9\u53e5 */\n"
"    border-radius: 5px; \n"
"}\n"
"\n"
"/*\u79fb\u9664\u4e0b\u62c9\u7bad\u5934 */\n"
"QComboBox::drop-down {\n"
"    width: 0px;                         /* \u5c06\u4e0b\u62c9\u533a\u57df\u5bbd\u5ea6\u8bbe\u4e3a0 */\n"
"    border: none;                       /* \u79fb\u9664\u53ef\u80fd\u5b58\u5728\u7684\u5206\u5272\u7ebf */\n"
"}\n"
"QComboBox::down-arrow {\n"
"    image: none;                        /* \u660e\u786e\u4e0d\u663e\u793a\u4efb\u4f55\u56fe\u6807 */\n"
"}")

        self.horizontalLayout_3.addWidget(self.korean_keyword_combo)

        self.korean_keyword_edit = QLineEdit(self.korean_tab)
        self.korean_keyword_edit.setObjectName(u"korean_keyword_edit")
        self.korean_keyword_edit.setMinimumSize(QSize(130, 30))
        self.korean_keyword_edit.setMaximumSize(QSize(500, 30))
        self.korean_keyword_edit.setStyleSheet(u"border-radius: 7px;\n"
"padding-left: 5px;")

        self.horizontalLayout_3.addWidget(self.korean_keyword_edit)

        self.korean_lemma_label = QLabel(self.korean_tab)
        self.korean_lemma_label.setObjectName(u"korean_lemma_label")
        sizePolicy1.setHeightForWidth(self.korean_lemma_label.sizePolicy().hasHeightForWidth())
        self.korean_lemma_label.setSizePolicy(sizePolicy1)
        self.korean_lemma_label.setMinimumSize(QSize(43, 0))
        self.korean_lemma_label.setMaximumSize(QSize(43, 30))
        self.korean_lemma_label.setFont(font1)

        self.horizontalLayout_3.addWidget(self.korean_lemma_label)

        self.korean_lemma_display = QLabel(self.korean_tab)
        self.korean_lemma_display.setObjectName(u"korean_lemma_display")
        self.korean_lemma_display.setMinimumSize(QSize(200, 30))
        self.korean_lemma_display.setMaximumSize(QSize(16777215, 30))
        self.korean_lemma_display.setFont(font)
        self.korean_lemma_display.setStyleSheet(u"/* \u9ed8\u8ba4\u6837\u5f0f (\u4f60\u7684\u57fa\u7840\u6837\u5f0f) */\n"
"QFrame {\n"
"    color: rgb(0, 0, 0);\n"
"    background-color: #f0f0f0;\n"
"    border: 2px solid #7953B1;\n"
"    border-radius: 9px;\n"
"    padding: 5px 15px;\n"
"}")
        self.korean_lemma_display.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_3.addWidget(self.korean_lemma_display)

        self.horizontalLayout_3.setStretch(2, 1)
        self.horizontalLayout_3.setStretch(4, 1)

        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setSpacing(8)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.korean_lemmalist_label = QLabel(self.korean_tab)
        self.korean_lemmalist_label.setObjectName(u"korean_lemmalist_label")
        sizePolicy1.setHeightForWidth(self.korean_lemmalist_label.sizePolicy().hasHeightForWidth())
        self.korean_lemmalist_label.setSizePolicy(sizePolicy1)
        self.korean_lemmalist_label.setMinimumSize(QSize(43, 0))
        self.korean_lemmalist_label.setMaximumSize(QSize(43, 30))
        self.korean_lemmalist_label.setFont(font1)

        self.horizontalLayout_5.addWidget(self.korean_lemmalist_label)

        self.korean_lemmalist_display = QLabel(self.korean_tab)
        self.korean_lemmalist_display.setObjectName(u"korean_lemmalist_display")
        self.korean_lemmalist_display.setMinimumSize(QSize(300, 70))
        self.korean_lemmalist_display.setMaximumSize(QSize(16777215, 70))
        self.korean_lemmalist_display.setFont(font)
        self.korean_lemmalist_display.setStyleSheet(u"/* \u9ed8\u8ba4\u6837\u5f0f (\u4f60\u7684\u57fa\u7840\u6837\u5f0f) */\n"
"QFrame {\n"
"    color: rgb(0, 0, 0);\n"
"    background-color: #f0f0f0;\n"
"    border: 1px solid #7953B1;\n"
"    border-radius: 9px;\n"
"}")
        self.korean_lemmalist_display.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)

        self.horizontalLayout_5.addWidget(self.korean_lemmalist_display)


        self.verticalLayout.addLayout(self.horizontalLayout_5)


        self.verticalLayout_3.addLayout(self.verticalLayout)

        self.corpus_tab_widget.addTab(self.korean_tab, "")

        self.horizontalLayout.addWidget(self.corpus_tab_widget)

        self.gridLayout = QGridLayout()
        self.gridLayout.setSpacing(10)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(-1, 0, -1, -1)
        self.search_btn = QPushButton(self.centralwidget)
        self.search_btn.setObjectName(u"search_btn")
        self.search_btn.setMinimumSize(QSize(81, 40))
        self.search_btn.setMaximumSize(QSize(100, 100))
        self.search_btn.setFont(font)
        self.search_btn.setStyleSheet(u"/* \u6309\u94ae\u9ed8\u8ba4\u6837\u5f0f */\n"
"QPushButton {\n"
"    color: rgb(0, 0, 0);\n"
"    background-color:#00b8a9;\n"
"    border-radius: 9px;\n"
"    padding: 5px 15px;\n"
"    border: none;\n"
"}\n"
"\n"
"/* \u60ac\u6d6e\u7279\u6548\uff1a\u80cc\u666f\u989c\u8272\u53d8\u6d45\uff0c\u5e76\u589e\u52a0\u84dd\u8272\u8fb9\u6846\u611f */\n"
"QPushButton:hover {\n"
"    background-color: rgb(0, 214, 196); /* \u989c\u8272\u6bd4\u9ed8\u8ba4\u7a0d\u4eae */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    /* 1. \u5411\u4e0b\u63a8\u6587\u5b57 */\n"
"    padding-top: 5px; \n"
"    /* 2. \u540c\u65f6\u51cf\u5c11\u5e95\u90e8\uff0c\u786e\u4fdd\u5185\u90e8\u6709\u6548\u7a7a\u95f4\u9ad8\u5ea6\u4e0d\u53d8 */\n"
"    padding-bottom: 0px; \n"
"    /* 3. \u5f3a\u5236\u5185\u5bb9\u6c34\u5e73\u5782\u76f4\u5c45\u4e2d\uff0c\u9632\u6b62\u5bf9\u9f50\u65b9\u5f0f\u5e72\u6270 */\n"
"    text-align: center;\n"
"}")
        icon3 = QIcon()
        icon3.addFile(u"../icons/search.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.search_btn.setIcon(icon3)
        self.search_btn.setIconSize(QSize(28, 28))

        self.gridLayout.addWidget(self.search_btn, 2, 0, 1, 1)

        self.english_regex_check = QCheckBox(self.centralwidget)
        self.english_regex_check.setObjectName(u"english_regex_check")
        self.english_regex_check.setFont(font)

        self.gridLayout.addWidget(self.english_regex_check, 0, 0, 1, 1)

        self.stop_search_btn = QPushButton(self.centralwidget)
        self.stop_search_btn.setObjectName(u"stop_search_btn")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.stop_search_btn.sizePolicy().hasHeightForWidth())
        self.stop_search_btn.setSizePolicy(sizePolicy2)
        self.stop_search_btn.setMinimumSize(QSize(81, 40))
        self.stop_search_btn.setMaximumSize(QSize(100, 100))
        font2 = QFont()
        font2.setPointSize(12)
        font2.setWeight(QFont.DemiBold)
        font2.setKerning(True)
        font2.setHintingPreference(QFont.PreferNoHinting)
        self.stop_search_btn.setFont(font2)
        self.stop_search_btn.setStyleSheet(u"/* \u6309\u94ae\u9ed8\u8ba4\u6837\u5f0f */\n"
"QPushButton {\n"
"color: rgb(0, 0, 0);\n"
"background-color: #f6416c;\n"
"border-radius: 9px;\n"
"padding: 5px 15px;\n"
"border: none;\n"
"}\n"
"\n"
"/* \u60ac\u6d6e\u7279\u6548\uff1a\u80cc\u666f\u989c\u8272\u53d8\u6d45\uff0c\u5e76\u589e\u52a0\u84dd\u8272\u8fb9\u6846\u611f */\n"
"QPushButton:hover {\n"
"background-color: rgb(255, 102, 117);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    /* 1. \u5411\u4e0b\u63a8\u6587\u5b57 */\n"
"    padding-top: 5px; \n"
"    /* 2. \u540c\u65f6\u51cf\u5c11\u5e95\u90e8\uff0c\u786e\u4fdd\u5185\u90e8\u6709\u6548\u7a7a\u95f4\u9ad8\u5ea6\u4e0d\u53d8 */\n"
"    padding-bottom: 0px; \n"
"    /* 3. \u5f3a\u5236\u5185\u5bb9\u6c34\u5e73\u5782\u76f4\u5c45\u4e2d\uff0c\u9632\u6b62\u5bf9\u9f50\u65b9\u5f0f\u5e72\u6270 */\n"
"    text-align: center;\n"
"}")
        icon4 = QIcon()
        icon4.addFile(u"../../Qt_Widgets_Designer/Icons/stop.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.stop_search_btn.setIcon(icon4)
        self.stop_search_btn.setIconSize(QSize(28, 28))
        self.stop_search_btn.setCheckable(False)
        self.stop_search_btn.setChecked(False)

        self.gridLayout.addWidget(self.stop_search_btn, 2, 1, 1, 1)

        self.english_case_sensitive_check = QCheckBox(self.centralwidget)
        self.english_case_sensitive_check.setObjectName(u"english_case_sensitive_check")
        self.english_case_sensitive_check.setFont(font)

        self.gridLayout.addWidget(self.english_case_sensitive_check, 0, 1, 1, 1)

        self.history_btn = QPushButton(self.centralwidget)
        self.history_btn.setObjectName(u"history_btn")
        self.history_btn.setMinimumSize(QSize(81, 40))
        self.history_btn.setMaximumSize(QSize(100, 100))
        self.history_btn.setFont(font)
        self.history_btn.setStyleSheet(u"/* \u6309\u94ae\u9ed8\u8ba4\u6837\u5f0f */\n"
"QPushButton {\n"
"    color: rgb(0, 0, 0);\n"
"    background-color: #f8f3d4;\n"
"    border-radius: 9px;\n"
"    padding: 5px 15px;\n"
"    border: none;\n"
"}\n"
"\n"
"/* \u60ac\u6d6e\u7279\u6548\uff1a\u80cc\u666f\u989c\u8272\u53d8\u6d45\uff0c\u5e76\u589e\u52a0\u84dd\u8272\u8fb9\u6846\u611f */\n"
"QPushButton:hover {\n"
"    background-color: rgb(218, 213, 186); /* \u989c\u8272\u6bd4\u9ed8\u8ba4\u7a0d\u4eae */\n"
"}\n"
"\n"
"/* \u6309\u4e0b\u7279\u6548\uff1a\u70b9\u51fb\u65f6\u989c\u8272\u53d8\u6df1\uff0c\u4ea7\u751f\u7269\u7406\u538b\u4e0b\u7684\u9519\u89c9 */\n"
"QPushButton:pressed {\n"
"    padding-top: 8px;\n"
"}\n"
"\n"
"")
        icon5 = QIcon()
        icon5.addFile(u"../icons/history.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.history_btn.setIcon(icon5)
        self.history_btn.setIconSize(QSize(30, 30))

        self.gridLayout.addWidget(self.history_btn, 1, 0, 1, 1)

        self.lemmalist_btn = QPushButton(self.centralwidget)
        self.lemmalist_btn.setObjectName(u"lemmalist_btn")
        self.lemmalist_btn.setMinimumSize(QSize(81, 40))
        self.lemmalist_btn.setMaximumSize(QSize(100, 100))
        self.lemmalist_btn.setFont(font)
        self.lemmalist_btn.setStyleSheet(u"/* \u6309\u94ae\u9ed8\u8ba4\u6837\u5f0f */\n"
"QPushButton {\n"
"    color: rgb(0, 0, 0);\n"
"    background-color: #ffde7d;\n"
"    border-radius: 9px;\n"
"    padding: 5px 15px;\n"
"    border: none;\n"
"}\n"
"\n"
"/* \u60ac\u6d6e\u7279\u6548\uff1a\u80cc\u666f\u989c\u8272\u53d8\u6d45\uff0c\u5e76\u589e\u52a0\u84dd\u8272\u8fb9\u6846\u611f */\n"
"QPushButton:hover {\n"
"    background-color: rgb(255, 234, 152); /* \u989c\u8272\u6bd4\u9ed8\u8ba4\u7a0d\u4eae */\n"
"}\n"
"\n"
"/* \u6309\u4e0b\u7279\u6548\uff1a\u70b9\u51fb\u65f6\u989c\u8272\u53d8\u6df1\uff0c\u4ea7\u751f\u7269\u7406\u538b\u4e0b\u7684\u9519\u89c9 */\n"
"QPushButton:pressed {\n"
"    padding-top: 8px;\n"
"}\n"
"\n"
"\n"
"")
        icon6 = QIcon()
        icon6.addFile(u"../icons/start-up.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.lemmalist_btn.setIcon(icon6)
        self.lemmalist_btn.setIconSize(QSize(28, 28))

        self.gridLayout.addWidget(self.lemmalist_btn, 1, 1, 1, 1)

        self.gridLayout.setRowStretch(1, 1)
        self.gridLayout.setRowStretch(2, 1)

        self.horizontalLayout.addLayout(self.gridLayout)

        self.horizontalLayout.setStretch(0, 1)

        self.verticalLayout_2.addLayout(self.horizontalLayout)


        self.verticalLayout_5.addLayout(self.verticalLayout_2)

        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setSpacing(5)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.result_table = QTableWidget(self.centralwidget)
        if (self.result_table.columnCount() < 5):
            self.result_table.setColumnCount(5)
        __qtablewidgetitem = QTableWidgetItem()
        __qtablewidgetitem.setFont(font);
        self.result_table.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        __qtablewidgetitem1.setFont(font);
        self.result_table.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        __qtablewidgetitem2.setFont(font);
        self.result_table.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        __qtablewidgetitem3.setFont(font);
        self.result_table.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        __qtablewidgetitem4.setFont(font);
        self.result_table.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        self.result_table.setObjectName(u"result_table")
        self.result_table.setMinimumSize(QSize(450, 300))
        self.result_table.setStyleSheet(u"QPlainTextEdit {\n"
"    /* 1. \u5fc5\u987b\u6709\u8fb9\u6846\uff0c\u900f\u660e\u5373\u53ef */\n"
"    border: 1px solid transparent;\n"
"    border-radius: 10px;\n"
"    /* 1. \u663e\u5f0f\u58f0\u660e background\uff0c\u4e0d\u8981\u53ea\u7528 background-color */\n"
"    background: palette(base);\n"
"    /* 3. \u6838\u5fc3\uff1a\u5fc5\u987b\u5b9a\u4e49\u80cc\u666f\u8272\uff0c\u5706\u89d2\u624d\u80fd\u88ab\u201c\u586b\u5145\u201d\u51fa\u6765 */\n"
"    /* palette(base) \u4f1a\u81ea\u52a8\u8ddf\u968f\u4e3b\u9898\uff1a\u6d45\u8272\u65f6\u662f\u767d\u8272\uff0c\u6df1\u8272\u65f6\u662f\u6df1\u7070 */\n"
"    background-color: palette(base);\n"
"    \n"
"    /* 4. \u6587\u5b57\u989c\u8272\u4e5f\u8ddf\u968f\u4e3b\u9898 */\n"
"    color: palette(text);\n"
"    \n"
"    /* \u5efa\u8bae\u52a0\u70b9\u5185\u8fb9\u8ddd\uff0c\u5426\u5219\u5b57\u4f1a\u8d34\u5230\u5706\u89d2\u8fb9\u4e0a */\n"
"    padding: 3px;\n"
"}\n"
"\n"
"/* \u6df1\u8272\u6a21\u5f0f\u7ec6\u5316 */\n"
"[theme=\"dark\"] QMenu {\n"
"    color: #eeeeee;\n"
" "
                        "   background-color: #2b2b2b; /* \u4f7f\u7528\u6df1\u7070\u8272\u6bd4\u7eaf\u9ed1\u66f4\u5177\u9ad8\u7ea7\u611f */\n"
"    border-color: #555555; \n"
"    border-radius: 9px;\n"
"}\n"
"\n"
"/* \u6d45\u8272\u6a21\u5f0f\u7ec6\u5316 */\n"
"[theme=\"light\"] QMenu {\n"
"    color: #333333;\n"
"    background-color: #ffffff;\n"
"    border-color: #cccccc;\n"
"    border-radius: 9px;\n"
"}\n"
"\n"
"/* \u83dc\u5355\u9879\u6574\u4f53\u6837\u5f0f */\n"
"QMenu::item {\n"
"    padding: 6px 25px 6px 20px; /* \u589e\u52a0\u70b9\u51fb\u533a\u57df\u5927\u5c0f */\n"
"    border-radius: 3px;\n"
"}\n"
"\n"
"/* \u9009\u4e2d/\u60ac\u505c\u72b6\u6001 */\n"
"QMenu::item:selected {\n"
"    background-color: #FFC209; /* \u9ec4\u8272\u9009\u4e2d\u6548\u679c\uff0c\u66f4\u7b26\u5408\u4e3b\u6d41\u5ba1\u7f8e */\n"
"    color: black;              /* \u786e\u4fdd\u9009\u4e2d\u65f6\u6587\u5b57\u4f9d\u7136\u6e05\u6670 */\n"
"}\n"
"\n"
"/* \u7981\u7528\u72b6\u6001\uff08\u6bd4\u5982\u6ca1\u6709\u5185\u5bb9\u53ef\u7c98\u8d34\u65f6\uff09 */\n"
"Q"
                        "Menu::item:disabled {\n"
"    color: #888888;\n"
"}")
        self.result_table.setColumnCount(5)
        self.result_table.horizontalHeader().setVisible(True)
        self.result_table.verticalHeader().setVisible(False)

        self.verticalLayout_8.addWidget(self.result_table)

        self.ProgressBar = QProgressBar(self.centralwidget)
        self.ProgressBar.setObjectName(u"ProgressBar")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.ProgressBar.sizePolicy().hasHeightForWidth())
        self.ProgressBar.setSizePolicy(sizePolicy3)
        self.ProgressBar.setMinimumSize(QSize(400, 15))
        self.ProgressBar.setMaximumSize(QSize(16777215, 15))
        self.ProgressBar.setStyleSheet(u"/* \u8fdb\u5ea6\u6761\u80cc\u666f\u69fd */\n"
"QProgressBar {\n"
"    border: none;                /* \u53bb\u6389\u8fb9\u6846 */\n"
"    color: white;                /* \u767e\u5206\u6bd4\u6587\u5b57\u989c\u8272 */\n"
"    text-align: center;          /* \u6587\u5b57\u5c45\u4e2d */\n"
"    background: #e0e0e0;         /* \u69fd\u7684\u80cc\u666f\u8272 */\n"
"    border-radius: 5px;          /* \u5706\u89d2\u9ad8\u5ea6\u7684\u4e00\u534a\u901a\u5e38\u770b\u8d77\u6765\u5f88\u8212\u670d */\n"
"    height: 10px;                /* \u8fd9\u91cc\u7684 height \u4f1a\u5f71\u54cd\u69fd\u7684\u7c97\u7ec6 */\n"
"}\n"
"\n"
"/* \u5df2\u586b\u5145\u7684\u8fdb\u5ea6\u90e8\u5206 */\n"
"QProgressBar::chunk {\n"
"    background-color: #05B8CC;   /* \u8fdb\u5ea6\u6761\u989c\u8272\uff1a\u9752\u84dd\u8272 */\n"
"    border-radius: 5px;          /* \u8fdb\u5ea6\u6761\u7684\u5706\u89d2 */\n"
"}")
        self.ProgressBar.setValue(24)
        self.ProgressBar.setTextVisible(False)
        self.ProgressBar.setOrientation(Qt.Orientation.Horizontal)
        self.ProgressBar.setInvertedAppearance(False)

        self.verticalLayout_8.addWidget(self.ProgressBar)


        self.verticalLayout_5.addLayout(self.verticalLayout_8)

        self.verticalLayout_5.setStretch(1, 1)

        self.verticalLayout_6.addLayout(self.verticalLayout_5)

        CorpusSearchTool.setCentralWidget(self.centralwidget)
        self.menuBar = QMenuBar(CorpusSearchTool)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 1000, 22))
        self.menuTheme = QMenu(self.menuBar)
        self.menuTheme.setObjectName(u"menuTheme")
        CorpusSearchTool.setMenuBar(self.menuBar)
        self.status_bar = QStatusBar(CorpusSearchTool)
        self.status_bar.setObjectName(u"status_bar")
        CorpusSearchTool.setStatusBar(self.status_bar)

        self.menuBar.addAction(self.menuTheme.menuAction())
        self.menuTheme.addAction(self.actionlight)
        self.menuTheme.addAction(self.actionDark)

        self.retranslateUi(CorpusSearchTool)

        self.corpus_tab_widget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(CorpusSearchTool)
    # setupUi

    def retranslateUi(self, CorpusSearchTool):
        CorpusSearchTool.setWindowTitle(QCoreApplication.translate("CorpusSearchTool", u"\u5b57\u5e55\u8bed\u6599\u5e93\u68c0\u7d22\u5de5\u5177", None))
        self.actionlight.setText(QCoreApplication.translate("CorpusSearchTool", u"Light", None))
        self.actionDark.setText(QCoreApplication.translate("CorpusSearchTool", u"Dark", None))
        self.ReadPathLabel.setText(QCoreApplication.translate("CorpusSearchTool", u"\u8f93\u5165\u8def\u5f84:", None))
        self.ReadPathInput.setPlaceholderText(QCoreApplication.translate("CorpusSearchTool", u"\u9009\u62e9\u6587\u4ef6\u6216\u76ee\u5f55...", None))
#if QT_CONFIG(tooltip)
        self.ReadPathSet.setToolTip(QCoreApplication.translate("CorpusSearchTool", u"\u66f4\u65b0\u76ee\u5f55", None))
#endif // QT_CONFIG(tooltip)
        self.ReadPathSet.setText("")
#if QT_CONFIG(tooltip)
        self.ReadPathSelect.setToolTip(QCoreApplication.translate("CorpusSearchTool", u"\u6d4f\u89c8\u76ee\u5f55", None))
#endif // QT_CONFIG(tooltip)
        self.ReadPathSelect.setText("")
#if QT_CONFIG(tooltip)
        self.ReadPathOpen.setToolTip(QCoreApplication.translate("CorpusSearchTool", u"\u6253\u5f00\u76ee\u5f55", None))
#endif // QT_CONFIG(tooltip)
        self.ReadPathOpen.setText("")
        self.english_keyword_label.setText(QCoreApplication.translate("CorpusSearchTool", u"\u5173\u952e\u8bcd:", None))
        self.english_keyword_combo.setItemText(0, QCoreApplication.translate("CorpusSearchTool", u"\u540d\u8bcd & \u526f\u8bcd", None))
        self.english_keyword_combo.setItemText(1, QCoreApplication.translate("CorpusSearchTool", u"\u52a8\u8bcd", None))
        self.english_keyword_combo.setItemText(2, QCoreApplication.translate("CorpusSearchTool", u"\u5f62\u5bb9\u8bcd", None))
        self.english_keyword_combo.setItemText(3, QCoreApplication.translate("CorpusSearchTool", u"\u8bcd\u7ec4", None))

        self.english_keyword_edit.setPlaceholderText(QCoreApplication.translate("CorpusSearchTool", u"\u8f93\u5165\u641c\u7d22\u5173\u952e\u8bcd...", None))
        self.english_lemma_label.setText(QCoreApplication.translate("CorpusSearchTool", u"\u8bcd\u5178\u578b:", None))
        self.english_lemma_display.setText(QCoreApplication.translate("CorpusSearchTool", u"\u5173\u952e\u8bcd \u2192 \u8bcd\u5178\u578b", None))
        self.english_lemmalist_label.setText(QCoreApplication.translate("CorpusSearchTool", u"\u53d8\u4f53\u8868:", None))
        self.english_lemmalist_display.setText(QCoreApplication.translate("CorpusSearchTool", u"\u53d8\u4f53\u578b\u5217\u8868", None))
        self.corpus_tab_widget.setTabText(self.corpus_tab_widget.indexOf(self.english_tab), QCoreApplication.translate("CorpusSearchTool", u"\u82f1\u8bed\u8bed\u6599\u5e93", None))
        self.korean_keyword_label.setText(QCoreApplication.translate("CorpusSearchTool", u"\u5173\u952e\u8bcd:", None))
        self.korean_keyword_combo.setItemText(0, QCoreApplication.translate("CorpusSearchTool", u"\u5355\u8bcd", None))
        self.korean_keyword_combo.setItemText(1, QCoreApplication.translate("CorpusSearchTool", u"\u60ef\u7528\u8bed", None))

        self.korean_keyword_edit.setPlaceholderText(QCoreApplication.translate("CorpusSearchTool", u"\u8f93\u5165\u641c\u7d22\u5173\u952e\u8bcd...", None))
        self.korean_lemma_label.setText(QCoreApplication.translate("CorpusSearchTool", u"\u8bcd\u5178\u578b:", None))
        self.korean_lemma_display.setText(QCoreApplication.translate("CorpusSearchTool", u"\u5173\u952e\u8bcd \u2192 \u8bcd\u5178\u578b", None))
        self.korean_lemmalist_label.setText(QCoreApplication.translate("CorpusSearchTool", u"\u53d8\u4f53\u8868:", None))
        self.korean_lemmalist_display.setText(QCoreApplication.translate("CorpusSearchTool", u"\u53d8\u4f53\u578b\u5217\u8868", None))
        self.corpus_tab_widget.setTabText(self.corpus_tab_widget.indexOf(self.korean_tab), QCoreApplication.translate("CorpusSearchTool", u"\u97e9\u8bed\u8bed\u6599\u5e93", None))
#if QT_CONFIG(tooltip)
        self.search_btn.setToolTip(QCoreApplication.translate("CorpusSearchTool", u"\u5f00\u59cb\u641c\u7d22", None))
#endif // QT_CONFIG(tooltip)
        self.search_btn.setText("")
        self.english_regex_check.setText(QCoreApplication.translate("CorpusSearchTool", u"\u6b63\u5219\u8868\u8fbe\u5f0f", None))
#if QT_CONFIG(tooltip)
        self.stop_search_btn.setToolTip(QCoreApplication.translate("CorpusSearchTool", u"\u505c\u6b62\u641c\u7d22", None))
#endif // QT_CONFIG(tooltip)
        self.stop_search_btn.setText("")
        self.english_case_sensitive_check.setText(QCoreApplication.translate("CorpusSearchTool", u"\u533a\u5206\u5927\u5c0f\u5199", None))
#if QT_CONFIG(tooltip)
        self.history_btn.setToolTip(QCoreApplication.translate("CorpusSearchTool", u"\u641c\u7d22\u5386\u53f2", None))
#endif // QT_CONFIG(tooltip)
        self.history_btn.setText("")
#if QT_CONFIG(tooltip)
        self.lemmalist_btn.setToolTip(QCoreApplication.translate("CorpusSearchTool", u"\u751f\u6210\u53d8\u4f53\u8868", None))
#endif // QT_CONFIG(tooltip)
        self.lemmalist_btn.setText("")
        ___qtablewidgetitem = self.result_table.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("CorpusSearchTool", u"\u51fa\u5904", None));
        ___qtablewidgetitem1 = self.result_table.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("CorpusSearchTool", u"\u65f6\u95f4\u8f74", None));
        ___qtablewidgetitem2 = self.result_table.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("CorpusSearchTool", u"\u5bf9\u5e94\u53f0\u8bcd", None));
        ___qtablewidgetitem3 = self.result_table.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("CorpusSearchTool", u"\u884c\u53f7", None));
        ___qtablewidgetitem4 = self.result_table.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("CorpusSearchTool", u"\u6587\u4ef6\u540d", None));
        self.menuTheme.setTitle(QCoreApplication.translate("CorpusSearchTool", u"\u4e3b\u9898", None))
    # retranslateUi

