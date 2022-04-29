### Koffie Labs Backend Challenge

Using _Python 3.10.4_ and built-in SQLite database

To run:

```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app/main.py
```

Documentation available at http://localhost:8000/docs/

To run the automated tests, make sure the server is running and execute `./schemathesis.sh` in your terminal.

Several areas of this application that would be refined if it were to be used in production (and if I had more time to work on it):

- More robust error handling and tracing in the event that any communication with the NHTSA API or the database failed.
- Improved parsing of the JSON response returned from the NHTSA API.
- Unit test and integration testing, hooked into the deployment pipeline via CI to ensure no breaking changes would be introduced during merges.
- Better OpenAPI documentation.

For deployment, the simplest approach would be deploying it onto AWS Lambda as a serverless application. I would not opt to use SQLite as the database solution for a production deployment, instead using Amazon RDS and utilizing CloudFormation to formalize the provisioning of these resources.
