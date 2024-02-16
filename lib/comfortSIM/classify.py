# Description: This file contains functions for classifying subjects into differenty types of thermal comfort offset classes.

def compute_offset(df, set_key, tsv_key):
    """
    Compute the offset between the actual and predicted Thermal Sensation Vote.

    This function adds two new columns to the DataFrame:
    - 'set_tsv': The predicted value, calculated using a function describing the relationship
    between SET and TSV in the ASHRAE database II.
    - 'ts_offset': The offset between the actual and predicted values.

    Parameters:
    ----------
    df : pandas.DataFrame
        The DataFrame containing the data.
    set_key : str
        The column name in df for the SET values.
    tsv_key : str
        The column name in df for the recorded TSV values.

    Returns:
    -------
    pandas.DataFrame
        The DataFrame with the added 'set_tsv' and 'ts_offset' columns.
    """

    parameters = [-13.58271,
                  1.36316,
                  -0.04643,
                  0.00056]
    
    df['set_tsv'] = parameters[0] + parameters[1] * df[set_key] + parameters[2] * df[set_key]**2 + parameters[3] * df[set_key]**3
    df['ts_offset'] = df[tsv_key] - df['set_tsv']

    return df


def generate_mean_personal_offset(df, subject_id_key):
    """
    Generate the mean personal offset for each subject.

    This function calculates the mean 'ts_offset' for each subject and adds it as a new column 
    'personal_mean_ts_offset' to the DataFrame.

    Parameters:
    ----------
    df : pandas.DataFrame
        The DataFrame containing the 'ts_offset' values.
    subject_id_key : str
        The column name in df for the subject IDs.

    Returns:
    -------
    pandas.DataFrame
        The DataFrame with the added 'personal_mean_ts_offset' column.
    """
    
    mean_ts_offset = df.groupby(subject_id_key)['ts_offset'].mean()
    df['personal_mean_ts_offset'] = df[subject_id_key].apply(lambda x: mean_ts_offset[x])

    return df



def classify_into_offset_classes(row, col):
    """
    Allocate subjects into five offset classes.
    
    Based on mean personal offset, classify subjects into offset classes. Note that this function requires the 
    'generate_mean_personal_offset' function to be run first.

    Parameters:


    Returns:
    type.

    """

    if row[col] <= -1.5:
        return -2
    elif row[col] > -1.5 and row[col] <= -0.5:
        return -1
    elif row[col] > -0.5 and row[col] <= 0.5:
        return 0
    elif row[col] > 0.5 and row[col] <= 1.5:
        return 1
    elif row[col] > 1.5:
        return 2
    else:
        return None