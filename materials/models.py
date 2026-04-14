from django.db import models

# Create your models here.
#Модел за описание на материалите. Включва по-голямата част от характеристиките, които са важни за качеството на продукт.
class Material(models.Model):
    class DurabilityGrade(models.TextChoices):
        LOW = ('LOW', 'Standard - (Internal use)')
        MEDIUM = ('MED', 'Reinforced (PPC / Impact resistant)')
        HIGH = ('HIGH', 'Industrial/Outdoor (GF / UV-stabilised)')

    MATERIAL_TYPES=(
        ('block','PPC (Block Copolymer)'),
        ('clear','Clear PPR (Random Copolymer)'),
        ('homopolymer','PPH (Homopolymer)'),
        ('other','Other'),
    )
    OPTICAL_PROPERTIES = (
        ('TRANSP', 'Transparent'),
        ('TRANSL', 'Translucent'),
        ('OPAQUE', 'Opaque'),
    )
    name = models.CharField(max_length=100)
    supplier=models.ForeignKey('traidingparties.Supplier', on_delete=models.CASCADE, related_name='materials')
    type=models.CharField(max_length=20,choices=MATERIAL_TYPES)
    mfi_mfr=models.CharField(max_length=3)
    density=models.DecimalField(max_digits=4,decimal_places=3)
    product_durability=models.CharField(max_length=10,choices=DurabilityGrade.choices)
    product_optic=models.CharField(max_length=10,choices=OPTICAL_PROPERTIES)
    additional_notes = models.TextField()

    def __str__(self):
        return self.name

#Модел за описание на добавките към материала.
class Additive(models.Model):
    additive_code=models.CharField(max_length=10)
    name=models.CharField(max_length=100)
    supplier=models.ForeignKey('traidingparties.Supplier', on_delete=models.CASCADE, related_name='additives')
    additional_notes = models.TextField()
    def __str__(self):
        return self.name


