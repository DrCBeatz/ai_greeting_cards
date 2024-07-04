# aigreetingcards/tasks.py

from celery import shared_task
from django.conf import settings
from openai import OpenAI
from .models import Image

@shared_task
def generate_image_task(prompt, user_id):
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )

    img_url = response.data[0].url

    new_image = Image(title=prompt, image_url=img_url, user_id=user_id)
    new_image.get_remote_image()
    new_image.save()
