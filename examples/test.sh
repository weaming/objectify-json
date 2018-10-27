#!/bin/bash
# File Name : test.sh

cat train.json | object '.fn_filter(lambda x: x["sellOut"]._data==0).fn_filter(lambda x: x["trainNum"]._data.startswith("G")).fn_map(lambda x: x.fn_include_keys(["trainNum", "destStationName", "departStationName", "trainTypeName", "departureCityName", "arrivalCityName", "durationStr"]))'
