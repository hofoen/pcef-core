# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'search_panel.ui'
#
# Created: Thu Jul  4 21:06:51 2013
#      by: PyQt4 UI code generator 4.10
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_SearchPanel(object):
    def setupUi(self, SearchPanel):
        SearchPanel.setObjectName(_fromUtf8("SearchPanel"))
        SearchPanel.resize(686, 81)
        SearchPanel.setStyleSheet(_fromUtf8(""))
        self.verticalLayout = QtGui.QVBoxLayout(SearchPanel)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.frame = QtGui.QFrame(SearchPanel)
        self.frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.frame)
        self.verticalLayout_2.setSpacing(9)
        self.verticalLayout_2.setMargin(9)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.widgetSearch = QtGui.QWidget(self.frame)
        self.widgetSearch.setObjectName(_fromUtf8("widgetSearch"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.widgetSearch)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.widgetSearch)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(0, 0))
        self.label.setMaximumSize(QtCore.QSize(18, 18))
        self.label.setText(_fromUtf8(""))
        self.label.setPixmap(QtGui.QPixmap(_fromUtf8(":/icons/rc/edit-find.png")))
        self.label.setScaledContents(True)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.lineEditSearch = QtGui.QLineEdit(self.widgetSearch)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditSearch.sizePolicy().hasHeightForWidth())
        self.lineEditSearch.setSizePolicy(sizePolicy)
        self.lineEditSearch.setMinimumSize(QtCore.QSize(200, 0))
        self.lineEditSearch.setObjectName(_fromUtf8("lineEditSearch"))
        self.horizontalLayout.addWidget(self.lineEditSearch)
        self.pushButtonUp = QtGui.QPushButton(self.widgetSearch)
        self.pushButtonUp.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/rc/go-up.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonUp.setIcon(icon)
        self.pushButtonUp.setObjectName(_fromUtf8("pushButtonUp"))
        self.horizontalLayout.addWidget(self.pushButtonUp)
        self.pushButtonDown = QtGui.QPushButton(self.widgetSearch)
        self.pushButtonDown.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/rc/go-down.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonDown.setIcon(icon1)
        self.pushButtonDown.setObjectName(_fromUtf8("pushButtonDown"))
        self.horizontalLayout.addWidget(self.pushButtonDown)
        self.checkBoxCase = QtGui.QCheckBox(self.widgetSearch)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        self.checkBoxCase.setPalette(palette)
        self.checkBoxCase.setStyleSheet(_fromUtf8(""))
        self.checkBoxCase.setObjectName(_fromUtf8("checkBoxCase"))
        self.horizontalLayout.addWidget(self.checkBoxCase)
        self.checkBoxWholeWords = QtGui.QCheckBox(self.widgetSearch)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        self.checkBoxWholeWords.setPalette(palette)
        self.checkBoxWholeWords.setObjectName(_fromUtf8("checkBoxWholeWords"))
        self.horizontalLayout.addWidget(self.checkBoxWholeWords)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.labelMatches = QtGui.QLabel(self.widgetSearch)
        self.labelMatches.setObjectName(_fromUtf8("labelMatches"))
        self.horizontalLayout.addWidget(self.labelMatches)
        self.pushButtonClose = QtGui.QPushButton(self.widgetSearch)
        self.pushButtonClose.setText(_fromUtf8(""))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/rc/close.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonClose.setIcon(icon2)
        self.pushButtonClose.setIconSize(QtCore.QSize(12, 12))
        self.pushButtonClose.setObjectName(_fromUtf8("pushButtonClose"))
        self.horizontalLayout.addWidget(self.pushButtonClose)
        self.verticalLayout_2.addWidget(self.widgetSearch)
        self.widgetReplace = QtGui.QWidget(self.frame)
        self.widgetReplace.setObjectName(_fromUtf8("widgetReplace"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.widgetReplace)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_2 = QtGui.QLabel(self.widgetReplace)
        self.label_2.setMaximumSize(QtCore.QSize(18, 18))
        self.label_2.setText(_fromUtf8(""))
        self.label_2.setPixmap(QtGui.QPixmap(_fromUtf8(":/icons/rc/edit-find-replace.png")))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)
        self.lineEditReplace = QtGui.QLineEdit(self.widgetReplace)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditReplace.sizePolicy().hasHeightForWidth())
        self.lineEditReplace.setSizePolicy(sizePolicy)
        self.lineEditReplace.setMinimumSize(QtCore.QSize(200, 0))
        self.lineEditReplace.setObjectName(_fromUtf8("lineEditReplace"))
        self.horizontalLayout_2.addWidget(self.lineEditReplace)
        self.pushButtonReplace = QtGui.QPushButton(self.widgetReplace)
        self.pushButtonReplace.setObjectName(_fromUtf8("pushButtonReplace"))
        self.horizontalLayout_2.addWidget(self.pushButtonReplace)
        self.pushButtonReplaceAll = QtGui.QPushButton(self.widgetReplace)
        self.pushButtonReplaceAll.setObjectName(_fromUtf8("pushButtonReplaceAll"))
        self.horizontalLayout_2.addWidget(self.pushButtonReplaceAll)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout_2.addWidget(self.widgetReplace)
        self.verticalLayout.addWidget(self.frame)
        self.actionSearch = QtGui.QAction(SearchPanel)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/rc/edit-find.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSearch.setIcon(icon3)
        self.actionSearch.setIconVisibleInMenu(True)
        self.actionSearch.setObjectName(_fromUtf8("actionSearch"))
        self.actionActionSearchAndReplace = QtGui.QAction(SearchPanel)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/rc/edit-find-replace.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionActionSearchAndReplace.setIcon(icon4)
        self.actionActionSearchAndReplace.setIconVisibleInMenu(True)
        self.actionActionSearchAndReplace.setObjectName(_fromUtf8("actionActionSearchAndReplace"))
        self.actionFindNext = QtGui.QAction(SearchPanel)
        self.actionFindNext.setIcon(icon1)
        self.actionFindNext.setIconVisibleInMenu(True)
        self.actionFindNext.setObjectName(_fromUtf8("actionFindNext"))
        self.actionFindPrevious = QtGui.QAction(SearchPanel)
        self.actionFindPrevious.setIcon(icon)
        self.actionFindPrevious.setIconVisibleInMenu(True)
        self.actionFindPrevious.setObjectName(_fromUtf8("actionFindPrevious"))

        self.retranslateUi(SearchPanel)
        QtCore.QMetaObject.connectSlotsByName(SearchPanel)
        SearchPanel.setTabOrder(self.lineEditSearch, self.lineEditReplace)
        SearchPanel.setTabOrder(self.lineEditReplace, self.pushButtonUp)
        SearchPanel.setTabOrder(self.pushButtonUp, self.pushButtonDown)
        SearchPanel.setTabOrder(self.pushButtonDown, self.checkBoxCase)
        SearchPanel.setTabOrder(self.checkBoxCase, self.checkBoxWholeWords)
        SearchPanel.setTabOrder(self.checkBoxWholeWords, self.pushButtonReplace)
        SearchPanel.setTabOrder(self.pushButtonReplace, self.pushButtonReplaceAll)
        SearchPanel.setTabOrder(self.pushButtonReplaceAll, self.pushButtonClose)

    def retranslateUi(self, SearchPanel):
        SearchPanel.setWindowTitle(_translate("SearchPanel", "Form", None))
        self.checkBoxCase.setText(_translate("SearchPanel", "Match case", None))
        self.checkBoxWholeWords.setText(_translate("SearchPanel", "Whole words", None))
        self.labelMatches.setText(_translate("SearchPanel", "0 matches", None))
        self.pushButtonReplace.setText(_translate("SearchPanel", "Replace", None))
        self.pushButtonReplaceAll.setText(_translate("SearchPanel", "Replace All", None))
        self.actionSearch.setText(_translate("SearchPanel", "Search", None))
        self.actionSearch.setToolTip(_translate("SearchPanel", "Show the search panel", None))
        self.actionSearch.setShortcut(_translate("SearchPanel", "Ctrl+F", None))
        self.actionActionSearchAndReplace.setText(_translate("SearchPanel", "Search and replace", None))
        self.actionActionSearchAndReplace.setToolTip(_translate("SearchPanel", "Show the search and replace panel", None))
        self.actionActionSearchAndReplace.setShortcut(_translate("SearchPanel", "Ctrl+R", None))
        self.actionFindNext.setText(_translate("SearchPanel", "Find next", None))
        self.actionFindNext.setToolTip(_translate("SearchPanel", "Find the next occurrence (downward)", None))
        self.actionFindNext.setShortcut(_translate("SearchPanel", "F3", None))
        self.actionFindPrevious.setText(_translate("SearchPanel", "Find previous", None))
        self.actionFindPrevious.setToolTip(_translate("SearchPanel", "Find previous occurrence (upward)", None))
        self.actionFindPrevious.setShortcut(_translate("SearchPanel", "Shift+F3", None))

import pcef_icons_rc
