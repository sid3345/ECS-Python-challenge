"""Routines associated with the application data.
"""
#import json
import pandas as pd

#courses = {}

# Using dataframe to store data from JSON file to in-memory data structure.


def load_data():
    """Load the data from the json file.
    """
    '''
    with open('json/course.json') as f:

        courses = json.load(f)
    '''
    courses = pd.read_json('json/course.json')

    # print(courses[:5])

    return courses
