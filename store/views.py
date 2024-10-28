from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.generic import ListView, DetailView
from .models import Product, Category, SliderImage, CartItem
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Order
from .models import *
from .admin import *
from .urls import *
from django.shortcuts import render
from .models import Category, Product
def home(request):
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    return render(request, 'store/index.html', {
        'categories': categories,
        'products': products,
    })

class ProductListView(ListView):
    model = Product
    template_name = 'store/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            return Product.objects.filter(
                category__slug=category_slug,
                available=True
            )
        return Product.objects.filter(available=True)
class ProductDetailView(DetailView):
    model = Product
    template_name = 'store/product_detail.html'
def index(request):
    slider_images = SliderImage.objects.all()
    categories = Category.objects.all()
    products = Product.objects.all()
    print(f"Categories: {categories}")
    print(f"Products: {products}")
    context = {
        'slider_images': slider_images,
        'products': products,
        'categories': categories,
    }
    return render(request, 'store/index.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'store/product_detail.html', {'product': product})


def cart(request):
    return render(request, 'store/cart.html')


def cart(request):
    session_id = request.session.session_key
    if not session_id:
        request.session.create()
        session_id = request.session.session_key

    cart_items = CartItem.objects.filter(session_id=session_id)
    total = sum(item.total_price() for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'store/cart.html', context)


def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        size = request.POST.get('size')

        session_id = request.session.session_key
        if not session_id:
            request.session.create()
            session_id = request.session.session_key

        product = get_object_or_404(Product, id=product_id)

        # Проверяем, есть ли уже такой товар в корзине
        cart_item, created = CartItem.objects.get_or_create(
            session_id=session_id,
            product=product,
            size=size,
            defaults={'quantity': quantity}
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'})


def update_cart(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        quantity = int(request.POST.get('quantity'))

        cart_item = get_object_or_404(CartItem, id=item_id)
        cart_item.quantity = quantity
        cart_item.save()

        return JsonResponse({
            'status': 'success',
            'total': cart_item.total_price()
        })

    return JsonResponse({'status': 'error'})


def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    return redirect('cart')

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'store/order_list.html', {'orders': orders})

