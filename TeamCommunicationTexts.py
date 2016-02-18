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


def get_text_explanation():
    txt = trans_TC(u"To display a grid, click on its number.")
    txt += trans_TC(u"\nTo indicate the number of '1' included in the grid, enter "
               u"this number directly in the box under its number")
    if pms.TREATMENT == pms.get_treatment("avec_communication"):
        txt += trans_TC(u"The chat window allows you to communicate freely for {} "
                   u"minutes with other group players.".format(
                        pms.TEMPS_PARTIE.minute))
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
    txt = trans_TC(u"Among your {}, how much to you think are rights?").format(
        get_pluriel(nbanswers, trans_TC(u"answer")))
    return txt


def get_text_infosatisfaction():
    txt = trans_TC(u"In a scale ranged from 1 (not satisfied at all) to 7 "
                   u"(very satisfied), <br />where is your level of "
                   u"satisfaction in regards of <br />the informations you "
                   u"exchanged with your group members?")
    return txt


def get_text_jobsatisfaction():
    txt = trans_TC(u"In a scale ranged from 1 (not satisfied at all) to 7 "
                   u"(very satisfied), <br />where is you level of "
                   u"satisfaction in regards of the task <br />you "
                   u"participated in?")
    return txt


def get_text_predictiondictator():
    txt = trans_TC(u"To your opinion, how much was sent, on average, to "
                   u"players B in the current session?")
    return txt
