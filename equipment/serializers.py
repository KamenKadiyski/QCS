from rest_framework import serializers
from equipment.models import Machine, Tool
from equipment.signals import tool_is_compatible

class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

class MachineSerializer(serializers.ModelSerializer):
    compatible_tools = serializers.PrimaryKeyRelatedField(queryset=Tool.objects.all(),
                                                          many=True,
                                                          required=False)
    class Meta:
        model = Machine
        fields = '__all__'

    def validate(self, attrs):
        compatible_tools = attrs.get('compatible_tools')
        if compatible_tools is None:
            return attrs

        if self.instance is not None:
            machine = Machine(
                max_clamping_force=attrs.get('max_clamping_force', self.instance.max_clamping_force),
                max_tool_width=attrs.get('max_tool_width', self.instance.max_tool_width),
                max_tool_height=attrs.get('max_tool_height', self.instance.max_tool_height),
                max_tool_thickness=attrs.get('max_tool_thickness', self.instance.max_tool_thickness),
                max_moving_platen_stroke=attrs.get('max_moving_platen_stroke', self.instance.max_moving_platen_stroke),
                max_injection_capacity=attrs.get('max_injection_capacity', self.instance.max_injection_capacity),
                max_ejecting_stroke=attrs.get('max_ejecting_stroke', self.instance.max_ejecting_stroke),
                number_of_ejector_cores=attrs.get('number_of_ejector_cores', self.instance.number_of_ejector_cores),
            )
        else:
            machine = Machine(
                max_clamping_force=attrs['max_clamping_force'],
                max_tool_width=attrs['max_tool_width'],
                max_tool_height=attrs['max_tool_height'],
                max_tool_thickness=attrs['max_tool_thickness'],
                max_moving_platen_stroke=attrs['max_moving_platen_stroke'],
                max_injection_capacity=attrs['max_injection_capacity'],
                max_ejecting_stroke=attrs['max_ejecting_stroke'],
                number_of_ejector_cores=attrs['number_of_ejector_cores'],
            )
        attrs['compatible_tools'] = [tool for tool in compatible_tools if tool_is_compatible(tool, machine)]
        return attrs

    def create(self,validated_data):
        compatible_tools_data = validated_data.pop('compatible_tools', [])
        machine = Machine.objects.create(**validated_data)
        if compatible_tools_data:
            machine.compatible_tools.add(*compatible_tools_data)

        return machine

    def update(self, instance, validated_data):
        compatible_tools_data = validated_data.pop('compatible_tools', None)
        instance = super().update(instance, validated_data)
        if compatible_tools_data is not None:
            instance.compatible_tools.set(compatible_tools_data)

        return instance







class ToolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tool
        fields = '__all__'






