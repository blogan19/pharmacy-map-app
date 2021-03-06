from flask import Flask, render_template, request, flash
import folium 
import pandas as pd
import numpy as np
from  pharmacies import createPharmacyList
from create_map import create_map


#Creates a class for the app
app = Flask(__name__)
app.secret_key = "pharmmapapp"

@app.route("/")
def index():
    pharmacy_list = createPharmacyList()
    return render_template("index.html",pharmacy_list_data = pharmacy_list)

#Creates the map which is saved as map.html and then displayed in iframe
@app.route("/map", methods=["POST","GET"])
def map():
    pharm_code = request.form['pharm_select']
    distance = request.form.getlist('distance_radio')
    pharm = create_map(pharm_code,int(distance[0]))
    html_map = pharm[2]._repr_html_()

    flash("Selected Pharmacy: " +  pharm[0])
    pharmacy_list = createPharmacyList()
    local_table = pharm[1]
    
    return render_template("index.html",pharmacy_list_data = pharmacy_list, local_table=local_table,html_map=html_map)

#Creates a route to create the iframe to display map
@app.route("/render_map")
def render_map():
    return render_template("map.html")

@app.route("/jupyter")
def jupyter():
    return render_template("jupyter.html")

#app.run(port=5000, debug=True)
