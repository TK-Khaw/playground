#!/usr/bin/bash

PRODDIST_FILE=prod_dist.json
CHECK=${1:-4}

jq "to_entries | map({ key, value: .value.distribution | with_entries(select(.key|tonumber > ${CHECK}) ) | add}) | sort_by(.value)" ${PRODDIST_FILE}
