# -*- coding: utf-8 -*-
"""
This module contains the texts for the screens
"""
from util.utiltools import get_pluriel
import TeamCommunicationParams as pms
import os
import configuration.configparam as params
import gettext
from util.utili18n import le2mtrans


localedir = os.path.join(params.getp("PARTSDIR"), "TeamCommunication", "locale")
trans_TC = gettext.translation(
  "TeamCommunication", localedir, languages=[params.getp("LANG")]).ugettext


COUNTRY_RESIDENCE = {
    1: trans_TC(u"Germany"),
    2: trans_TC(u"Belgium"),
    3: trans_TC(u"France"),
    4: trans_TC(u"Luxembourg")
}

LANGUAGE_SKILLS = {
    1: trans_TC(u"No difficulty"),
    2: trans_TC(u"Some difficulty"),
    3: trans_TC(u"Considerable difficulty"),
    4: trans_TC(u"No notion")
}

DISCIPLINES = {
    1: le2mtrans(u'Archeology'),
    2: le2mtrans(u'Biology'),
    3: le2mtrans(u'Chemistry'),
    4: le2mtrans(u'Law'),
    5: le2mtrans(u'Economics'),
    6: le2mtrans(u'Geography'),
    7: trans_TC(u"Gerontology"),
    8: le2mtrans(u'History'),
    9: trans_TC(u"Management"),
    10: trans_TC(u"Information and communication"),
    11: le2mtrans(u'Informatics'),
    12: le2mtrans(u'Letters'),
    13: le2mtrans(u'Medicine'),
    14: le2mtrans(u'Music'),
    15: le2mtrans(u'Pharmacy'),
    16: le2mtrans(u'Philosophy'),
    17: trans_TC(u"Psychology"),
    18: le2mtrans(u"Educational Sciences"),
    19: le2mtrans(u'Political Science'),
    20: le2mtrans(u'Sociology'),
}

PROFESSIONS = {
    1: trans_TC(u"Apprentice"),
    2: trans_TC(u"Male / Housewife"),
    3: trans_TC(u"Postdoc"),
    4: trans_TC(u"Retirement"),
    5: trans_TC(u"Employee (Private)"),
    6: trans_TC(u"Employee (Public)"),
    7: trans_TC(u"Unemployed"),
    8: trans_TC(u"Self employed")
}


ETUDES_ANNEES = {
    1: trans_TC(u'Bachelor') + u' 1',
    2: trans_TC(u'Bachelor') + u' 2',
    3: trans_TC(u'Bachelor') + u' 3',
    4: trans_TC(u'Master') + u' 1',
    5: trans_TC(u'Master') + u' 2',
    6: trans_TC(u'PhD'),
}


def get_text_explanation():
    txt = trans_TC(u"To display a grid, click on its number.")
    txt += trans_TC(u"<br />To indicate the number of '1' included in the grid, "
                    u"enter this number directly in the box under its number")

    if pms.TREATMENT == pms.get_treatment("avec_communication"):
        txt += trans_TC(u"<br />The chat window allows you to communicate "
                        u"freely with other group players.").format(
            pms.TEMPS_PARTIE.minute)
    return txt


def get_text_summary(period_content):
    txt = trans_TC(u"You've found {}.<br />Your group have found a total of "
              u"{}.<br />Each group member earns {}.").format(
        get_pluriel(period_content.get("TC_goodanswers"),
                    trans_TC(u"good answer")),
        get_pluriel(period_content.get("TC_goodanswers_group"),
                    trans_TC(u"good answer")),
        get_pluriel(period_content.get("TC_periodpayoff"), pms.MONNAIE))
    return txt


# ADDITIONNAL QUESTIONS
def get_text_reponses(nbanswers):
    txt = trans_TC(u"Among your {}, how much do you think are rights?").format(
        get_pluriel(nbanswers, trans_TC(u"answer")))
    return txt


def get_text_infosatisfaction():
    txt = trans_TC(u"In a scale ranged from 1 (not satisfied at all) to 7 "
                   u"(very satisfied), <br />where is your level of "
                   u"satisfaction in regards to <br />the informations you "
                   u"exchanged with your group members?")
    return txt


def get_text_jobsatisfaction():
    txt = trans_TC(u"In a scale ranged from 1 (not satisfied at all) to 7 "
                   u"(very satisfied), <br />where is you level of "
                   u"satisfaction in regards to the task <br />you "
                   u"participated in?")
    return txt


def get_text_predictiondictator():
    txt = trans_TC(u"To your opinion, how much was sent, on average, to "
                   u"players B in the current session?")
    return txt


def get_payoff_text(pay_euros, pay_ecus=None):
    if pay_ecus is not None:
        txt = trans_TC(u"You've earned {} which corresponds to {}.").format(
            get_pluriel(pay_ecus, pms.MONNAIE), get_pluriel(pay_euros, u"euro"))
    else:
        txt = trans_TC(u"You've earned {}.".format(
            get_pluriel(pay_euros, u"euro")))
    return txt
