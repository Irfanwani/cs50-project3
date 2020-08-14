from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate
from django.urls import reverse
from .models import *
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    messages.info(request, "WELCOME! pizza for pizza lovers.")
    return render(request, "orders/index.html")


@login_required(login_url="user:login")
def menu(request):
    context = {
        "regularpizza": RegularPizza.objects.all(),
        "toppings": Toppings.objects.all(),
        "sicilianpizza": SicilianPizza.objects.all(),
        "subs": Subs.objects.all(),
        "subsextras": SubsExtras.objects.all(),
        "pasta": Pasta.objects.all(),
        "salads": Salads.objects.all(),
        "dinnerplatters": DinnerPlatters.objects.all(),
    }

    return render(request, "orders/menu.html", context)


@login_required(login_url="user:login")
def cart(request):
    pza = ''
    tp = ''
    tpl = []
    size = request.POST["size"]

    title1 = ''
    try:
        title1 = request.POST["pizzatype"]
        if title1 == "Regular Pizza":
            title = "Regular Pizza"
            pizza = RegularPizza
            t = "topping"
        else:
            title = "Sicilian Pizza"
            pizza = SicilianPizza
            t = "item"
    except:
        pass

    subs = ''
    try:
        subs = request.POST["subs"]
        title = "Subs"
        pza = Subs.objects.get(name=subs)
    except:
        pass
    subsextras = SubsExtras.objects.all()
    sel = []
    for subextra in subsextras:
        try:
            se = request.POST[f"{subextra.name}"]
            sel.append(se)
            tpl.append(se)
        except:
            pass

    toppings = Toppings.objects.all()
    for topping in toppings:
        try:
            tp = request.POST[f"{topping.name}"]
            if tp not in tpl:
                tpl.append(tp)
        except KeyError:
            pass

    pasta = ''
    try:
        pasta = request.POST["pasta"]
        title = "Pasta"
        pza = Pasta.objects.get(name=pasta)
    except:
        pass

    salads = ''
    try:
        salads = request.POST["salads"]
        title = "Salads"
        pza = Salads.objects.get(name=salads)
    except:
        pass

    dinnerplatters = ''
    try:
        dinnerplatters = request.POST["dinnerplatters"]
        title = "DinnerPlatters"
        pza = DinnerPlatters.objects.get(name=dinnerplatters)
    except:
        pass

    try:
        if len(tpl) == 0:
            pza = pizza.objects.get(name="Cheese")
        if len(tpl) == 1:
            pza = pizza.objects.get(name=f"1 {t}")
        if len(tpl) == 2:
            pza = pizza.objects.get(name=f"2 {t}s")
        if len(tpl) == 3:
            pza = pizza.objects.get(name=f"3 {t}s")
        if len(tpl) >= 4:
            pza = pizza.objects.get(name="Special")
    except:
        pass

    if "cart" not in request.session:
        request.session["cart"] = []
    if size == "Small":
        price = pza.min_price + (0.5 * len(sel))
    if size == "Large":
        price = pza.max_price + (0.5 * len(sel))
    
    if "totalprice" not in request.session:
        request.session["totalprice"] = []
        
    request.session["totalprice"].append(price)
    
    piz = [f"[{title}]<{pza.name}>Price: $<{price}><{tpl}><{size}>", ]

    if f"[{title}]<{pza.name}>Price: $<{price}><{tpl}><{size}>" in request.session["cart"]:
        messages.warning(request, "Item already in your cart.")
        return HttpResponseRedirect(reverse("orders:menu"))
    request.session["cart"] += piz
    messages.success(request, f"{piz} added to cart!")

    return HttpResponseRedirect(reverse("orders:menu"))
    

@login_required(login_url="user:login")
def cart_items(request):
    if "cart" in request.session and "totalprice" in request.session:
        tp = 0
        for i in range(len(request.session["totalprice"])):
            tp += float(request.session["totalprice"][i])

        return render(request, "orders/cart.html", {"pizzacart": request.session["cart"], "totalprice": tp, "pcl": len(request.session["cart"])})
    else:
        return render(request, "orders/cart.html", {"pizzacart": [], "totalprice": 0})


@login_required(login_url="user:login")
def remove(request, pizza_id):
    try:
        (request.session["totalprice"]).pop((request.session["cart"]).index(pizza_id))
        request.session.modified = True
        (request.session["cart"]).remove(pizza_id)
        request.session.modified = True
        messages.success(request, "Item removed from your cart.")
    except:
        pass
    return HttpResponseRedirect(reverse("orders:cart_items"))


@login_required(login_url="user:login")
def removeall(request):
    try:
        del request.session["cart"]
        del request.session["totalprice"]
        messages.success(request, "All items removed.")
    except:
        pass
    return HttpResponseRedirect(reverse("orders:cart_items"))