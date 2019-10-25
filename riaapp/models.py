from django.db import models
from .modules.utils import PreProcessing as pp
from django.db.models.query_utils import DeferredAttribute


#class Project(models.Model):
#	Issues []
#	HighDeps []
#	name []
#	(clf, vec)s files []
#	DepLearnInstances []
#	isAnalyzed boolean



#class Issue(models.Model):
#	Category
#	created_by
#	assigned_to [text]
#	Reqs []
#	main_req	maybe
#	priority
#	

#class HighDeps(models.Model):
#	DepType
#	source issue
#	destination issue
#	strength = models.IntegerField(default = 1)



#in coofti ro move kon tu khode req, shayad behtare
class NLPDoc(models.Model):
	doc = models.BinaryField(max_length=None, default = None)

class Req(models.Model):
    text = models.CharField(max_length=2000)
    indeg = models.IntegerField(default = -1)
    outdeg = models.IntegerField(default = -1)
    nlp_doc =  models.ForeignKey(NLPDoc, related_name='+', on_delete=models.CASCADE, default=-1, null=True)
    def __str__(self):
        return self.text

class DepType(models.Model):
	name = models.CharField(max_length=100)
	directional = models.BooleanField(default=True)
	def __str__(self):
		return self.name


class Dep(models.Model):
	dep_type = models.ForeignKey(DepType, related_name='+', on_delete=models.CASCADE, null=True)
	source = models.ForeignKey(Req, related_name='+', on_delete=models.CASCADE)
	destination = models.ForeignKey(Req, related_name='+', on_delete=models.CASCADE)
	strength = models.IntegerField(default = 1)
	indirect = models.BooleanField(default= False)
	def __str__(self):
		return "{" + self.dep_type.name + "} : from [" + self.source.text + "] to [" + self.destination.text + "]"

class DepLearnInstance(models.Model):
	dep_type = models.ForeignKey(DepType, related_name='+', on_delete=models.CASCADE, null=True)
	r1 = models.CharField(max_length=2000, null=True)
	r2 = models.CharField(max_length=2000, null=True)
	positive =  models.BooleanField(default=True)
	def __str__(self):
		return str(self.positive) + ";" + self.dep.source.text + ";" + self.dep.destination.text


class Path(models.Model):
	name = models.CharField(max_length=100)
	deps = models.ManyToManyField(Dep, related_name='+')
	def __str__(self):
		return self.name


