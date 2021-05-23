# functions to be used by the routes

# retrieve all the names from the dataset and put them into a list
def get_names(source):
    names = []
    for row in source:
        # lowercase all the names for better searching
        name = row["Name"].lower()
        names.append(name)
    return sorted(names)

# find the row that matches the id in the URL, retrieve name and photo
def gen_qr(image_name, image_url, path_url):
    import qrcode
    import os
    from pathlib import Path
    
    img = qrcode.make(image_name)
        
    #add site url here
    img.save(image_name)
    
    #Delete QR if exists
    if os.path.exists("." + image_url + image_name):
        os.remove("." + image_url + image_name)
    
    #Move image to static location
    Path(image_name).rename("." + image_url + image_name)
        
    # return these if id is not valid - not a great solution, but simple
    return "QR_Generated"

# find QR codes
def get_id(name, Type):
    from build_data import DB as build_db
    from component_data import DB as component_db
    
    
    print("Extracting ID")
    ID = 0
    
    if(Type=="Component"):
        for row in component_db:
            if name == row['Name']:
                ID = row['Component ID']
    elif(Type=="Inventory"):
       for row in build_db:
            if name == row['Name']:
                ID = row['Inventory ID']
            
    else:
        print("Type not found")
        return()
        
    return(ID)
    



#Used to write local string text files
def line_prepender(filename, line):
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0,0)
        f.write(line.rstrip('\r') + content)

#Create local .py files
def gen_py_db(Query, output, Type):
    import pyodbc
    import json

    print("Starting Server Connection")
        
    #Write SQL database into json location
    server = 'qrinventory.database.windows.net' 
    database = 'Main' 
    username = 'qr@umich.edu@qrinventory' 
    password = 'ScrambledEggs73' 
    
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = cnxn.cursor().execute(Query)
    
    
    if(Type == "DB_write"):
    
        columns = [column[0] for column in cursor.description]
        
        #Write local validation code
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
           
        
        with open(output, "w") as write_file:
            json.dump(results, write_file)
            
        line_prepender(output, "DB = ")
        
    elif(Type == "Get_Name"):
        if (output == "build_data.py"):
            selection = []
            for row in cursor.fetchall():
                selection.append(row[1])
        elif (output == "component_data.py"):
            selection = []
            for row in cursor.fetchall():
                selection.append(row[0])
        return(selection)
        
    return "done"

def exe_py_proc(Type, ID, Quantity, direction, Build_Send):
    import pyodbc

    print("Executing Stored Proc")
        
    #Write SQL database into json location
    server = 'qrinventory.database.windows.net' 
    database = 'Main' 
    username = 'qr@umich.edu@qrinventory' 
    password = 'ScrambledEggs73' 
    
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = cnxn.cursor()
    
    
    if(Type=="Inventory"):
        if(Build_Send=="Build"):
            cursor.execute("exec Build_proc " + ID + "," + Quantity + "," + direction)
        elif(Build_Send=="Send"):
            cursor.execute("exec Send_proc " + ID + "," + Quantity + "," + direction)
        else:
            print("Build/Send is non-existant")
    elif(Type=="Component"):
        cursor.execute("exec Increment_Component_proc " + ID + "," + Quantity + "," + direction)
    else:
        print("Stored Proc Type is non-existant")
        
    #Send stored proc execution
    cnxn.commit()
    
    return("Complete")
    
    