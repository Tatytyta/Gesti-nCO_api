from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CursoViewSet, horas_semanales, evaluacion_aprobacion

app_name = 'cursos'

router = DefaultRouter()
router.register(r'cursos', CursoViewSet, basename='curso')

urlpatterns = [
    path('reportes/horas-semanales', horas_semanales, name='horas-semanales'),
    path('reportes/evaluacion-aprobacion', evaluacion_aprobacion, name='evaluacion-aprobacion'),
    path('reportes/aprobacion', evaluacion_aprobacion, name='aprobacion'),  # Alias
] + router.urls
