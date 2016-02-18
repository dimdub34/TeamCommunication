# -*- coding: utf-8 -*-

import random
import pickle
import argparse
import time


def one_or_zero(proba, valeur):
    return 1 if valeur >= proba else 0


def create_grid(file_name):
    tables = {}
    for t in range(100):
        grille = []
        probazero = random.random()
        nbun = 0
        while nbun == 0:
            for l in range(10):
                grille.append([one_or_zero(probazero, random.random()) for i in range(10)])
            nbun = sum([ligne.count(1) for ligne in grille])
        tables[t] = {"grille": grille, "count": nbun}

    with open("{}.pck".format(file_name), "wb") as f:
        pickle.dump(tables, file=f)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--number", action="store", default=2,
                        help=u"Set the number of grid to create")

    args = parser.parse_args()
    prefix = time.strftime("%y%m%d%H%M", time.localtime())
    for i in range(args.number):
        create_grid(prefix + "_grid_{}".format(i))

    print("Ok, {} grids created".format(args.number))