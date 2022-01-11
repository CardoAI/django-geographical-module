import os

import pandas as pd
from django.db import connection, transaction

from geographical_module.models.geography import NutsPostcode
from .cons import FINAL_DOCS_DIR, NUTS_POSTCODE_FILE


def create_nuts_postcode_csvs():
    nuts_postcode_path = create_path_to_directory_or_file(FINAL_DOCS_DIR, NUTS_POSTCODE_FILE)
    remove_old_nuts_postcode_file(nuts_postcode_path)
    overall_df = pd.DataFrame(columns=['NUTS3', 'CODE'])
    print('Iterating and creating overall_df...')
    for item in os.listdir(create_path_to_directory_or_file('nuts_postcode_csvs')):
        df = pd.read_csv(create_path_to_directory_or_file('nuts_postcode_csvs', item),
                         delimiter=';')
        df.sort_values(by=['NUTS3', 'CODE'], inplace=True, ignore_index=True)
        df['NUTS3'] = df['NUTS3'].str.strip("''")
        df['CODE'] = df['CODE'].str.strip("''")
        overall_df = overall_df.append(df, ignore_index=True)
    print(f'Creating csv from dataframe with {overall_df.shape[0]:,} rows...')
    overall_df.to_csv(path_or_buf=nuts_postcode_path, header=['nuts', 'postcode'], index=False,
                      sep=';')
    print('Finished creating nuts_postcodes_file')


def remove_old_nuts_postcode_file(file_path):
    if os.path.isfile(file_path):
        os.remove(file_path)


def create_path_to_directory_or_file(directory, filename=None):
    cur_path = os.path.dirname(__file__)
    return os.path.join(cur_path, directory, filename) if filename else os.path.join(cur_path,
                                                                                     directory)


@transaction.atomic()
def create_nuts_postcode_records_for_db():
    df = pd.read_csv(create_path_to_directory_or_file(FINAL_DOCS_DIR, NUTS_POSTCODE_FILE),
                     delimiter=';')
    print(df.shape[0])
    clear_and_reset_indexes_of_nuts_postcode_table()
    print('Creating list, processing df...')
    nuts_postcodes = [NutsPostcode(nuts=row.nuts, postcode=row.postcode) for _, row in
                      df.iterrows()]
    print('Bulk inserting data in db...')
    NutsPostcode.objects.bulk_create(nuts_postcodes, batch_size=200000)
    print('Finished bulk inserting...')


def clear_and_reset_indexes_of_nuts_postcode_table():
    # TODO-Find a way to clear the table and reset index via orm or smthg else to not be dependent
    #  on the TRUNCATE statement
    with connection.cursor() as cursor:
        cursor.execute("TRUNCATE TABLE geographical_module_nutspostcode RESTART IDENTITY;")
