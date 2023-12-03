#!/usr/bin/python3

import sys
import logging
import random
import json
import argparse

logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG
)

logger = logging.getLogger("gen_prob_dist")

DICE_FILE="dice.json"
NO_OF_SAMPLES=10000


def gen_prob_dist(param, dict_dice, no_of_samples=NO_OF_SAMPLES):
    distribution = {}
    for i in range(no_of_samples):
        roll = [ random.choice(dict_dice[die]) for die in param ]
        if roll.count(0) > 1:
            distribution[0] = distribution.get(0, 0) + 1
        else:
            value = sum(roll)
            distribution[value] = distribution.get(value, 0) + 1

    distribution = { k: v/NO_OF_SAMPLES for k,v in distribution.items() }
    return distribution

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="""
            Probability distribution generator for oathsworn dice.

            Generate probability distribution for arbitrary number of different dice
            using numerical methods.
            """
    )
    parser.add_argument("parameter", help="paramerter of prob dist. e.g. AABBBC")

    args = parser.parse_args()
    with open(DICE_FILE, "r") as f:
        dict_dice = json.load(f)
        if any(p not in dict_dice.keys() for p in args.parameter):
            logger.error("Parameter not recognized.")
            exit(-1)
        distribution = gen_prob_dist(args.parameter, dict_dice)
        logger.info(f"Distribution for {args.parameter}")
        logger.info(f"VAL | PROB")
        logger.info(f"----+-----")
        for x in sorted(distribution):
            logger.info(f"{x:3} | {distribution[x]}")
