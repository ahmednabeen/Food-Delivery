import json
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Order

FOOD_DATA = {
    'eat-frio': {
        'name': 'Eat Frio', 'image': 'frio.png', 'time': '25 mins',
        'rating': '★★★★☆', 'price': 12.99, 'category': 'Italian',
        'description': 'Curabitur mollis bibendum luctus. Duis suscipit vitae dui sed suscipit. Vestibulum auctor nunc vitae diam eleifend.',
    },
    'turkish-cuisine': {
        'name': 'Turkish Cuisine', 'image': 'cousine.png', 'time': '50 mins',
        'rating': '★★★★☆', 'price': 18.99, 'category': 'Turkish',
        'description': 'Curabitur mollis bibendum luctus. Duis suscipit vitae dui sed suscipit. Vestibulum auctor nunc vitae diam eleifend, in maximus metus sollicitudin.',
    },
    'pizzario': {
        'name': 'Pizzario', 'image': 'pizzario.png', 'time': '45 mins',
        'rating': '★★★★☆', 'price': 15.99, 'category': 'Italian',
        'description': 'Curabitur mollis bibendum luctus. Duis suscipit vitae dui sed suscipit. Vestibulum auctor nunc vitae diam eleifend.',
    },
    'sushi-delight': {
        'name': 'Sushi Delight', 'image': 'frio.png', 'time': '30 mins',
        'rating': '★★★★☆', 'price': 22.99, 'category': 'Japanese',
        'description': 'Curabitur mollis bibendum luctus. Duis suscipit vitae dui sed suscipit.',
    },
    'burger-haven': {
        'name': 'Burger Haven', 'image': 'cousine.png', 'time': '20 mins',
        'rating': '★★★★☆', 'price': 11.99, 'category': 'American',
        'description': 'Curabitur mollis bibendum luctus. Duis suscipit vitae dui sed suscipit.',
    },
    'pasta-palace': {
        'name': 'Pasta Palace', 'image': 'pizza.png', 'time': '40 mins',
        'rating': '★★★★☆', 'price': 14.99, 'category': 'Italian',
        'description': 'Curabitur mollis bibendum luctus. Duis suscipit vitae dui sed suscipit.',
    },
    'salad-fresh': {
        'name': 'Salad Fresh', 'image': 'frio.png', 'time': '25 mins',
        'rating': '★★★★☆', 'price': 9.99, 'category': 'Healthy',
        'description': 'Curabitur mollis bibendum luctus. Duis suscipit vitae dui sed suscipit.',
    },
    'steak-house': {
        'name': 'Steak House', 'image': 'cousine.png', 'time': '50 mins',
        'rating': '★★★★☆', 'price': 29.99, 'category': 'American',
        'description': 'Curabitur mollis bibendum luctus. Duis suscipit vitae dui sed suscipit.',
    },
    'taco-fiesta': {
        'name': 'Taco Fiesta', 'image': 'pizza.png', 'time': '35 mins',
        'rating': '★★★★☆', 'price': 10.99, 'category': 'Mexican',
        'description': 'Curabitur mollis bibendum luctus. Duis suscipit vitae dui sed suscipit.',
    },
    'ramen-bowl': {
        'name': 'Ramen Bowl', 'image': 'frio.png', 'time': '30 mins',
        'rating': '★★★★☆', 'price': 13.99, 'category': 'Japanese',
        'description': 'Curabitur mollis bibendum luctus. Duis suscipit vitae dui sed suscipit.',
    },
    'curry-delight': {
        'name': 'Curry Delight', 'image': 'cousine.png', 'time': '45 mins',
        'rating': '★★★★☆', 'price': 16.99, 'category': 'Indian',
        'description': 'Curabitur mollis bibendum luctus. Duis suscipit vitae dui sed suscipit.',
    },
}


def get_cart(request):
    return json.loads(request.session.get('cart', '{}'))


def save_cart(request, cart):
    request.session['cart'] = json.dumps(cart)


def cart_count(request):
    cart = get_cart(request)
    return sum(item['qty'] for item in cart.values())


def index(request):
    return render(request, 'index.html', {'cart_count': cart_count(request)})


def account(request):
    return render(request, 'account.html', {'cart_count': cart_count(request)})


def browse(request):
    food_data = {slug: {**info, 'slug': slug} for slug, info in FOOD_DATA.items()}
    return render(request, 'browse.html', {
        'cart_count': cart_count(request),
        'food_data_json': json.dumps(food_data, default=str),
    })


def login(request):
    return render(request, 'login.html')


def register(request):
    return render(request, 'register.html')


def food_detail(request, slug):
    food = FOOD_DATA.get(slug)
    if not food:
        from django.http import Http404
        raise Http404("Food not found")
    return render(request, 'food-detail.html', {
        'food': food, 'slug': slug,
        'food_image': 'images/' + food['image'],
        'cart_count': cart_count(request),
    })


def add_to_cart(request, slug):
    food = FOOD_DATA.get(slug)
    if not food:
        from django.http import Http404
        raise Http404("Food not found")
    cart = get_cart(request)
    if slug in cart:
        cart[slug]['qty'] += 1
    else:
        cart[slug] = {'qty': 1, 'name': food['name'], 'price': float(food['price']), 'image': food['image']}
    save_cart(request, cart)
    next_url = request.GET.get('next', 'view_cart')
    return redirect(next_url)


def view_cart(request):
    cart = get_cart(request)
    items = []
    total = Decimal('0.00')
    for slug, data in cart.items():
        subtotal = Decimal(str(data['price'])) * data['qty']
        total += subtotal
        items.append({
            'slug': slug,
            'name': data['name'],
            'price': data['price'],
            'qty': data['qty'],
            'subtotal': float(subtotal),
            'image': data['image'],
        })
    return render(request, 'view-cart.html', {
        'items': items,
        'total': float(total),
        'cart_count': cart_count(request),
    })


def update_cart(request, slug):
    if request.method == 'POST':
        action = request.POST.get('action')
        cart = get_cart(request)
        if slug in cart:
            if action == 'inc':
                cart[slug]['qty'] += 1
            elif action == 'dec':
                cart[slug]['qty'] -= 1
                if cart[slug]['qty'] <= 0:
                    del cart[slug]
            elif action == 'remove':
                del cart[slug]
        save_cart(request, cart)
    return redirect('view_cart')


def checkout(request):
    cart = get_cart(request)
    if not cart:
        return redirect('view_cart')

    items = []
    total = Decimal('0.00')
    for slug, data in cart.items():
        subtotal = Decimal(str(data['price'])) * data['qty']
        total += subtotal
        items.append({
            'slug': slug,
            'name': data['name'],
            'price': data['price'],
            'qty': data['qty'],
            'subtotal': float(subtotal),
            'image': data['image'],
        })

    if request.method == 'POST':
        order = Order.objects.create(
            name=request.POST.get('name'),
            address=request.POST.get('address'),
            phone=request.POST.get('phone'),
            email=request.POST.get('email'),
            items=json.dumps(items),
            total=total,
        )
        request.session['cart'] = json.dumps({})
        return redirect('order_confirmation', order_id=order.id)

    return render(request, 'checkout.html', {
        'items': items,
        'total': float(total),
        'cart_count': cart_count(request),
    })


def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    items = json.loads(order.items)
    for item in items:
        item.setdefault('image', 'frio.png')
    return render(request, 'order-confirmation.html', {
        'order': order,
        'items': items,
        'cart_count': 0,
    })


def order_history(request):
    orders = Order.objects.all().order_by('-created_at')
    for order in orders:
        items = json.loads(order.items)
        for item in items:
            item.setdefault('image', 'frio.png')
        order.items_list = items
    return render(request, 'order-history.html', {
        'orders': orders,
        'cart_count': cart_count(request),
    })
