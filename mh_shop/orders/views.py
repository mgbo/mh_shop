

from django.shortcuts import render, get_object_or_404
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from .models import Order

from django.conf import settings
from django.http import HttpResponse

from django.template.loader import get_template
from xhtml2pdf import pisa

from django.core.mail import EmailMessage


def order_create(request):
    cart = Cart(request)
    # order_d = get_object_or_404(Order, id=order_id)


    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        
        if form.is_valid():
            order = form.save(commit=False)

            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()

            for item in cart:
                OrderItem.objects.create(order=order,
                                        product=item['product'],
                                        price=item['price'],
                                        quantity=item['quantity'])
            # clear the cart
            cart.clear()
            # launch asynchronous task
            order_created.delay(order.id)

            # my sent email
            # subject = 'My Shop - Invoice no. {}'.format(order_d.id)
            # message = 'Please, find attached the invoice for your recent purchase.'
            # email = EmailMessage(subject,
            #                      message,
            #                      'mmmmipt307@gmail.com',
            #                      [order.email])

            return render(request,
                          'orders/order/created.html',
                          {'order': order})
    else:
        form = OrderCreateForm()
    return render(request,
                  'orders/order/create.html',
                  {'cart': cart, 'form': form})


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'admin/orders/order/detail.html', {'order':order})



@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    template_path = 'orders/order/pdf.html'
    context = {'order':order}

    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')

    # if you want to download:
    # response['Content-Disposition'] = 'attachment; filename="report.pdf"'

    # if you want to display:
    response['Content-Disposition'] = 'filename="order_{}.pdf"'.format(order.id)

    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response













