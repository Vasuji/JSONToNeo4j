import sys
import json
from dbConfig import dbConfig
from neomodel import db
db.set_connection(
    f'bolt://{dbConfig["username"]}:{dbConfig["password"]}@{dbConfig["addr"]}:{dbConfig["port"]}'
)

from neomodel import (StructuredNode, StructuredRel, StringProperty,
                      IntegerProperty, FloatProperty, Relationship,
                      RelationshipTo, RelationshipFrom)


class PhraseLink(StructuredRel):
    value = FloatProperty(required=True)


class Phrase(StructuredNode):
    phraseId = StringProperty(unique_index=True, required=True)
    name = StringProperty(unique_index=True, required=True)
    phraseType = StringProperty(required=True)
    identical = Relationship('Phrase', 'IDENTICAL', model=PhraseLink)
    overlap = Relationship('Phrase', 'OVERLAP', model=PhraseLink)
    cooccurence = Relationship('Phrase', 'CO-OCCURANCE', model=PhraseLink)
    center = RelationshipFrom('Phrase', 'Center', model=PhraseLink)
    before = RelationshipTo('Phrase', 'BEFORE', model=PhraseLink)
    modify = RelationshipTo('Phrase', 'MODIFY', model=PhraseLink)
    sub_procedure = RelationshipTo('Phrase', 'SUB_PROCEDURE', model=PhraseLink)
    after = RelationshipTo('Phrase', 'AFTER', model=PhraseLink)
    cause = RelationshipTo('Phrase', 'CAUSE', model=PhraseLink)
    decrease_to = RelationshipTo('Phrase', 'DECREASE_TO', model=PhraseLink)
    decrease_from = RelationshipTo('Phrase', 'DECREASE_FROM', model=PhraseLink)
    increase_from = RelationshipTo('Phrase', 'INCREASE_FROM', model=PhraseLink)
    increase_to = RelationshipTo('Phrase', 'INCREASE_TO', model=PhraseLink)


def main():
    if len(sys.argv[1:]) != 1:
        sys.stderr.write(
            'Wrong number of inputs. Please provide a filename to the desired json file.\n'
        )
    filename = sys.argv[1]

    with open(filename) as f:
        data = json.load(f)

    nodes = data['nodes']
    links = data['links']

    for node in nodes:
        _ = Phrase(
            phraseId=node['id'],
            name=node['name'].strip(),
            phraseType=node['type']).save()

    for link in links:
        sourcePhrase = Phrase.nodes.get_or_none(phraseId=link['source'])
        targetPhrase = Phrase.nodes.get_or_none(phraseId=link['target'])

        # get the right type of neo4j relation
        relType = link['name']
        if relType is 'CO-OCCURENCE':
            relType = 'cooccurence'
        else:
            relType = relType.lower()

        # save the relation
        getattr(sourcePhrase, relType).connect(targetPhrase, {
            'value': link['value']
        }).save()


if __name__ == '__main__':
    main()
