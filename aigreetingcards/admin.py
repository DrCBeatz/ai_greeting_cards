from django.contrib import admin

from .models import Image, Prompt

class ImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'image_file', 'image_url']

class PromptAdmin(admin.ModelAdmin):
    list_display = ['text']

admin.site.register(Image, ImageAdmin)
admin.site.register(Prompt, PromptAdmin)
