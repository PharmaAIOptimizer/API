

import pandas as pd
import re

def cleanData(file_path):
    # Reading the file

    # Load the data from the CSV file
    data = pd.read_csv(file_path)

    # Removing the specified columns and reordering the 'Item Number – 8 digit' column
    columns_to_remove = ['Item Number – 6 digit', 'UPC Number', 'Constant', 
                        'Customer-Specific Item Number', 'Pack Size Divisor', 
                        'RX/OTC Indicator']

    # Removing the columns
    data_cleaned = data.drop(columns=columns_to_remove)

    # Reordering 'Item Number – 8 digit' to the left
    column_to_move = data_cleaned.pop('Item Number – 8 digit')
    data_cleaned.insert(0, 'Item Number – 8 digit', column_to_move)

    # Moving all price columns and the contract flag to the right
    columns_to_move = ['AWP Price', 'Acquisition Price', 'Retail Price', 'WAC Price', 'Contract Flag']
    for col in columns_to_move:
        data_cleaned[col] = data_cleaned.pop(col)

    # Function to split the generic description into generic name and form
    def split_description(desc):
        match = re.search(r'[A-Z]', desc)
        if match:
            index = match.start()
            return desc[:index].strip(), desc[index:].strip()
        else:
            return desc, ''

    # Applying the function to split 'Generic Description'
    data_cleaned['Generic Name'], data_cleaned['Form'] = zip(*data_cleaned['Generic Description'].apply(split_description))
    data_cleaned.drop(columns=['Generic Description'], inplace=True)

    # Removing rows where 'Generic Name' is empty or whitespace
    data_cleaned = data_cleaned[data_cleaned['Generic Name'].str.strip() != '']

    # Function to split the description into name and size
    def split_description_on_number(desc):
        match = re.search(r'\d', desc)
        if match:
            index = match.start()
            return desc[:index].strip(), desc[index:].strip()
        else:
            return desc, ''

    # Applying the function to split 'Description'
    data_cleaned['Name'], data_cleaned['Size'] = zip(*data_cleaned['Description'].apply(split_description_on_number))
    data_cleaned.drop(columns=['Description'], inplace=True)

    return data_cleaned
