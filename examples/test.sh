#!/bin/bash
# File Name : test.sh

cat train.json | object --safe --indent 2 '.fn_filter(lambda x: x["sellOut"]._data==0).fn_filter(lambda x: x["trainNum"]._data.startswith("G")).fn_map(lambda x: x.fn_items_update(lambda k, v: (v.seatName, v.price) if k.startswith("price_") else v)).fn_map(lambda x: x.fn_include_keys(["trainNum", "destStationName", "departStationName", "trainTypeName", "departureCityName", "arrivalCityName", "durationStr", "price_0", "price_1", "price_2", "price_3"]))'

