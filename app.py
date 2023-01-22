from flask import Flask, request, render_template

import requests
import validators

app = Flask(__name__, static_folder='staticFiles')

def getSummary(article):
    # Define the API endpoint and API key
    base_url = "https://api.smmry.com"
    API_KEY = "33DB752F19"
    response = None
    params = { "SM_API_KEY": API_KEY }

    if validators.url(article):
        params["SM_URL"] = article
        # Make the API request
        response = requests.get(base_url, params=params)
    else:
        data = { "sm_api_input": article }
        header_params = {"Expect":"100-continue"}
        # Make the API request
        response = requests.post(base_url, params=params, data=data, headers=header_params)

    # Get the summary from the response
    summary = response.json()["sm_api_content"]
    
    return summary

@app.route("/")
def hello_world():
    return render_template('home.html')

@app.post('/submit')
def submit():
    articleText= request.form['articlee']
    summary=getSummary(articleText)
    return render_template('home.html', summary=summary, articleText=articleText)


if __name__=='__main__':
    app.run(debug = True)