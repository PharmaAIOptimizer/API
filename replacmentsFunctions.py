import pandas as pd

from Analysis.ExactDrugAlgoFunction import ExactDrugAlgoFunction
from Analysis.getReplacements import getReplacements
from Analysis.CleanData import cleanData
from Analysis.AddPrice import addPriceAverage
from historyFunctions import insertHistory


def replacements(sessionCookie, number, isMultiple=False, w1=0.34, w2=0.33, w3=0.33):
    filename = 'Analysis/Daily Snapshot.csv'

    # Clean the data
    data_cleaned = cleanData(filename)

    # Similarity
    data, input = ExactDrugAlgoFunction(number, data_cleaned)

    # get replacements
    replacements = getReplacements(input, data, isMultiple)

    # Add the average price
    replacements = addPriceAverage(w1, w2, w3, replacements)

    # JSON format
    replacements = replacements.to_json(orient='records')

    # Save the history
    insertHistory(sessionCookie, number, w1, w2, w3, replacements)
    
    return replacements
