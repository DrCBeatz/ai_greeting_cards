# aigreetingcards/tasks.py

from celery import shared_task
from django.conf import settings
from openai import OpenAI
from .models import Image
from accounts.models import CustomUser
import redis

redis_client = redis.StrictRedis(host='redis', port=6379, db=0)

@shared_task
def generate_image_task(prompt, size, quality, style, user_id):
    task_id = generate_image_task.request.id
    redis_client.set(f"task_status:{task_id}", "processig")

    user = CustomUser.objects.get(id=user_id)

    try:
        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size=size,
            quality=quality,
            # num_images=1,
            style=style,            
            n=1,
        )

        img_url = response.data[0].url
        new_image = Image(title=prompt, image_url=img_url, user_id=user_id)
        new_image.get_remote_image()
        new_image.save()

        # Determine how many credits to deduct based on the quality
        if quality == 'hd':
            user.credits -= 20
        else:
            user.credits -= 10

        user.save()
        
        redis_client.set(f"task_status:{task_id}", "completed")

    except Exception as e:
        redis_client.set(f"task_status:{task_id}", f"failed: {str(e)}")
        user.save()