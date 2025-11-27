from django.db import models

class Curso(models.Model):
    NIVEL_CHOICES = [
        ('basico', 'Básico'),
        ('intermedio', 'Intermedio'),
        ('avanzado', 'Avanzado'),
    ]
    
    MODALIDAD_CHOICES = [
        ('presencial', 'Presencial'),
        ('virtual', 'Virtual'),
        ('hibrida', 'Híbrida'),
    ]
    
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
        ('finalizado', 'Finalizado'),
    ]
    
    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=20, unique=True)
    titulo = models.CharField(max_length=200)
    subtitulo = models.CharField(max_length=300, blank=True)
    descripcion = models.TextField()
    nivel = models.CharField(max_length=20, choices=NIVEL_CHOICES)
    duracion_horas = models.PositiveIntegerField()
    costo = models.DecimalField(max_digits=10, decimal_places=2)
    modalidad = models.CharField(max_length=20, choices=MODALIDAD_CHOICES)
    fecha_inicio = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='activo')
    
    def __str__(self):
        return f"{self.codigo} - {self.titulo}"
    
    class Meta:
        db_table = 'curso'
