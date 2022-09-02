from django.db import models

class Producto(models.Model):
    #producto_id = models.AutoField(primary_key=True, unique=True, default=1000)
    nombre = models.CharField(max_length=50)
    stock = models.PositiveIntegerField()
    precio = models.PositiveIntegerField()
    medidas = models.CharField(max_length=20)
    colores = models.CharField(max_length=20)
    foto = models.ImageField(upload_to='api/static/img')

    def __str__(self):
        return self.nombre
    
    class Meta:
        ordering = ['stock']

