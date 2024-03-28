import pandas as pd

from Analysis.ExactDrugAlgoFunction import ExactDrugAlgoFunction
from Analysis.getReplacements import getReplacements
from Analysis.CleanData import cleanData


def replacements(number, isMultiple=False):
    filename = 'Analysis/Daily Snapshot.csv'

    # Clean the data
    data_cleaned = cleanData(filename)

    # Similarity
    data, input = ExactDrugAlgoFunction(number, data_cleaned)

    # get replacements
    replacements = getReplacements(input, data, isMultiple)

    # JSON format
    replacements = replacements.to_json(orient='records')
    
    return replacements
