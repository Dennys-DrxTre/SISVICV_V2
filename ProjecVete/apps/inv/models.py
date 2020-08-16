from django.db import models

from apps.inicio.models import ClaseModelo

class Departamento(ClaseModelo):
    descripcion = models.CharField(max_length=100, help_text='Descripción del Departamento', unique=True)

    def __str__(self):
        return '{}'.format(self.descripcion)
    
    def save(self):
        self.descripcion = self.descripcion.upper()
        super(Departamento, self).save()
    
    class Meta:
        verbose_name_plural = 'Departamentos'

class Categoria(ClaseModelo):
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=100, help_text='Descripción de la Categoria')

    def __str__(self):
        return '{}:{}'.format(self.departamento.descripcion,self.descripcion)

    def save(self):
        self.descripcion = self.descripcion.upper()
        super(Categoria, self).save()
    
    class Meta:
        verbose_name_plural = 'Categorias'
        unique_together = ('departamento','descripcion')

class Producto(models.Model):
    codigo= models.CharField(max_length= 50, verbose_name= 'Codigo del Producto')
    nombre = models.CharField(max_length= 50, verbose_name= 'Nombre del Producto')
    descripcion = models.TextField(verbose_name= 'Descripción del Producto')
    stock = models.IntegerField(verbose_name= 'Cantidad del Producto')
    precioCompra = models.FloatField(verbose_name= 'Precio de Compra')
    precioVenta = models.FloatField(verbose_name= 'Precio de Venta')
    ganancia = models.FloatField(default=0, verbose_name='Ganancias por venta')
    estado = models.BooleanField(default=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['-id']

    def __str__(self):
        return self.nombre

    def save(self):
        self.ganancia = self.precioVenta - self.precioCompra
        # CONDICIONAL PARA QUE EL PRECIO DE VENTA NO SEA MENOR AL PRECIO DE COMPRA
        if self.precioVenta < self.precioCompra:
            self.precioVenta = self.precioCompra
        super(Producto, self).save()
