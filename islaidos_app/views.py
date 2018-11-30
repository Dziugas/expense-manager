from django.shortcuts import render, redirect
from .models import Islaidos
from .forms import IslaidosForm

def sarasas(request):
    islaidos = Islaidos.objects.all()
    return render(request, 'islaidos.html', {'islaidos': islaidos})

def sukurti(request):
    form = IslaidosForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('sarasas')

    return render(request, 'islaidos-form.html', {'form': form})

def pakeisti(request, id):
    islaidos = Islaidos.objects.get(id=id)
    form = IslaidosForm(request.POST or None, instance=islaidos)

    if form.is_valid():
         form.save()
         return redirect('sarasas')

    return render(request, 'islaidos-form.html', {'form':form, 'islaidos': islaidos})

def istrinti(request, id):
    islaidos = Islaidos.objects.get(id=id)

    if request.method == 'POST':
        islaidos.delete()
        return redirect('sarasas')

    return render(request, 'islaidu-istrynimo-patvirtinimas.html', {'islaidos': islaidos})

