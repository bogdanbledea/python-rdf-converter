from flask import Flask, request
from rdflib.namespace import FOAF, XSD, ClosedNamespace
from rdflib import Graph, Literal, RDF, URIRef, Namespace

EDU = ClosedNamespace(
    uri=URIRef('http://elearning.upt.ro/ontology/edu#'),
    terms=[
        'Student', 'viewUsers', 'viewCourse'
    ]
)

app = Flask(__name__)

@app.route('/api/convert', methods=['POST'])
def convert_rdf():
    json_form = request.get_json()

    eventName = json_form['eventName']
    user = json_form['userFullName']

    # create a Graph
    g = Graph()

    # parse in an RDF file hosted on the Internet
    g.parse("ontologies/person.rdf", format="xml")
    g.parse("ontologies/activity.rdf", format="xml")
    g.parse("ontologies/course.rdf", format="xml")

    user = URIRef('http://elearning.upt.ro/ontology/edu#BogdanBledea')
    g.add((user, EDU.Student, Literal("Bogdan Bledea")))


    if(eventName == 'User profile viewed'):
        the_viewed_student = URIRef('http://elearning.upt.ro/ontology/edu#VladAlexandra')
        g.add((user, EDU.viewUsers, the_viewed_student))

    if(eventName == 'Course viewed'):
        viewed_course = URIRef('http://elearning.upt.ro/ontology/edu#LP2')
        g.add((user, EDU.viewCourse, viewed_course))

    # return the Graph in the RDF Turtle format
    return g.serialize(format="turtle").decode("utf-8")


if __name__ == '__main__':
    app.run()
