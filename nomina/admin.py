from django.contrib import admin
from .models import TipoIngreso, TipoDeduccion, Empleado, Transaccion, AsientoContable


@admin.register(TipoIngreso)
class TipoIngresoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'depende_de_salario', 'estado')
    list_filter = ('depende_de_salario', 'estado')
    search_fields = ('nombre',)


@admin.register(TipoDeduccion)
class TipoDeduccionAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'depende_de_salario', 'estado')
    list_filter = ('depende_de_salario', 'estado')
    search_fields = ('nombre',)


@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cedula', 'nombre', 'departamento', 'puesto', 'salario_mensual', 'id_nomina')
    search_fields = ('cedula', 'nombre', 'id_nomina', 'departamento', 'puesto')
    list_filter = ('departamento', 'puesto')


@admin.register(Transaccion)
class TransaccionAdmin(admin.ModelAdmin):
    list_display = ('id', 'empleado', 'tipo_transaccion', 'tipo_ingreso', 'tipo_deduccion', 'fecha', 'monto', 'estado')
    list_filter = ('tipo_transaccion', 'estado', 'fecha')
    search_fields = ('empleado__nombre', 'empleado__cedula')


@admin.register(AsientoContable)
class AsientoContableAdmin(admin.ModelAdmin):
    list_display = ('id', 'descripcion', 'empleado', 'cuenta', 'tipo_movimiento', 'fecha_asiento', 'monto_asiento', 'estado')
    list_filter = ('tipo_movimiento', 'estado', 'fecha_asiento')
    search_fields = ('descripcion', 'empleado__nombre', 'cuenta')
