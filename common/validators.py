from datetime import date
from rest_framework.exceptions import ValidationError

def validate_age(birthday):
    if not birthday:
        raise ValidationError("Укажите дату рождения, чтобы создать продукт")
    
    today = date.today()
    age = today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))

    if age < 18:
        raise ValidationError("Age should be at least 18")