from ...models import Req, IntDep, IntDepType

class ReqGraph(object):
    def __init__(self):
        super(ReqGraph, self).__init__()

    def setMaxInDeg(self, val):
        self.max_indeg = val
        if val:
        	self.max_indeg_value = val[0].indeg
        else:
        	self.max_indeg_value = -1
    def setMaxOutDeg(self, val):
        self.max_outdeg = []
    def setMinInDeg(self, val):
        self.min_indeg = val
        if val:
        	self.min_indeg_value = val[0].indeg
        else:
        	self.min_indeg_value = -1
    def setMinOutDeg(self, val):
        self.min_outdeg = []

    def setLongestPaths(self, val):
        self.longest_paths = []
    def setShortestPaths(self, val):
        self.shortest_paths = []


def calculateNodeDegrees(rgraph):
    max_val = 0
    min_val = 9999
    maxs = []
    mins = []
    for r in Req.objects.all():
        val = calNodeInDegree(r)
        if val == max_val:
            maxs.append(r)
        elif val > max_val:
            maxs.clear()
            maxs.append(r)
            max_val = val

        if val == min_val:
            mins.append(r)
        elif val < min_val:
            mins.clear()
            mins.append(r)
            min_val = val
        r.indeg = val
        r.save()
    rgraph.setMinInDeg(mins)
    rgraph.setMaxInDeg(maxs)
    return rgraph

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