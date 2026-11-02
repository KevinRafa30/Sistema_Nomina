# Sistema de Gestión de Nóminas e Interfaz

Sistema web de administración de nóminas desarrollado para la asignatura **Nómina e Interfaz** de la **Universidad APEC**. El proyecto implementa una arquitectura híbrida (**Tecnología Open Source + Tecnología Propietaria**) diseñada para interoperar a futuro con el Sistema de Contabilidad mediante Servicios Web.

---

##  Alcance Funcional del Sistema

El sistema cubre la gestión completa del ciclo de nóminas a través de interfaces administrativas modernas:

1. **Gestión de Tipos de Ingresos:** Catálogo para registrar conceptos de ingresos (Horas extras, Comisiones, Bonos), especificando si dependen de salario y controlando su estado (Activo/Inactivo).
2. **Gestión de Tipos de Deducciones:** Catálogo para registrar deducciones de ley y de empresa (AFP, SFS, ISR, Préstamos), con indicador de dependencia salarial y estado.
3. **Gestión de Empleados:** Administración del personal con registro de Cédula (validada mediante algoritmo Módulo 10 / Luhn), Nombre, Departamento (opcional), Puesto (opcional), Salario Mensual (> 0) e Identificador de Nómina.
4. **Registro de Transacciones de Entrada y Salida:** Formulario reactivo donde la selección del tipo (Ingreso/Deducción) actualiza al instante los conceptos activos disponibles mediante HTMX, asociando empleado, concepto, fecha, monto y estado.
5. **Módulos Siguientes:**
   - Consulta multicriterio por empleado, tipo y rango de fechas.
   - Generación y envío del asiento contable del período hacia el Sistema de Contabilidad mediante Servicio Web.

---

##  Stack Tecnológico (Enfoque Híbrido)

* **Capa Open Source:**
  - **Backend:** Python 3.x con Django Framework.
  - **Interactividad Dinámica:** HTMX (solicitudes asíncronas y reemplazo de fragmentos HTML sin recargar).
  - **Interfaz de Usuario:** Plantilla Material Dashboard Free de Creative Tim basada en Bootstrap 5, HTML5 y CSS3.
* **Capa Propietaria:**
  - **Motor de Base de Datos:** Microsoft SQL Server (o configuración compatible para producción) / Integración corporativa Microsoft.
  - **Conector de Datos:** Microsoft ODBC Driver for SQL Server y mssql-django.

---

##  Estructura del Proyecto

```text
Sistema_Nomina/
├── core/                  # Configuración principal de Django (settings, urls, wsgi)
├── nomina/                # Aplicación principal de nómina
│   ├── migrations/        # Historial de migraciones de base de datos
│   ├── templates/nomina/  # Vistas HTML (empleados, ingresos, deducciones, transacciones)
│   ├── forms.py           # Formularios con validaciones de negocio
│   ├── models.py          # Modelos de datos (Empleado, Transaccion, AsientoContable, etc.)
│   ├── urls.py            # Enrutador de módulos y endpoints HTMX
│   ├── validators.py      # Algoritmo de validación de cédula dominicana
│   └── views.py           # Controladores de negocio y endpoints dinámicos
├── static/                # Archivos estáticos de Material Dashboard (css, js, img)
├── manage.py              # Administrador de comandos de Django
├── requirements.txt       # Dependencias del proyecto
└── README.md              # Documentación general
```

---

##  Guía de Instalación y Puesta en Marcha

Sigue estos pasos para clonar y ejecutar el proyecto en tu equipo local:

### 1. Clonar el repositorio
```bash
git clone https://github.com/KevinRafa30/Sistema_Nomina.git
cd Sistema_Nomina
```

### 2. Crear y activar el entorno virtual
* **En Windows (PowerShell):**
  ```powershell
  python -m venv .venv
  Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
  .\.venv\Scripts\Activate.ps1
  ```
* **En macOS / Linux:**
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Ejecutar migraciones de la base de datos
```bash
python manage.py migrate
```

### 5. Iniciar el servidor local
```bash
python manage.py runserver
```
Abre tu navegador e ingresa a `http://127.0.0.1:8000/`.

---

##  Estándares de Trabajo en Git

Para mantener la trazabilidad de los cambios en el repositorio, se sigue la regla de **commits atómicos individuales por archivo modificado**, utilizando mensajes concisos en español:
* `feat(archivo): descripción` para nuevas características.
* `fix(archivo): descripción` para corrección de errores.
* `docs(archivo): descripción` para cambios en documentación.
* `style(archivo): descripción` para estilos o maquetación.
