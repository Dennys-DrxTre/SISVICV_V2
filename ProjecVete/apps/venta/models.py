from django.db import models

#Para los signals
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum

from apps.regmedic.models import Cliente
from apps.inv.models import Producto

# MODELS DE LAS VENTAS

class FacturaHeader(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete = models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
    sub_total = models.FloatField(default=0)
    descuento = models.FloatField(default=0)
    total = models.FloatField(default=0)

    class Meta:
        verbose_name = "Encabezado de venta"
        verbose_name_plural = "Encabezado de ventas"

    def __str__(self):
        return '{}'.format(self.cliente)

    def save(self):
        self.total = self.sub_total - self.descuento
        super(FacturaHeader, self).save()


class FacturaBody(models.Model):
    factura = models.ForeignKey(FacturaHeader, on_delete= models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete= models.CASCADE)
    cantidad = models.BigIntegerField(default=0)
    precio = models.FloatField(default=0)
    sub_total = models.FloatField(default=0)
    descuento = models.FloatField(default=0)
    total = models.FloatField(default=0)
    ganancias = models.FloatField(default=0)

    def __str__(self):
        return '{}'.format(self.producto)

    def save(self):
        self.sub_total = float(float(int(self.cantidad)) * float(self.precio))
        self.total = self.sub_total - float(self.descuento)
        super(FacturaBody, self).save()

    class Meta:
        verbose_name = "Detalle de venta"
        verbose_name_plural = "Detalles de ventas"

# Calculando el total de la venta

@receiver(post_save, sender = FacturaBody)
def detalle(sender, instance, **kwargs):
    factura_id = instance.factura.id
    producto_id = instance.producto.id

    enc = FacturaHeader.objects.get(pk=factura_id)

    if enc:
        sub_total = FacturaBody.objects.filter(factura=factura_id).aggregate(sub_total=Sum('sub_total')).get('sub_total', 0.00)
        descuento = FacturaBody.objects.filter(factura=factura_id).aggregate(descuento=Sum('descuento')).get('descuento', 0.00)

        enc.sub_total = sub_total
        enc.descuento = descuento
        enc.save()

    prod = Producto.objects.filter(pk=producto_id).first()
    if prod:
        cantidad = int(prod.stock) - int(instance.cantidad)
        prod.stock = cantidad
        prod.save()
