from django.shortcuts import render
from django.http import JsonResponse

from .models import Order, ActiveOrder, ReleaseOrder
from customers.models import Customer
# Create your views here.


def total_orders(request):
    """
    Данное представление отображает все ордера (активные и неактивные) от всех пользователей.
    :param request: обращается к представлению
    :return: JSONResponse всех ордеров всех пользователей
    """

    customers = Customer.objects.all()
    data = list()

    for customer in customers:

        order_list = list()
        orders = Order.objects.filter(customer_id=customer.pk).values('order')
        for order in orders:
            order_list.append(order)

        order_list = dict(orders=order_list)
        data.append(order_list)

    data = dict(customers=data)

    return JsonResponse(data, safe=False)


def active_orders(request):
    """
    Данное представление отображает все активные ордера  от всех пользователей.
    :param request: обращается к представлению
    :return: JSONResponse всех активных ордеров всех пользователей
    """

    customers = Customer.objects.all()
    data = list()

    for customer in customers:

        order_list = list()
        orders = ActiveOrder.objects.filter(customer_id=customer.pk).values('order')
        for order in orders:
            order_list.append(order)

        order_list = dict(orders=order_list)
        data.append(order_list)

    data = dict(customers=data)

    return JsonResponse(data, safe=False)


def realised_orders(request):
    """
    Данное представление отображает все реализованные ордера от всех пользователей.
    :param request: обращается к представлению
    :return: JSONResponse всех реализованных ордеров всех пользователей
    """

    customers = Customer.objects.all()
    data = list()

    for customer in customers:

        order_list = list()
        orders = ReleaseOrder.objects.filter(customer_id=customer.pk).values('order')
        for order in orders:
            order_list.append(order)

        order_list = dict(orders=order_list)
        data.append(order_list)

    data = dict(customers=data)

    return JsonResponse(data, safe=False)
