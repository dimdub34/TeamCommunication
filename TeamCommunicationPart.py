# -*- coding: utf-8 -*-

from __future__ import division
import logging
from datetime import datetime
from twisted.internet import defer
from twisted.spread import pb
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, String
from server.servbase import Base
from server.servparties import Partie
import TeamCommunicationParams as pms
import TeamCommunicationTexts as texts
import util.utiltwisted as twu
from util.utiltools import get_module_attributes


logger = logging.getLogger("le2m")


class PartieTC(Partie, pb.Referenceable):
    __tablename__ = "partie_TeamCommunication"
    __mapper_args__ = {'polymorphic_identity': 'TeamCommunication'}
    partie_id = Column(Integer, ForeignKey('parties.id'), primary_key=True)
    repetitions = relationship('RepetitionsTC')
    events = relationship("EventsTC")

    def __init__(self, le2mserv, joueur):
        super(PartieTC, self).__init__("TeamCommunication", "TC")
        self._le2mserv = le2mserv
        self.joueur = joueur
        self._texte_recapitulatif = u""
        self._texte_final = u""
        self.TC_gain_ecus = 0
        self.TC_gain_euros = 0
        self._sequences = {}
        self._currentperiod = None
        self._currentsequence = 0
        self._tcserver = None
        self._othergroupmembers = None

    @property
    def sequences(self):
        return self._sequences

    @property
    def currentperiod(self):
        return self._currentperiod

    @property
    def othergroupmembers(self):
        return self._othergroupmembers

    @othergroupmembers.setter
    def othergroupmembers(self, others):
        self._othergroupmembers = others

    @defer.inlineCallbacks
    def configure(self, tcserver, currentsequence):
        """
        Allow to make changes in the part parameters
        :param tcserver:
        :param currentsequence:
        :return:
        """
        logger.debug(u"{} Configure".format(self.joueur))
        self._tcserver = tcserver
        self._currentsequence = currentsequence
        self.sequences[self._currentsequence] = {}
        yield (self.remote.callRemote(
            "configure", self, get_module_attributes(pms)))
        self.joueur.info(u"Ok")

    @defer.inlineCallbacks
    def newperiod(self, period):
        """
        Create a new period and inform the remote
        If this is the first period then empty the historic
        :param periode:
        :return:
        """
        logger.debug(u"{} New Period".format(self.joueur))
        self._currentperiod = RepetitionsTC(self._currentsequence, period)
        self.currentperiod.TC_group = self.joueur.groupe
        self._le2mserv.gestionnaire_base.ajouter(self.currentperiod)
        self.repetitions.append(self.currentperiod)
        yield (self.remote.callRemote("newperiod", period))
        logger.info(u"{} Ready for period {}".format(self.joueur, period))

    @defer.inlineCallbacks
    def display_decision(self):
        """
        Display the decision screen on the remote
        Get back the decision
        :return:
        """
        logger.debug(u"{} Decision".format(self.joueur))
        rep_grilles = yield (self.remote.callRemote("display_decision"))

        # nb answers and nb good answers
        nbanswers, goodrep = 0, 0
        for k, v in rep_grilles.iteritems():
            setattr(self.currentperiod, "TC_grille_{}".format(k), v)
            if v > 0:
                nbanswers += 1
                if v == pms.GRILLES[k]["count"]:
                    goodrep += 1
        self.currentperiod.TC_goodanswers = goodrep
        self.currentperiod.TC_nbanswers = nbanswers

        # stats about events
        currentevents = [e for e in self.events if
                         e.TC_sequence == self._currentsequence and
                         e.TC_period == self.currentperiod.TC_period]

        self.currentperiod.TC_nblooks = len(
            [i for i in currentevents if i.TC_eventType == pms.EVENT_LOOK])
        self.currentperiod.TC_nbtries = len(
            [i for i in currentevents if i.TC_eventType == pms.EVENT_TRY])
        messages = [m for m in currentevents if
                    m.TC_eventType == pms.EVENT_MESSAGE]
        self.currentperiod.TC_nbmsgsent = len(
            [m for m in messages if m.TC_sentorreceived == pms.MSG_ENVOYE])
        self.currentperiod.TC_nbmsgreceived = len(
            [m for m in messages if m.TC_sentorreceived == pms.MSG_RECU])

        # display of stats on client list
        self.joueur.info(u"NBA {} - GA {} - NBL {} - NBT {} - NBMS {} - "
                         u"NBMR {}".format(
            self.currentperiod.TC_nbanswers,
            self.currentperiod.TC_goodanswers,
            self.currentperiod.TC_nblooks,
            self.currentperiod.TC_nbtries,
            self.currentperiod.TC_nbmsgsent,
            self.currentperiod.TC_nbmsgreceived))
        self.joueur.remove_waitmode()

    def remote_send_look(self, numgrille):
        logger.debug(u"{} send_look {}".format(self.joueur, numgrille))
        self._tcserver.onglet_looks.add(u"{} grille {}".format(
            self.joueur, numgrille))
        self.events.append(EventsTC(
            self._currentsequence, self.currentperiod.TC_period, pms.EVENT_LOOK,
            grille=numgrille))

    def remote_send_try(self, numgrille, nbun):
        logger.debug(u"{} send_try {}: {}".format(self.joueur, numgrille, nbun))
        self._tcserver.onglet_essais.add(u"{} grille {} valeur {}".format(
            self.joueur, numgrille, nbun))
        self.events.append(EventsTC(
            self._currentsequence, self.currentperiod.TC_period, pms.EVENT_TRY,
            grille=numgrille, answer=nbun,
            goodanswer=True if nbun == pms.GRILLES[numgrille]["count"] else
            False))

    @defer.inlineCallbacks
    def remote_send_message(self, message):
        logger.debug(u"{} send_message {}".format(self.joueur, message))
        self._tcserver.onglet_messages.add(u"{}: {}".format(
            self.joueur, message))
        self.events.append(EventsTC(
            self._currentsequence, self.currentperiod.TC_period,
            pms.EVENT_MESSAGE, message=message, messagetype=pms.MSG_ENVOYE))
        yield (twu.forAll(self.othergroupmembers, "display_message", message))

    @defer.inlineCallbacks
    def display_message(self, message):
        logger.debug(u"{} display_message {}".format(self.joueur, message))
        self.events.append(EventsTC(
            self._currentsequence, self.currentperiod.TC_period,
            pms.EVENT_MESSAGE, message=message, messagetype=pms.MSG_RECU))
        yield (self.remote.callRemote("display_message", message))

    def compute_periodpayoff(self):
        """
        Compute the payoff for the period
        :return:
        """
        logger.debug(u"{} Period Payoff".format(self.joueur))
        self.currentperiod.TC_periodpayoff = \
            self.currentperiod.TC_goodanswers_group / pms.TAILLE_GROUPES

        # cumulative payoff since the first period
        if self.currentperiod.TC_period < 2:
            self.currentperiod.TC_cumulativepayoff = \
                self.currentperiod.TC_periodpayoff
        else: 
            previousperiod = self.sequences[self._currentsequence][
                self.currentperiod.TC_period - 1]
            self.currentperiod.TC_cumulativepayoff = \
                previousperiod.TC_cumulativepayoff + \
                self.currentperiod.TC_periodpayoff

        # we store the period in the self.periodes dictionnary
        self.sequences[self._currentsequence][self.currentperiod.TC_period] = \
            self.currentperiod

        logger.debug(u"{} Period Payoff {}".format(
            self.joueur, self.currentperiod.TC_periodpayoff))

    @defer.inlineCallbacks
    def display_summary(self):
        """
        Create the summary (txt and historic) and then display it on the
        remote
        :return:
        """
        logger.debug(u"{} Summary".format(self.joueur))
        yield (self.remote.callRemote(
            "display_summary", self.currentperiod.todict()))
        self.joueur.info("Ok")
        self.joueur.remove_waitmode()

    @defer.inlineCallbacks
    def compute_partpayoff(self):
        logger.debug(u"{} Part Payoff".format(self.joueur))

        self.TC_gain_ecus = self.currentperiod.TC_cumulativepayoff
        self.TC_gain_euros = float(self.TC_gain_ecus) * float(pms.TAUX_CONVERSION)

        yield (self.remote.callRemote(
            "set_payoffs_TC", self._currentsequence, self.TC_gain_euros,
            self.TC_gain_ecus))

        self.sequences[self._currentsequence]["gain_euros"] = self.TC_gain_euros

        logger.info(u'{} Payoff ecus {} Payoff euros {:.2f}'.format(
            self.joueur, self.TC_gain_ecus, self.TC_gain_euros))

    @defer.inlineCallbacks
    def display_payoffs(self, sequence):
        yield (self.remote.callRemote("display_payoffs_TC", sequence))
        self.joueur.info("ok")
        self.joueur.remove_waitmode()

    @defer.inlineCallbacks
    def display_additionnalquestions(self):
        logger.debug(u"{} display_additionnalquestions".format(self.joueur))
        rep = yield (self.remote.callRemote(
            "display_additionnalquestions", self.currentperiod.TC_nbanswers))
        for k, v in rep.viewitems():
            setattr(self.currentperiod, k, v)
        self.joueur.info(rep)
        self.joueur.remove_waitmode()

    @defer.inlineCallbacks
    def display_questionapresdictator(self):
        logger.debug(u"{} display_questionapresdictator".format(self.joueur))
        self.currentperiod.TC_croyancedictator = yield (
            self.remote.callRemote("display_questionapresdictator"))
        self.joueur.remove_waitmode()
        self.joueur.info(u"{}".format(self.currentperiod.TC_croyancedictator))

    @defer.inlineCallbacks
    def display_questfinal(self):
        logger.debug(u"{} display_questfinal".format(self.joueur))
        inputs = yield (self.remote.callRemote("display_questfinal"))
        part_questfinal = self.joueur.get_part("questionnaireFinal")
        for k, v in inputs.viewitems():
            setattr(part_questfinal, k, v)
            setattr(self.currentperiod, "TC_{}".format(k), v)
        self.joueur.info('ok')
        self.joueur.remove_waitmode()


class RepetitionsTC(Base):
    __tablename__ = 'partie_TeamCommunication_repetitions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    partie_partie_id = Column(
        Integer,
        ForeignKey("partie_TeamCommunication.partie_id"))

    TC_sequence = Column(Integer)
    TC_period = Column(Integer)
    TC_treatment = Column(Integer)
    TC_group = Column(Integer)
    TC_grille_0 = Column(Integer)
    TC_grille_1 = Column(Integer)
    TC_grille_2 = Column(Integer)
    TC_grille_3 = Column(Integer)
    TC_grille_4 = Column(Integer)
    TC_grille_5 = Column(Integer)
    TC_grille_6 = Column(Integer)
    TC_grille_7 = Column(Integer)
    TC_grille_8 = Column(Integer)
    TC_grille_9 = Column(Integer)
    TC_grille_10 = Column(Integer)
    TC_grille_11 = Column(Integer)
    TC_grille_12 = Column(Integer)
    TC_grille_13 = Column(Integer)
    TC_grille_14 = Column(Integer)
    TC_grille_15 = Column(Integer)
    TC_grille_16 = Column(Integer)
    TC_grille_17 = Column(Integer)
    TC_grille_18 = Column(Integer)
    TC_grille_19 = Column(Integer)
    TC_grille_20 = Column(Integer)
    TC_grille_21 = Column(Integer)
    TC_grille_22 = Column(Integer)
    TC_grille_23 = Column(Integer)
    TC_grille_24 = Column(Integer)
    TC_grille_25 = Column(Integer)
    TC_grille_26 = Column(Integer)
    TC_grille_27 = Column(Integer)
    TC_grille_28 = Column(Integer)
    TC_grille_29 = Column(Integer)
    TC_grille_30 = Column(Integer)
    TC_grille_31 = Column(Integer)
    TC_grille_32 = Column(Integer)
    TC_grille_33 = Column(Integer)
    TC_grille_34 = Column(Integer)
    TC_grille_35 = Column(Integer)
    TC_grille_36 = Column(Integer)
    TC_grille_37 = Column(Integer)
    TC_grille_38 = Column(Integer)
    TC_grille_39 = Column(Integer)
    TC_grille_40 = Column(Integer)
    TC_grille_41 = Column(Integer)
    TC_grille_42 = Column(Integer)
    TC_grille_43 = Column(Integer)
    TC_grille_44 = Column(Integer)
    TC_grille_45 = Column(Integer)
    TC_grille_46 = Column(Integer)
    TC_grille_47 = Column(Integer)
    TC_grille_48 = Column(Integer)
    TC_grille_49 = Column(Integer)
    TC_grille_50 = Column(Integer)
    TC_grille_51 = Column(Integer)
    TC_grille_52 = Column(Integer)
    TC_grille_53 = Column(Integer)
    TC_grille_54 = Column(Integer)
    TC_grille_55 = Column(Integer)
    TC_grille_56 = Column(Integer)
    TC_grille_57 = Column(Integer)
    TC_grille_58 = Column(Integer)
    TC_grille_59 = Column(Integer)
    TC_grille_60 = Column(Integer)
    TC_grille_61 = Column(Integer)
    TC_grille_62 = Column(Integer)
    TC_grille_63 = Column(Integer)
    TC_grille_64 = Column(Integer)
    TC_grille_65 = Column(Integer)
    TC_grille_66 = Column(Integer)
    TC_grille_67 = Column(Integer)
    TC_grille_68 = Column(Integer)
    TC_grille_69 = Column(Integer)
    TC_grille_70 = Column(Integer)
    TC_grille_71 = Column(Integer)
    TC_grille_72 = Column(Integer)
    TC_grille_73 = Column(Integer)
    TC_grille_74 = Column(Integer)
    TC_grille_75 = Column(Integer)
    TC_grille_76 = Column(Integer)
    TC_grille_77 = Column(Integer)
    TC_grille_78 = Column(Integer)
    TC_grille_79 = Column(Integer)
    TC_grille_80 = Column(Integer)
    TC_grille_81 = Column(Integer)
    TC_grille_82 = Column(Integer)
    TC_grille_83 = Column(Integer)
    TC_grille_84 = Column(Integer)
    TC_grille_85 = Column(Integer)
    TC_grille_86 = Column(Integer)
    TC_grille_87 = Column(Integer)
    TC_grille_88 = Column(Integer)
    TC_grille_89 = Column(Integer)
    TC_grille_90 = Column(Integer)
    TC_grille_91 = Column(Integer)
    TC_grille_92 = Column(Integer)
    TC_grille_93 = Column(Integer)
    TC_grille_94 = Column(Integer)
    TC_grille_95 = Column(Integer)
    TC_grille_96 = Column(Integer)
    TC_grille_97 = Column(Integer)
    TC_grille_98 = Column(Integer)
    TC_grille_99 = Column(Integer)
    TC_nbanswers = Column(Integer)
    TC_goodanswers = Column(Integer)
    TC_goodanswers_group = Column(Integer)
    TC_periodpayoff = Column(Float)
    TC_nblooks = Column(Integer)
    TC_nbtries = Column(Integer)
    TC_nbmsgsent = Column(Integer)
    TC_nbmsgreceived = Column(Integer)
    TC_confidence = Column(Integer)
    TC_infosatisfaction = Column(Integer)
    TC_jobsatisfaction = Column(Integer)
    TC_cumulativepayoff = Column(Float)
    TC_croyancedictator = Column(Integer)
    TC_residence = Column(Integer)
    TC_luxembourgish_speak = Column(Integer)
    TC_luxembourgish_understand = Column(Integer)
    TC_luxembourgish_read = Column(Integer)
    TC_luxembourgish_write = Column(Integer)
    TC_french_speak = Column(Integer)
    TC_french_understand = Column(Integer)
    TC_french_read = Column(Integer)
    TC_french_write = Column(Integer)
    TC_german_speak = Column(Integer)
    TC_german_understand = Column(Integer)
    TC_german_read = Column(Integer)
    TC_german_write = Column(Integer)
    TC_english_speak = Column(Integer)
    TC_english_understand = Column(Integer)
    TC_english_read = Column(Integer)
    TC_english_write = Column(Integer)


    def __init__(self, sequence, period):
        self.TC_sequence = sequence
        self.TC_treatment = pms.TREATMENT
        self.TC_period = period
        self.TC_decisiontime = 0
        self.TC_periodpayoff = 0
        self.TC_cumulativepayoff = 0

    def todict(self, joueur=None):
        temp = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        if joueur:
            temp["joueur"] = joueur
        return temp


class EventsTC(Base):
    __tablename__ = "partie_TeamCommunication_repetitionsevents"
    id = Column(Integer, primary_key=True, autoincrement=True)
    partie_partie_id = Column(
        Integer, ForeignKey("partie_TeamCommunication.partie_id"))

    TC_sequence = Column(Integer)
    TC_period = Column(Integer)
    TC_eventType = Column(Integer)
    TC_time = Column(DateTime)
    TC_grille = Column(Integer)
    TC_value = Column(Integer)
    TC_goodnumber = Column(Integer)
    TC_message = Column(String)
    TC_sentorreceived = Column(Integer)

    def __init__(self, sequence, period, eventtype, **kwargs):
        self.TC_sequence = sequence
        self.TC_period = period
        self.TC_eventType = eventtype
        self.TC_time = datetime.now()

        if self.TC_eventType == pms.EVENT_LOOK:
            self.TC_grille = kwargs["grille"]

        elif self.TC_eventType == pms.EVENT_TRY:
            self.TC_grille = kwargs["grille"]
            self.TC_value = kwargs["answer"]
            self.TC_goodnumber = kwargs["goodanswer"]

        elif self.TC_eventType == pms.EVENT_MESSAGE:
            self.TC_message = kwargs["message"]
            self.TC_sentorreceived = kwargs["messagetype"]

    def todict(self, joueur):
        temp = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        temp["joueur"] = joueur
        return temp
