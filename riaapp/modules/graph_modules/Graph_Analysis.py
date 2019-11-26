from ...models import Issue, DepIssue, DepType

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
    max_val_in = 0
    min_val_in = 9999
    maxs_in = []
    mins_in = []
    max_val_out = 0
    min_val_out = 9999
    maxs_out = []
    mins_out = []
    for r in Issue.objects.all():
        val_in = calNodeInDegree(r)
        val_out = calNodeOutDegree(r)
        #in degree max caclculation
        if val_in == max_val_in:
            maxs_in.append(r)
        elif val_in > max_val_in:
            maxs_in.clear()
            maxs_in.append(r)
            max_val_in = val_in

        #out degree max caclculation
        if val_out == max_val_out:
            maxs_out.append(r)
        elif val_out > max_val_out:
            maxs_out.clear()
            maxs_out.append(r)
            max_val_out = val_out


        #in degree min caclculation
        if val_in == min_val_in:
            mins_in.append(r)
        elif val_in < min_val_in:
            mins_in.clear()
            mins_in.append(r)
            min_val_in = val_in

        #out degree min caclculation
        if val_out == min_val_out:
            mins_out.append(r)
        elif val_out < min_val_out:
            mins_out.clear()
            mins_out.append(r)
            min_val_out = val_out


        r.indeg = val_in
        r.outdeg = val_out
        r.save()

    rgraph.setMinInDeg(mins_in)
    rgraph.setMaxInDeg(maxs_in)
    rgraph.setMinOutDeg(mins_out)
    rgraph.setMaxOutDeg(maxs_out)
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
            if not(d.source in countedlist) and not(d.source in deplist):
                deplist.append(d.source)
                res = res + 1
    return res

def getDepsIn(r):
    return DepIssue.objects.filter(destination=r)


def calNodeOutDegree(r):
    res = 0
    deplist = [r]
    countedlist = []
    while deplist:
        rx = deplist.pop()
        if (rx in countedlist):
            continue
        countedlist.append(rx)
        for d in getDepsOut(rx):
            if not(d.destination in countedlist) and not(d.destination in deplist):
                deplist.append(d.destination)
                res = res + 1
    return res

def getDepsOut(r):
    return DepIssue.objects.filter(source=r)