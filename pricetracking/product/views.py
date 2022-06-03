from django.shortcuts import redirect, render
from django.views.generic import DeleteView
from django.urls import reverse_lazy
from .forms import AddForm
from .models import Link




def home_view(request):
    error = None
    no_discounted = 0
    no_rised = 0
    form = AddForm(request.POST or None)

    if request.method == 'POST':
        try:
            if form.is_valid():
                form.save()
        except AttributeError:
            error = "Impossible to get the name or the price - the good might have been sold out"
        except:
            error = "Something went completely wrong :("

    form = AddForm()

    qs = Link.objects.all()
    items_no = qs.count()


    if items_no > 0:
        discount_list = []
        rised_list = []
        for item in qs:
            if item.old_price > item.current_price:
                discount_list.append(item)
            no_discounted = len(discount_list)

            if item.old_price != 0:
                if item.old_price < item.current_price:
                    rised_list.append(item)
                no_rised = len(rised_list)


    context = {
        'qs': qs,
        'items_no': items_no,
        'no_discounted': no_discounted,
        'no_rised': no_rised,
        'form': form,
        'error': error,
    }
    return render(request, 'product/main.html', context)

class LinkDeleteView(DeleteView):
    model = Link
    template_name = 'product/confirm_del.html'
    success_url = reverse_lazy('home')

def update_prices(request):
    qs = Link.objects.all()
    for link in qs:
        link.save()
    return redirect('home')


#TO_DOTO_DOTO_DOTO_DOTO_DOTO_DOTO_DOTO_DOTO_DOTO_DOTO_DOTO_DOTO_DOTO_DOTO_DOTO_DOTO_DOTO_DO
def monitor_price(request):
    Link.monitored = True

def stop_monitoring(request):
    Link.monitored = True