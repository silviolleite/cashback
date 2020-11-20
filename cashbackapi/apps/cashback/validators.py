import logging
import re

from django.utils.translation import ugettext_lazy as _
from django.forms import ValidationError

logger = logging.getLogger(__name__)

default_error_messages = {
    'invalid': _('Número de CPF inválido.'),
    'max-digits': _('CPF deve ter 11 digitos.'),
    'not-upper': _('Este deve conter apenas caracteres minúsculo.'),
    'not-special-char': _('Este campo não deve conter caracteres especiais e espaços.'),
}

cpf_digits_re = re.compile(r'^(\d{3})\.(\d{3})\.(\d{3})-(\d{2})$')


def validate_cpf(value):
    logger.info("Checking if document is valid")
    logger.debug(f"Checking is CPF={value} is valid")
    if not value.isdigit():
        logger.info("Document is not valid")
        raise ValidationError(default_error_messages['invalid'], 'format')

    logger.info("Document is valid")
    return value


def validate_username(value):
    if not value.isalnum():
        raise ValidationError(default_error_messages['not-special-char'], 'format')

    if value.lower() != value:
        raise ValidationError(default_error_messages['not-upper'], 'format')

    return value
