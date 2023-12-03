#!/usr/bin/python3

import sys
import logging
import itertools
import json
import random
from gen_prob_dist import gen_prob_dist

logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG
)

logger = logging.getLogger("gen_all_prob_dist")

DICE_FILE="dice.json"
OUT_FILE="prob_dist.json"
MAX_ROLLS = 10
NO_OF_SAMPLES = 10000

DICT_DICE = {}

with open(DICE_FILE, "r") as f:
    DICT_DICE = json.load(f)

# generate all possible prob dist parameters.
dict_prob_dists = {}
for no_of_roll in range(1, MAX_ROLLS +1):
    logger.info(f"adding prob dist for {no_of_roll} dices.")
    for item in itertools.product(DICT_DICE.keys(), repeat=no_of_roll):
        buf = list(item)
        buf.sort()
        dict_prob_dists["".join(buf)] = {
            "parameter" : {
                k: buf.count(k) for k in DICT_DICE.keys()
            }
        }

logger.info(f"length of set prob dist : {len(dict_prob_dists)}")

param_cnt = 1

# compute all prob dist.
for param, data in dict_prob_dists.items():
    data["distribution"] = gen_prob_dist(param, DICT_DICE, NO_OF_SAMPLES)
    logger.debug(f"{param_cnt} prob dist generated. Current: {param}")
    param_cnt += 1

# export prob dist.
logger.info("Done generating all prob dist. Export to file.")
with open(OUT_FILE, "w+") as f:
    json.dump(dict_prob_dists, f)
logger.info("Done.")
