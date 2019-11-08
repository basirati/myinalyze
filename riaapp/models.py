from django.db import models
from .modules.utils import PreProcessing as pp
from django.db.models.query_utils import DeferredAttribute

# market point ya issue ham biad bara idea vahe jaleb mishe


#	Issues []
#	DepTypes []
#	(clf, vec)s files []
#	isAnalyzed boolean
class Project(models.Model):
	name = models.CharField(max_length=80)
	description = models.CharField(max_length=1000, null=True, default='')
	clf_addr = models.CharField(max_length=100, default='')
	vec_addr = models.CharField(max_length=100, default='')
	isAnalyzed = models.BooleanField(default=False)


class Issue(models.Model):
	proj = models.ForeignKey(Project, related_name='+', on_delete=models.CASCADE, null=True)
	issue_type = models.CharField(max_length=80, default='task')
	priority = models.IntegerField(default = 1)
	effort = models.IntegerField(default = 1)

#	created_by
#	assigned_to [text]
#	main_req	maybe


#
#in coofti ro move kon tu khode req, shayad behtare
class NLPDoc(models.Model):
	doc = models.BinaryField(max_length=None, default = None)

class Req(models.Model):
	issue = models.ForeignKey(Issue, related_name='+', on_delete=models.CASCADE, null=True, default=None)
	text = models.CharField(max_length=2000)
	indeg = models.IntegerField(default = -1)
	outdeg = models.IntegerField(default = -1)
	nlp_doc =  models.ForeignKey(NLPDoc, related_name='+', on_delete=models.CASCADE, null=True)
	def __str__(self):
		return self.text

class DepType(models.Model):
	proj = models.ForeignKey(Project, related_name='+', on_delete=models.CASCADE, null=True)
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
	dep_types = models.ManyToManyField(DepType, related_name='+')
	r1 = models.CharField(max_length=2000, null=True)
	r2 = models.CharField(max_length=2000, null=True)
	positive =  models.BooleanField(default=True)
	def __str__(self):
		return str(self.positive) + ";" + self.dep.source.text + ";" + self.dep.destination.text

###########################################################
class Path(models.Model):
	name = models.CharField(max_length=100)
	deps = models.ManyToManyField(Dep, related_name='+')
	def __str__(self):
		return self.name


