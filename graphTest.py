import shelve
def shelvify(obj):
    d = shelve.open("lingFile") # open, with (g)dbm filename -- no suffix
    d["graph"] = obj  # store data at key (overwrites old data if
    data = d["graph"]   # retrieve a COPY of the data at key (raise
    # delete data stored at key (raises KeyError
    #flag = "key" in d # true if the key exists
    #list = d.keys() # a list of all existing keys (slow!)
    print data
    d.close()       # close it


class Vertex:
    def __init__(self, node):
        self.id = node
        self.adjacent = {}

    def __str__(self):
        return str(self.id) + ' adjacent: ' + str([x.id for x in self.adjacent])

    def add_neighbor(self, neighbor, weight=0):
        self.adjacent[neighbor] = weight

    def get_connections(self):
        return self.adjacent.keys()  

    def get_id(self):
        return self.id

    def get_weight(self, neighbor):
        return self.adjacent[neighbor]

class Graph:
    def __init__(self):
        self.vert_dict = {}
        self.num_vertices = 0

    def __iter__(self):
        return iter(self.vert_dict.values())

    def add_vertex(self, node):
        self.num_vertices = self.num_vertices + 1
        new_vertex = Vertex(node)
        self.vert_dict[node] = new_vertex
        return new_vertex

    def get_vertex(self, n):
        if n in self.vert_dict:
            return self.vert_dict[n]
        else:
            return None

    def add_edge(self, frm, to, cost = 0):
        if frm not in self.vert_dict:
            self.add_vertex(frm)
        if to not in self.vert_dict:
            self.add_vertex(to)

        self.vert_dict[frm].add_neighbor(self.vert_dict[to], cost)
        self.vert_dict[to].add_neighbor(self.vert_dict[frm], cost)

    def get_vertices(self):
        return self.vert_dict.keys()


g = Graph()


def linguify():
    sentence=""
    for line in open("book.txt"):
        if "." in line:
            sentence=sentence+line[0:line.index(".")]
            sentence=sentence.split(" ")
            for x in range(1,len(sentence)-1):
                if x==1:
                    if g.get_vertex(sentence[0]) == None:
                        g.add_vertex(sentence[x])

                if g.get_vertex(sentence[x]) == None:
                    g.add_vertex(sentence[x])

                if x == len(sentence)-1:
                    g.add_edge(sentence[x-1],sentence[x],1)
                

            sentence = line[line.index(".")+1:len(line)-1] 
        else:
            sentence += " "+line+" "


def getEm():
    d = shelve.open("lingFile") # open, with (g)dbm filename -- no suffix
    for x in d["graph"]:
        print x
    d.close()       

# g.add_vertex('a')
# g.add_vertex('b')
# g.add_vertex('c')
# g.add_vertex('d')
# g.add_vertex('e')
# g.add_vertex('f')

# g.add_edge('a', 'b', 7)  
# g.add_edge('a', 'c', 9)
# g.add_edge('a', 'f', 14)
# g.add_edge('b', 'c', 10)
# g.add_edge('b', 'd', 15)
# g.add_edge('c', 'd', 11)
# g.add_edge('c', 'f', 2)
# g.add_edge('d', 'e', 6)
# g.add_edge('e', 'f', 9)

# for v in g:
#     for w in v.get_connections():
#         vid = v.get_id()
#         wid = w.get_id()
#         print '( %s , %s, %3d)'  % ( vid, wid, v.get_weight(w))

# for v in g:
#     print 'g.vert_dict[%s]=%s' %(v.get_id(), g.vert_dict[v.get_id()])

shelvify(g)

