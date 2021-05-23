from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField
from modules import gen_py_db


from modules import get_names, get_actor, get_id

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
    
    #QR Codes goes here
    
    #Gen build py script
    gen_py_db("Select * from dbo.Build", "build_data.py", "DB_write")
    
    #Gen component py script
    gen_py_db("Select * from dbo.Components", "component_data.py", "DB_write")
    
    
    Build_name = gen_py_db("Select * from dbo.Build", "build_data.py", "Get_Name")
    Component_name = gen_py_db("Select * from dbo.Components", "component_data.py", "Get_Name")
    
    columns = Build_name + Component_name
    print(columns)
    

    from build_data import DB as Build_DB
    from component_data import DB as Comp_DB
    
    names = columns

    
    class NameForm(FlaskForm):
        name = SelectField(label = 'Possible Builds or Components are listed below', choices=columns)
        submit = SubmitField('Submit')
    # you must tell the variable 'form' what you named the class, above
    # 'form' is the variable name used in this template: index.html
    form = NameForm()
    message = ""
    if form.validate_on_submit():
        name = form.name.data
        
        if name in names:
            return redirect( url_for('test', name=name, type="Component"))
        elif:
            return redirect( url_for('test', name=name, type="Inventory"))
        else:
            message = "Build or Component does not exist in database."
    return render_template('index.html', names=names, form=form, message=message)

@app.route('/module/<name>/<type>', methods =["GET", "POST"])
def module(name, type):
    
   
    
    from build_data import DB as Build_DB
    from component_data import DB as Comp_DB
    
    # run function to get actor data based on the id in the path
    
    img_base = "/static/"
    
    if(type == "Component"):
        id, name, qr = get_actor(Comp_DB, name, "Component")
    elif(type == "Inventory"):
        id, name, qr = get_actor(Build_DB, name, "Inventory")
    elif name == "Unknown":
        
        # redirect the browser to the error template
        print("404")
        return render_template('404.html'), 404
    else:
        
        
        if request.method == "POST":
            req = request.form
            print(req)
        
            return render_template('actor.html', id=id, name=name, qr= img_base + qr)
        else:
        # pass all the data for the selected actor to the template
            return render_template('actor.html', id=id, name=name, qr= img_base + qr)
    
@app.route('/test/<name>/<type>')
def test(name, type):
    from build_data import DB as Build_DB
    from component_data import DB as Comp_DB
    
    # run function to get actor data based on the id in the path
    
    img_base = "/static/"
    
    id = 1
    name = "Leather Grip Rubber (Thick)"
    qr = "qr_InventoryBuild EQUINOX 2.0.jpg"
    
    if name == "Unknown":
        # redirect the browser to the error template
        return render_template('404.html'), 404
    else:
        # pass all the data for the selected actor to the template
        return render_template('actor.html', id=id, name=name, qr= img_base + qr)
    
    

# 2 routes to handle errors - they have templates too

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


# keep this as is
if __name__ == '__main__':
    app.run(debug=True)
