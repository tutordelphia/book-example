from django.shortcuts import render, redirect
from lists.models import Item

# Create your views here.
def home_page(request):
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/lists/only-list/')

    return render(request, 'home.html')

def view_list(request):
    view_data = {
        'items': Item.objects.all()
    }
    return render(request, 'list.html', view_data)