from decimal import Decimal
from django import forms
from .models import Empleado, TipoIngreso, TipoDeduccion, Transaccion


class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = [
            'cedula',
            'nombre',
            'departamento',
            'puesto',
            'salario_mensual',
            'id_nomina',
        ]
        widgets = {
            'cedula': forms.TextInput(attrs={
                'class': 'w-full rounded-lg border border-gray-300 bg-white px-4 py-2 text-gray-900 shadow-sm focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 sm:text-sm',
                'placeholder': 'Ej. 402-0057193-9',
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'w-full rounded-lg border border-gray-300 bg-white px-4 py-2 text-gray-900 shadow-sm focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 sm:text-sm',
                'placeholder': 'Nombre completo del empleado',
            }),
            'departamento': forms.TextInput(attrs={
                'class': 'w-full rounded-lg border border-gray-300 bg-white px-4 py-2 text-gray-900 shadow-sm focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 sm:text-sm',
                'placeholder': 'Ej. Tecnología / Contabilidad',
            }),
            'puesto': forms.TextInput(attrs={
                'class': 'w-full rounded-lg border border-gray-300 bg-white px-4 py-2 text-gray-900 shadow-sm focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 sm:text-sm',
                'placeholder': 'Ej. Desarrollador Senior',
            }),
            'salario_mensual': forms.NumberInput(attrs={
                'class': 'w-full rounded-lg border border-gray-300 bg-white px-4 py-2 text-gray-900 shadow-sm focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 sm:text-sm',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0.01',
            }),
            'id_nomina': forms.TextInput(attrs={
                'class': 'w-full rounded-lg border border-gray-300 bg-white px-4 py-2 text-gray-900 shadow-sm focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 sm:text-sm',
                'placeholder': 'Ej. NOM-001',
            }),
        }

    def clean_salario_mensual(self):
        salario = self.cleaned_data.get('salario_mensual')
        if salario is not None and salario <= Decimal('0.00'):
            raise forms.ValidationError('El salario mensual debe ser mayor que cero.')
        return salario


class TipoIngresoForm(forms.ModelForm):
    class Meta:
        model = TipoIngreso
        fields = ['nombre', 'depende_de_salario', 'estado']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'w-full rounded-lg border border-gray-300 bg-white px-4 py-2 text-gray-900 shadow-sm focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 sm:text-sm',
                'placeholder': 'Nombre del tipo de ingreso',
            }),
            'depende_de_salario': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500',
            }),
            'estado': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500',
            }),
        }


class TipoDeduccionForm(forms.ModelForm):
    class Meta:
        model = TipoDeduccion
        fields = ['nombre', 'depende_de_salario', 'estado']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'w-full rounded-lg border border-gray-300 bg-white px-4 py-2 text-gray-900 shadow-sm focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 sm:text-sm',
                'placeholder': 'Nombre del tipo de deducción',
            }),
            'depende_de_salario': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500',
            }),
            'estado': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500',
            }),
        }


class TransaccionForm(forms.ModelForm):
    class Meta:
        model = Transaccion
        fields = [
            'empleado',
            'tipo_transaccion',
            'tipo_ingreso',
            'tipo_deduccion',
            'fecha',
            'monto',
            'estado',
        ]
        widgets = {
            'empleado': forms.Select(attrs={
                'class': 'w-full rounded-lg border border-gray-300 bg-white px-4 py-2 text-gray-900 shadow-sm focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 sm:text-sm',
            }),
            'tipo_transaccion': forms.Select(attrs={
                'class': 'w-full rounded-lg border border-gray-300 bg-white px-4 py-2 text-gray-900 shadow-sm focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 sm:text-sm',
                'hx-get': '/nomina/obtener-conceptos/',
                'hx-target': '#contenedor-conceptos',
                'hx-trigger': 'change',
            }),
            'tipo_ingreso': forms.Select(attrs={
                'class': 'w-full rounded-lg border border-gray-300 bg-white px-4 py-2 text-gray-900 shadow-sm focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 sm:text-sm',
            }),
            'tipo_deduccion': forms.Select(attrs={
                'class': 'w-full rounded-lg border border-gray-300 bg-white px-4 py-2 text-gray-900 shadow-sm focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 sm:text-sm',
            }),
            'fecha': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full rounded-lg border border-gray-300 bg-white px-4 py-2 text-gray-900 shadow-sm focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 sm:text-sm',
            }),
            'monto': forms.NumberInput(attrs={
                'class': 'w-full rounded-lg border border-gray-300 bg-white px-4 py-2 text-gray-900 shadow-sm focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 sm:text-sm',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0.01',
            }),
            'estado': forms.Select(attrs={
                'class': 'w-full rounded-lg border border-gray-300 bg-white px-4 py-2 text-gray-900 shadow-sm focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 sm:text-sm',
            }),
        }

    def clean_monto(self):
        monto = self.cleaned_data.get('monto')
        if monto is not None and monto <= Decimal('0.00'):
            raise forms.ValidationError('El monto debe ser mayor que cero.')
        return monto

    def clean(self):
        cleaned_data = super().clean()
        tipo_transaccion = cleaned_data.get('tipo_transaccion')
        tipo_ingreso = cleaned_data.get('tipo_ingreso')
        tipo_deduccion = cleaned_data.get('tipo_deduccion')

        if tipo_transaccion == Transaccion.TipoTransaccion.INGRESO:
            if not tipo_ingreso:
                self.add_error('tipo_ingreso', 'El tipo de ingreso es obligatorio cuando la transacción es de tipo Ingreso.')
            cleaned_data['tipo_deduccion'] = None

        elif tipo_transaccion == Transaccion.TipoTransaccion.DEDUCCION:
            if not tipo_deduccion:
                self.add_error('tipo_deduccion', 'El tipo de deducción es obligatorio cuando la transacción es de tipo Deducción.')
            cleaned_data['tipo_ingreso'] = None

        return cleaned_data
