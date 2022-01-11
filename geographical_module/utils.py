import json
import os

import pandas as pd


def nuts_link_2():
    os.chdir('nuts')
    overall_df = pd.DataFrame(columns=['NUTS3', 'CODE'])
    nuts_dict = dict()
    nuts_list = []
    for item in os.listdir('.'):
        read_item = pd.read_csv(item, delimiter=';')
        read_item.sort_values(by=['NUTS3', 'CODE'], inplace=True, ignore_index=True)

        previous_nuts = None
        start_range = None
        end_range = None

        for i, elm in read_item.iterrows():
            # row = elm.values
            if previous_nuts == None and start_range == None:
                previous_nuts = elm.NUTS3
                start_range = elm.CODE
                end_range = elm.CODE
                nuts_dict[elm.NUTS3.strip("''")] = {'start': start_range.strip("''"), 'end': None}
                
                
            if previous_nuts != elm.NUTS3:
                # fill dict() and change previous_nuts
                nuts_dict[previous_nuts.strip("''")]['end'] = end_range.strip("''")
                nuts_dict[elm.NUTS3.strip("''")] = {'start': elm.CODE.strip("''"), 'end': None}
                previous_nuts = elm.NUTS3

            end_range = elm.CODE

        nuts_dict[previous_nuts.strip("''")]['end'] = end_range.strip("''")
        overall_df = overall_df.append(read_item, ignore_index=True)

    for k, v in nuts_dict.items():
        nuts_list.append({'nuts': k, 'start': v['start'], 'end': v['end']})

    overall_df.to_pickle('../nuts.pickle')
    with open('../final_docs/nuts_json.txt', 'w') as json_file:
        json.dump(nuts_dict, json_file)
    with open('../final_docs/nuts_json2.txt', 'w') as json_file:
        json.dump(nuts_list, json_file)
    duplicated = overall_df[overall_df.duplicated(['CODE'], keep=False)]
    duplicated.to_csv('../final_docs/duplikate.csv')

