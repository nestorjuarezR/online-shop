from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreatedForm
from cart.cart import Cart

def order_created(request):
    cart = Cart(request)

    if request.method == 'POST':
        form = OrderCreatedForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                                                    product = item['product'],
                                                                    price = item['price'],
                                                                    quantity = item['quantity'])
            cart.clear()
        return render(request, 'orders/created.html',
                                {'order': order})
    
    else:
        form = OrderCreatedForm()
        
    return render(request,
                                'orders/create.html',
                                {'cart': cart,
                                 'form': form})