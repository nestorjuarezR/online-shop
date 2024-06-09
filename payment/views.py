from decimal import Decimal
import stripe
from django.conf import settngs
from django.shortcuts import render, redirect, reverse, get_object_or_404
from orders.models import Order


#Create the Stripe instance
stripe.api_key = settngs.STRIPE_SECRET_KEY
stripe.api_version = settngs.STRIPE_API_VERSION

def payment_process(request):
    order_id = request.session.get('order_id', None)
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        success_url = request.build_absolute_uri(
                                                                                        reverse('payment:completed')
                                                                                        )
        cancel_url = request.build_absolute_uri(
                                                                                        reverse('payment:canceled')
                                                                                        )
        
        #Stripe checkout session data
        session_data = {
                                        'mode': 'payment',
                                        'client_reference_id': order.id,
                                        'success_url' : success_url,
                                        'cancel_url': cancel_url,
                                        'line_items': []
                                    }   
        
        #Create Stripe checkout session
        session = stripe.checkout.Session.create(**session_data)
        #redirect to Stripe payment form
        return redirect(session.url, code=303)
    else:
        return render(request, 'payment/process.html', locals())


