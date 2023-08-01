import json
from django.shortcuts import render, redirect
from django.http import JsonResponse

from cake_shop.models import Layer, Shape, Topping, Berry, Decor, Client, Order

from cake_shop.models import Cake, OrderedCake


def index(request):
    data = {
        'js_data': {
            'Levels': ['не выбрано'],
            'Forms': ['не выбрано'],
            'Toppings': ['не выбрано'],
            'Berries': ['не выбрано'],
            'Decors': ['не выбрано'],
        },
        'layers': [],
        'shapes': [],
        'toppings': [],
        'berries': [],
        'decors': [],
        'js_costs': {
            'Levels': [0],
            'Forms': [0],
            'Toppings': [0],
            'Berries': [0],
            'Decors': [0],
            'Words': 500,
        }
    }
    for layer in Layer.objects.all():
        data['js_data']['Levels'].append(layer.title)
        data['js_costs']['Levels'].append(int(layer.price))
        data['layers'].append(layer.title)

    for shape in Shape.objects.all():
        data['js_data']['Forms'].append(shape.title)
        data['js_costs']['Forms'].append(int(shape.price))
        data['shapes'].append(shape.title)

    for topping in Topping.objects.all():
        data['js_data']['Toppings'].append(topping.title)
        data['js_costs']['Toppings'].append(int(topping.price))
        data['toppings'].append(topping.title)

    for berry in Berry.objects.all():
        data['js_data']['Berries'].append(berry.title)
        data['js_costs']['Berries'].append(int(berry.price))
        data['berries'].append(berry.title)

    for decor in Decor.objects.all():
        data['js_data']['Decors'].append(decor.title)
        data['js_costs']['Decors'].append(int(decor.price))
        data['decors'].append(decor.title)

    return render(request, 'index.html', context=data)



def lk(request, slug):
    client = Client.objects.filter(slug=slug).first()
    if client:

        mail = client.mail
        if not mail:
            mail = 'example@mail.ru'

        orders = Order.objects.filter(client=client)
        serialize_orders = []
        for order in orders:
            order = {
                'id': order.id,
                'cakes': order.cakes.all(),
                'price': order.order_price,
                'delivery_time': order.delivery_time
            }
            serialize_orders.append(order)

        data = {
            'js_client': {
                    "name": client.name,
                    "phone": client.phone,
                    "mail": mail,
                    "address": client.address,
                    "slug": client.slug,
            },
            'orders': orders
        }
        
    else:
        #  Test data
        orders = Order.objects.all()
        data = {
            'js_client': {
                    "name": 'myname',
                    "phone": '88005553535',
                    "mail": 'my@mail.ru',
                    "address": 'my address',
                    "slug": "slug",
            },
            'orders': orders
        }

    return render(request, 'lk_template.html', context=data)
    


def check_time_period(time):
    [hours, minutes] = ":".split(time)
    if minutes > 30:
        minutes = 0
        hours += 1
    else:
        minutes = 0
    if hours <= 10:
        period = '01'
    elif hours <= 12:
        period = '02'
    elif hours <= 14:
        period = '03'
    elif hours <= 16:
        period = '04'
    elif hours <= 18:
        period = '05'
    elif hours <= 20:
        period = '06'
    elif hours <= 22:
        period = '07'
    elif hours <= 22:
        period = '07'
    else:
        period = '07'

    return period


def find_layer(level, components):
    return Layer.objects.filter(title=components['Levels'][int(level)]).first()


def find_shape(shape, components):
    return Shape.objects.filter(title=components['Forms'][int(shape)]).first()


def find_topping(topping, components):
    return Topping.objects.filter(title=components['Toppings'][int(topping)]).first()


def find_berries(berries, components):
    return Berry.objects.filter(title=components['Berries'][int(berries)]).first()


def find_decor(decor, components):
    return Decor.objects.filter(title=components['Decors'][int(decor)]).first()


def get_input_price(input):
    if input:
        return 500
    return 0


def order(request):
    if request.method == "POST":
        data = json.loads(request.body)
        print(data)
        client, created = Client.objects.get_or_create(phone=data['Phone'])
        if client.name != data['Name']:
            client.name = data['Name']
        if client.mail != data['Email']:
            client.mail = data['Email']
        if client.address != data['Address']:
            client.address = data['Address']
        client.save()

        cake, created = Cake.objects.get_or_create(
            layers=find_layer(data['Levels'], data['components']),
            shape=find_shape(data['Form'], data['components']),
            toppings=find_topping(data['Topping'], data['components']),
            berries=find_berries(data['Berries'], data['components']),
            decor=find_decor(data['Decor'], data['components']),
        )

        order = Order.objects.create(
            client=client,
            comment=data['DelivComments'],
            delivery_date=data['Dates'],  # высчитать дату
            delivery_time=data['Time'],  # выбрать период по времени
            urgency=False,  # оценить срочность
            order_price=cake.get_price() + get_input_price(data['Words']),  # вычислить цену с учетом срочности
        )

        ordered_cake = OrderedCake.objects.create(
            order=order,
            cake=cake,
            comment=data['Comments'],
            cake_text=data['Words'],
        )

    return redirect('index')


def lk_order(request):
    return render(request, 'lk-order.html')


def serialize_cakes(cakes):
    serialized = []
    for cake in cakes:
        serialized.append(
            {
                'title': cake.title,
                'description': cake.description,
                'picture': cake.picture.url,
                'category': cake.category,
                'layers': cake.layers,
                'shape': cake.shape,
                'toppings': cake.toppings,
                'berries': cake.berries,
                'decor': cake.decor,
                'price':cake.get_price()
            }
        )
    return serialized


def cakes(request):
    default_cakes = Cake.objects.filter(default=True)
    context = {
        'cakes': serialize_cakes(default_cakes)
    }
    return render(request, 'cakes.html', context)
