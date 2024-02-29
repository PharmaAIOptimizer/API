import pandas as pd
import re
import numpy as np

def addDosageInfo(inputData):
    def extractDosage(size_str):
        # Ensure the input is a string
        size_str = str(size_str)
        # Initialize a dictionary to hold the extracted values
        extracted_values = {'MG': None, '%': None, 'ML': None, 'GM': None, 'MCG': None, 'M': None, 'OZ': None, 'IU': None, 'MEQ': None, 'UN': None, 'MM': None, 'HR': None, 'MMOL': None, 'KG': None, 'BP': None, 'L': None, 'CM': None, 'CC': None, 'CAL': None, 'LB': None, 'IN': None, 'GR': None, 'GAL': None, 'LT': None, 'USP': None, 'G': None, 'MU': None}

        # Turn string to uppercase for case-insensitive matching
        size_str = size_str.upper()

        # Change 'X' to ' * ' for easier matching
        size_str = size_str.replace('X', ' * ')

        # Change '/' to ' / ' for easier matching
        size_str = size_str.replace('/', ' / ')
        
        # Simplified logic for MG, %, ML extraction
        # Looks for a number (with optional decimal) immediately before the unit, with optional space
        for unit in ['MG', '%', 'ML', 'GM', 'MCG', 'OZ', 'IU', 'MEQ', 'UN', 'MM', 'HR', 'MMOL', 'KG', 'BP', 'L', 'CM', 'CC', 'CAL', 'LB', 'IN', 'GR', 'GAL', 'LT', 'USP', 'MU']:
            pattern = r'(\d+(?:\.\d*)?)\s*{}'.format(unit)
            match = re.search(pattern, size_str, re.IGNORECASE)
            if match and 'X' not in match.group(1):
                # Convert matched value to float and assign to the correct unit
                extracted_values[unit] = float(match.group(1))

        # If no MG, ML, MCG, MEQ, MM, MMOL, MU, GM, GR, GAL are not found, check for M and G
        if extracted_values['MG'] is None and extracted_values['ML'] is None and extracted_values['MCG'] is None and extracted_values['MEQ'] is None and extracted_values['MM'] is None and extracted_values['MMOL'] is None and extracted_values['MU'] is None and extracted_values['GM'] is None and extracted_values['GR'] is None and extracted_values['GAL'] is None:
            # Check for M and G
            for unit in ['M', 'G']:
                pattern = r'(\d+(?:\.\d*)?)\s*{}'.format(unit)
                match = re.search(pattern, size_str, re.IGNORECASE)
                if match and 'X' not in match.group(1):
                    # Convert matched value to float and assign to the correct unit
                    extracted_values[unit] = float(match.group(1))
        
        return extracted_values

    # Apply the adjusted function to extract all values
    df_updated_extracted = inputData['Size'].apply(extractDosage)

    # Update the DataFrame with the new extracted values
    inputData['MG'] = df_updated_extracted.apply(lambda x: x['MG'])
    inputData['%'] = df_updated_extracted.apply(lambda x: x['%'])
    inputData['ML'] = df_updated_extracted.apply(lambda x: x['ML'])
    inputData['GM'] = df_updated_extracted.apply(lambda x: x['GM'])
    inputData['MCG'] = df_updated_extracted.apply(lambda x: x['MCG'])
    inputData['M'] = df_updated_extracted.apply(lambda x: x['M'])
    inputData['OZ'] = df_updated_extracted.apply(lambda x: x['OZ'])
    inputData['IU'] = df_updated_extracted.apply(lambda x: x['IU'])
    inputData['MEQ'] = df_updated_extracted.apply(lambda x: x['MEQ'])
    inputData['UN'] = df_updated_extracted.apply(lambda x: x['UN'])
    inputData['MM'] = df_updated_extracted.apply(lambda x: x['MM'])
    inputData['HR'] = df_updated_extracted.apply(lambda x: x['HR'])
    inputData['MMOL'] = df_updated_extracted.apply(lambda x: x['MMOL'])
    inputData['KG'] = df_updated_extracted.apply(lambda x: x['KG'])
    inputData['BP'] = df_updated_extracted.apply(lambda x: x['BP'])
    inputData['L'] = df_updated_extracted.apply(lambda x: x['L'])
    inputData['CM'] = df_updated_extracted.apply(lambda x: x['CM'])
    inputData['CC'] = df_updated_extracted.apply(lambda x: x['CC'])
    inputData['CAL'] = df_updated_extracted.apply(lambda x: x['CAL'])
    inputData['LB'] = df_updated_extracted.apply(lambda x: x['LB'])
    inputData['IN'] = df_updated_extracted.apply(lambda x: x['IN'])
    inputData['GR'] = df_updated_extracted.apply(lambda x: x['GR'])
    inputData['GAL'] = df_updated_extracted.apply(lambda x: x['GAL'])
    inputData['LT'] = df_updated_extracted.apply(lambda x: x['LT'])
    inputData['USP'] = df_updated_extracted.apply(lambda x: x['USP'])
    inputData['G'] = df_updated_extracted.apply(lambda x: x['G'])
    inputData['MU'] = df_updated_extracted.apply(lambda x: x['MU'])

    # Perform the conversions
    inputData['Total_MG'] = (inputData['MG'].fillna(0) +
                            inputData['GM'].fillna(0) * 1000 +
                            inputData['KG'].fillna(0) * 1000000 +
                            inputData['OZ'].fillna(0) * 28349.5 +
                            inputData['LB'].fillna(0) * 453592 +
                            inputData['GR'].fillna(0) * 1000 + 
                            inputData['G'].fillna(0) * 1000)
    inputData['Total_MG'] = inputData['Total_MG'].replace(0.0, np.nan)

    inputData['Total_ML'] = (inputData['ML'].fillna(0) +
                            inputData['L'].fillna(0) * 1000 +
                            inputData['GAL'].fillna(0) * 3785.41 +
                            inputData['LT'].fillna(0) * 1000 +
                            inputData['CC'].fillna(0) * 1)
    inputData['Total_ML'] = inputData['Total_ML'].replace(0.0, np.nan)

    inputData['Total_MM'] = (inputData['MM'].fillna(0) +
                            inputData['CM'].fillna(0) * 10 +
                            inputData['IN'].fillna(0) * 25.4)
    inputData['Total_MM'] = inputData['Total_MM'].replace(0.0, np.nan)

    # List of columns to drop (all the original measurement columns)
    cols_to_drop = ['MG', 'ML', 'GM', 'KG', 'OZ', 'LB', 'GR', 'L', 'GAL', 'LT', 'CC', 'MM', 'CM', 'IN', 'G']

    # Drop the original measurement columns
    inputData.drop(columns=cols_to_drop, inplace=True)

    # Now inputData contains only the totalized columns and any other non-related columns
    return inputData
    