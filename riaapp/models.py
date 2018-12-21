from django.db import models

class Req(models.Model):
    text = models.CharField(max_length=2000)
    indeg = models.IntegerField(default = -1)
    outdeg = models.IntegerField(default = -1)
    def __str__(self):
        return self.text

class IntDepType(models.Model):
	name = models.CharField(max_length=100)
	directional = models.BooleanField(default=True)
	def __str__(self):
		return self.name


class IntDep(models.Model):
	typ = models.ForeignKey(IntDepType, related_name='deptype', on_delete=models.CASCADE)
	fro = models.ForeignKey(Req, related_name='reqfrom', on_delete=models.CASCADE)
	to = models.ForeignKey(Req, related_name='reqto', on_delete=models.CASCADE)
	def __str__(self):
		return "{" + self.typ.name + "} : from [" + self.fro.text + "] to [" + self.to.text + "]"