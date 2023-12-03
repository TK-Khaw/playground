import json

PROBDIST_FILE="prob_dist.json"
OUTFILE="prob_dist.csv"

MAX_ROLLS=10

j = {}
with open(PROBDIST_FILE, "r") as f:
    j = json.load(f)

with open(OUTFILE, "w+") as f:
    f.write("A,B,C,D,")
    f.write(",".join([str(i) for i in range(MAX_ROLLS*5)]))
    f.write("\n")
    for pb in j.values():
        for key in [ "A", "B", "C", "D" ]:
            f.write(str(pb["parameter"][key]) + ",")
        f.write(",".join(
            str(pb["distribution"].get(str(i), 0)) for i in range(MAX_ROLLS*5)
        ))
        f.write("\n")
