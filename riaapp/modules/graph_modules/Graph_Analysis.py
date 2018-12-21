from ...models import Req, IntDep, IntDepType

class ReqGraph(object):
    def __init__(self):
        super(ReqGraph, self).__init__()

    def setMaxInDeg(self, val):
        self.max_indeg.append(val)
    def setMaxOutDeg(self, val):
        self.max_outdeg = []
    def setMinInDeg(self, val):
        self.min_indeg = []
    def setMinOutDeg(self, val):
        self.min_outdeg = []

    def setLongestPaths(self, val):
        self.longest_paths = []
    def setShortestPaths(self, val):
        self.shortest_paths = []


def calculateNodeDegrees():
    max_ = 0
    min_ = Req.objects.get(0)
    for r in Req.objects.all():
        val = calNodeInDegree(r)
        r.indeg = val
        r.save()
        if val > max_:
            max_ = val

def calNodeInDegree(r):
    res = 0
    deplist = [r]
    countedlist = []
    while deplist:
        rx = deplist.pop()
        if (rx in countedlist):
            continue
        countedlist.append(rx)
        for d in getDepsIn(rx):
            if not(d.fro in countedlist) and not(d.fro in deplist):
                deplist.append(d.fro)
                res = res + 1
    return res

def getDepsIn(r):
    res = []
    for d in IntDep.objects.all():
        if d.to == r:
            res.append(d)
    return res