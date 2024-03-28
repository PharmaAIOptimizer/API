import pandas as pd

def addPriceAverage(w1, w2, w3, replacements):
    #Calculate the average price
    replacements['Average Price'] = (w1 * replacements['AWP Price'] + w2 * replacements['Acquisition Price'] + w3 * replacements['WAC Price']) / (w1 + w2 + w3)

    #Sort the replacements by the average price
    replacements = replacements.sort_values(by='Average Price')

    return replacements