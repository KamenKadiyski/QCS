from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import JobLog


@receiver(post_save, sender=JobLog)
def update_resource_status(sender, instance, **kwargs):
    tool = instance.current_tool
    machine = instance.current_machine

    status = not instance.is_complete
    tool.is_in_use = status
    tool.save()

    machine.is_in_use = status
    machine.save()
