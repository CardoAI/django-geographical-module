import os

import pandas as pd


def create_nuts_postcode_csv(nuts_files_directory: str, output_file: str):
    """
    Read from all the csv file supplied from EU regarding NUTS3 and their postcodes. CSV files are stored in 'nuts_postcode_csvs' directory.
    After reading all the files create a df with all the data and export it to a new csv file name: 'nuts_postcodes' in the 'final_docs' directory.
    This file is used to create the records in db.
    If no files are found in the nuts_postcode_csvs dir than an exception will be raised since no file will be created from an empty df.
    """

    overall_df = pd.DataFrame(columns=['NUTS3', 'CODE'])

    print('Iterating and creating overall_df...')

    list_of_file_paths = os.listdir(nuts_files_directory)
    if not list_of_file_paths:
        raise Exception(
            "Dataframe with all NUTS-Postcode is empty! "
            "No csv file to be created! "
            "Check if the csv' containing the nuts3-postcodes exist!"
        )

    for item in list_of_file_paths:
        df = pd.read_csv(os.path.join(nuts_files_directory, item), delimiter=';')
        df.sort_values(by=['NUTS3', 'CODE'], inplace=True, ignore_index=True)
        df['NUTS3'] = df['NUTS3'].str.strip("''")
        df['CODE'] = df['CODE'].str.strip("''")
        overall_df = overall_df.append(df, ignore_index=True)

    print(f'Creating csv from dataframe with {len(overall_df)} rows...')
    overall_df.to_csv(output_file, header=['nuts', 'postcode'], index=False, sep=';')
    print('Finished creating nuts_postcodes_file')
