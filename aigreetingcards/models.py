# aigreetingcards/models.py

from django.db import models
from django.core.files import File
from urllib import request
from django.contrib.auth.models import User
from django.conf import settings

import os

class Image(models.Model):
    image_file = models.ImageField(upload_to='images', max_length=500)
    image_url = models.URLField(max_length=500)
    title = models.CharField(max_length=500, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    def get_remote_image(self):
        if self.image_url and not self.image_file:
            result = request.urlretrieve(self.image_url)
            self.image_file.save(
                    os.path.basename(self.image_url),
                    File(open(result[0], 'rb'))
                    )
            self.save()

class Prompt(models.Model):
    text = models.TextField()