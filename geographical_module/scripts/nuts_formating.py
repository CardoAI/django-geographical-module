#
# ASK IF NEEDED IN PRODUCTION
# IF YES, ADD THE PyYAML and pandas TO REQUIREMENTS AND setup.cfg
#

import pandas as pd
import yaml


def nuts_format():
    file = 'scripts/nuts.csv'
    nuts_df = pd.read_csv(filepath_or_buffer=file, delimiter=';')
    nuts_df.en_name = nuts_df.en_name.fillna('').astype(str)
    nuts_df.top_parent = nuts_df.top_parent.fillna(-1).astype(int)
    nuts_df.parent = nuts_df.parent.fillna(-1).astype(int)
    levels_dict = dict()
    flag = check_sequence(nuts_df['level'].tolist())
    print(flag)
    for index, row in nuts_df.iterrows():
        if row.level == 0:  # if level == 0 -> means top parent, we start a group
            levels_dict[0] = row.id
        else:
            levels_dict[row.level] = row.id
            nuts_df.at[index, 'top_parent'] = levels_dict[0]
            nuts_df.at[index, 'parent'] = levels_dict[row.level - 1]
    dict_file = []
    for index, row in nuts_df.iterrows():
        dict_file.append({
            'model': 'geographical_module.Geography',
            'pk': row.id,
            'fields': {
                'level': row['level'],
                'original_name': row['original_name'],
                'en_name': row['en_name'] if row['en_name'] else None,
                'code': row['code'],
                'parent': row['parent'] if row.parent != -1 else None,
                'top_parent': row['top_parent'] if row.parent != -1 else None
            }
        })
    with open('/home/kristi/Workspace/djangoProjectTest/geographical_module/fixtures/nuts.yaml',
              'w+') as file:
        yaml.dump(dict_file, file, default_flow_style=False, sort_keys=False, allow_unicode=True)


def check_sequence(nr_list):
    max_nr = max(nr_list)
    for index, nr in enumerate(nr_list[:-1]):
        if nr < nr_list[index + 1] != nr + 1:
            return False
        if nr_list[index + 1] == 0 and nr != max_nr:
            return False
    if nr_list[-2] != max_nr and nr_list[-1] - nr_list[-2] != 1:
        return False
    return True
