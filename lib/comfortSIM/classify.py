# Description: This file contains functions for classifying subjects into differenty types of thermal comfort offset classes.

def compute_offset():
    """
    Compute offset based on ASHRAE Global Thermal Comfort Database II.

    Based on a function describing the relationship between Standard Effective Temperature (SET) and
    Thermal Sensation Vote (TSV) in ASHRAE Global Thermal Comfort Database II. For each sample, the
    offset is calculated as the difference between the TSV as predicted by the function and actual
    TSV.
    
    Parameters:


    Returns:
    type.
    """

    # Function implementation goes here
    pass



def generate_mean_personal_offset():
    """
    Generate mean personal offset for each subject.

    For each subject (identified by 'subject_ID') the mean offset is calculated. Note that this function
    requires the 'compute_offset' function to be run first.
    
    Parameters:


    Returns:
    type.
    """

    # Function implementation goes here
    pass



def classify_into_offset_classes():
    """
    Allocate subjects into five offset classes.
    
    Based on mean personal offset, classify subjects into offset classes. Note that this function requires the 
    'generate_mean_personal_offset' function to be run first.

    Parameters:


    Returns:
    type.

    """