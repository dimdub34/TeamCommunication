# -*- coding: utf-8 -*-
"""
Ce module contient les variables et les paramètres de la partie
Les variables ne doivent pas être changées
Les paramètres peuvent être changés, mais, par sécurité, demander au développeur
"""
import datetime

# variables: ne pas changer
# SANS_COMMUNICATION = 0
# AVEC_COMMUNICATION = 1
# treatmentcodes = {0: "SANS_COMMUNICATION", 1: "AVEC_COMMUNICATION"}
TREATMENTS = {0: "sans_communication", 1: "avec_communication"}
MSG_ENVOYE = 0
MSG_RECU = 1
EVENT_LOOK = 0
EVENT_TRY = 1
EVENT_MESSAGE = 2

# paramètres
TREATMENT = 0  # peut être changé dans l'appli
TEMPS_PARTIE = datetime.time(0, 2, 0)  # heures, minutes, secondes
TAUX_CONVERSION = 0.6
NOMBRE_PERIODES = 0
TAILLE_GROUPES = 4
GROUPES_CHAQUE_PERIODE = False
MONNAIE = u"ecu"
GRILLES = None  # chargées avec menu configuration de l'appli


def get_treatment(code_or_name):
    if type(code_or_name) is int:
        return TREATMENTS.get(code_or_name, None)
    elif type(code_or_name) is str:
        for k, v in TREATMENTS.viewitems():
            if v == code_or_name.lower():
                return k
    else:
        return None
