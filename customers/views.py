import re

from django.shortcuts import get_object_or_404, redirect, reverse
from django.http import JsonResponse, HttpResponse
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt

from .models import Customer
from orders.models import Order, ActiveOrder
from robots.models import RobotOffer, RobotRelease
# Create your views here.

email_regex = r'^[A-Za-z0-9._-]*[@]{1}[А-Яа-яЁёA-Za-z0-9.]*[.]{1}[a-z.]*[a-z]{1}$'
regex_serial = r'^[A-Z0-9]{2}[\-]{1}[A-Z0-9]{2}$'

email_message= 'Добрый день!\nНедавно вы интересовались нашим роботом модели {}, версии {}.\nЭтот робот теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами\n'


@csrf_exempt
def total_customers(request):
    """
    Данное представление создано для того, чтобы отображать всех зарегистрированных
    в системе потребителей. Также данное представление позволяет создавать новых покупателей.
    :param request: с помощью GET запроса из строки url можно создать нового пользователя,
    введя после параметра email валидный email:
    например: "http://127.0.0.1:8000/customers?email=vasya@example.com"
    :return:JSONResponse со всеми созданными потребителями
    """

    if request.GET.get('email'):
        email = request.GET.get('email')
        if not re.match(email_regex, email):
            return HttpResponse('Пожалуйста, введите валидный адрес электронной почты')
        if not Customer.objects.filter(email=email):
            Customer.objects.create(email=email)
            return redirect(reverse('customers:customers'))
        else:
            return HttpResponse('Данный покупатель зарегитрирован')

    customers = Customer.objects.all()
    data = list()

    for customer in customers:
        customer = dict(email=customer.email,
                        hyperlink=f'http://127.0.0.1:8000/customers/{customer.pk}/')
        data.append(customer)

    data = dict(customers=data)

    return JsonResponse(data, safe=False)


@csrf_exempt
def customer_order_list(request, pk):
    """
    Данное представление позволяет создать новый ордер заказчика. Если после создание ордера
    обнаружится, что робот под таким серийным номером уже существует, заказчику придет соответсвующее
    письмо на электронную почту, а одер переместиться из актиных в неактивные. Если ордер будет составлен
    некорректно, поступит соответствующее сообщение.
    :param request: с помощью запроса к url, можно создать заказ, присвоив значение параметру serial,
    например: "http://127.0.0.1:8000/customers/1?serial=R2-D2"
    :param pk: это id заказчика
    :return:JSONResponse со всеми активными заказами заказчика
    """

    customer = get_object_or_404(Customer, pk=pk)

    if request.GET.get('serial'):
        serial = request.GET.get('serial')

        if not re.match(regex_serial, serial):
            return HttpResponse('Введите серийный номер в формате: '
                                '2 символа - дефис- 2 символа '
                                '(допускаются прописные буквы латинского алфавита и цифры. Например:'
                                '"T3-L0". '
                                'Серийные номера можно посмотреть по адресу: http://127.0.0.1:8000/')
        else:
            customer.order_set.create(robot_serial=serial)
            active = customer.actives.create(robot_serial=serial)
            if not RobotOffer.objects.filter(serial=serial):
                return redirect(reverse('customers:customer', kwargs={
                    'pk': customer.pk
                }))
            else:
                offer = RobotOffer.objects.filter(serial=serial).first()
                RobotRelease.objects.create(model=offer.model,
                                            version=offer.version,
                                            created=offer.created)
                customer.releases.create(robot_serial=serial)
                send_mail(
                    subject='Ваш заказ готов',
                    message=email_message.format(offer.model, offer.version),
                    from_email='vitalytanceforwork@gmail.com',
                    recipient_list=[customer.email]
                )
                offer.delete()
                active.delete()
                return redirect(reverse('customers:customer', kwargs={
                    'pk': customer.pk
                }))

    orders = customer.actives.all()
    data = list()
    for order in orders:
        order = dict(order=order.robot_serial)
        data.append(order)

    data = dict(customer=customer.email,
                orders=data)

    return JsonResponse(data, safe=False)
