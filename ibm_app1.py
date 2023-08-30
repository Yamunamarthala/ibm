import numpy as np
from flask import Flask, render_template,request
app = Flask(__name__)
import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "<Mk9HuwpSArs9lA9C9RQieYRaueuxyEWznF10pAwimNYD>"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=["GET", "POST"])
def predict():
    ssc_p = float(request.form.get('ssc_p'))
    hsc_p = float(request.form.get('hsc_p'))
    degree_p = float(request.form.get('degree_p'))
    etest_p = float(request.form.get('etest_p'))
    mba_p = float(request.form.get('mba_p'))
    if output == 1:
        out = 'You have high chances of getting placed!!!'
    else:
        out = 'You have low chances of getting placed. All the best.'
        
    
    arr = np.array([[ssc_p, hsc_p,  degree_p,  etest_p, mba_p]])
    brr=np.asarray(arr,dtype=float)
    



    # NOTE: manually define and pass the array(s) of values to be scored in the next line
    payload_scoring = {"input_data": [{"fields": [ssc_p, hsc_p,  degree_p,  etest_p, mba_p
    ], "values": [arr]}]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/6bfdaa4f-cd0c-4b41-9165-99c6d3bf1e6c/predictions?version=2021-05-01', json=payload_scoring,
    headers={'Authorization': 'Bearer ' + mltoken})
    print("response_scoring ")
    predictions =response_scoring.json()
    output =predictions['predictions'][0]['value'][0][0]
    print("Final prediction :",output)

    print(output)
    return render_template('out.html', output=out) 


if __name__ == '__main__':
    app.run(debug=True)