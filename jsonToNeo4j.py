import sys
import json
from dbConfig import dbConfig
from neomodel import db
db.set_connection(f'bolt://{dbConfig["username"]}:{dbConfig["password"]}@{dbConfig["addr"]}:{dbConfig["port"]}')

from neomodel import StructuredNode, StructuredRel, StringProperty, IntegerProperty, FloatProperty, RelationshipTo

class ProteinLink(StructuredRel):
    value = IntegerProperty(required=True)

class Protein(StructuredNode):
    proteinId = StringProperty(unique_index=True, required=True)
    name = StringProperty(unique_index=True, required=True)
    group = IntegerProperty()
    score = FloatProperty(required=True)
    target = RelationshipTo('Protein', 'TARGET', model=ProteinLink)

def main():
    if len(sys.argv[1:]) != 1:
        sys.stderr.write('Wrong number of inputs. Please provide a filename to the desired json file.\n')
    filename = sys.argv[1]

    with open(filename) as f:
        data = json.load(f)
    
    nodes = data['nodes']
    links = data['links']

    for node in nodes:
        _ = Protein(proteinId = node['id'], name = node['protein'], group = node['group'], score = node['score']).save()
    
    for link in links:
        sourceProtein = Protein.nodes.get_or_none(proteinId = link['source'])
        targetProtein = Protein.nodes.get_or_none(proteinId = link['target'])
        _ = sourceProtein.target.connect(targetProtein, {'value': link['value']}).save()

if __name__ == '__main__':
    main()
