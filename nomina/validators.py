import re
from django.core.exceptions import ValidationError


def validar_cedula_dominicana(value):
    """
    Valida que el texto tenga 11 dígitos numéricos y sea una cédula dominicana
    válida según el algoritmo de Luhn (Módulo 10).
    """
    if not value:
        raise ValidationError('La cédula no puede estar vacía.')

    cedula_str = str(value).strip()
    # Permitir ingresar la cédula con o sin guiones/espacios
    cedula_limpia = re.sub(r'[-\s]', '', cedula_str)

    if not cedula_limpia.isdigit() or len(cedula_limpia) != 11:
        raise ValidationError('La cédula debe contener exactamente 11 dígitos numéricos.')

    if cedula_limpia == '0' * 11:
        raise ValidationError('La cédula no puede estar compuesta solo de ceros.')

    # Algoritmo de Luhn (Módulo 10) para Cédula Dominicana
    multiplicadores = [1, 2, 1, 2, 1, 2, 1, 2, 1, 2]
    suma = 0

    for i in range(10):
        digito = int(cedula_limpia[i]) * multiplicadores[i]
        if digito > 9:
            digito = (digito // 10) + (digito % 10)
        suma += digito

    verificador_calculado = (10 - (suma % 10)) % 10
    verificador_real = int(cedula_limpia[10])

    if verificador_calculado != verificador_real:
        raise ValidationError('El número de cédula no es válido según el algoritmo de Luhn (Módulo 10).')

    return True
