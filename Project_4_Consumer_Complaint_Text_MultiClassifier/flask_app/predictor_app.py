from flask import Flask, render_template, url_for, request
from predictor_api import make_classification


app = Flask(__name__)

# An example of routing:
# If they go to the page "/" (this means a GET request
# to go to the page httP://127.0.0.1:5000/)

# GET method is the type of request your web browser will send the website
# When it accesses the URL of the web page
@app.route("/")
def hello():
    return "It's alive!!!"


@app.route('/predict', methods=["GET", "POST"])
def predict():
    print(request.args)
    # This is a dictionary (JSON) object that contains 
    # the information submitted when someone clicks the ‘Submit’ button on our form.
    

    if (request.args):
        # request.args contains all the arguments passed by our form.
        # Comes built in with flask.
        # It is a dictionary of the form
        # "form name (as set in templatle)"
        # (key): "string in the textbox" (value)

        # by using request.args.get('chat_in'), it will take the 'name (key), "chat_in"' from the input button in the html file
        # and then it will take the associated value of "chat_in"
        x_input, category_prediction, list_of_pred_probs_dict = \
            make_classification(request.args.get('chat_in')) # if key doesn't exist, returns None

        return render_template('predictor.html', x_input=x_input, 
                                                cat_prediction = category_prediction, 
                                                prediction = list_of_pred_probs_dict)
    
    else:
        # For the first load, request.args will be an 
        # empty ImmutableDict type
        # If this is the case we need to pass an empty string
        # into make_classification function so no errors are thrown.
        x_input, category_prediction, list_of_pred_probs_dict = make_classification('') 
        category_prediction = 'I think you are concerned about...'
        for dictionary in list_of_pred_probs_dict:
            for key, val in dictionary.items():
                dictionary[key] = '--'

        return render_template('predictor.html', x_input=x_input, 
                                                 cat_prediction=category_prediction, 
                                                 prediction = list_of_pred_probs_dict)


# Start the server, continuously listen to requests

if __name__ == '__main__':
    # For local development, set to True:
    app.run(debug=True)

    # For public web serving:
    # app.run(host='0.0.0.0')
    # app.run()
