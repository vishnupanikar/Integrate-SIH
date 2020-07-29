# Integrate-SIH
Add .flaskenv file in the parent directory
Inside .flaskenv add the following contents:
FLASK_APP=application.py
FLASK_DEBUG=1
FLASK_ENV=development

Note that debug and environment are used here because this is a development server
For deployment do not set debug and environment
