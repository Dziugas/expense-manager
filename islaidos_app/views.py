from django.shortcuts import render, redirect
from .models import Islaidos, IslaiduTipai
from .forms import IslaidosForm, TiekejaiForm
from django.db.models import Sum



def data_for_the_google_chart():
    visi_islaidu_tipai = IslaiduTipai.objects.all()
    islaidu_tipu_pavadinimai = [islaidu_tipas.tipas for islaidu_tipas in visi_islaidu_tipai]
    print(islaidu_tipu_pavadinimai)
    for islaidu_tipo_pavadinimas in islaidu_tipu_pavadinimai:
        islaidos_tipui = Islaidos.objects.filter(tipas__tipas=islaidu_tipo_pavadinimas)
        islaidu_tipui_suma = islaidos_tipui.aggregate(Sum('suma'))
        print(islaidos_tipui, islaidu_tipui_suma)

#BENDRAS PRADINIS
def sarasas(request):
    data_for_the_google_chart()
    islaidos = Islaidos.objects.all().order_by('-data')
    islaidu_tipai = IslaiduTipai.objects.all().order_by('-aktyvus', 'tipas')
    islaidu_suma = list(Islaidos.objects.aggregate(Sum('suma')).values())[0]

    return render(request, 'sarasas.html', {'islaidos': islaidos, 'islaidu_tipai':islaidu_tipai, 'islaidu_suma':islaidu_suma})


#IŠLAIDOS

def sukurti_is(request):
    form = IslaidosForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('sarasas')

    return render(request, 'islaidos-form.html', {'form': form})

def pakeisti_is(request, id):
    islaidu_irasas = Islaidos.objects.get(id=id)
    form = IslaidosForm(request.POST or None, instance=islaidu_irasas)

    if form.is_valid():
         form.save()
         return redirect('sarasas')

    return render(request, 'islaidos-form.html', {'form':form, 'islaidu_irasas': islaidu_irasas})

def istrinti_is(request, id):
    islaidu_irasas = Islaidos.objects.get(id=id)

    if request.method == 'POST':
        islaidu_irasas.delete()
        return redirect('sarasas')

    return render(request, 'islaidu-istrynimo-patvirtinimas.html', {'islaidu_irasas': islaidu_irasas})


# IŠLAIDŲ TIPAI

def sukurti_tipa(request):
    form = TiekejaiForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('sarasas')

    return render(request, 'tipas-form.html', {'form': form})

def pakeisti_tipa(request, id):
    islaidu_tipas = IslaiduTipai.objects.get(id=id)
    form = TiekejaiForm(request.POST or None, instance=islaidu_tipas)

    if form.is_valid():
        form.save()
        return redirect('sarasas')

    return render(request, 'tipas-form.html', {'form': form, 'islaidu_tipas': islaidu_tipas})

def istrinti_tipa(request, id):
    islaidu_tipas = IslaiduTipai.objects.get(id=id)

    if request.method == 'POST':
        islaidu_tipas.delete()
        return redirect('sarasas')

    return render(request, 'tipo-istrynimo-patvirtinimas.html', {'islaidu_tipas': islaidu_tipas})







