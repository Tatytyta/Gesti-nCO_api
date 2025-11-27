from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Curso
from .serializers import CursoSerializer

class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'message': 'Curso creado exitosamente',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'success': False,
            'message': 'Error al crear el curso',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'success': True,
            'message': 'Cursos obtenidos exitosamente',
            'data': serializer.data
        })
    
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response({
                'success': True,
                'message': 'Curso encontrado',
                'data': serializer.data
            })
        except Curso.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Curso no encontrado'
            }, status=status.HTTP_404_NOT_FOUND)
    
    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'success': True,
                    'message': 'Curso actualizado exitosamente',
                    'data': serializer.data
                })
            return Response({
                'success': False,
                'message': 'Error al actualizar el curso',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        except Curso.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Curso no encontrado'
            }, status=status.HTTP_404_NOT_FOUND)
    
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete()
            return Response({
                'success': True,
                'message': 'Curso eliminado exitosamente'
            })
        except Curso.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Curso no encontrado'
            }, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def horas_semanales(request):
    try:
        horas_por_dia = request.data.get('horasPorDia', [])
        
        if not horas_por_dia or len(horas_por_dia) != 7:
            return Response({
                'success': False,
                'message': 'Debe proporcionar exactamente 7 valores para horasPorDia'
            }, status=status.HTTP_400_BAD_REQUEST)
        
       
        total_horas = 0
        for horas in horas_por_dia:
            if not isinstance(horas, (int, float)) or horas < 0:
                return Response({
                    'success': False,
                    'message': 'Todos los valores deben ser números no negativos'
                }, status=status.HTTP_400_BAD_REQUEST)
            total_horas += horas
        
        promedio = total_horas / 7
        
       
        if promedio < 1:
            mensaje = "Estás estudiando muy poco"
        elif 1 <= promedio <= 3:
            mensaje = "Buen ritmo de estudio"
        else:
            mensaje = "Excelente dedicación"
        
        return Response({
            'success': True,
            'totalHoras': total_horas,
            'promedio': round(promedio, 2),
            'mensaje': mensaje
        })
        
    except Exception as e:
        return Response({
            'success': False,
            'message': f'Error al procesar datos: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def evaluacion_aprobacion(request):
    try:
        notas = request.data.get('notas', [])
        nota_minima = request.data.get('notaMinima')
        
        if not notas or len(notas) < 3 or len(notas) > 5:
            return Response({
                'success': False,
                'message': 'Debe proporcionar entre 3 y 5 notas'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if nota_minima is None:
            return Response({
                'success': False,
                'message': 'Debe proporcionar la nota mínima'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        
        suma_notas = 0
        for nota in notas:
            if not isinstance(nota, (int, float)):
                return Response({
                    'success': False,
                    'message': 'Todas las notas deben ser números'
                }, status=status.HTTP_400_BAD_REQUEST)
            suma_notas += nota
        
        promedio = suma_notas / len(notas)
        
        if promedio >= nota_minima:
            estado = "Aprobado"
            mensaje = f"¡Felicidades! Has aprobado con un promedio de {promedio:.2f}"
        else:
            estado = "Reprobado"
            mensaje = f"No has alcanzado la nota mínima. Promedio: {promedio:.2f}, Requerido: {nota_minima}"
        
        return Response({
            'success': True,
            'promedio': round(promedio, 2),
            'estado': estado,
            'mensaje': mensaje
        })
        
    except Exception as e:
        return Response({
            'success': False,
            'message': f'Error al procesar evaluación: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
