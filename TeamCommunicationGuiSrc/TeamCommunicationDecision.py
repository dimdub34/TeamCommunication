# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TeamCommunicationDecision.ui'
#
# Created: Mon Nov  2 09:41:57 2015
#      by: PyQt4 UI code generator 4.10.4
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(1164, 556)
        Dialog.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.verticalLayout_3 = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.textEdit_explication = QtGui.QTextEdit(Dialog)
        self.textEdit_explication.setMinimumSize(QtCore.QSize(400, 0))
        self.textEdit_explication.setMaximumSize(QtCore.QSize(16777215, 100))
        self.textEdit_explication.setObjectName(_fromUtf8("textEdit_explication"))
        self.horizontalLayout_2.addWidget(self.textEdit_explication)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_9 = QtGui.QHBoxLayout()
        self.horizontalLayout_9.setObjectName(_fromUtf8("horizontalLayout_9"))
        self.widget_timer = QtGui.QWidget(Dialog)
        self.widget_timer.setObjectName(_fromUtf8("widget_timer"))
        self.horizontalLayout_8 = QtGui.QHBoxLayout(self.widget_timer)
        self.horizontalLayout_8.setMargin(0)
        self.horizontalLayout_8.setObjectName(_fromUtf8("horizontalLayout_8"))
        self.label_timer_2 = QtGui.QLabel(self.widget_timer)
        self.label_timer_2.setObjectName(_fromUtf8("label_timer_2"))
        self.horizontalLayout_8.addWidget(self.label_timer_2)
        self.label_timer = QtGui.QLabel(self.widget_timer)
        self.label_timer.setObjectName(_fromUtf8("label_timer"))
        self.horizontalLayout_8.addWidget(self.label_timer)
        self.horizontalLayout_9.addWidget(self.widget_timer)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem2)
        self.verticalLayout_3.addLayout(self.horizontalLayout_9)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem3)
        self.widget_grilles = QtGui.QWidget(Dialog)
        self.widget_grilles.setMinimumSize(QtCore.QSize(0, 0))
        self.widget_grilles.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.widget_grilles.setObjectName(_fromUtf8("widget_grilles"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.widget_grilles)
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setMargin(5)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem4 = QtGui.QSpacerItem(171, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem4)
        self.gridLayout_grilles = QtGui.QGridLayout()
        self.gridLayout_grilles.setSizeConstraint(QtGui.QLayout.SetNoConstraint)
        self.gridLayout_grilles.setMargin(5)
        self.gridLayout_grilles.setSpacing(0)
        self.gridLayout_grilles.setObjectName(_fromUtf8("gridLayout_grilles"))
        self.horizontalLayout.addLayout(self.gridLayout_grilles)
        spacerItem5 = QtGui.QSpacerItem(171, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem5)
        self.horizontalLayout_4.addWidget(self.widget_grilles)
        spacerItem6 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem6)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        spacerItem7 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem7)
        self.widget_grille = QtGui.QWidget(Dialog)
        self.widget_grille.setMinimumSize(QtCore.QSize(500, 350))
        self.widget_grille.setMaximumSize(QtCore.QSize(500, 350))
        self.widget_grille.setObjectName(_fromUtf8("widget_grille"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.widget_grille)
        self.horizontalLayout_3.setMargin(0)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        spacerItem8 = QtGui.QSpacerItem(199, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem8)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.label_grille = QtGui.QLabel(self.widget_grille)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_grille.setFont(font)
        self.label_grille.setObjectName(_fromUtf8("label_grille"))
        self.verticalLayout_2.addWidget(self.label_grille)
        spacerItem9 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem9)
        self.horizontalLayout_3.addLayout(self.verticalLayout_2)
        spacerItem10 = QtGui.QSpacerItem(199, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem10)
        self.horizontalLayout_7.addWidget(self.widget_grille)
        spacerItem11 = QtGui.QSpacerItem(40, 40, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem11)
        self.widget_communication = QtGui.QWidget(Dialog)
        self.widget_communication.setMinimumSize(QtCore.QSize(500, 350))
        self.widget_communication.setMaximumSize(QtCore.QSize(500, 350))
        self.widget_communication.setObjectName(_fromUtf8("widget_communication"))
        self.verticalLayout = QtGui.QVBoxLayout(self.widget_communication)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.listWidget_communication = QtGui.QListWidget(self.widget_communication)
        self.listWidget_communication.setObjectName(_fromUtf8("listWidget_communication"))
        self.verticalLayout.addWidget(self.listWidget_communication)
        self.textEdit_ecriture = QtGui.QTextEdit(self.widget_communication)
        self.textEdit_ecriture.setMinimumSize(QtCore.QSize(300, 0))
        self.textEdit_ecriture.setMaximumSize(QtCore.QSize(16777215, 50))
        self.textEdit_ecriture.setObjectName(_fromUtf8("textEdit_ecriture"))
        self.verticalLayout.addWidget(self.textEdit_ecriture)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        spacerItem12 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem12)
        self.pushButton_send = QtGui.QPushButton(self.widget_communication)
        self.pushButton_send.setObjectName(_fromUtf8("pushButton_send"))
        self.horizontalLayout_6.addWidget(self.pushButton_send)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        spacerItem13 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem13)
        self.horizontalLayout_7.addWidget(self.widget_communication)
        spacerItem14 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem14)
        self.verticalLayout_3.addLayout(self.horizontalLayout_7)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.textEdit_explication.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Texte explication</p></body></html>", None))
        self.label_timer_2.setText(_translate("Dialog", "Temps restant", None))
        self.label_timer.setText(_translate("Dialog", "TextLabel", None))
        self.label_grille.setText(_translate("Dialog", "TextLabel", None))
        self.pushButton_send.setText(_translate("Dialog", "Envoyer", None))

