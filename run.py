"""Routes for the course resource.
"""

"""
-------------------------------------------------------------------------
Challenge general notes:
-------------------------------------------------------------------------

1. Bonus points for returning sensible HTTP codes from the API routes
2. Bonus points for efficient code (e.g. title search)
"""


#from run import app
#from routes.course import *
#from routes.course import app_file
#from flask import Flask

import data
import datetime
from data import load_data
from http import HTTPStatus
from flask import request, Blueprint, Flask
import numpy as np
app = Flask(__name__)

# Import the API routes
# app.register_blueprint(app_file)

"""Routes for the course resource.
"""
#import pandas as pd

courses = load_data()

# print(courses[:5])

#app = Blueprint('app', __name__)


@app.route("/course/<int:id>", methods=['GET'])
def get_course(id):
    """Get a course by id.

    :param int id: The record id.
    :return: A single course (see the challenge notes for examples)
    :rtype: object
    """

    """
    -------------------------------------------------------------------------
    Challenge notes:
    -------------------------------------------------------------------------
    1. Bonus points for not using a linear scan on your data structure.
    """
    # YOUR CODE HERE

    #courses = flask.request.json
    #print(courses[courses.id == id])

    return courses[courses.id == id].to_json()


@ app.route("/course", methods=['GET'])
def get_courses(page_number=1, page_size=10, title_words=''):
    """Get a page of courses, optionally filtered by title words (a list of
    words separated by commas".

    Query parameters: page-number, page-size, title-words
    If not present, we use defaults of page-number=1, page-size=10

    :return: A page of courses (see the challenge notes for examples)
    :rtype: object
    """

    """
    -------------------------------------------------------------------------
    Challenge notes:
    -------------------------------------------------------------------------
    1. Bonus points for not using a linear scan, on your data structure, if
       title-words is supplied
    2. Bonus points for returning resulted sorted by the number of words which
       matched, if title-words is supplied.
    3. Bonus points for including performance data on the API, in terms of
       requests/second.
    """
    # YOUR CODE HERE

    title_words = request.args.get('title')
    print(title_words)
    course_ = {}

    if title_words != '':
        each_word = title_words.split()
        print(each_word)
        # for word in each_word:

        course_ = courses[courses.title.str.contains(title_words)]

    else:
        course_ = courses

    return course_.to_json()


@ app.route("/course", methods=['POST'])
def create_course():
    """Create a course.
    :return: The course object (see the challenge notes for examples)
    :rtype: object
    """

    """
    -------------------------------------------------------------------------
    Challenge notes:
    -------------------------------------------------------------------------
    1. Bonus points for validating the POST body fields
    """
    # YOUR CODE HERE

    data = request.get_json(force=True)
    print('data: ', data)

    try:
        description = data['description']
        discount_price = int(data['discount_price'])
        title = data['title']
        price = int(data['price'])
        image_path = data['image_path']
        on_discount = data['on_discount']

        courses.loc[len(courses.index)] = [courses[-1]['id']+1,
                                           datetime.datetime.now(), datetime.datetime.now(), description, discount_price, image_path, on_discount, price, title]
        print('Index length: ', len(courses.index))

        return courses[len(courses.index)].to_json()

    except (KeyError, TypeError, ValueError):
        print('Invalid value.')


@ app.route("/course/<int:id>", methods=['PUT'])
def update_course(id):
    """Update a a course.
    :param int id: The record id.
    :return: The updated course object (see the challenge notes for examples)
    :rtype: object
    """

    """
    -------------------------------------------------------------------------
    Challenge notes:
    -------------------------------------------------------------------------
    1. Bonus points for validating the PUT body fields, including checking
       against the id in the URL

    """
    # YOUR CODE HERE

    data = request.get_json()
    print(data)

    try:
        description = data['description']
        discount_price = int(data['discount_price'])
        title = data['title']
        price = int(data['price'])
        image_path = data['image_path']
        on_discount = data['on_discount']

        courses.loc[courses[courses['id'] == id].index] = [np.nan, np.nan, datetime.datetime.now(),  description,
                                                           discount_price, image_path, on_discount, price, title]
        '''
        index_names = courses[courses['id'] == id].index
        courses.update(new_df)

        courses.at[index_names] += [datetime.datetime.now(),  description,
        discount_price, image_path, on_discount, price, title]
        '''

    except:
        raise 'Id does not match payload'

    return courses[courses['id'] == id].to_json()


@ app.route("/course/<int:id>", methods=['DELETE'])
def delete_course(id):
    """Delete a course
    :return: A confirmation message (see the challenge notes for examples)
    """
    """
    -------------------------------------------------------------------------
    Challenge notes:
    -------------------------------------------------------------------------
    None
    """
    # YOUR CODE HERE
    # if courses[courses['id'] == id].any():
    if id in courses['id']:
        index_names = courses[courses['id'] == id].index
        courses.drop(index_names, inplace=True)

        return 'The specified course was deleted'

    else:
        return 'Course does not exists'


# Required because app is imported in other modules
if __name__ == '__main__':
    '''
    print("Loading data", end=" ")
    data.load_data()
    print("... done")
    '''
    app.run(debug=True)
