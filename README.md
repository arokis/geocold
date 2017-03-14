# geocold
geographic coordinates from linked data

## before you start
install required libs:
- pip install rdflib
- pip install flask
- pip install flask_cors

## running web-app
To run the web-app you need to start the server first:
- go to /app
- run app.py (python app.py) from commandline
- check IP and port
- type <IP:PORT> as URL to your browser (e.g. localhost:5000)

## folders and files
- "app": python files representing the applications core#
- "app/app.py": the main-file routing the application
- "app/geocold.py": the logic-file with the main-classes and -functions
- "app/templates": all html-files used for templating the webpage
- "app/static": css, js, img
- "data": test-data
- "doc": some files with add info and ideas
- "maplib": maplib khtml-osm-api example
