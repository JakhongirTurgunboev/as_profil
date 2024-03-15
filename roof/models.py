from django.db import models

# Create your models here.
from rest_framework.exceptions import ValidationError


class RoofMaterial(models.Model):
    ROOF_TYPE = (
        ('p', 'profnastil'),
        ('s', 'shifer'),
        ('m', 'metall')
    )
    title = models.CharField(max_length=100, unique=True)
    type = models.CharField(choices=ROOF_TYPE, max_length=1)
    width_m = models.DecimalField(max_digits=10, decimal_places=2)
    height_m = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=0)

    def clean(self):
        if self.type in ['p', 'm'] and self.height_m is not None:
            raise ValidationError("Height should be null for 'profnastil' or 'metall' type.")
        elif self.type == 's' and (self.height_m is None or self.height_m == 0 or self.height_m < 0):
            raise ValidationError("Height should be provided and non-zero for 'shifer' type.")