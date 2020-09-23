# flask-signatures

This is a process improvement application to better manage our company email signatures. 

## Current Status

Most issues with the template have been fixed. Some email composers (Native macOS email application) are still a bit tricky. Mobile phone/tablet signatures still need some tweaking. Gmail and Front work great. 

## Future Plans

My plan is to build a fully functional web application complete with a RESTful API/relational database to manipulate user signatures as we see fit. Planning to integrate with the Gmail API and our existing GSuite environment to dynamically manage email signatures based on user data.

The back-end (API and database) is currently in the works. The technologies I am using for this are Python, Flask micro-framework, SQLAlchemy, with a SQLite database. I already have basic CRUD (Create, Read, Update, and Delete) functionality to add/remove employees, and a bulk user CSV upload endpoint exists as well.

The plan for the front-end is to build it out using React.
