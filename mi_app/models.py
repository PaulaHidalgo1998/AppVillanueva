from django.db import models


TIPO_DE_APORTACION = (
    ('adulto', 'Adultos (18-66 años)'),
    ('jubilado', 'Adulto desde los 67 años'),
    ('joven', 'Jovenes (12-17 años)'),
    ('otro', 'Otro')
)

class Persona(models.Model):
    nombre = models.CharField(max_length=100, default="")
    apellidos = models.CharField(max_length=150, default="")
    numero_socio = models.IntegerField(default=0)
    dinero = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tipo_aportacion = models.CharField(max_length=20, choices=TIPO_DE_APORTACION, default='adulto')

