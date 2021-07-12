#####################
# IMPORT STATEMENTS #
#####################

import pandas as pds
import numpy as np

#####################
#     MAIN CODE     #
#####################

# This gets the dataframe from the site and cleans it up.
def get_dataframe(remove_err = True, cols_to_remove = None):

    '''
        remove_err -> a Boolean flag asking whether or not to remove error columns.
                      True by default for our purposes.

        cols_to_remove -> a Python list of string keys corresponding to columns to be removed.
                          Consider that they will be the same keys after the dataframe
                          has been corrected for the '# System' shift.
    '''

    # Load the url and open it.  '\s+' means multiple space delimiter.
    debcat = 'https://www.astro.keele.ac.uk/jkt/debcat/debs.dat'
    df = pds.read_csv(debcat, delimiter = '\s+')

    # Now, we need to fix it, since '# System' as a key breaks the alignment.
    # We move everything to the right once.
    df = df.shift(1, axis = 1)

    # We drop the first column, since it's now empty.
    df = df.drop(['#'], axis = 1)

    if remove_err == True:

        keys = np.array(df.keys())

        # Find the locations where 'err' is in the keys.  NumPy is weird with strings.
        locs = (-np.core.defchararray.find(np.array(keys).astype(str), "err")).astype(bool)

        # Index the keys by these locations and then index the dataframe by these keys.
        df = df[keys[locs]]

    if cols_to_remove is not None:

        # In case only one column is passed.
        if type(cols_to_remove) == str:
            df = df.drop([cols_to_remove], axis = 1)

        else:
            df = df.drop(cols_to_remove, axis = 1)

    return df

# This removes any rows where the value is '-9.99' 
# as defined in the notes on the website.
def remove_invalid_values(df, columns_to_check):

    '''
        df -> the dataframe containing the DEBcat data
        columns_to_check -> a list of strings containing the keys to check for invalid values. 
    '''

    # In case only a string is passed.
    if type(columns_to_check) == str:

        # Save only the rows where that column is
        # not equal to -9.99.
        df = df[df[columns_to_check] != -9.99]

    else:
        for key in columns_to_check:
            
            df = df[df[key] != -9.99]

    return df
