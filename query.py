import rdflib
import pprint


'''
g = rdflib.Graph()
has_border_with = rdflib.term.URIRef('http://www.example.org/has_border_with')
located_in = rdflib.term.URIRef('http://www.example.org/located_in')

germany = rdflib.term.BNode('germany')
france = rdflib.term.BNode('france')
china = rdflib.term.BNode('china')
mongolia = rdflib.term.BNode('mongolia')

europa = rdflib.term.URIRef('http://www.example.org/part1')
asia = rdflib.term.URIRef('http://www.example.org/part2')
print type(asia)
g.add((germany, has_border_with, france))
g.add((china, has_border_with, mongolia))
g.add((germany, located_in, europa))
g.add((france, located_in, europa))
g.add((china, located_in, asia))
g.add((mongolia, located_in, asia))

for subj, pred, obj in g:
    print subj,pred,obj
'''
question = 'when Apple releases Ipad4, the stock of which support company increase most?'
q = "SELECT ?support ?p  " \
    "WHERE   " \
    "{ " \
    "?c <http://www.example.org/support> ?support . " \
    "?c <http://www.example.org/name> \"Apple\". " \
    "?event <http://www.example.org/subject> \"Apple\" ." \
    "?event <http://www.example.org/trigger> \"release\" ." \
    "?event <http://www.example.org/object> \"ipad4\" ." \
    "?event <http://www.example.org/time>  ?t." \
    "?supportnode <http://www.example.org/name>  ?support." \
    "?supportnode <http://www.example.org/stock>  ?stock." \
    "?stock <http://www.example.org/stocktime>  ?t." \
    "?stock <http://www.example.org/price>  ?p" \
    " }"
#x = g.query(q)
#print list(x)
# write graph to file, re-read it and query the newly created graph
#g.serialize("graph.rdf",format='nt')

g1 = rdflib.Graph()
g1.parse("graph.rdf", format='nt')
for subj, pred, obj in g1.triples((None,None,None)):

#for stmt in g1:
    #pprint.pprint(stmt)
    print subj,pred,obj
   # print  subj.__all__
x1 = g1.query(q)
print type(str(list(x1)[0][0]))
print list(x1)

