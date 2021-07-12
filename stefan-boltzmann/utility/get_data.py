import pandas as pds
import numpy as np

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
            df.drop([cols_to_remove], axis = 1)

        else:
            df.drop(cols_to_remove, axis = 1)

    return df

df = get_dataframe()
print(df.head())
