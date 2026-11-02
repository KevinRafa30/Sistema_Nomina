from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.db.models import Q
from .models import Empleado, TipoIngreso, TipoDeduccion, Transaccion
from .forms import EmpleadoForm, TipoIngresoForm, TipoDeduccionForm, TransaccionForm

# Helper properties para facilitar acceso a campos requeridos en vistas y templates
if not hasattr(Transaccion, 'concepto'):
    @property
    def transaccion_concepto(self):
        if self.tipo_transaccion == Transaccion.TipoTransaccion.INGRESO:
            return self.tipo_ingreso.nombre if self.tipo_ingreso else '-'
        elif self.tipo_transaccion == Transaccion.TipoTransaccion.DEDUCCION:
            return self.tipo_deduccion.nombre if self.tipo_deduccion else '-'
        return '-'
    Transaccion.concepto = transaccion_concepto

if not hasattr(Transaccion, 'tipo'):
    @property
    def transaccion_tipo(self):
        return self.tipo_transaccion
    Transaccion.tipo = transaccion_tipo


# ==========================================
# Empleados
# ==========================================
def empleados_list(request):
    busqueda = request.GET.get('busqueda') or request.GET.get('q') or request.GET.get('buscar') or ''
    busqueda = busqueda.strip()
    empleados = Empleado.objects.all()
    if busqueda:
        busqueda_limpia = busqueda.replace('-', '').replace(' ', '')
        empleados = empleados.filter(
            Q(nombre__icontains=busqueda) |
            Q(cedula__icontains=busqueda) |
            Q(cedula__icontains=busqueda_limpia)
        )
    return render(request, 'nomina/empleados_list.html', {
        'empleados': empleados,
        'busqueda': busqueda,
        'q': busqueda,
    })


def empleado_create(request):
    if request.method == 'POST':
        form = EmpleadoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('nomina:empleados_list')
    else:
        form = EmpleadoForm()
    return render(request, 'nomina/empleado_form.html', {
        'form': form,
        'titulo': 'Registrar Empleado',
    })


def empleado_update(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    if request.method == 'POST':
        form = EmpleadoForm(request.POST, instance=empleado)
        if form.is_valid():
            form.save()
            return redirect('nomina:empleados_list')
    else:
        form = EmpleadoForm(instance=empleado)
    return render(request, 'nomina/empleado_form.html', {
        'form': form,
        'titulo': 'Editar Empleado',
        'empleado': empleado,
    })


def empleado_toggle_estado(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    if hasattr(empleado, 'estado'):
        empleado.estado = not empleado.estado
        empleado.save()
    return redirect('nomina:empleados_list')


# ==========================================
# Tipos de Ingreso
# ==========================================
def tipos_ingreso_list(request):
    tipos = TipoIngreso.objects.all()
    return render(request, 'nomina/tipos_ingreso_list.html', {
        'tipos': tipos,
        'tipos_ingreso': tipos,
    })


def tipo_ingreso_create(request):
    if request.method == 'POST':
        form = TipoIngresoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('nomina:tipos_ingreso_list')
    else:
        form = TipoIngresoForm()
    return render(request, 'nomina/tipo_ingreso_form.html', {
        'form': form,
        'titulo': 'Nuevo Tipo de Ingreso',
    })


def tipo_ingreso_update(request, pk):
    tipo = get_object_or_404(TipoIngreso, pk=pk)
    if request.method == 'POST':
        form = TipoIngresoForm(request.POST, instance=tipo)
        if form.is_valid():
            form.save()
            return redirect('nomina:tipos_ingreso_list')
    else:
        form = TipoIngresoForm(instance=tipo)
    return render(request, 'nomina/tipo_ingreso_form.html', {
        'form': form,
        'titulo': 'Editar Tipo de Ingreso',
        'tipo': tipo,
        'tipo_ingreso': tipo,
    })


def tipo_ingreso_toggle_estado(request, pk):
    tipo = get_object_or_404(TipoIngreso, pk=pk)
    tipo.estado = not tipo.estado
    tipo.save()
    return redirect('nomina:tipos_ingreso_list')


# ==========================================
# Tipos de Deducción
# ==========================================
def tipos_deduccion_list(request):
    tipos = TipoDeduccion.objects.all()
    return render(request, 'nomina/tipos_deduccion_list.html', {
        'tipos': tipos,
        'tipos_deduccion': tipos,
    })


def tipo_deduccion_create(request):
    if request.method == 'POST':
        form = TipoDeduccionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('nomina:tipos_deduccion_list')
    else:
        form = TipoDeduccionForm()
    return render(request, 'nomina/tipo_deduccion_form.html', {
        'form': form,
        'titulo': 'Nuevo Tipo de Deducción',
    })


def tipo_deduccion_update(request, pk):
    tipo = get_object_or_404(TipoDeduccion, pk=pk)
    if request.method == 'POST':
        form = TipoDeduccionForm(request.POST, instance=tipo)
        if form.is_valid():
            form.save()
            return redirect('nomina:tipos_deduccion_list')
    else:
        form = TipoDeduccionForm(instance=tipo)
    return render(request, 'nomina/tipo_deduccion_form.html', {
        'form': form,
        'titulo': 'Editar Tipo de Deducción',
        'tipo': tipo,
        'tipo_deduccion': tipo,
    })


def tipo_deduccion_toggle_estado(request, pk):
    tipo = get_object_or_404(TipoDeduccion, pk=pk)
    tipo.estado = not tipo.estado
    tipo.save()
    return redirect('nomina:tipos_deduccion_list')


# ==========================================
# Transacciones
# ==========================================
def transacciones_list(request):
    transacciones = Transaccion.objects.select_related('empleado', 'tipo_ingreso', 'tipo_deduccion').all()
    for t in transacciones:
        if t.tipo_transaccion == Transaccion.TipoTransaccion.INGRESO:
            t.concepto = t.tipo_ingreso.nombre if t.tipo_ingreso else '-'
        elif t.tipo_transaccion == Transaccion.TipoTransaccion.DEDUCCION:
            t.concepto = t.tipo_deduccion.nombre if t.tipo_deduccion else '-'
        else:
            t.concepto = '-'
        t.tipo = t.tipo_transaccion
    return render(request, 'nomina/transacciones_list.html', {'transacciones': transacciones})


def transaccion_create(request):
    if request.method == 'POST':
        form = TransaccionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('nomina:transacciones_list')
    else:
        form = TransaccionForm()
    return render(request, 'nomina/transaccion_form.html', {
        'form': form,
        'titulo': 'Nueva Transacción',
    })


def transaccion_update(request, pk):
    transaccion = get_object_or_404(Transaccion, pk=pk)
    if request.method == 'POST':
        form = TransaccionForm(request.POST, instance=transaccion)
        if form.is_valid():
            form.save()
            return redirect('nomina:transacciones_list')
    else:
        form = TransaccionForm(instance=transaccion)
    return render(request, 'nomina/transaccion_form.html', {
        'form': form,
        'titulo': 'Editar Transacción',
        'transaccion': transaccion,
    })


def transaccion_toggle_estado(request, pk):
    transaccion = get_object_or_404(Transaccion, pk=pk)
    ciclo = {
        Transaccion.EstadoTransaccion.PENDIENTE: Transaccion.EstadoTransaccion.PROCESADA,
        Transaccion.EstadoTransaccion.PROCESADA: Transaccion.EstadoTransaccion.CANCELADA,
        Transaccion.EstadoTransaccion.CANCELADA: Transaccion.EstadoTransaccion.PENDIENTE,
    }
    transaccion.estado = ciclo.get(transaccion.estado, Transaccion.EstadoTransaccion.PENDIENTE)
    transaccion.save()
    return redirect('nomina:transacciones_list')


# ==========================================
# Endpoint HTMX para Conceptos Dinámicos
# ==========================================
def obtener_conceptos(request):
    tipo = request.GET.get('tipo') or request.GET.get('tipo_transaccion') or request.POST.get('tipo') or request.POST.get('tipo_transaccion') or ''
    tipo = tipo.strip()

    if tipo.lower() in ['ingreso', 'ingresos'] or tipo == Transaccion.TipoTransaccion.INGRESO:
        conceptos = TipoIngreso.objects.filter(estado=True)
        opciones = ''.join(f'<option value="{c.id}">{c.nombre}</option>' for c in conceptos)

        hx_target = request.headers.get('HX-Target', '').replace('#', '')
        if request.GET.get('format') == 'options' or hx_target in ['id_tipo_ingreso', 'id_concepto', 'concepto']:
            return HttpResponse(f'<option value="">-- Seleccione un tipo de ingreso --</option>{opciones}')

        return HttpResponse(
            f'''
            <label class="block text-sm font-medium text-gray-700 mb-1">Tipo de Ingreso</label>
            <select name="tipo_ingreso" id="id_tipo_ingreso" class="w-full rounded-lg border border-gray-300 bg-white px-4 py-2 text-gray-900 shadow-sm focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 sm:text-sm">
                <option value="">-- Seleccione un tipo de ingreso --</option>
                {opciones}
            </select>
            '''
        )
    elif tipo.lower() in ['deduccion', 'deducción', 'deducciones'] or tipo == Transaccion.TipoTransaccion.DEDUCCION:
        conceptos = TipoDeduccion.objects.filter(estado=True)
        opciones = ''.join(f'<option value="{c.id}">{c.nombre}</option>' for c in conceptos)

        hx_target = request.headers.get('HX-Target', '').replace('#', '')
        if request.GET.get('format') == 'options' or hx_target in ['id_tipo_deduccion', 'id_concepto', 'concepto']:
            return HttpResponse(f'<option value="">-- Seleccione un tipo de deducción --</option>{opciones}')

        return HttpResponse(
            f'''
            <label class="block text-sm font-medium text-gray-700 mb-1">Tipo de Deducción</label>
            <select name="tipo_deduccion" id="id_tipo_deduccion" class="w-full rounded-lg border border-gray-300 bg-white px-4 py-2 text-gray-900 shadow-sm focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 sm:text-sm">
                <option value="">-- Seleccione un tipo de deducción --</option>
                {opciones}
            </select>
            '''
        )
    return HttpResponse(
        '<div class="text-sm text-gray-500 italic p-2 bg-gray-50 rounded-lg">Seleccione un tipo de transacción para cargar los conceptos disponibles.</div>'
    )
