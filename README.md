#Project Name
Address Book Application

An address book application where users can create, update and delete their addresses. Users can also retrieve the addresses that are within a given distance and location coordinates.
The address are basically the location coordinates(Latitude & Longitude) and other basic deatils of user like name and email.


#Installation

pip install -r requirements.txt
uvicorn address_book.main:app --reload

Above two commands will start the application, first command will install the necessary project dependencies and the second command will start the service.