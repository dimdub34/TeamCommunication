# -*- coding: utf-8 -*-
"""
This module contains the texts for the screens
"""
from util.utiltools import get_pluriel
import TeamCommunicationParams as pms

import os
import configuration.configparam as params
import gettext
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


def get_text_explanation():
    txt = trans_TC(u"To display a grid, click on its number.")
    txt += trans_TC(u"<br />To indicate the number of '1' included in the grid, "
                    u"enter this number directly in the box under its number")

    if pms.TREATMENT == pms.get_treatment("avec_communication"):
        txt += trans_TC(u"<br />The chat window allows you to communicate "
                        u"freely for {} minutes with other group "
                        u"players.").format(pms.TEMPS_PARTIE.minute)
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
