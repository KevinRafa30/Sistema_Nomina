from decimal import Decimal
from datetime import date
from django.test import TestCase, Client
from django.urls import reverse
from django.core.exceptions import ValidationError
from .validators import validar_cedula_dominicana
from .models import TipoIngreso, TipoDeduccion, Empleado, Transaccion, AsientoContable
from .forms import EmpleadoForm, TransaccionForm


class CedulaValidatorTest(TestCase):
    def test_valid_cedula(self):
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


class FormsNominaTest(TestCase):
    def setUp(self):
        self.empleado = Empleado.objects.create(
            cedula='40200571939',
            nombre='Ana Torres',
            salario_mensual=Decimal('50000.00'),
            id_nomina='NOM-003'
        )
        self.tipo_ingreso = TipoIngreso.objects.create(nombre='Bono Desempeño', estado=True)
        self.tipo_deduccion = TipoDeduccion.objects.create(nombre='Cooperativa', estado=True)

    def test_empleado_form_salario_positivo(self):
        form = EmpleadoForm(data={
            'cedula': '00100000017',
            'nombre': 'Luis Martínez',
            'departamento': 'Ventas',
            'puesto': 'Ejecutivo',
            'salario_mensual': '45000.00',
            'id_nomina': 'NOM-004'
        })
        self.assertTrue(form.is_valid())

    def test_empleado_form_salario_cero_o_negativo(self):
        form = EmpleadoForm(data={
            'cedula': '00100000017',
            'nombre': 'Luis Martínez',
            'salario_mensual': '0.00',
            'id_nomina': 'NOM-004'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('salario_mensual', form.errors)

    def test_transaccion_form_ingreso_sin_tipo_ingreso(self):
        form = TransaccionForm(data={
            'empleado': self.empleado.id,
            'tipo_transaccion': Transaccion.TipoTransaccion.INGRESO,
            'tipo_ingreso': '',
            'tipo_deduccion': '',
            'fecha': '2026-11-01',
            'monto': '1500.00',
            'estado': Transaccion.EstadoTransaccion.PENDIENTE
        })
        self.assertFalse(form.is_valid())
        self.assertIn('tipo_ingreso', form.errors)

    def test_transaccion_form_deduccion_sin_tipo_deduccion(self):
        form = TransaccionForm(data={
            'empleado': self.empleado.id,
            'tipo_transaccion': Transaccion.TipoTransaccion.DEDUCCION,
            'tipo_ingreso': '',
            'tipo_deduccion': '',
            'fecha': '2026-11-01',
            'monto': '800.00',
            'estado': Transaccion.EstadoTransaccion.PENDIENTE
        })
        self.assertFalse(form.is_valid())
        self.assertIn('tipo_deduccion', form.errors)

    def test_transaccion_form_ingreso_valido(self):
        form = TransaccionForm(data={
            'empleado': self.empleado.id,
            'tipo_transaccion': Transaccion.TipoTransaccion.INGRESO,
            'tipo_ingreso': self.tipo_ingreso.id,
            'tipo_deduccion': '',
            'fecha': '2026-11-01',
            'monto': '2500.00',
            'estado': Transaccion.EstadoTransaccion.PENDIENTE
        })
        self.assertTrue(form.is_valid())

    def test_htmx_obtener_conceptos(self):
        client = Client()
        url = reverse('nomina:obtener_conceptos')
        resp = client.get(url, {'tipo_transaccion': 'Ingreso'})
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Bono Desempeño')

        resp2 = client.get(url, {'tipo_transaccion': 'Deducción'})
        self.assertEqual(resp2.status_code, 200)
        self.assertContains(resp2, 'Cooperativa')
