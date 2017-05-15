import rdflib



class Action:
    def __init__(self, actiontype):
        self.action_type=actiontype  # sparql, minus, max
        self.command = ""
        self.inputtype = ''  # 'table' 'timestamp' 'latertimestamp' 'None
        self.returntype = '' # 'value'  'table'
        self.keydict = dict()

    def setCommand(self, command):
        self.command = command

    def Do_it(self, input = []):
        if self.action_type == 'sparql':
            if len(input) < 1:
                print 'The list parameter input should have 1 item!'
                print 'Usage: input = [graph, timestamp]'
                return

            if 'timestamp' in self.inputtype:
                timestamp = input[1]
                self.command = (self.command %(timestamp))


            graph = input[0]
            if graph == None:
                print 'A graph is needed!'
                return
            else:
               # print self.command
                x1 = graph.query(self.command)
                x1 = rdflib.util.list2set(x1)
                x2 = [[str(item) for item in line] for line in list(x1) ]
                #x2 = list(x2)

               # print x2
                return x2


        elif self.action_type == 'minus':
            if len(input)!=2:
                print 'The list parameter input should have 2 items!'
                print 'Usage: input = [table1, table2]'
            table1 = input[0]
            table2 = input[1]
            table1_map = {inc: stock for inc, stock in table1}
            table2_map = {inc: stock for inc, stock in table2}
            res=[]
            keyset = set(table1_map.keys() + table2_map.keys())
            for key in keyset:
                if key in table1_map and key in table2_map:
                    res.append((key, float(table2_map[key]) - float(table1_map[key])))

            return res

        elif self.action_type == 'max':
            if len(input)!=1:
                print 'The list parameter input should have 1 item!'
                print 'Usage: input = [table1]'

            table1 = input[0]

            res = table1[0]
            for line in table1:
                if res[1] < line[1]:
                    res = line

            return res







