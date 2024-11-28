from django.db import models
from django.contrib.auth.models import User

class Plato(models.Model):
    CATEGORIAS = [
        ('desayuno', 'Desayuno'),
        ('postre', 'Postre'),
        ('te', 'Te'),
    ]
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    disponible = models.BooleanField(default=True)
    imagen = models.ImageField(upload_to='platos/', blank=True, null=True)
    categoria = models.CharField(max_length=10, choices=CATEGORIAS, null=True, blank=True)
    oculto = models.BooleanField(default=False)  # Nuevo campo para ocultar

    def __str__(self):
        return f"{self.nombre} - ${self.precio:.2f}"

class Encuesta(models.Model):
    plato = models.ForeignKey(Plato, on_delete=models.CASCADE, related_name='encuestas')  # Agregar related_name
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])  # 1 a 5 estrellas
    comentario = models.TextField(blank=True)

    def __str__(self):
        return f'Encuesta para {self.plato.nombre} - Rating: {self.rating}'
    
class Factura(models.Model):
    METODOS_PAGO = [
         ('tarjeta','Tarjeta de Credito'),
         ('efectivo', 'Efectivo'),
         ]
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)    
    direccion = models.CharField(max_length=255)
    fecha = models.DateTimeField(auto_now_add=True)    
    metodo_pago = models.CharField(max_length=20, choices=METODOS_PAGO)    
    total = models.DecimalField(max_digits=10, decimal_places=2)    


def __str__(self):
        return f'Factura {self.id} - {self.usuario.username} - ${self.total:.2f}'

class DetalleFactura(models.Model):
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE, related_name='detalles')
    plato = models.ForeignKey(Plato, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.cantidad} x {self.plato.nombre} en Factura {self.factura.id}"

class DiaEspecial(models.Model):
    nombre = models.CharField(max_length=100)
    fecha = models.DateField()

    def __str__(self):
        return f"{self.nombre} - {self.fecha}"

class Oferta(models.Model):
    nombre = models.CharField(max_length=100)
    platos = models.ManyToManyField(Plato, related_name='ofertas')
    precio_oferta = models.DecimalField(max_digits=10, decimal_places=2)
    dias_especiales = models.ManyToManyField(DiaEspecial, related_name='ofertas', blank=True)  

    def __str__(self):
        return f"{self.nombre} - ${self.precio_oferta:.2f}"
    


