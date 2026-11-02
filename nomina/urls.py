from django.urls import path
from . import views
from django.views.generic import RedirectView

app_name = 'nomina'

urlpatterns = [

    # Redirección de la raíz a la lista de empleados
    path('', RedirectView.as_view(url='empleados/', permanent=False), name='nomina_home'),
    
    # Empleados
    path('empleados/', views.empleados_list, name='empleados_list'),
    path('empleados/crear/', views.empleado_create, name='empleado_create'),
    path('empleados/<int:pk>/editar/', views.empleado_update, name='empleado_update'),
    path('empleados/<int:pk>/alternar-estado/', views.empleado_toggle_estado, name='empleado_toggle_estado'),

    # Tipos de Ingreso
    path('tipos-ingreso/', views.tipos_ingreso_list, name='tipos_ingreso_list'),
    path('tipos-ingreso/crear/', views.tipo_ingreso_create, name='tipo_ingreso_create'),
    path('tipos-ingreso/<int:pk>/editar/', views.tipo_ingreso_update, name='tipo_ingreso_update'),
    path('tipos-ingreso/<int:pk>/alternar-estado/', views.tipo_ingreso_toggle_estado, name='tipo_ingreso_toggle_estado'),

    # Tipos de Deducción
    path('tipos-deduccion/', views.tipos_deduccion_list, name='tipos_deduccion_list'),
    path('tipos-deduccion/crear/', views.tipo_deduccion_create, name='tipo_deduccion_create'),
    path('tipos-deduccion/<int:pk>/editar/', views.tipo_deduccion_update, name='tipo_deduccion_update'),
    path('tipos-deduccion/<int:pk>/alternar-estado/', views.tipo_deduccion_toggle_estado, name='tipo_deduccion_toggle_estado'),

    # Transacciones
    path('transacciones/', views.transacciones_list, name='transacciones_list'),
    path('transacciones/crear/', views.transaccion_create, name='transaccion_create'),
    path('transacciones/<int:pk>/editar/', views.transaccion_update, name='transaccion_update'),
    path('transacciones/<int:pk>/alternar-estado/', views.transaccion_toggle_estado, name='transaccion_toggle_estado'),

    # HTMX Helper
    path('obtener-conceptos/', views.obtener_conceptos, name='obtener_conceptos'),
]
