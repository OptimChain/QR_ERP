# -*- coding: utf-8 -*-
"""
Created on Tue Dec 29 15:57:47 2020

@author: Jason
"""

import pyodbc
 #Write SQL database into json location
server = 'qrinventory.database.windows.net' 
database = 'Main' 
username = 'qr@umich.edu@qrinventory' 
password = 'ScrambledEggs73' 

cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()
cursor.execute("exec Build_proc 1, 3, 1")
cnxn.commit()