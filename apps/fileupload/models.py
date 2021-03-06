# encoding: utf-8
import os
import shutil

from django.db import models
from django.contrib.auth.decorators import permission_required



class Picture(models.Model):
    """This is a small demo using just two fields. The slug field is really not
    necessary, but makes the code simpler. ImageField depends on PIL or
    pillow (where Pillow is easily installable in a virtualenv. If you have
    problems installing pillow, use a more generic FileField instead.

    """
    file = models.FileField(upload_to="Archivos")
    slug = models.SlugField(max_length=100, blank=True)
    anonimo = models.IntegerField(default=0,blank=True,null=True)
    def __str__(self):
        #return self.file.name
        return '{}'.format(self.slug)



    @models.permalink
    def get_absolute_url(self):
        return ('upload-new', )

    def save(self, *args, **kwargs):
        super(Picture, self).save(*args, **kwargs)


