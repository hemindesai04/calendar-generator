# calendar-generator
Repository to generate calendar of a specific year containing date-specific information. The calendar is generated in docx format based on a template. This template is based on Jinja2 template framework and is saved in docx format. The date-specific data is parsed from a propritery format generated by a third-party tool. 

### Pre-requisites for running the calendar-generator tool:
1. Create a virtual environment with Python3.8 or above
` %python3 -m venv <path/where/venv/will/be/created>`
2. Activate the newly created virtual environment
` %source <path/where/venv/is/created>/bin/activate`
3. Install requirements from the `requirements.txt` file
` %pip install -r requirements.txt `

### Run the calendar-generator tool to generate monthly calendars using the data and the template:
` %python3 calendar_generator_app.py`

### Questions?
You can reach out to me at hemin_desai04@yahoo.com for any questions.
