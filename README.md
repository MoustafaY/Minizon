# Minizon

The goal of this project was to develope complex relationships between users and products to simulate a functioning ecommerce web application. A user can be a supplier, where a supplier has a one-to-many relationship with products. A supplier can create, update, delete, and send shipments of products to inventory. A user can also be a customer, a customer has a one-to-one relationship with their shopping cart. A customer can add, update, delete or purchase products in their shopping cart. Both supplier and customer would have their history recorded of their shipments and purchases respectively. The project is setup so that it can also be used in the cloud, currently the project can use aws secrets manager to get important credentials such as database username and password to access it's database.

## Technologies used
### Backend
* Flask
* SqlAlchemy

### Frontend
* Reactjs

## Installation of app
To install the web application, have the backend and frontend folders in the same directory, add the flask proxy server in the package.json file in the frontend folder, using the `pip freeze > requirements.txt` command you can install all the necessary libraries for the flask backend. Run the flask server first using `python run main.py` command in the backend folder, then run the `npm start` command in the frontend folder.

## Deployment of app
To deploy the web application in aws, create and deploy the flask backend in elastic beanstalk, edit the frontend api calls to include the calls from elastic beanstalk urls, run the `npm run build` command in the frontend folder, upload frontend folder in an s3 and enable static web hosting. Use the url from the s3 static web hosting.
