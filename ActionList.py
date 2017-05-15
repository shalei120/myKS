import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

from Action import *

class ActionList:
    def __init__(self,graph):
        self.actionlist = []
        self.graph = graph

    def __str__(self):
        res = ''
        for act in self.actionlist:
            res += act.action_type + ': \n \t'
            res += act.command + '\n\n'
        return res


    def add(self, action):
        self.actionlist.append(action)

    def addtime(self, time):
        if len(time) == 6:
            year = int(time[:4])
            month = int(time[4:])
            if month ==12:
                month=1
                year += 1
            else:
                month+=1

            sy = str(year)
            sm = str(month)
            if len(sm)==1:
                sm = '0' + sm

            return sy + sm

        return '000000'

    def do_it(self):
        prev_out = []
        for act in self.actionlist:
            if act.action_type == 'sparql':
                if act.inputtype == 'timestamp':
                    time = prev_out[-1]
                    prev_out.append(act.Do_it(input = [self.graph, time[0][0]]))
                elif act.inputtype == 'latertimestamp':
                    time = prev_out[-2]
                    time = self.addtime(time[0][0])
                    prev_out.append(act.Do_it(input = [self.graph, time]))
                elif act.inputtype == 'None':
                    prev_out.append(act.Do_it(input = [self.graph]))
                else:
                    print ('ERROR!!!!!!')

            elif act.action_type == 'minus':
                b = prev_out.pop()
                a = prev_out.pop()
                prev_out.append(act.Do_it(input = [a,b]))
            elif act.action_type == 'max':
                a = prev_out.pop()
                prev_out.append(act.Do_it(input = [a]))

        return prev_out[-1]


