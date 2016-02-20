# -*- coding: utf-8 -*-

from PyQt4 import QtGui
import logging
from collections import OrderedDict
from twisted.internet import defer
from util import utiltools, utili18n
import TeamCommunicationParams as pms
from TeamCommunicationGui import DConfiguration, Wlist, DGains
from time import strftime
from parts.Dictator import DictatorParams
from server.servgest import servgestgroups
from TeamCommunicationTexts import trans_TC
from util.utili18n import le2mtrans

logger = logging.getLogger("le2m.{}".format(__name__))


class Serveur(object):
    def __init__(self, le2mserv):
        self._le2mserv = le2mserv

        # creation of the menu (will be placed in the "part" menu on the
        # server screen
        actions = OrderedDict()
        actions[trans_TC(u"Configure")] = self._configure
        actions[trans_TC(u"Display the parameters")] = \
            lambda _: self._le2mserv.gestionnaire_graphique. \
            display_information2(
                utiltools.get_module_info(pms), trans_TC(u"Parameters"))
        actions[trans_TC(u"Start")] = lambda _: self._demarrer()
        actions[trans_TC(u"Form groups for the dictator game")] = self._prepare_dictator
        actions[trans_TC(u"Display the question after the dictator game")] = \
            lambda _: self._run_questionapresdictator()
        actions[trans_TC(u"Display payoffs")] = self._display_payoffs

        self._le2mserv.gestionnaire_graphique.add_topartmenu(
            u"Team Communication", actions)

        # ajout d'onglets ------------------------------------------------------
        self._onglet_looks = Wlist()
        self._onglet_essais = Wlist()
        self._onglet_messages = Wlist()
        self._le2mserv.gestionnaire_graphique.screen.ui.onglets.addTab(
            self._onglet_looks, trans_TC(u"Looks of grids"))
        self._le2mserv.gestionnaire_graphique.screen.ui.onglets.addTab(
            self._onglet_essais, trans_TC(u"Tries"))
        self._le2mserv.gestionnaire_graphique.screen.ui.onglets.addTab(
            self._onglet_messages, trans_TC(u"Messages"))

        # final question
        self._le2mserv.gestionnaire_graphique.screen.action_finalquest.\
            triggered.disconnect()
        self._le2mserv.gestionnaire_graphique.screen.action_finalquest.\
            triggered.connect(lambda _: self._display_questfinal())

        self._currentsequence = -1

    @property
    def onglet_looks(self):
        return self._onglet_looks

    @property
    def onglet_essais(self):
        return self._onglet_essais

    @property
    def onglet_messages(self):
        return self._onglet_messages

    def _configure(self):
        """
        To make changes in the parameters
        :return:
        """
        dconfig = DConfiguration(self._le2mserv.gestionnaire_graphique.screen)
        if dconfig.exec_():
            pms.TEMPS_PARTIE, pms.TREATMENT, pms.GRILLES = dconfig.get_config()
            self._le2mserv.gestionnaire_graphique.infoserv(
                [trans_TC(u"Part time: {}").format(pms.TEMPS_PARTIE),
                 trans_TC(u"Treatment: {}").format(pms.get_treatment(pms.TREATMENT)),
                 trans_TC(u"Grids: {}").format(len(pms.GRILLES))])

    @defer.inlineCallbacks
    def _demarrer(self):
        # checks of consistency ================================================
        if (divmod(len(self._le2mserv.gestionnaire_joueurs.get_players()),
                pms.TAILLE_GROUPES)[1] != 0):
            self._le2mserv.gestionnaire_graphique.display_error(
                trans_TC(u"Impossible to form groups of size {} with {} "
                    u"players").format(
                        pms.TAILLE_GROUPES,
                        self._le2mserv.gestionnaire_joueurs.nombre_joueurs))
            return
        if not pms.GRILLES:
            self._le2mserv.gestionnaire_graphique.display_error(
                trans_TC(u"Grids must be loaded before to start the part"))
            return

        # confirmation start
        confirmation = self._le2mserv.gestionnaire_graphique.\
            question(trans_TC(u"Start TeamCommunication?"))
        if not confirmation:
            return

        # init part ============================================================
        if not self._le2mserv.gestionnaire_experience.has_part(
                "TeamCommunication"):  # init part
            yield (self._le2mserv.gestionnaire_experience.init_part(
                "TeamCommunication", "PartieTC", "RemoteTC", pms))
            self._tous = self._le2mserv.gestionnaire_joueurs.get_players(
                'TeamCommunication')
        else:  # uniquement affichage
            self._le2mserv.gestionnaire_graphique.infoserv(None)
            self._le2mserv.gestionnaire_graphique.infoserv(
                "TeamCommunication".upper(), fg="white", bg="blue")
            self._le2mserv.gestionnaire_graphique.infoclt(None)
            self._le2mserv.gestionnaire_graphique.infoclt(
                "TeamCommunication".upper(), fg="white", bg="blue")
            self._le2mserv.gestionnaire_graphique.infoserv(
                utili18n.le2mtrans(u"Start time: {st}").format(
                    st=strftime("%H:%M:%S")))

        self._currentsequence += 1
        self._le2mserv.gestionnaire_graphique.infoserv(u"Sequence {}".format(
            self._currentsequence))
        self.onglet_looks.clear()
        self.onglet_essais.clear()
        self.onglet_messages.clear()

        # groups formation
        if self._currentsequence == 0:
            try:
                self._le2mserv.gestionnaire_groupes.former_groupes(
                    liste_joueurs=self._le2mserv.gestionnaire_joueurs.get_players(),
                    taille_groupes=pms.TAILLE_GROUPES, roundrobin=True)
            except ValueError as e:
                self._le2mserv.gestionnaire_graphique.display_error(e.message)
                return
        else:
            self._le2mserv.gestionnaire_groupes.roundrobinnext()
    
        # configuration of players and remote
        yield (self._le2mserv.gestionnaire_experience.run_step(
            u"Configure", self._tous, "configure", self, self._currentsequence))
        for j in self._tous:
            j.othergroupmembers = [
                k.get_part("TeamCommunication") for k in
                self._le2mserv.gestionnaire_groupes.get_autres_membres_groupe(
                    j.joueur)]

        # Start of repetitions =================================================
        for period in xrange(1 if pms.NOMBRE_PERIODES else 0,
                             pms.NOMBRE_PERIODES + 1):

            if self._le2mserv.gestionnaire_experience.stop_repetitions:
                break

            # init period
            self._le2mserv.gestionnaire_graphique.infoserv(
                [None, u"Period {}".format(period)])
            self._le2mserv.gestionnaire_graphique.infoclt(
                [None, u"Period {}".format(period)], fg="white", bg="gray")
            yield (self._le2mserv.gestionnaire_experience.run_func(
                self._tous, "newperiod", period))
            
            # decision
            yield (self._le2mserv.gestionnaire_experience.run_step(
                u"Decision", self._tous, "display_decision"))

            # computation of good answers in each group
            self._le2mserv.gestionnaire_graphique.infoserv(u"Good answers")
            for g, m in self._le2mserv.gestionnaire_groupes.get_groupes(
                    "TeamCommunication").viewitems():
                nbbonnesrep = sum([j.currentperiod.TC_goodanswers for j in m])
                for j in m:
                    j.currentperiod.TC_goodanswers_group = nbbonnesrep
                self._le2mserv.gestionnaire_graphique.infoserv(
                    u"G{}: {}".format(g.split("_")[2], nbbonnesrep))

            # period payoffs
            self._le2mserv.gestionnaire_experience.compute_periodpayoffs(
                "TeamCommunication")

            # questions about self confidence and satisfaction
            yield (self._le2mserv.gestionnaire_experience.run_step(
                trans_TC(u"Additionnal questions"), self._tous,
                "display_additionnalquestions"))
        
            # period summary
            yield (self._le2mserv.gestionnaire_experience.run_step(
                trans_TC(u"Summary"), self._tous, "display_summary"))
        
        # End of part ==========================================================
        yield (self._le2mserv.gestionnaire_experience.finalize_part(
            "TeamCommunication"))

    def _display_payoffs(self):
        if self._currentsequence >= 0:
            sequence, ok = QtGui.QInputDialog.getInt(
                self._le2mserv.gestionnaire_graphique.screen,
                trans_TC(u"Sequence choice"), trans_TC(u"Choose the sequence"),
                min=0, max=self._currentsequence, step=1, value=0)
            if ok:
                self._ecran_gains = DGains(self._le2mserv, sequence)
                self._ecran_gains.show()

        else:  # no sequence has been run
            return

    def _prepare_dictator(self):
        if self._currentsequence == -1:
            self._le2mserv.gestionnaire_graphique.display_error(
                u"Il faut au moins avoir lancé une séquence de "
                u"TeamCommunication")
            return
        if not self._le2mserv.gestionnaire_graphique.question(
                u"Préparer les groupes de Dictator?"):
            return

        DictatorParams.TAILLE_GROUPES = 0
        self._le2mserv.gestionnaire_groupes.roundrobinnext()
        groups = self._le2mserv.gestionnaire_groupes.get_groupes()
        newgroups = {}
        for v in groups.viewvalues():
            newgroups["{}_g_{}".format(
                self._le2mserv.nom_session, servgestgroups.compteur_groupe)] = \
                [v[0], v[1]]
            servgestgroups.compteur_groupe += 1
            newgroups["{}_g_{}".format(
                self._le2mserv.nom_session, servgestgroups.compteur_groupe)] = \
                [v[2], v[3]]
            servgestgroups.compteur_groupe += 1
        self._le2mserv.gestionnaire_groupes.set_groupes(newgroups)
        self._le2mserv.gestionnaire_groupes.set_attributes()
        self._le2mserv.gestionnaire_graphique.infoserv(
            self._le2mserv.gestionnaire_groupes.get_groupes_string())

    @defer.inlineCallbacks
    def _run_questionapresdictator(self):
        if self._currentsequence == -1 or \
                not self._le2mserv.gestionnaire_joueurs.get_players()[0].\
                        get_part("Dictator"):
            self._le2mserv.gestionnaire_graphique.display_error(
                u"Il faut avoir fait au moins une séquence de "
                u"TeamCommunication et la partie Dictator")
            return
        if not self._le2mserv.gestionnaire_graphique.question(
                u"Lancer la question d'après Dictator?"):
            return
        yield (self._le2mserv.gestionnaire_experience.run_step(
            step_name=u"Question après Dictator", step_participants=self._tous,
            step_function="display_questionapresdictator"))


    @defer.inlineCallbacks
    def _display_questfinal(self):
        if not self._le2mserv.gestionnaire_base.is_created():
            QtGui.QMessageBox.warning(
                self._le2mserv.gestionnaire_graphique.screen,
                le2mtrans(u"Warning"),
                le2mtrans(u"There is no database yet. You first need to "
                          u"load at least one part."))
            return
        if not hasattr(self, "_tous"):
            QtGui.QMessageBox.warning(
                self._le2mserv.gestionnaire_graphique.screen,
                le2mtrans(u"Warning"),
                trans_TC(u"TeamCommunication has to be run before to "
                         u"start this questionnaire"))
            return

        confirmation = QtGui.QMessageBox.question(
            self._le2mserv.gestionnaire_graphique.screen,
            le2mtrans(u"Confirmation"),
            le2mtrans(u"Start the final questionnaire?"),
            QtGui.QMessageBox.Cancel | QtGui.QMessageBox.Ok)
        if confirmation != QtGui.QMessageBox.Ok:
            return

        yield (self._le2mserv.gestionnaire_experience.run_step(
            trans_TC(u"Final questionnaire"), self._tous,
            "display_questfinal"))
