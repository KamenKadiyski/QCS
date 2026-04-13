from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import Building, Machine, Tool
from .serializers import MachineSerializer, ToolSerializer


class ProductionSystemTest(TestCase):
    def setUp(self):
        # 1. Setup Building
        self.building = Building.objects.create(
            name="Plant A",
            crane_capacity=10000,
            number_of_silos=2,
            is_centralised_cooling=True
        )

        # 2. Setup BMB Machine (11500 kN)
        # Safe Clamping Force (90%): 10350 kN
        # Safe Injection (85%): 9350 cm3
        # Min Thickness (30%): 420 mm
        self.machine_data = {
            "machine_number": "BMB-01",
            "building": self.building.id,
            "machine_model": "eKW 1150PI/11500",
            "machine_description": "Large Scale BMB",
            "max_clamping_force": 11500,
            "max_tool_width": 1300.0,
            "max_tool_height": 1200.0,
            "max_tool_thickness": 1400.0,
            "max_moving_platen_stroke": 1400.0,
            "max_injection_capacity": 11000.0,
            "max_ejecting_stroke": 400.0,
            "number_of_ejector_cores": 12
        }
        self.machine = Machine.objects.create(
            building=self.building,
            **{k: v for k, v in self.machine_data.items() if k != 'building'}
        )

    # --- ТЕСТОВЕ ЗА МОДЕЛИ И ВАЛИДАТОРИ ---

    def test_min_value_validator(self):
        """Проверка дали валидаторът спира стойности <= 0."""
        building = Building(name="Test", crane_capacity=0, number_of_silos=1, is_centralised_cooling=True)
        with self.assertRaises(ValidationError):
            building.full_clean()
        print("✓ Model: min_value_validator correctly blocked zero value.")

    # --- ТЕСТОВЕ ЗА MACHINE SERIALIZER (Филтриране на матрици) ---

    def test_machine_serializer_filters_incompatible_tool(self):
        """Проверка дали Serializer-ът премахва несъвместими матрици при запис на машина."""
        # Създаваме две матрици - една пасваща и една твърде голяма (сила 11000 > 10350)
        tool_ok = Tool.objects.create(code="OK", clamping_force=9000, tool_width=1000, tool_height=1000,
                                      tool_thickness=800, moving_platen_stroke=1000, injection_capacity=5000,
                                      ejecting_stroke=300, number_of_ejector_cores=8)

        tool_bad = Tool.objects.create(code="BAD", clamping_force=11000, tool_width=1000, tool_height=1000,
                                       tool_thickness=800, moving_platen_stroke=1000, injection_capacity=5000,
                                       ejecting_stroke=300, number_of_ejector_cores=8)

        data = self.machine_data.copy()
        data['compatible_tools'] = [tool_ok.id, tool_bad.id]

        # Validate against the existing machine instance so we test
        # compatibility filtering, not unique-constraint failure.
        serializer = MachineSerializer(instance=self.machine, data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        validated_data = serializer.validated_data

        # Проверяваме дали BAD е премахнат от списъка в Serializer-а
        self.assertIn(tool_ok, validated_data['compatible_tools'])
        self.assertNotIn(tool_bad, validated_data['compatible_tools'])
        print("✓ MachineSerializer: Successfully filtered incompatible tools using safety margins.")

    # --- ТЕСТОВЕ ЗА TOOL SERIALIZER И СИГНАЛИ (Автоматично свързване) ---

    def test_tool_signal_auto_link(self):
        """Проверка дали нова матрица се свързва автоматично към съществуваща машина."""
        tool_data = {
            "code": "AUTO-01",
            "description": "Auto Test Mold",
            "clamping_force": 9500,
            "tool_width": 1100,
            "tool_height": 1000,
            "tool_thickness": 700,  # OK (700 > 420)
            "moving_platen_stroke": 1000,
            "injection_capacity": 4000,
            "ejecting_stroke": 300,
            "number_of_ejector_cores": 8
        }

        # Записваме през сериализатора
        serializer = ToolSerializer(data=tool_data)
        self.assertTrue(serializer.is_valid())
        tool = serializer.save()

        # Проверяваме дали сигналът е свързал матрицата с BMB-01
        self.assertIn(tool, self.machine.compatible_tools.all())
        print(f"✓ ToolSerializer/Signal: Tool {tool.code} automatically linked to compatible machine.")

    def test_tool_rejection_by_30_percent_rule(self):
        """Проверка дали матрица се отхвърля, ако е под 30% от дебелината на машината."""
        tool_too_thin = Tool.objects.create(
            code="THIN", clamping_force=5000, tool_width=500, tool_height=500,
            tool_thickness=300,  # 300 < 420 (which is 1400 * 0.3)
            moving_platen_stroke=500, injection_capacity=2000,
            ejecting_stroke=200, number_of_ejector_cores=4
        )

        self.assertNotIn(tool_too_thin, self.machine.compatible_tools.all())
        print("✓ Signal: Corrected rejected tool due to 30% thickness rule.")

    def test_auto_unlink_on_parameter_update(self):
        """Проверка за автоматично премахване на връзка при промяна на параметър на матрица."""
        # 1. Създаваме съвместима матрица
        tool = Tool.objects.create(
            code="DYNAMIC", clamping_force=8000, tool_width=800, tool_height=800,
            tool_thickness=800, moving_platen_stroke=800, injection_capacity=3000,
            ejecting_stroke=200, number_of_ejector_cores=4
        )
        self.assertIn(tool, self.machine.compatible_tools.all())

        # 2. Променяме я така, че да не е съвместима (твърде голям обем)
        tool.injection_capacity = 10500  # 10500 > 9350 (safe limit)
        tool.save()

        # КРИТИЧНАТА СТЪПКА: Опресняваме обекта на машината от базата данни
        self.machine.refresh_from_db()

        self.assertNotIn(tool, self.machine.compatible_tools.all())
        print("✓ Signal: Successfully unlinked tool after parameters became incompatible.")

        self.assertNotIn(tool, self.machine.compatible_tools.all())
        print("✓ Signal: Successfully unlinked tool after parameters became unsafe.")
