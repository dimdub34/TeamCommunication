# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
import logging
import random
import datetime
import pickle
from util.utili18n import le2mtrans
from client.cltgui.cltguiwidgets import WExplication, WCompterebours, WChat, \
    WSpinbox, WSlider, WCombo, WLabel
import TeamCommunicationParams as pms
import TeamCommunicationTexts as texts_TC
from TeamCommunicationGuiSrc import TeamCommunicationConfiguration, \
    TeamCommunicationWlist, TeamCommunicationCellule, TC_widGrilles, \
    TC_widDisplayer
from util.utiltools import get_pluriel
from server.servgui.servguidialogs import GuiPayoffs
from twisted.internet import defer
from TeamCommunicationTexts import trans_TC
from client.cltgui.cltguidialogs import DQuestFinal

logger = logging.getLogger("le2m")


def _get_html(numero, grille):
    html = "<p>" + trans_TC("Grid") + " {}<br />".format(numero)
    html += "<table style='width: 150px;'>"
    for l in grille:
        html += "<tr>"
        for c in l:
            html += "<td style='width: 15px;'>{}</td>".format(c)
        html += "</tr>"
    html += "</table>"
    return html


class WCell(QtGui.QWidget):

    edit_end = QtCore.pyqtSignal()

    def __init__(self, numero, displayer, tcremote):
        super(WCell, self).__init__()
        self.ui = TeamCommunicationCellule.Ui_Form()
        self.ui.setupUi(self)

        self._numero = numero
        self._displayer = displayer
        self._tcremote = tcremote

        self.ui.pushButton.setText("{}".format(numero))
        self.ui.pushButton.setFixedSize(45, 25)
        self.ui.pushButton.setStyleSheet(
            'QPushButton {border: 1px ridge gray;}')
        self.ui.spinBox.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.ui.spinBox.setFixedSize(45, 25)

        self.ui.pushButton.clicked.connect(lambda _: self._displayer.setText(
            _get_html(self._numero, pms.GRILLES[self._numero]["grille"])))
        self.ui.pushButton.clicked.connect(lambda _: self._send_look())
        self.ui.spinBox.valueChanged.connect(lambda _: self._send_try())

        self.setFixedSize(55, 75)

    def set_value(self, val):
        """
        Used in automatic and simulation modes
        :param val:
        :return:
        """
        self.ui.spinBox.setValue(val)

    @defer.inlineCallbacks
    def _send_look(self):
        try:
            yield (self._tcremote.send_look(self._numero))
        except Exception as e:
            logger.error(e.message)
        defer.returnValue(None)

    @defer.inlineCallbacks
    def _send_try(self):
        try:
            yield (self._tcremote.send_try(
                self._numero, self.ui.spinBox.value()))
        except Exception as e:
            logger.error(e.message)
        defer.returnValue(None)


class WGrilles(QtGui.QWidget):
    def __init__(self, parent, displayer, tcremote):
        super(WGrilles, self).__init__(parent)
        self.ui = TC_widGrilles.Ui_Form()
        self.ui.setupUi(self)

        for i in range(4):
            for j in range(25):
                num = 25 * i + j
                setattr(self, "grille_{}".format(num),
                        WCell(numero=num, displayer=displayer,
                              tcremote=tcremote))
                self.ui.gridLayout.addWidget(
                    getattr(self, "grille_{}".format(num)), i, j)

    def set_value(self, grille, value):
        getattr(self, "grille_{}".format(grille)).set_value(value)

    def get_values(self):
        values = {}
        for i in range(100):
            values[i] = getattr(
                self, "grille_{}".format(i)).ui.spinBox.value()
        return values


class WDisplayer(QtGui.QWidget):
    def __init__(self, parent):
        super(WDisplayer, self).__init__(parent)
        self.ui = TC_widDisplayer.Ui_Form()
        self.ui.setupUi(self)
        self.ui.label.setText(
            trans_TC(u"Click on a number\nto see the corresponding grid"))
        font_grille = QtGui.QFont()
        font_grille.setPointSize(14)
        font_grille.setBold(True)
        self.ui.label.setFont(font_grille)


class GuiDecision(QtGui.QDialog):
    def __init__(self, defered, automatique, parent, tcremote):
        super(GuiDecision, self).__init__(parent)

        self._defered = defered
        self._automatique = automatique
        self._tcremote = tcremote

        layout = QtGui.QVBoxLayout(self)

        self._widexplication = WExplication(
            text=texts_TC.get_text_explanation(), parent=self, size=(600, 50))
        layout.addWidget(self._widexplication)

        self._widcompterebours = WCompterebours(
            parent=self, temps=pms.TEMPS_PARTIE, actionfin=self._accept)
        layout.addWidget(self._widcompterebours)

        self._widdisplayer = WDisplayer(parent=self)
        self._widdisplayer.ui.label.setFixedSize(400, 300)
        self._widgrilles = WGrilles(
            parent=self, displayer=self._widdisplayer.ui.label,
            tcremote=self._tcremote)
        self._widgrilles.setFixedSize(1250, 350)
        layout.addWidget(self._widgrilles)

        hlayout = QtGui.QHBoxLayout()
        hlayout.addWidget(self._widdisplayer)
        hlayout.addSpacerItem(QtGui.QSpacerItem(
            20, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding))
        self.widchat = WChat(parent=self, action_send=self._send_message)
        self.widchat.setStyleSheet("border: 1px solid gray;")
        hlayout.addWidget(self.widchat)
        layout.addLayout(hlayout)

        if pms.TREATMENT == pms.get_treatment("sans_communication"):
            self.widchat.setVisible(False)

        if self._automatique:
            self._timer = QtCore.QTimer()
            self._timer.timeout.connect(self._handle_automatic)
            self._timer.start(random.randint(1000, 15000))

        self.setWindowTitle(u"Décisions")
        self.adjustSize()
        self.setFixedSize(self.size())

    @defer.inlineCallbacks
    def _handle_automatic(self):
        if not self._widcompterebours.compterebours.isRunning():
            self._timer.stop()
        grille = random.randint(0, 99)
        try:
            yield (self._tcremote.send_look(grille))
        except Exception as e:
            logger.error(e.message)
        if random.random() >= 0.25:  # on fait un essai
            if random.randint(0, 1):  # on donne la bonne réponse
                nbun = pms.GRILLES[grille]["count"]
            else:
                nbun = random.randint(0, 100)
            self._widgrilles.set_value(grille, nbun)
            try:
                yield (self._tcremote.send_try(grille, nbun))
            except Exception as e:
                logger.error(e.message)

        if pms.TREATMENT == pms.get_treatment("avec_communication"):
            if random.random() >= 0.60:  # on envoit un message
                self.widchat.write(u"Message automatique")
                self.widchat.ui.pushButton.click()
        defer.returnValue(None)

    def reject(self):
        pass

    def _accept(self):
        answers = self._widgrilles.get_values()
        logger.debug(u"Renvoi {}".format(answers))
        self._defered.callback(answers)
        self.accept()

    @defer.inlineCallbacks
    def _send_message(self, msg):
        try:
            yield (self._tcremote.send_message(msg))
        except Exception as e:
            logger.error(e.message)
        self.add_message(trans_TC(u"You:") + u" {}".format(msg))
        self.widchat.clear_writespace()
        defer.returnValue(None)

    def add_message(self, msg):
        self.widchat.add_text(msg)


class DConfiguration(QtGui.QDialog):
    def __init__(self, parent):
        super(DConfiguration, self).__init__(parent)
        self.ui = TeamCommunicationConfiguration.Ui_Dialog()
        self.ui.setupUi(self)

        treatmentscles = sorted(pms.TREATMENTS.viewkeys())
        self.ui.comboBox_communication.addItems(
            [pms.TREATMENTS[t].upper() for t in treatmentscles])
        self.ui.comboBox_communication.setCurrentIndex(pms.TREATMENT)
        self.ui.timeEdit_tempspartie.setTime(QtCore.QTime(
            pms.TEMPS_PARTIE.hour, pms.TEMPS_PARTIE.minute,
            pms.TEMPS_PARTIE.second))

        self.setWindowTitle(u"Configuration")
        self.setFixedSize(280, 150)

        self.ui.pushButton_grilles.clicked.connect(self._load_grilles)
        self.ui.buttonBox.accepted.connect(self._accept)
        self.ui.buttonBox.rejected.connect(self.reject)

    def _accept(self):
        self._communication = self.ui.comboBox_communication.currentIndex()
        tpspart = self.ui.timeEdit_tempspartie.time()
        self._tempspartie = datetime.time(
            tpspart.hour(), tpspart.minute(), tpspart.second())
        if not self._tempspartie:
            QtGui.QMessageBox.critical(
                self, u"Attention", u"Il faut un temps de partie positif")
            return
        if not hasattr(self, "_grilles"):
            QtGui.QMessageBox.critical(
                self, u"Attention", u"Il faut charger les grilles")
            return

    def _load_grilles(self):
        fichier = str(QtGui.QFileDialog.getOpenFileName(
            self, u"Choisir le fichier de grilles", "",
            u"Fichier pickle (*.pck)"))
        with open(fichier, "rb") as f:
            self._grilles = pickle.load(f)
            self.ui.label_grilles_nb.setText(
                get_pluriel(len(self._grilles), u"grille"))
        logger.info(u"Grilles loaded")

    def get_config(self):
        return self._tempspartie, self._communication, self._grilles


class Wlist(QtGui.QWidget):
    def __init__(self):
        super(Wlist, self).__init__()
        self.ui = TeamCommunicationWlist.Ui_Form()
        self.ui.setupUi(self)

    def clear(self):
        self.ui.listWidget.clear()

    def add(self, texte):
        txt = texte or u""
        self.ui.listWidget.addItem(txt)


class DGains(GuiPayoffs):
    def __init__(self, le2mserver, sequence):

        self._le2mserv = le2mserver
        self._sequence = sequence
        self._players = self._le2mserv.gestionnaire_joueurs.get_players(
            "TeamCommunication")
        self._gains = {}
        for j in self._players:
            self._gains[j.joueur] = j.sequences[sequence]["gain_euros"]
        gains_txt = [[str(k), u"{:.2f}".format(v)] for k, v in
                     sorted(self._gains.viewitems())]

        GuiPayoffs.__init__(self, le2mserver, "TeamCommunication", gains_txt)
        self.ui.pushButton_afficher.clicked.disconnect()
        self.ui.pushButton_afficher.clicked.connect(
            lambda _: self._display_onremotes2())

    @defer.inlineCallbacks
    def _display_onremotes2(self):
        confirm = self._le2mserv.gestionnaire_graphique.question(
            trans_TC(u"Display payoff on remotes' screen?"))
        if not confirm:
            return
        self._le2mserv.gestionnaire_graphique.set_waitmode(self._players)
        yield (self._le2mserv.gestionnaire_experience.run_func(
            self._players, "display_payoffs", self._sequence))

    def _addto_finalpayoffs(self):
        if not self._gains:
            return
        for k, v in self._gains.viewitems():
            k.get_part("base").paiementFinal += float(v)
        self._le2mserv.gestionnaire_base.enregistrer()
        self._le2mserv.gestionnaire_graphique.infoserv(
            trans_TC(u"TC payoffs added to final payoffs"), fg="red")


class DAdditionnalquestions(QtGui.QDialog):
    def __init__(self, defered, automatique, parent, nbanswers):
        super(DAdditionnalquestions, self).__init__(parent)

        self._defered = defered
        self._automatique = automatique
        self._nbanswers = nbanswers

        layout = QtGui.QVBoxLayout(self)

        self._widanswers = WSpinbox(
            label=texts_TC.get_text_reponses(nbanswers),
            minimum=0, maximum=nbanswers, automatique=self._automatique,
            parent=self)
        layout.addWidget(self._widanswers)

        if pms.TREATMENT == pms.get_treatment("avec_communication"):
            self._widinfosatisfaction = WSlider(
                label=texts_TC.get_text_infosatisfaction(),
                minimum=1, maximum=7, automatique=self._automatique,
                parent=self)
            layout.addWidget(self._widinfosatisfaction)

        self._widjobsatisfaction = WSlider(
            label=texts_TC.get_text_jobsatisfaction(),
            minimum=1, maximum=7, automatique=self._automatique,
            parent=self)
        layout.addWidget(self._widjobsatisfaction)

        buttons = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok)
        buttons.accepted.connect(self._accept)
        layout.addWidget(buttons)

        if self._automatique:
            self._timer = QtCore.QTimer()
            self._timer.timeout.connect(
                buttons.button(QtGui.QDialogButtonBox.Ok).click)
            self._timer.start(7000)

        self.setWindowTitle(trans_TC(u"Additionnal questions"))
        self.adjustSize()
        self.setFixedSize(self.size())

    def reject(self):
        pass

    def _accept(self):
        try:
            self._timer.stop()
        except AttributeError:
            pass
        rep = {"TC_confidence": self._widanswers.get_value(),
               "TC_jobsatisfaction": self._widjobsatisfaction.get_value()}
        if pms.TREATMENT == pms.get_treatment("avec_communication"):
            rep["TC_infosatisfaction"] = self._widinfosatisfaction.get_value()
        if not self._automatique:
            confirm = QtGui.QMessageBox.question(
                self, u"Confirmation", trans_TC(u"Do you confirm your answers?"),
                QtGui.QMessageBox.No | QtGui.QMessageBox.Yes)
            if confirm != QtGui.QMessageBox.Yes:
                return
        logger.info(u"Renvoi {}".format(rep))
        self.accept()
        self._defered.callback(rep)


class DQuestionDictator(QtGui.QDialog):
    def __init__(self, defered, automatique, parent):
        super(DQuestionDictator, self).__init__(parent)

        self._defered = defered
        self._automatique = automatique

        layout = QtGui.QVBoxLayout(self)

        self._widPrediction = WSpinbox(
            label=texts_TC.get_text_predictiondictator(), minimum=0, maximum=10,
            automatique=self._automatique, parent=self)
        layout.addWidget(self._widPrediction)

        buttons = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok)
        buttons.accepted.connect(self._accept)
        layout.addWidget(buttons)

        if self._automatique:
            self._timer = QtCore.QTimer()
            self._timer.timeout.connect(
                buttons.button(QtGui.QDialogButtonBox.Ok).click)
            self._timer.start(7000)

        self.setWindowTitle(trans_TC(u"Prediction"))
        self.adjustSize()
        self.setFixedSize(self.size())

    def reject(self):
        pass

    def _accept(self):
        try:
            self._timer.stop()
        except AttributeError:
            pass

        if not self._automatique:
            confirm = QtGui.QMessageBox.question(
                self, u"Confirmation", trans_TC(u"Do you confirm your choice?"),
                QtGui.QMessageBox.No | QtGui.QMessageBox.Yes)
            if confirm != QtGui.QMessageBox.Yes:
                return
        dec = self._widPrediction.get_value()
        logger.info(u"Send back {}".format(dec))
        self._defered.callback(dec)
        self.accept()


class DQuestFinalTC(DQuestFinal):
    def __init__(self, defered, automatique, parent):
        DQuestFinal.__init__(self, defered, automatique, parent)

        self._religion_place.setVisible(False)
        self._religion_place.ui.comboBox.setCurrentIndex(1)
        self._religion_name.setVisible(False)
        self._religion_name.ui.comboBox.setCurrentIndex(1)
        self._religion_belief.setVisible(False)
        self._religion_belief.ui.comboBox.setCurrentIndex(1)

        residence = [v for k, v in sorted(texts_TC.COUNTRY_RESIDENCE.viewitems())]
        residence.insert(0, le2mtrans(u"Choose"))
        residence.append(le2mtrans(u"Not in the list above"))
        self._residence = WCombo(
            parent=self, automatique=self._automatique,
            label=trans_TC(u"Country of residence"), items=residence)
        self._gridlayout.addWidget(self._residence, 0, 2)

        # language skills
        skills = [v for k, v in sorted(texts_TC.LANGUAGE_SKILLS.viewitems())]
        skills.insert(0, le2mtrans(u"Choose"))

        # luxembourgish
        self._luxembourgish_speak = WCombo(
            parent=self, automatique=self._automatique,
            label=u"<strong>" + trans_TC(u"Luxembourgish") + u"</strong>  " +
                  trans_TC(u"Speak"), items=skills)
        self._gridlayout.addWidget(self._luxembourgish_speak, 7, 0)
        self._luxembourgish_understrand = WCombo(
            parent=self, automatique=self._automatique,
            label=trans_TC(u"Understand"), items=skills)
        self._gridlayout.addWidget(self._luxembourgish_understrand, 7, 1)
        self._luxembourgish_read = WCombo(
            parent=self, automatique=self._automatique,
            label=trans_TC(u"Read"), items=skills)
        self._gridlayout.addWidget(self._luxembourgish_read, 7, 2)
        self._luxembourgish_write = WCombo(
            parent=self, automatique=self._automatique,
            label=trans_TC(u"Write"), items=skills)
        self._gridlayout.addWidget(self._luxembourgish_write, 7, 3)

        # french
        self._french_speak = WCombo(
            parent=self, automatique=self._automatique,
            label=u"<strong>" + trans_TC(u"French") + u"</strong>  " +
                  trans_TC(u"Speak"), items=skills)
        self._gridlayout.addWidget(self._french_speak, 8, 0)
        self._french_understrand = WCombo(
            parent=self, automatique=self._automatique,
            label=trans_TC(u"Understand"), items=skills)
        self._gridlayout.addWidget(self._french_understrand, 8, 1)
        self._french_read = WCombo(
            parent=self, automatique=self._automatique,
            label=trans_TC(u"Read"), items=skills)
        self._gridlayout.addWidget(self._french_read, 8, 2)
        self._french_write = WCombo(
            parent=self, automatique=self._automatique,
            label=trans_TC(u"Write"), items=skills)
        self._gridlayout.addWidget(self._french_write, 8, 3)

        # german
        self._german_speak = WCombo(
            parent=self, automatique=self._automatique,
            label=u"<strong>" + trans_TC(u"German") + u"</strong>  " +
                  trans_TC(u"Speak"), items=skills)
        self._gridlayout.addWidget(self._german_speak, 9, 0)
        self._german_understrand = WCombo(
            parent=self, automatique=self._automatique,
            label=trans_TC(u"Understand"), items=skills)
        self._gridlayout.addWidget(self._german_understrand, 9, 1)
        self._german_read = WCombo(
            parent=self, automatique=self._automatique,
            label=trans_TC(u"Read"), items=skills)
        self._gridlayout.addWidget(self._german_read, 9, 2)
        self._german_write = WCombo(
            parent=self, automatique=self._automatique,
            label=trans_TC(u"Write"), items=skills)
        self._gridlayout.addWidget(self._german_write, 9, 3)

        # english
        self._english_speak = WCombo(
            parent=self, automatique=self._automatique,
            label=u"<strong>" + trans_TC(u"English") + u"</strong>  " +
                  trans_TC(u"Speak"), items=skills)
        self._gridlayout.addWidget(self._english_speak, 10, 0)
        self._english_understrand = WCombo(
            parent=self, automatique=self._automatique,
            label=trans_TC(u"Understand"), items=skills)
        self._gridlayout.addWidget(self._english_understrand, 10, 1)
        self._english_read = WCombo(
            parent=self, automatique=self._automatique,
            label=trans_TC(u"Read"), items=skills)
        self._gridlayout.addWidget(self._english_read, 10, 2)
        self._english_write = WCombo(
            parent=self, automatique=self._automatique,
            label=trans_TC(u"Write"), items=skills)
        self._gridlayout.addWidget(self._english_write, 10, 3)

        self.adjustSize()
        self.setFixedSize(self.size())

    def _accept(self):
        try:
            self._timer_automatique.stop()
        except AttributeError:
            pass
        inputs = self._get_inputs()
        if type(inputs) is dict:

            try:

                inputs["residence"] = self._residence.get_currentindex()
                inputs["luxembourgish_speak"] = self._luxembourgish_speak.get_currentindex()
                inputs["luxembourgish_understand"] = self._luxembourgish_understrand.get_currentindex()
                inputs["luxembourgish_read"] = self._luxembourgish_read.get_currentindex()
                inputs["luxembourgish_write"] = self._luxembourgish_write.get_currentindex()
                inputs["french_speak"] = self._french_speak.get_currentindex()
                inputs["french_understand"] = self._french_understrand.get_currentindex()
                inputs["french_read"] = self._french_read.get_currentindex()
                inputs["french_write"] = self._french_write.get_currentindex()
                inputs["german_speak"] = self._german_speak.get_currentindex()
                inputs["german_understand"] = self._german_understrand.get_currentindex()
                inputs["german_read"] = self._german_read.get_currentindex()
                inputs["german_write"] = self._german_write.get_currentindex()
                inputs["english_speak"] = self._english_speak.get_currentindex()
                inputs["english_understand"] = self._english_understrand.get_currentindex()
                inputs["english_read"] = self._english_read.get_currentindex()
                inputs["english_write"] = self._english_write.get_currentindex()

            except ValueError:
                return QtGui.QMessageBox.warning(
                    self, le2mtrans(u"Warning"),
                    le2mtrans(u"You must answer to all the questions"))

            if not self._automatique:
                confirm = QtGui.QMessageBox.question(
                    self, le2mtrans(u"Confirmation"),
                    le2mtrans(u"Do you confirm your answers?"),
                    QtGui.QMessageBox.No | QtGui.QMessageBox.Yes)
                if confirm != QtGui.QMessageBox.Yes:
                    return

            logger.info(u"Send back: {}".format(inputs))
            self.accept()
            self._defered.callback(inputs)

        else:
            return
