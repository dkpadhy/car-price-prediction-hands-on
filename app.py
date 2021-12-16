from flask import Flask, render_template, request
import jsonify
#import requests
import pickle
import numpy as np
#import sklearn
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)
model = pickle.load(open('insurance_product_prediction_regression_model.pkl', 'rb'))
@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')


standard_to = StandardScaler()
@app.route("/predict", methods=['POST'])
def predict():
    Fuel_Type_Diesel=0
    gender_Male=0
    marital_status_M=0
    marital_status_U=0
    #marital_status_D=0
    products=['','Auto Insurance','Home Insurance','Life Insurance','Health & Accident Insurance','Senior Citizen Health Insurance']

    if request.method == 'POST':
        age = int(request.form['age'])
        gender_Male=request.form['gender_Male']
#        Kms_Driven=int(request.form['Kms_Driven'])
#        Kms_Driven2=np.log(Kms_Driven)
#        Owner=int(request.form['Owner'])
        gender_MaleS=request.form['gender_Male']
        if(gender_MaleS=='Male'):
                gender_Male=1
        else:
            gender_Male=0
        #marital_status_M
        marital_status_MS=request.form['marital_status_M']
        if(marital_status_MS=='M'):
            marital_status_M=1
            marital_status_U=0
            #marital_status_D=0
        elif (marital_status_MS=='U'):
            marital_status_M=0
            marital_status_U=1
            #marital_status_D=0
        else:
            marital_status_M=0
            marital_status_U=0
            #marital_status_D=1
#annual_income(L)
        annual_income=float(request.form['annual_income(L)'])

#        prediction=model.predict([[age,gender_Male,marital_status_M,marital_status_U,annual_income]])
        prediction=model.predict([[age,annual_income,gender_Male]])

        #output=round(prediction)
        output=np.round(prediction)
        
        if output<0:
            return render_template('index.html',prediction_texts="Sorry you cannot sell this car")
        else:
            return render_template('index.html',prediction_text="Prediction {} Output {} Your policy Prediction is {}".format(prediction,output,products[int(output)]))
    else:
        return render_template('index.html')

@app.route("/unqorkPredict", methods=['POST'])
def unqorkPredict():
    print("|*********************STARTING PROCESSING*********************|");
    data = request.get_json()
    print(data)
    products=['','an Auto Insurance','a Home Insurance','a Life Insurance','a Health & Accident Insurance','a Senior Citizen Health Insurance']
    age = data['age']
    gender_MaleS=data['gender']
    if(gender_MaleS=='Male'):
            gender_Male=1
    else:
        gender_Male=0
    #marital_status_M
    marital_status_MS=data['marital_status']
    annual_income=float(data['annual_income'])
# =============================================================================
#     if(marital_status_MS=='M'):
#         marital_status_M=1
#         marital_status_U=0
#         #marital_status_D=0
#     elif (marital_status_MS=='U'):
#         marital_status_M=0
#         marital_status_U=1
#         #marital_status_D=0
#     else:
#         marital_status_M=0
#         marital_status_U=0
#         #marital_status_D=1
# =============================================================================

#        prediction=model.predict([[age,gender_Male,marital_status_M,marital_status_U,annual_income]])
    prediction=model.predict([[age,annual_income,gender_Male]])

    output=np.round(prediction)
    
    if output<0:
        return  jsonify("DATA INCONSISTENCY!!!") 
    else:
        prediction_text="Prediction {}. Output {}. Analytical Data Suggests {} For You.".format(prediction,output,products[int(output)])
        return prediction_text
    


if __name__=="__main__":
    app.run(debug=True)

