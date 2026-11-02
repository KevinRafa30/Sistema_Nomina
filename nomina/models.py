from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator
from .validators import validar_cedula_dominicana


class TipoIngreso(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    depende_de_salario = models.BooleanField(default=False, verbose_name="Depende de salario")
    estado = models.BooleanField(default=True, verbose_name="Estado")

    class Meta:
        verbose_name = "Tipo de Ingreso"
        verbose_name_plural = "Tipos de Ingresos"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class TipoDeduccion(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    depende_de_salario = models.BooleanField(default=False, verbose_name="Depende de salario")
    estado = models.BooleanField(default=True, verbose_name="Estado")

    class Meta:
        verbose_name = "Tipo de Deducción"
        verbose_name_plural = "Tipos de Deducciones"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Empleado(models.Model):
    cedula = models.CharField(
        max_length=15,
        unique=True,
        validators=[validar_cedula_dominicana],
        verbose_name="Cédula",
    )
    nombre = models.CharField(max_length=150, verbose_name="Nombre")
    departamento = models.CharField(max_length=100, blank=True, null=True, verbose_name="Departamento")
    puesto = models.CharField(max_length=100, blank=True, null=True, verbose_name="Puesto")
    salario_mensual = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Salario mensual",
    )
    id_nomina = models.CharField(max_length=50, verbose_name="ID Nómina")

    class Meta:
        verbose_name = "Empleado"
        verbose_name_plural = "Empleados"
        ordering = ["nombre"]

    def __str__(self):
        return f"{self.nombre} ({self.cedula})"


class Transaccion(models.Model):
    class TipoTransaccion(models.TextChoices):
        INGRESO = 'Ingreso', 'Ingreso'
        DEDUCCION = 'Deducción', 'Deducción'

    class EstadoTransaccion(models.TextChoices):
        PENDIENTE = 'Pendiente', 'Pendiente'
        PROCESADA = 'Procesada', 'Procesada'
        CANCELADA = 'Cancelada', 'Cancelada'

    empleado = models.ForeignKey(
        Empleado,
        on_delete=models.CASCADE,
        related_name="transacciones",
        verbose_name="Empleado",
    )
    tipo_transaccion = models.CharField(
        max_length=20,
        choices=TipoTransaccion.choices,
        verbose_name="Tipo de transacción",
    )
    tipo_ingreso = models.ForeignKey(
        TipoIngreso,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="transacciones",
        verbose_name="Tipo de ingreso",
    )
    tipo_deduccion = models.ForeignKey(
        TipoDeduccion,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="transacciones",
        verbose_name="Tipo de deducción",
    )
    fecha = models.DateField(verbose_name="Fecha")
    monto = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Monto",
    )
    estado = models.CharField(
        max_length=20,
        choices=EstadoTransaccion.choices,
        default=EstadoTransaccion.PENDIENTE,
        verbose_name="Estado",
    )

    class Meta:
        verbose_name = "Transacción"
        verbose_name_plural = "Transacciones"
        ordering = ["-fecha"]

    def __str__(self):
        return f"{self.tipo_transaccion} - {self.empleado.nombre} - ${self.monto}"


class AsientoContable(models.Model):
    class TipoMovimiento(models.TextChoices):
        DB = 'DB', 'DB'
        CR = 'CR', 'CR'

    descripcion = models.CharField(max_length=255, verbose_name="Descripción")
    empleado = models.ForeignKey(
        Empleado,
        on_delete=models.CASCADE,
        related_name="asientos_contables",
        verbose_name="Empleado",
    )
    cuenta = models.CharField(max_length=50, verbose_name="Cuenta")
    tipo_movimiento = models.CharField(
        max_length=2,
        choices=TipoMovimiento.choices,
        verbose_name="Tipo de movimiento",
    )
    fecha_asiento = models.DateField(verbose_name="Fecha de asiento")
    monto_asiento = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Monto de asiento",
    )
    estado = models.CharField(max_length=50, default='Pendiente', verbose_name="Estado")

    class Meta:
        verbose_name = "Asiento Contable"
        verbose_name_plural = "Asientos Contables"
        ordering = ["-fecha_asiento"]

    def __str__(self):
        return f"{self.cuenta} ({self.tipo_movimiento}) - ${self.monto_asiento}"
