# flask-signatures

This is a process improvement application to better manage our company email signatures. 

##Current Status

Most issues with the template have been fixed. Some email composers (Native macOS email application) are still a bit tricky. Mobile phone/tablet signatures still need some tweaking. Gmail and Front work great. 

Currently, I have created an application using vanilla JavaScript that allows a user to enter information into a form, and download a signature for specific employees.

##Future Plans

My plan is to build a fully functional web application complete with a RESTful API/relational database to manipulate user signatures as we see fit. Possible integration with Google's Gmail API to simplify the process even further has been considered, although that remains to be seen.

The back-end (API and database) is currently in the works. The technologies I am using for this are Python, Flask micro-framework, SQLAlchemy, with a SQLite database. I already have basic CRUD (Create, Read, Update, and Delete) functionality to add/remove employees, but uploading a CSV file to bulk upload a company directory would be incredibly useful. Bulk deletion would be helpful as well.

The plan for the front-end is to build it out using React. I will begin this when I have a robust back-end to ensure minimal refactoring in the future. 
