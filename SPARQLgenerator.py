# coding=utf-8

import jieba,copy, rdflib
from ActionList import ActionList
from Action import Action
import nltk
from nltk import  StanfordPOSTagger

jieba.load_userdict('./dict.txt')
class ActionListGenerator:
    def __init__(self,sentence, graph):
        self.Construct_Pattern_House()
        self.sentence = sentence
        self.rdfgraph = graph
       # self.sentence = sentence
        self.st = StanfordPOSTagger('chinese-distsim.tagger')
        self.nodecount = dict()

    def Construct_Pattern_House(self):
        self.patterns = []
        self.patterns.append([u'当 (N) (V) (N) 时', 'event'])
        self.patterns.append([u'{哪} () [的]{0,1} (N) [的]{0,1} 股价　{涨幅} [会]{0,1}　[最大|最多]', 'stock_increase'])
        self.patterns.append([u'{哪} (N) 股 [的|将]{0,1} 　{涨} [会]{0,1} [得]{0,1} 　[最大|最多]', 'specific_type_stock_increase'])

    def Generate(self):
        self.words = jieba.cut(self.sentence)
        self.sentence2 = ' '.join(list(self.words))
        self.pos = self.st.tag(self.sentence2.split())

        self.senpos = [(sp.split('#')[0], sp.split('#')[1]) for _, sp in self.pos]
        print self.sentence2
        print self.pos

        self.actions = ActionList(self.rdfgraph)

        for pat in self.patterns:
            self.match(self.senpos, pat[0], pat[1])

        print self.actions

    def GetCount(self, pattype):
        if pattype in self.nodecount:
            ID = self.nodecount[pattype]
            self.nodecount[pattype] += 1
            return ID
        else:
            self.nodecount[pattype] = 1
            return 0


    def match(self, senpos, pattern, pattype):
        patarr = pattern.split()
        paralist = []
        i=0
        canmatch = True
        while i < len(senpos):
            canmatch = True
            regextra = 0
            j = 0
            while j < len(patarr):
                if patarr[j][0]=='(':
                    if patarr[j][1:-1] in senpos[i+j + regextra][1]:
                        paralist.append(senpos[i+j + regextra][0])
                    else:
                        canmatch = False
                        break
                elif patarr[j][0]=='[':
                    contentstr = patarr[j].split(']')[0][1:]
                    contents = contentstr.split('|')
                    if patarr[j][-1]=='}':
                        times = patarr[j].split('{')[1][:-1].split(',')
                        minimum_allowed_occurance = int(times[0])
                        maximum_allowed_occurance = int(times[1])
                        repeat = 0
                        for repeatednum in range(minimum_allowed_occurance, maximum_allowed_occurance + 1):
                            if senpos[i + j + regextra + repeatednum][0] in contents:
                                repeat = repeatednum
                            else:
                                if repeatednum == 0:
                                    regextra -= 1
                                else:
                                    regextra += repeat
                                break
                    else:
                        if senpos[i + j + regextra][0] in contents:
                            pass
                        else:
                            canmatch = False
                            break

                elif patarr[j][0]=='{':
                    content = patarr[j][1:-1]
                    if content in senpos[i+j + regextra][0]:
                        pass
                    else:
                        canmatch = False
                        break


                elif patarr[j] == senpos[i+j + regextra][0]:
                    pass
                else:
                    canmatch = False
                    break

                j+=1

            if canmatch:
                break
            else:
                paralist = []

            i += 1




        ID = lambda x: str(self.GetCount(x))
        if pattype == 'event':
            if len(paralist) != 3 or not canmatch:
                return []

            tid =  ID('t')

            res  = ['SELECT ?t'+ tid, "  WHERE   ", "{ "]
            NodeID = ID(pattype)
            res.append('?event'+NodeID + ' <http://www.example.org/subject>  \"' + paralist[0]+'\" .')
            res.append('?event'+NodeID + ' <http://www.example.org/trigger> \"' + paralist[1]+'\" .')
            res.append('?event'+NodeID + ' <http://www.example.org/object> \"' + paralist[2]+'\" .')
            res.append('?event'+NodeID + ' <http://www.example.org/time>  ?t' + tid + '  .')
            res.append('}')


            command = '\n'.join(res)

            act = Action('sparql')
            act.setCommand(command)
            act.inputtype = 'None'
            act.keydict['subject'] = paralist[0]
            act.returntype = 'value'
            self.actions.add(act)


        elif pattype == 'stock_increase':
            if  not canmatch:
                return []

            if len(paralist) == 1:
                companyname = self.actions[-1].keydict['subject']
                pass
            elif len(paralist) == 2:
                companyname = paralist[0]
                pass

            res = ['SELECT ?support ?p  ', "WHERE   ", "{ "]
            NodeID = ID('company')
            res.append('?company'+NodeID + ' <http://www.example.org/support>  ?support .')
            res.append('?company'+NodeID + ' <http://www.example.org/name> \"' + companyname +'\" .')
            supportNodeID = ID('supportnode')
            stockNodeID = ID('stocknode')
            res.append('?supportnode'+supportNodeID + ' <http://www.example.org/name>  ?support .')
            res.append('?supportnode'+supportNodeID + ' <http://www.example.org/stock>  ?stock'+stockNodeID + ' .')
            res.append('?stock'+stockNodeID + ' <http://www.example.org/stocktime>  \"%s\" .')
            res.append('?stock'+stockNodeID + ' <http://www.example.org/price>  ?p .')
            res.append('}')
            command = '\n'.join(res)

            act = Action('sparql')
            act.inputtype = 'timestamp'
            act.setCommand(command)
            self.actions.add(act)

            act1 = copy.deepcopy(act)
            act1.inputtype = 'latertimestamp'
            self.actions.add(act1)

            actminus = Action('minus')
            actminus.inputtype='table'
            self.actions.add(actminus)


            actmax = Action('max')
            actmax.inputtype='table'
            self.actions.add(actmax)

        elif pattype == 'specific_type_stock_increase':
            if  not canmatch:
                return []

            stocktype = paralist[0]

            res = ['SELECT ?company ?p  ', "WHERE   ", "{ "]
            companyNodeID = ID('company')
            stockNodeID = ID('stocknode')
            res.append('?companynode' + companyNodeID + ' <http://www.example.org/name>  ?company .')
            res.append('?companynode' + companyNodeID + ' <http://www.example.org/stock>  ?stock' + stockNodeID + ' .')
            res.append('?companynode' + companyNodeID + ' <http://www.example.org/type>  \"' + stocktype + '\" .')
            res.append('?stock' + stockNodeID + ' <http://www.example.org/stocktime>  \"%s\" .')
            res.append('?stock' + stockNodeID + ' <http://www.example.org/price>  ?p .')
            res.append('}')
            command = '\n'.join(res)

            act = Action('sparql')
            act.inputtype = 'timestamp'
            act.setCommand(command)
            self.actions.add(act)

            act1 = copy.deepcopy(act)
            act1.inputtype = 'latertimestamp'
            self.actions.add(act1)

            actminus = Action('minus')
            actminus.inputtype='table'
            self.actions.add(actminus)


            actmax = Action('max')
            actmax.inputtype='table'
            self.actions.add(actmax)








if __name__=='__main__':
    g1 = rdflib.Graph()
    g1.parse("graph.rdf", format='nt')
    s = ActionListGenerator('d', g1)
    s.Generate()
    print s.actions.do_it()
