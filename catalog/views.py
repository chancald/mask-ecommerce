from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from django.views.generic import ListView, DetailView, View
from .models import Item, Order, OrderItem, Address, Promo
from .forms import AddressForm, PromoForm
from django.http import HttpResponseRedirect
from django.core.mail import send_mail


class HomeView(ListView):
    model = Item
    template_name = 'home.html'

class ProductDetail(DetailView):
    model = Item
    template_name = 'product.html'

class OrderSummaryView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        context = {
            'order': order
        }
        return render(self.request, 'order_summary.html', context)

def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(item=item, user=request.user, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            messages.success(request, f"{item.title} ya esta en el carrito")
            return redirect('product', slug=slug)
        else:
            order.items.add(order_item)
            order.save()
            messages.success(request, f"{item.title} fue anadido al carrito")
            return redirect('product', slug=slug)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered=False, ordered_date=ordered_date)
        order.items.add(order_item)
        order.save()
        messages.success(request, f"{item.title} fue anadido al carrito")
        return redirect('product', slug=slug)

def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(item=item, user=request.user, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            OrderItem.objects.filter(id=order_item.id).delete()
            messages.warning(request, f"{item.title} fue eliminado del carrito")
            return redirect('product', slug=slug)
        else:
            messages.warning(request, f"{item.title} no esta en el carrito")
            return redirect('product', slug=slug)
    else:
        messages.warning(request, f"{item.title} no hay una orden activa")
        return redirect('product', slug=slug)

def add_item_quantity(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(item=item, user=request.user, ordered=False)
    order_item.quantity += 1
    order_item.save()
    return redirect('order_summary')

def remove_item_quantity(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(item=item, user=request.user, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order = order_qs[0]
    if order_item.quantity > 1:
        order_item.quantity -= 1
        order_item.save()
    else:
        order.items.remove(order_item)
        order.save()
        messages.warning(request, f"{item.title} fue eliminado del carrito")

    return redirect('order_summary')

def remove_from_cart_summary(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(item=item, user=request.user, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order = order_qs[0]
    OrderItem.objects.filter(id=order_item.id).delete()
    messages.warning(request, f"{item.title} el producto fue eliminado del carrito")
    return redirect('order_summary')

class AfterCheckoutView(DetailView):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        context = {
            'order': order
        }
        return render(self.request, 'after_checkout.html', context)

class CheckoutView(View):
    def get(self, *args, **kwargs):
        form = AddressForm()
        order = Order.objects.get(user=self.request.user, ordered=False)
        context = {
            'form': form,
            'order': order,
        }
        return render(self.request, 'checkout.html', context)
    
    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        form = AddressForm(self.request.POST or None)
        context = {}
        #promo_form = PromoForm(self.request.POST or None)
        
        if 'submit_promo' in self.request.POST:
            if form.is_valid():
                promo_code = form.cleaned_data.get('promo_code')
                promo = Promo.objects.filter(title=promo_code)
                if promo:
                    order.promo.clear()
                    order.promo.add(promo[0])
                    order.save()
                else:
                    order.promo.clear()
                    order.save()
                    messages.warning(self.request, f"{promo_code} no es un codigo valido de promoción")
        
        if 'submit_info' in self.request.POST:
            if form.is_valid():
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                phone = form.cleaned_data.get('phone')
                email = form.cleaned_data.get('email')            
                street_address = form.cleaned_data.get('street_address')
                street_address_2 = form.cleaned_data.get('street_address_2')
                save_info = form.cleaned_data.get('save_info')
                default = form.cleaned_data.get('default')
                use_default = form.cleaned_data.get('use_default')
                state_option = form.cleaned_data.get('state_option')
                payment_option = form.cleaned_data.get('payment_option')
                # Create address and save it
                address = Address(
                    user=self.request.user,
                    street_address=street_address,
                    street_address_2=street_address_2,
                    state_option=state_option,
                )
                address.save()

                # Print form data
                print(form.cleaned_data)
                
                # Send emails
                subject = 'Mascarillas y mas - Su orden fue recibida'
                message = f'¡Gracias por ordenar!\n{first_name} {last_name} Su orden fue recibida. Lo antes posible alguien lo estara contactando para confirmar su orden.'
                    
                                             
                from_email = 'chandler240@gmail.com'
                recipient_list = [email,]
                send_mail(subject, message, from_email, recipient_list)

                return redirect('after_checkout')
            else:
                # Check errors
                # print(form.errors)
                messages.warning(self.request, "Los campos Nombre, Apellido, Telefono y Email son necesarios")
        # always return an address        
        return redirect('checkout')
    