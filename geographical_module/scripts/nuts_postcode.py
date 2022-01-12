import os

import pandas as pd
from django.db import connection, transaction

from geographical_module.models.geography import NutsPostcode
from .cons import FINAL_DOCS_DIR, NUTS_POSTCODE_FILE
from .utils import create_path_to_directory_or_file, remove_file, file_exists


def create_nuts_postcode_csv():
    nuts_postcode_path = create_path_to_directory_or_file(FINAL_DOCS_DIR, NUTS_POSTCODE_FILE)
    overall_df = pd.DataFrame(columns=['NUTS3', 'CODE'])
    print('Iterating and creating overall_df...')
    for item in os.listdir(create_path_to_directory_or_file('nuts_postcode_csvs')):
        df = pd.read_csv(create_path_to_directory_or_file('nuts_postcode_csvs', item),
                         delimiter=';')
        df.sort_values(by=['NUTS3', 'CODE'], inplace=True, ignore_index=True)
        df['NUTS3'] = df['NUTS3'].str.strip("''")
        df['CODE'] = df['CODE'].str.strip("''")
        overall_df = overall_df.append(df, ignore_index=True)
    if (df_size := overall_df.shape[0]) == 0:
        raise Exception(
            "Dataframe with all NUTS-Postcode is empty! No csv file to be created! Check if the csv' containing the nuts3-postcodes exist!")
    else:
        print(f'Creating csv from dataframe with {df_size:,} rows...')
        remove_file(nuts_postcode_path)
        overall_df.to_csv(path_or_buf=nuts_postcode_path, header=['nuts', 'postcode'], index=False,
                          sep=';')
        print('Finished creating nuts_postcodes_file')


@transaction.atomic()
def create_nuts_postcode_records_for_db():
    nuts_postcode_csv = create_path_to_directory_or_file(FINAL_DOCS_DIR, NUTS_POSTCODE_FILE)
    if file_exists(nuts_postcode_csv, raise_exception=True):
        df = pd.read_csv(nuts_postcode_csv,
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
