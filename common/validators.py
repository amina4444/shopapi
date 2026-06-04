from rest_framework import serializers
from datetime import date,datetime

def validate_birthdate(birthdate):
    if birthdate is None:
        raise serializers.ValidationError(
            "Укажите дату рождения, чтобы создать продукт."
        )

    if isinstance(birthdate, str):
        birthdate = datetime.strptime( birthdate, "%Y-%m-%d" ).date()

    today = date.today()
    age = (today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day)) )

    if age < 18:
        raise serializers.ValidationError(
            "Вам должно быть 18 лет, чтобы создать продукт."
        )

    return birthdate

        
