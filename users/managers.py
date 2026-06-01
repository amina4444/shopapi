from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email,password=None,**extra_fields):
        if not email:
            raise ValueError('email is reqwired')
        email = self.normalize_email(email)
        user = self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save()
        return user 
    def create_superuser(self, email,password=None,phone_number=None,**extra_fields):
        extra_fields.setdefault("is_staff",True)
        extra_fields.setdefault("is_superuser",True)
        extra_fields.setdefault("is_active",True)
        if not phone_number:
            raise ValueError("Superuser must have a phone number")

        extra_fields["phone_number"] = phone_number
        
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_staff=True")
        if extra_fields.get("is_active") is not True:
            raise ValueError("Superuser must have is_staff=True")
        if not phone_number:
            raise ValueError("Superuser must have a phone number")

        extra_fields["phone_number"] = phone_number

        return self.create_user(email,password,**extra_fields)



