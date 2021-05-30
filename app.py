from flask import Flask, request
from rdflib.namespace import FOAF, XSD, ClosedNamespace
from rdflib import Graph, Literal, RDF, URIRef, Namespace, RDFS
import re
import json

EDU = ClosedNamespace(
    uri=URIRef('http://elearning.upt.ro/ontology/edu#'),
    terms=[
        'Student', 'viewUsers', 'viewCourse', 'startTest', 'viewTestReport',
        'viewTest', 'startTest', 'submitTest'
    ]
)

EduDate = ClosedNamespace(
    uri=URIRef('http://cv.upt.ro/date#'),
    terms=[]
)

app = Flask(__name__)

@app.route('/api/convert', methods=['POST'])
def convert_rdf():
    # create a Graph
    g = Graph()

    # get json from the request
    json_form_list = request.get_json()

    # convert string to json
    json_list = json.loads(json_form_list)

    for event in json_list:
        eventName = event['Event name']
        userFullName = event['User full name']
        user = event['User full name']
        description = event['Description']

        g.bind("edu", EDU)
        g.bind("date", EduDate)
        g.bind("foaf", FOAF)
        #
        # # parse in an RDF file hosted on the Internet
        # # g.parse("ontologies/person.rdf", format="xml")
        # # g.parse("ontologies/activity.rdf", format="xml")
        # # g.parse("ontologies/course.rdf", format="xml")
        #
        user = URIRef(f'http://cv.upt.ro/date#{userFullName}')
        g.add((user, RDF.type, EDU.Student))
        g.add((user, FOAF.name, Literal(userFullName)))
        #
        #
        if eventName == 'User profile viewed':
            # Extract the info from description
            result = re.findall('\*{2}(.*?)\*{2}', description)

            user_who_viewed = result[0]
            viewed_user = result[1]
            the_student_who_viewed = URIRef(f'http://cv.upt.ro/date#{user_who_viewed}')
            the_viewed_student = URIRef(f'http://cv.upt.ro/date#{viewed_user}')
            g.add((the_student_who_viewed, EDU.viewUsers, the_viewed_student))

        if eventName == 'Course viewed':
            viewed_course = URIRef('http://elearning.upt.ro/ontology/edu#LP2')
            g.add((user, EDU.viewCourse, viewed_course))

        # Quiz cases
        if eventName == 'Quiz attempt started':
            asterix_split = re.findall('\*{2}(.*?)\*{2}', description)
            user_who_started_test = result[0]
            quote_split = re.findall(r"'(.*?)'", description)
            g.add((user, EDU.startTest, ))

        if eventName == 'Quiz attempt viewed':
            asterix_split = re.findall('\*{2}(.*?)\*{2}', description)
            quote_split = re.findall(r"'(.*?)'", description)

    # return the Graph in the RDF Turtle format
    return g.serialize(format="turtle").decode("utf-8")


if __name__ == '__main__':
    app.run()
