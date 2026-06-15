from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from users.models import CustomUser 
from product.models import Product

@shared_task
def add(x,y):
    print("start adding",x,y)
    from time import sleep

    sleep(15)
    return x + y

@shared_task
def send_otp_mail(email,code):
    send_mail(
        subject="OTP for registration",
        message=f"code: {code}",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False ,
    )
    return "OK"


@shared_task
def send_report_mail():
    send_mail(
        subject="report!!!",
        message="lalallaa",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=["aminaismailova869@gmail.com"],
        fail_silently=False ,
    )
    return "OK"

@shared_task 
def send_great_mail(email):
    send_mail(
        subject="Welcome!",
        message="thank you for choosing our shop!",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False ,
    )
    from time import sleep

    sleep(10)
    return "OK"

@shared_task 
def send_list_produckts():
    users = CustomUser.objects.filter(is_active=True)

    emails = [user.email for user in users]

    if emails:
        send_mail(
            subject="Новинки!!!",
            message="проверьте наши товары!!!!!",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=emails,
            fail_silently=False ,
    )
    return "OK"

@shared_task
def number_of_products():
    count_products = Product.objects.count()

    send_mail(
        subject="monthly statistic",
        message=f"number of Products:  {count_products} ",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=["admin@gmail.com"],
        fail_silently=False,
    )
    print(count_products)
    return f"number of Products:  {count_products} "


