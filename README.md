
# QR_ERP: Automated Cloud Based Inventory Control



QR ERP is a product demo for a cloud based QR scanning system. Small manufacturing facilities need an inventory tracking solution that is lightweight, fast, and accessible without all the expensive bells and whistles that large ERPs typically come with. With our setup, small manufacturing factories can print QRcodes as action modules and auto-increment inventory, reconcillate warehouse stock, and create full builds via Bill of Materials with their phone! The Azure SQL solution also makes it easy to maintain and keep track of existing tables to update future functionality. This provides an end-to-end inventory, warehouse, and logistics solution within a single hosted azure app (Figure 1)

Figure 1: End to End Inventory flow
<img width="863" alt="QR ERP BG" src="https://user-images.githubusercontent.com/16582383/118562065-df697900-b720-11eb-9fa6-c8a76dfc289c.PNG">

To run the flask app, clone the repo and run app.py inside the main App folder. A cloud database setup comes with a bit more work. To begin you need an azure account. Contact cloud@optimchain.org to see how we can help you setup your backend! (Figure 2)

Figure 2: Front end app interface

![image](https://user-images.githubusercontent.com/16582383/118562976-974b5600-b722-11eb-85da-b22b557fa781.png)




At it's core, QR ERP comes with the following set of features:

	* Backend Azure System with different Azure SQL tables
	* Front-end triggerable stored procs to manipulate Azure SQL tables
	* Auto QR generation to trigger front-end app for incrementing inventory
	* DataFeed into excel to see on-hand inventory


Repo: <https://github.com/IamJasonBian/QR_ERP>

Demo Slide: <https://github.com/IamJasonBian/QR_ERP/blob/master/QR-ERP-Manufacturing%20Implementation.pptx>

Demo Site (Please wait 60 seconds for it to load as we are using a small VM): <https://qr-app-test.azurewebsites.net>
