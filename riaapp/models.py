from django.db import models

class Req(models.Model):
    text = models.CharField(max_length=2000)
    indeg = models.IntegerField(default = -1)
    outdeg = models.IntegerField(default = -1)
    def __str__(self):
        return self.text

class DepType(models.Model):
	name = models.CharField(max_length=100)
	directional = models.BooleanField(default=True)
	def __str__(self):
		return self.name


class Dep(models.Model):
	dep_type = models.ForeignKey(DepType, related_name='+', on_delete=models.CASCADE)
	source = models.ForeignKey(Req, related_name='+', on_delete=models.CASCADE)
	destination = models.ForeignKey(Req, related_name='+', on_delete=models.CASCADE)
	strength = models.IntegerField(default = 1)
	indirect = models.BooleanField(default= False)
	def __str__(self):
		return "{" + self.typ.name + "} : from [" + self.source.text + "] to [" + self.dest.text + "]"


class Path(models.Model):
	name = models.CharField(max_length=100)
	deps = models.ManyToManyField(Dep, related_name='+')
	def __str__(self):
		return self.name