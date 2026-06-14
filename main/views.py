import json
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core.paginator import Paginator
from .models import Order, Food


def get_cart(request):
    return json.loads(request.session.get('cart', '{}'))


def save_cart(request, cart):
    request.session['cart'] = json.dumps(cart)


def cart_count(request):
    cart = get_cart(request)
    return sum(item['qty'] for item in cart.values())


def index(request):
    top_foods = Food.objects.all().order_by('-rating')[:6]
    return render(request, 'index.html', {
        'cart_count': cart_count(request),
        'top_foods': top_foods,
    })


def account(request):
    return render(request, 'account.html', {'cart_count': cart_count(request)})


def browse(request):
    foods = Food.objects.all()
    categories = Food.objects.values_list('category', flat=True).distinct().order_by('category')

    category = request.GET.get('category')

    if category:
        foods = foods.filter(category__iexact=category)

    paginator = Paginator(foods, 12)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    food_list = [{
        'slug': f.slug,
        'name': f.name,
        'image_url': f.image.url if f.image else '',
        'time': f.time,
        'rating': f.rating,
        'star_rating': f.star_rating(),
        'price': float(f.price),
        'category': f.category,
        'description': f.description[:50] + '...' if len(f.description) > 50 else f.description,
    } for f in foods]

    query_params = request.GET.copy()
    query_params.pop('page', None)
    query_string = query_params.urlencode()

    current_path = request.get_full_path()

    ctx = {
        'cart_count': cart_count(request),
        'foods': page_obj,
        'page_obj': page_obj,
        'food_data_json': json.dumps(food_list),
        'filter_category': category or '',
        'categories': categories,
        'query_string': query_string,
        'current_path': current_path,
    }

    return render(request, 'browse.html', ctx)


def login(request):
    return render(request, 'login.html')


def register(request):
    return render(request, 'register.html')


def food_detail(request, slug):
    food = get_object_or_404(Food, slug=slug)
    next_url = request.GET.get('next', '')
    return render(request, 'food-detail.html', {
        'food': food, 'slug': slug,
        'cart_count': cart_count(request),
        'next_url': next_url,
    })


def add_to_cart(request, slug):
    food = get_object_or_404(Food, slug=slug)
    cart = get_cart(request)
    if slug in cart:
        cart[slug]['qty'] += 1
    else:
        cart[slug] = {'qty': 1, 'name': food.name, 'price': float(food.price), 'image': food.image.url if food.image else ''}
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
        img = data.get('image', '')
        if img and not img.startswith('/media/') and not img.startswith('http'):
            img = ''
        items.append({
            'slug': slug,
            'name': data['name'],
            'price': data['price'],
            'qty': data['qty'],
            'subtotal': float(subtotal),
            'image': img,
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
        img = item.get('image', '')
        if img and not img.startswith('/media/') and not img.startswith('http'):
            item['image'] = ''

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
            img = item.get('image', '')
            if img and not img.startswith('/media/') and not img.startswith('http'):
                item['image'] = ''

        order.items_list = items
    return render(request, 'order-history.html', {
        'orders': orders,
        'cart_count': cart_count(request),
    })
