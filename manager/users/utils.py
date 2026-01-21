import re
from django.core.exceptions import ValidationError


def validate_digit(string: str, digit: str):
    counter = 10
    final_sum = 0

    for c in string:
        final_sum += int(c) * counter
        counter -= 1

    mod = final_sum % 11

    if mod in [0, 1]:
        return int(digit) == 0
    
    return int(digit) == 11 - mod


def validate_cpf(value: str):
    """
    Validates CPF format and applies custom logic.
    """
    
    CPF_REGEX = r'^\d{3}\.\d{3}\.\d{3}-\d{2}$'

    if not re.match(CPF_REGEX, value):
        raise ValidationError("CPF deve estar no formato 000.000.000-00")

    numbers = value.replace(".", "").replace("-", "")

    if len(numbers) != 11:
        raise ValidationError("CPF deve conter 11 dígitos")
    
    if validate_digit(numbers[0:9], numbers[9]) and validate_digit(numbers[1:10], numbers[10]):
        return
    


def validate_cpf_schema(value: str):
    """
    Validates CPF format and applies custom logic.
    """
    
    CPF_REGEX = r'^\d{3}\.\d{3}\.\d{3}-\d{2}$'

    if not re.match(CPF_REGEX, value):
        return False

    numbers = value.replace(".", "").replace("-", "")

    if len(numbers) != 11:
        return False
    
    if validate_digit(numbers[0:9], numbers[9]) and validate_digit(numbers[1:10], numbers[10]):
        return True
    
    

