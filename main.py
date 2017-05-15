# coding=utf-8
import numpy


from ActionList import  *
from Action import  *
from SPARQLgenerator import  *
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

sentence = u'当苹果公司发布iPad4时，哪家苹果公司的供应商股价上涨幅度会最大？'
sentence1 = u'当三级飓风袭击福罗里达州时，哪支水泥股的涨幅会最大？'
sentence2 = u'当朝鲜试射导弹时，哪支国防股将涨得最多？'

if __name__=='__main__':

    question = raw_input("请输入问题：")
   # print question
    g1 = rdflib.Graph()
    g1.parse("graph.rdf", format='nt')
    s = ActionListGenerator(question, g1)
    s.Generate()
    result = s.actions.do_it()
    print (result[0].decode('utf-8'), result[1])