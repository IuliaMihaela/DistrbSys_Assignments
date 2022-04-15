WEB SERVICE/ FRAMEWORK


WHY WE CHOSE REST?

- Compared to gRPC and SOAP we are more familiar with REST which we worked with during our second semester.
- Rest is more flexible in that it supports a variety of data formats, rather than requiring XML. JSON is easier for us to read and write than XML.
- Rest API’s can also offer better performance than SOAP because they can cache information.
- SOAP messages utilize a lot of bandwidth. So, in case if there might be a problem of resources and bandwidth, REST is a better option. 
- The coding of REST APIs and services is far more seamless than SOAP. 



MODULES
- Flask [Requests, Jsonify]
- Flask_restful [Resource]
- uuid
- Flask_sqlalchemy ( We used it as our permanent storage.)

STRUCTURE
- We have seperated the 2 services [Authentication and master data services] into 2 files that are located into the services directory. 
- In the services directory we also have the __init__ py file that creates the Flask application, loads the configuration and then creates the SQLAlchemy object, passing it to the Flask application.
- In order to create the initial database and its tables, it is needed to import the db from the services and in the Python shell to run the 'db.create_all()' method.
