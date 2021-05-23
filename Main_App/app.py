from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField
from modules import gen_py_db
import pandas as pd

from modules import gen_qr, exe_py_proc, get_id

import json
import qrcode
import pyodbc





app = Flask(__name__)

# Flask-WTF requires an enryption key - the string can be anything
app.config['SECRET_KEY'] = 'C2HWGVoMGfNTBsrYQg8EcMrdTimkZfAb'

# Flask-Bootstrap requires this line
Bootstrap(app)

# with Flask-WTF, each web form is represented by a class
# "NameForm" can change; "(FlaskForm)" cannot
# see the route for "/" and "index.html" to see how this is used

# all Flask routes below


@app.route('/', methods=['GET', 'POST'])
def index():
    
    
        if request.method == "POST":
            #On Form Submit
            req = request.form
    
            Quantity = req.get("Quantity")
            direction = req.get("direction")
            
            if(direction == "+"):
                direction = "1"
            else:
                direction = "0"
            
            Build_Send = req.get("Build_Send")
            Warranty_ID = req.get("Warranty ID")
            name = req.get("Item_name")
            Type = req.get("type")
            
            ID = str(get_id(name, Type))
            
            print(Quantity)
            print(direction)
            print(Build_Send)
            print(Warranty_ID)
            print(name)
            print(Type)
            print(ID)
            
            Quantity= Quantity
            direction = direction
            
            #Need to figure this out later
            Warranty_ID = Warranty_ID
            
            exe_py_proc(Type, ID, Quantity, direction, Build_Send)
            #Trigger the stored procs

        #Gen build py script
        gen_py_db("Select * from dbo.Build", "build_data.py", "DB_write")
        
        #Gen component py script
        gen_py_db("Select * from dbo.Components", "component_data.py", "DB_write")
        
        
        Build_name = gen_py_db("Select * from dbo.Build", "build_data.py", "Get_Name")
        #Generate build label
        Type_1 = ["Inventory"] * len(Build_name)
        
        Component_name = gen_py_db("Select * from dbo.Components", "component_data.py", "Get_Name")
        #Generate component label
        Type_2 = ["Component"] * len(Component_name)
        
        names = Build_name + Component_name
        types = Type_1 + Type_2
        
        dropdown_df = pd.DataFrame(list(zip(names, types)), 
                   columns =['names', 'types']) 
    
        
        class NameForm(FlaskForm):
            name = SelectField(label = 'Possible Builds or Components are listed below', choices=dropdown_df['names'])
            submit = SubmitField('Submit')
        # you must tell the variable 'form' what you named the class, above
        # 'form' is the variable name used in this template: index.html
        form = NameForm()
        message = ""
        if form.validate_on_submit():
            name = form.name.data
            
            print(dropdown_df[dropdown_df['types'] == 'Component']['names'].tolist())
            print(dropdown_df[dropdown_df['types'] == 'Inventory']['names'].tolist())
            
            
            if name in dropdown_df[dropdown_df['types'] == 'Component']['names'].tolist():
                return redirect(url_for('input', name=name, type="Component"))
            elif name in dropdown_df[dropdown_df['types'] == 'Inventory']['names'].tolist():
                return redirect(url_for('input', name=name, type="Inventory"))
            else:
                message = "Build or Component does not exist in database."
        return render_template('index.html', names=names, form=form, message=message)

    
@app.route('/input/<name>/<type>', methods=["GET", "POST"])
def input(name, type):
    
    
    
    
    # run function to get actor data based on the id in the path
    if(type == "Inventory"):
        image_url = "/static/Inventory/"
        
    elif(type == "Component"):
        image_url = "/static/Component/"
       

    #image_url = img_base + name + ".jpg"
    image_name =  name + ".jpg"
    
    path_url = ""
    
    print(image_url)
    
    gen_qr(image_name, image_url, path_url)
    
    if name == "Unknown":
        # redirect the browser to the error template
        return render_template('404.html'), 404
    elif(type == "Inventory"):
        # pass all the data for the selected actor to the template
        return render_template('Inventory.html', name=name, qr= image_url + image_name)
    elif(type == "Component"):
        # pass all the data for the selected actor to the template
        return render_template('Component.html', name=name, qr= image_url + image_name)
    else:
        # redirect the browser to the error template
        return render_template('404.html'), 404
    
    
# 2 routes to handle errors - they have templates too

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/output', methods=['GET', 'POST'])
def output():
        
    if request.method == "POST":
            req = request.form
        
            Quantity = req.get("Quantity")
            direction = req.get("direction")
            Build_Send = req.get("Build_Send")
            Warranty_ID = req.get("Warranty ID")
            
            print(Quantity)
            print(direction)
            print(Build_Send)
            print(Warranty_ID)
        
            return redirect(request.url)
    else:
        return render_template('index.html'), 404
    


# keep this as is
if __name__ == '__main__':
    app.run(debug=True)
