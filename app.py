from flask import Flask, request, render_template
import pandas as pd
import numpy
import pickle
from babel.numbers import format_currency

data = pd.read_csv("cleaned_data.csv")
model = pickle.load(open('model.pkl','rb'))


app = Flask(__name__)


#flask app
@app.route('/')
def index():
    Item_Identifier = sorted(data['Item_Identifier'].unique())
    Item_Fat_Content = sorted(data['Item_Fat_Content'].unique())
    Item_Type = sorted(data['Item_Type'].unique())
    Outlet_Size = sorted(data['Outlet_Size'].unique())
    Outlet_Identifier = sorted(data['Outlet_Identifier'].unique())
    Outlet_Location_Type = sorted(data['Outlet_Location_Type'].unique())
    Outlet_Type = sorted(data['Outlet_Type'].unique())

    return render_template('index.html', Item_Identifier = Item_Identifier, Item_Fat_Content = Item_Fat_Content,
                            Item_Type = Item_Type,Outlet_Identifier = Outlet_Identifier,
                            Outlet_Size = Outlet_Size, Outlet_Location_Type = Outlet_Location_Type,
                            Outlet_Type = Outlet_Type)


@app.route('/predict', methods = ['POST'])
def predict():
    Product_ID = request.form.get('Product_ID')
    Product_weight = request.form.get('Product_weight')
    Product_fat_content = request.form.get('Product_fat_content')
    Product_visibility = request.form.get('Product_visibility')
    Product_type = request.form.get('Product_type')
    Product_MRP = request.form.get('Product_MRP')
    Outlet_ID = request.form.get('Outlet_ID')
    Outlet_Size = request.form.get('Outlet_Size')
    Outlet_Location_Type = request.form.get('Outlet_Location_Type')
    Outlet_Type = request.form.get('Outlet_Type')

    

    if not all([Product_ID, Product_weight,Product_fat_content, Product_visibility, Product_type, Product_MRP,
                Outlet_ID, Outlet_Size, Outlet_Location_Type, Outlet_Type]):
        return "ERROR: Please fill all fields before submitting."
    else:
        store_age = data.loc[data['Outlet_Identifier'] == Outlet_ID, 'store_age'].iloc[0]
        prediction = model.predict(pd.DataFrame([[Product_ID, Product_weight, Product_fat_content, 
                                              Product_visibility, Product_type, Product_MRP, Outlet_ID, 
                                              Outlet_Size, Outlet_Location_Type, Outlet_Type, store_age]],
                                             columns=['Item_Identifier', 'Item_Weight', 'Item_Fat_Content',
                                                       'Item_Visibility', 'Item_Type', 'Item_MRP', 
                                                       'Outlet_Identifier', 'Outlet_Size',
                                                        'Outlet_Location_Type', 'Outlet_Type', 'store_age']))

        return format_currency(prediction[0], 'INR', locale='en_IN')


