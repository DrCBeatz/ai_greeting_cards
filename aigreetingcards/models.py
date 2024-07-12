# aigreetingcards/models.py

from django.db import models
from django.core.files import File
from urllib import request
from django.contrib.auth.models import User
from django.conf import settings
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, Transpose

import os

class Image(models.Model):
    image_file = models.ImageField(upload_to='images', max_length=500)
    image_url = models.URLField(max_length=500, blank=True, null=True)
    thumbnail = ImageSpecField(source='image_file', id='aigreetingcards:image_file:image_file_thumbnail', processors=[Transpose(),ResizeToFill(650, 650)], format='JPEG', options={'quality':100})
    title = models.CharField(max_length=500, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    test = models.BooleanField(default=False)

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