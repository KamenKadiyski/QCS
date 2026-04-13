from django.db.models.signals import post_save
from django.dispatch import receiver

from django.conf import settings
from .models import Tool, Machine
from django.db.models import Q
import logging

logger = logging.getLogger(__name__)

THICKNESS_MIN_RATIO = 0.30
TOOL_TOLERANCE = settings.TOOL_TOLERANCE

def tool_is_compatible(tool, machine, tolerance=TOOL_TOLERANCE):
    is_compatible = (
        tool.clamping_force <= machine.max_clamping_force * tolerance and
        tool.tool_width <= machine.max_tool_width * tolerance and
        tool.tool_height <= machine.max_tool_height * tolerance and
        machine.max_tool_thickness * THICKNESS_MIN_RATIO <= tool.tool_thickness <= machine.max_tool_thickness and
        tool.moving_platen_stroke <= machine.max_moving_platen_stroke * tolerance and
        tool.injection_capacity <= machine.max_injection_capacity * tolerance and
        tool.ejecting_stroke <= machine.max_ejecting_stroke * tolerance and
        tool.number_of_ejector_cores <= machine.number_of_ejector_cores
    )
    if not is_compatible:
        logger.debug(f"Tool {tool.code} NOT compatible with {machine.machine_number}")
    return is_compatible

def compatible_tool_for_machine(machine, tolerance=TOOL_TOLERANCE):
    compatible_tools = Tool.objects.filter(
        Q(clamping_force__lte=machine.max_clamping_force * tolerance) &
        Q(tool_width__lte=machine.max_tool_width * tolerance) &
        Q(tool_height__lte=machine.max_tool_height * tolerance) &
        Q(tool_thickness__gte=machine.max_tool_thickness * THICKNESS_MIN_RATIO) &
        Q(tool_thickness__lte=machine.max_tool_thickness) &
        Q(moving_platen_stroke__lte=machine.max_moving_platen_stroke * tolerance) &
        Q(injection_capacity__lte=machine.max_injection_capacity * tolerance) &
        Q(ejecting_stroke__lte=machine.max_ejecting_stroke * tolerance) &
        Q(number_of_ejector_cores__lte=machine.number_of_ejector_cores)
    )
    return compatible_tools

@receiver(post_save, sender=Machine)
def add_compatible_tools_on_machine_create(sender, instance, created, **kwargs):
    if created:
        compatible_tools = compatible_tool_for_machine(instance)
        instance.compatible_tools.set(compatible_tools)


@receiver(post_save, sender=Tool)
def add_tool_to_compatible_machines(sender, instance, created, **kwargs):
    compatible_machines = []

    # Find compatible machines for the new tool
    for machine in Machine.objects.all():
        if tool_is_compatible(instance, machine):
            compatible_machines.append(machine)
    
    # Update the ManyToMany relationship

    instance.compatible_machines.set(compatible_machines)
    if not compatible_machines:
        logger.info(f"No compatible machines found for tool {instance.code}")
