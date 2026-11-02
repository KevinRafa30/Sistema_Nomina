from decimal import Decimal
from django.test import TestCase
from django.core.exceptions import ValidationError
from datetime import date
from .validators import validar_cedula_dominicana
from .models import TipoIngreso, TipoDeduccion, Empleado, Transaccion, AsientoContable


class CedulaValidatorTest(TestCase):
    def test_valid_cedula(self):
        # Cédulas válidas con algoritmo de Luhn (Módulo 10)
        self.assertTrue(validar_cedula_dominicana('40200571939'))
        self.assertTrue(validar_cedula_dominicana('402-0057193-9'))
        self.assertTrue(validar_cedula_dominicana('00100000017'))

    def test_invalid_cedula_length(self):
        with self.assertRaises(ValidationError):
            validar_cedula_dominicana('12345')

    def test_invalid_cedula_all_zeros(self):
        with self.assertRaises(ValidationError):
            validar_cedula_dominicana('00000000000')

    def test_invalid_cedula_checksum(self):
        with self.assertRaises(ValidationError):
            validar_cedula_dominicana('40200571931')


class ModelosNominaTest(TestCase):
    def setUp(self):
        self.tipo_ingreso = TipoIngreso.objects.create(
            nombre='Horas Extras',
            depende_de_salario=True,
            estado=True
        )
        self.tipo_deduccion = TipoDeduccion.objects.create(
            nombre='Seguro Médico',
            depende_de_salario=False,
            estado=True
        )
        self.empleado = Empleado.objects.create(
            cedula='40200571939',
            nombre='Juan Pérez',
            departamento='Tecnología',
            puesto='Desarrollador',
            salario_mensual=Decimal('75000.00'),
            id_nomina='NOM-001'
        )

    def test_creacion_empleado_valido(self):
        self.assertEqual(self.empleado.nombre, 'Juan Pérez')
        self.empleado.full_clean()

    def test_empleado_cedula_invalida(self):
        empleado_invalido = Empleado(
            cedula='00011122233',
            nombre='Carlos Gómez',
            salario_mensual=Decimal('50000.00'),
            id_nomina='NOM-002'
        )
        with self.assertRaises(ValidationError):
            empleado_invalido.full_clean()

    def test_creacion_transaccion(self):
        transaccion = Transaccion.objects.create(
            empleado=self.empleado,
            tipo_transaccion=Transaccion.TipoTransaccion.INGRESO,
            tipo_ingreso=self.tipo_ingreso,
            fecha=date.today(),
            monto=Decimal('5000.00')
        )
        self.assertEqual(transaccion.estado, Transaccion.EstadoTransaccion.PENDIENTE)
        self.assertEqual(transaccion.empleado, self.empleado)

    def test_creacion_asiento_contable(self):
        asiento = AsientoContable.objects.create(
            descripcion='Pago nómina quincenal',
            empleado=self.empleado,
            cuenta='6101-01',
            tipo_movimiento=AsientoContable.TipoMovimiento.DB,
            fecha_asiento=date.today(),
            monto_asiento=Decimal('75000.00'),
            estado='Pendiente'
        )
        self.assertEqual(asiento.cuenta, '6101-01')
        self.assertEqual(asiento.tipo_movimiento, AsientoContable.TipoMovimiento.DB)
