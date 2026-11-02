from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Empleado, TipoIngreso, TipoDeduccion, Transaccion
from .forms import EmpleadoForm, TipoIngresoForm, TipoDeduccionForm, TransaccionForm


# ==========================================
# Empleados
# ==========================================
def empleados_list(request):
    empleados = Empleado.objects.all()
    return render(request, 'nomina/empleados_list.html', {'empleados': empleados})


def empleado_create(request):
    if request.method == 'POST':
        form = EmpleadoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('nomina:empleados_list')
    else:
        form = EmpleadoForm()
    return render(request, 'nomina/empleado_form.html', {'form': form, 'titulo': 'Registrar Empleado'})


def empleado_update(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    if request.method == 'POST':
        form = EmpleadoForm(request.POST, instance=empleado)
        if form.is_valid():
            form.save()
            return redirect('nomina:empleados_list')
    else:
        form = EmpleadoForm(instance=empleado)
    return render(request, 'nomina/empleado_form.html', {'form': form, 'titulo': 'Editar Empleado', 'empleado': empleado})


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
    return render(request, 'nomina/tipos_ingreso_list.html', {'tipos': tipos})


def tipo_ingreso_create(request):
    if request.method == 'POST':
        form = TipoIngresoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('nomina:tipos_ingreso_list')
    else:
        form = TipoIngresoForm()
    return render(request, 'nomina/tipo_ingreso_form.html', {'form': form, 'titulo': 'Nuevo Tipo de Ingreso'})


def tipo_ingreso_update(request, pk):
    tipo = get_object_or_404(TipoIngreso, pk=pk)
    if request.method == 'POST':
        form = TipoIngresoForm(request.POST, instance=tipo)
        if form.is_valid():
            form.save()
            return redirect('nomina:tipos_ingreso_list')
    else:
        form = TipoIngresoForm(instance=tipo)
    return render(request, 'nomina/tipo_ingreso_form.html', {'form': form, 'titulo': 'Editar Tipo de Ingreso', 'tipo': tipo})


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
    return render(request, 'nomina/tipos_deduccion_list.html', {'tipos': tipos})


def tipo_deduccion_create(request):
    if request.method == 'POST':
        form = TipoDeduccionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('nomina:tipos_deduccion_list')
    else:
        form = TipoDeduccionForm()
    return render(request, 'nomina/tipo_deduccion_form.html', {'form': form, 'titulo': 'Nuevo Tipo de Deducción'})


def tipo_deduccion_update(request, pk):
    tipo = get_object_or_404(TipoDeduccion, pk=pk)
    if request.method == 'POST':
        form = TipoDeduccionForm(request.POST, instance=tipo)
        if form.is_valid():
            form.save()
            return redirect('nomina:tipos_deduccion_list')
    else:
        form = TipoDeduccionForm(instance=tipo)
    return render(request, 'nomina/tipo_deduccion_form.html', {'form': form, 'titulo': 'Editar Tipo de Deducción', 'tipo': tipo})


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
    return render(request, 'nomina/transacciones_list.html', {'transacciones': transacciones})


def transaccion_create(request):
    if request.method == 'POST':
        form = TransaccionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('nomina:transacciones_list')
    else:
        form = TransaccionForm()
    return render(request, 'nomina/transaccion_form.html', {'form': form, 'titulo': 'Nueva Transacción'})


def transaccion_update(request, pk):
    transaccion = get_object_or_404(Transaccion, pk=pk)
    if request.method == 'POST':
        form = TransaccionForm(request.POST, instance=transaccion)
        if form.is_valid():
            form.save()
            return redirect('nomina:transacciones_list')
    else:
        form = TransaccionForm(instance=transaccion)
    return render(request, 'nomina/transaccion_form.html', {'form': form, 'titulo': 'Editar Transacción', 'transaccion': transaccion})


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
    tipo = request.GET.get('tipo_transaccion') or request.POST.get('tipo_transaccion')
    if tipo == Transaccion.TipoTransaccion.INGRESO:
        conceptos = TipoIngreso.objects.filter(estado=True)
        opciones = ''.join(f'<option value="{c.id}">{c.nombre}</option>' for c in conceptos)
        return HttpResponse(
            f'''
            <label class="block text-sm font-medium text-gray-700 mb-1">Tipo de Ingreso</label>
            <select name="tipo_ingreso" id="id_tipo_ingreso" class="w-full rounded-lg border border-gray-300 bg-white px-4 py-2 text-gray-900 shadow-sm focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 sm:text-sm">
                <option value="">-- Seleccione un tipo de ingreso --</option>
                {opciones}
            </select>
            '''
        )
    elif tipo == Transaccion.TipoTransaccion.DEDUCCION:
        conceptos = TipoDeduccion.objects.filter(estado=True)
        opciones = ''.join(f'<option value="{c.id}">{c.nombre}</option>' for c in conceptos)
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
