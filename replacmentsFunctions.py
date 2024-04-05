import pandas as pd
import os

from Analysis.ExactDrugAlgoFunction import ExactDrugAlgoFunction
from Analysis.getReplacements import getReplacements
from Analysis.CleanData import cleanData
from Analysis.AddPrice import addPriceAverage
from historyFunctions import insertHistory
from s3Functions import download_file, find_object_with_highest_number


def replacements(sessionCookie, number, isMultiple=False, w1=0.34, w2=0.33, w3=0.33):
    # Find latest snapshot in S3 bucket
    objectName = find_object_with_highest_number('dailysupplysnapshot')
    
    # Download file from S3
    download_file('dailysupplysnapshot', objectName, 'snapshot.csv')
    filename = 'snapshot.csv'

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
    insertHistory(sessionCookie, number, w1, w2, w3, replacements, isMultiple)

    # Remove file
    os.remove(filename)
    
    return replacements
