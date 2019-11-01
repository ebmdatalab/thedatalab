from django.db.models.signals import post_save
from django.dispatch import receiver

from . import models


@receiver(post_save, sender=models.TopicTags)
def create_topic_for_tag(sender, instance, created, **kwargs):
    if created:
        if models.Topic.objects.filter(topic_tag=instance).count() == 0:
            models.Topic.objects.create(
                topic_tag=instance,
                title=instance.label,
                short_title=instance.label,
                description=instance.label
            )
