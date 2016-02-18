# -*- coding: utf-8 -*-

import logging
import random
from twisted.internet import defer
from client.cltremote import IRemote
import TeamCommunicationParams as pms
import TeamCommunicationTexts as texts_TC
from TeamCommunicationGui import GuiDecision, DAdditionnalquestions, \
    DQuestionDictator


logger = logging.getLogger("le2m")


class RemoteTC(IRemote):
    """
    Class remote, remote_ methods can be called by the server
    """
    def __init__(self, le2mclt):
        IRemote.__init__(self, le2mclt)
        self._le2mclt = le2mclt
        self._tcremoteplayer = None  # to send message
        self._ecran_decision = None
        self._payoffs = {}

    @property
    def tcremoteplayer(self):
        return self._tcremoteplayer

    def remote_configure(self, tcremoteplayer, params):
        logger.info(u"{} configure".format(self._le2mclt.uid))
        self._tcremoteplayer = tcremoteplayer
        for k, v in params.viewitems():
            setattr(pms, k, v)

    def remote_newperiod(self, period):
        logger.info(u"{} Period {}".format(self._le2mclt.uid, period))
        self.currentperiod = period
        if self.currentperiod == 1:
            del self.histo[1:]

    def remote_display_decision(self):
        """
        Display the decision screen
        :return: deferred
        """
        logger.info(u"{} Decision".format(self._le2mclt.uid))
        defered = defer.Deferred()
        if self._le2mclt.simulation:
            self._ecran_decision = GuiDecision(
                defered, True, self._le2mclt.screen, self)
            return defered
        else:
            self._ecran_decision = GuiDecision(
                defered, self._le2mclt.automatique, self._le2mclt.screen, self)
            self._ecran_decision.show()
            return defered

    @defer.inlineCallbacks
    def send_look(self, grille):
        logger.info(u"{} send_look grille {}".format(self._le2mclt.uid, grille))
        yield (self.tcremoteplayer.callRemote("send_look", grille))

    @defer.inlineCallbacks
    def send_try(self, grille, valeur):
        logger.info(u"{} send_try grille {} valeur {}".format(
            self._le2mclt.uid, grille, valeur))
        yield (self.tcremoteplayer.callRemote("send_try", grille, valeur))

    @defer.inlineCallbacks
    def send_message(self, message):
        logger.info(u"{} send_message {}".format(self._le2mclt.uid, message))
        yield (self.tcremoteplayer.callRemote("send_message", message))

    def remote_display_message(self, message):
        logger.info(u"{} display_message {}".format(self._le2mclt.uid, message))
        if self._le2mclt.simulation:
            pass
        else:
            self._ecran_decision.add_message(message)

    def remote_display_additionnalquestions(self, nbanswers):
        logger.info(u"{} display_additionnalquestions".format(
            self._le2mclt.uid))
        if self._le2mclt.simulation:
            rep = {"TC_confidence": random.randint(0, nbanswers),
                   "TC_jobsatisfaction": random.randint(0, 7)}
            if pms.TREATMENT == pms.get_treatment("avec_communication"):
                rep["TC_infosatisfaction"] = random.randint(0, 7)
            logger.info(u"{} renvoi {}".format(self._le2mclt.uid, rep))
            return rep
        else:
            defered = defer.Deferred()
            ecran_additionnalquestions = DAdditionnalquestions(
                defered, self._le2mclt.automatique, self._le2mclt.screen,
                nbanswers)
            ecran_additionnalquestions.show()
            return defered

    def remote_display_questionapresdictator(self):
        logger.info(u"{} remote_display_questionapresdictator".format(
            self._le2mclt.uid))
        if self._le2mclt.simulation:
            rep = random.randint(0, 10)
            logger.info(u"{} renvoi {}".format(self._le2mclt.uid, rep))
            return rep
        else:
            defered = defer.Deferred()
            screen = DQuestionDictator(
                defered, self._le2mclt.automatique, self._le2mclt.screen)
            screen.show()
            return defered

    def remote_display_summary(self, period_content):
        txt = texts_TC.get_text_summary(period_content)
        return self._le2mclt.get_remote("base").remote_display_information(txt)

    def remote_set_payoffs_TC(self, sequence, in_euros, in_ecus=None):
        self.remote_set_payoffs(in_euros, in_ecus)
        self._payoff_text = texts_TC.get_payoff_text(
            self._payoff_euros, self._payoff_ecus)
        self._payoffs[sequence] = {
            "euro": self.payoff_euros, "ecu": self.payoff_ecus,
            "txt": self.payoff_text}

    def remote_display_payoffs_TC(self, sequence):
        return self.le2mclt.get_remote("base").remote_display_information(
            self._payoffs[sequence]["txt"])
