# Python RDF Converter
Log to RDF converter. Used to provide data for a Machine Learning fraud detection system.

This application listens on the `/api/convert` endpoint for json logs, and then writes the touples in a GraphDB repository.

# How to use it:
Submit a POST request to the endpoint `/api/convert` with this form of json body:
```
{
    "time": "",
    "userFullName": "",
    "affectedUser": "",
    "eventContext": "",
    "component": "",
    "eventName": "",
    "description": "",
    "origin": "",
    "ipAddress": ""
}
```
