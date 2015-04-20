import sys, os

parent = os.path.dirname(os.path.realpath(__file__))
sys.path.append('/path/to/MITIE-Server') #change path to MITIE top level

import tangelo
import cherrypy
import requests
import json
from mitie import *
from collections import defaultdict
 
#from bottle import Bottle, route, get, post, request, run, response
 
print "loading NER model..."
ner = named_entity_extractor('/path/to/MITIE-server/MITIE-models/english/ner_model.dat')

print "\nTags output by this NER model:", ner.get_possible_ner_tags()


@tangelo.restful
def post(*arg, **kwargs):
    params = json.loads(tangelo.request_body().read())
    text   = params['text']
    ###if text.upper():
    ###        text = text.title()
    tokens = tokenize(text)
    tokens.append(' x ')
    entities = ner.extract_entities(tokens)
    print "\nEntities found:", entities
    out = [];
    for e in entities:
        range = e[0]
        tag = e[1]
        entity_text = " ".join(tokens[i] for i in range)
        out.append({'tag' : tag, 'text' : entity_text})
        print "    " + tag + ": " + entity_text
    for e in reversed(entities):
        range = e[0]
        tag = e[1]
        newt = tokens[range[0]]
        if len(range) > 1:
            for i in range:
                if i != range[0]:
                    print i
                    print tokens[i]
                    newt += ' ' + tokens[i]
        newt = '<span class="mitie-' + tag  + '">' + newt + '</span>'
        tokens = tokens[:range[0]] + [newt] + tokens[(range[-1] + 1):]
    del tokens[-1]
    html = ' '.join(tokens)
    return {"entities" : out, "html" : html}

