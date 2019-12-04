# predictor_api.py - contains functions to run model
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import numpy as np
import pandas as pd
import pickle

def raw_complaint_to_model_input(raw_input_string):
    ## KeyNote: request.args gives you an Immutable Dictionary with a key: value pair of what the user inputs into the form
    ## The input here has to be a raw string! Therefore, use a request.get('chat_in') to get the value from the name button
    # Converts string into cleaned and vectorized text, converts it to model input
    with open('data/fitted_tfidf_to_use.pickle', 'rb') as to_read:
        fitted_tfidf_to_use = pickle.load(to_read)  # Pickled file is a Tfidf object already fitted with training data
    # importing TfidfVectorizer will allow you to call the methods off the pickled trained TfidfVectorizer
    return fitted_tfidf_to_use.transform([raw_input_string]) 


def make_classification(raw_input_string):
    '''
    Given string to classify, returns the input argument and the    
    dictionary of model classifications in a dict so that it may be
    passed back to the HTML page.
    '''
    # Takes in a user input string, makes a classification
    model_input = raw_complaint_to_model_input(raw_input_string)

    # Load pre-trained Logistic Regression Model
    with open('data/logit_finalized.pickle', 'rb') as to_read:
        logit_finalized = pickle.load(to_read) 

    # Save model outputs    
    # Save the prediction of the most probable category 
    classification_prediction = logit_finalized.predict(model_input) + '!'

    # The following two lines returns a list of classes and prediction probabilities that have the same respective indexes
    pred_probs = logit_finalized.predict_proba(model_input).flat # Returns a <numpy.flatiter at 0x1a2e5fe54f0> of which can be indexed
    classification_classes = logit_finalized.classes_  # Returns a list of classes in the classifier

    # A list of dictionaries sorted by highest prediction probability
    list_of_pred_probs_dict = [{'name': classification_classes[index], 'prob': round(100 * pred_probs[index], 2)}
                                for index in np.argsort(pred_probs)[::-1]]

    return (raw_input_string, classification_prediction[0], list_of_pred_probs_dict)