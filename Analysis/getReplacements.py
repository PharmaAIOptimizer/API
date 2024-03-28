import pandas as pd
from Analysis.DosageInfo import addDosageInfo

def getReplacements(input, data, isMultiple = False):
    units = ['%', 'MCG', 'M', 'IU', 'MEQ', 'UN', 'HR', 'MMOL', 'BP', 'CAL', 'USP', 'MU', 'Total_ML', 'Total_MM', 'Total_MG']
    # Define a function to classify the basic form based on the units present
    def classify_basic_form(row):
        if pd.notna(row['Total_MG']) and pd.isna(row[units]).all():
            return 'Solid'
        # Add more classifications as needed based on other units
        else:
            return 'Other/Undefined'
        
    def isMultipleOf(num, multiple):
        return num % multiple == 0
    
    # Remove items with a True Similarity less that 0.5
    data = data[data['True Similarity'] > 0.5]

    # Apply the function to the dataset
    data = addDosageInfo(data)

    # Add dosage info to the input
    input = addDosageInfo(input)

    # Apply the classification function to each row
    data['Basic Form'] = data.apply(classify_basic_form, axis=1)

    # Apply the classification function to intput
    input['Basic Form'] = input.apply(classify_basic_form, axis=1)

    if input['Basic Form'].iloc[0] == 'Solid' and isMultiple:
        print('Solid')
        solids_data = data[data['Basic Form'] == 'Solid']

        # Remove items with a Total MG bigger than the input Total MG
        solids_data = solids_data[solids_data['Total_MG'] <= input['Total_MG'].iloc[0]]

        # Remove items where the input Total MG is not a multiple of the item's Total MG
        solids_data = solids_data[solids_data['Total_MG'].apply(lambda x: isMultipleOf(input['Total_MG'].iloc[0], x))]

        result = solids_data
    else:
        print('Not Solid or rule off')

        # Remove items where all units are not equal to the input units
        units = ['%', 'MCG', 'M', 'IU', 'MEQ', 'UN', 'HR', 'MMOL', 'BP', 'CAL', 'USP', 'MU', 'Total_ML', 'Total_MM', 'Total_MG']
        for unit in units:
            result = data[data[unit] == input[unit].iloc[0]]

    return result
