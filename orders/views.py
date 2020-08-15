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

    if size == "Small":
        price = pza.min_price + (0.5 * len(sel))
    if size == "Large":
        price = pza.max_price + (0.5 * len(sel))
        
    t = "Toppings"
    if title == "Subs":
        t = "Extras"
    if tpl == []:
        tpl = f'No {t} selected'

    piz = f"[{title}] ({pza.name}) | Price: ${price} | {t}: {tpl} | Size: {size}"

    mycart = Cart.objects.filter(name=request.user.username)
    for p in mycart:
        if piz == p.details:
            messages.warning(request, "Item already in your cart.")
            return HttpResponseRedirect(reverse("orders:menu"))
    Cart.objects.create(name=request.user.username, details=piz, price=price)
    messages.success(request, f"{piz} added to cart!")

    return HttpResponseRedirect(reverse("orders:menu"))
    

@login_required(login_url="user:login")
def cart_items(request):
    try:
        cartitems = Cart.objects.filter(name=request.user.username)
        tp = 0
        for item in cartitems:
            tp += item.price
        
        context =  {
            "pizzacart": cartitems, 
            "totalprice": tp, 
            "pcl": Cart.objects.filter(name=request.user.username).count(),
            }

        return render(request, "orders/cart.html", context)
    except:
        return render(request, "orders/cart.html", {"pizzacart": [], "totalprice": 0})


@login_required(login_url="user:login")
def remove(request, pizza_id):
    try:
        Cart.objects.get(id=pizza_id).delete()
        messages.success(request, "Item removed from your cart.")
    except:
        pass
    return HttpResponseRedirect(reverse("orders:cart_items"))


@login_required(login_url="user:login")
def removeall(request):
    try:
        Cart.objects.filter(name=request.user.username).delete()
        messages.success(request, "All items removed.")
    except:
        pass
    return HttpResponseRedirect(reverse("orders:cart_items"))


@login_required(login_url="user:login")
def order(request, pizza_id):
    if request.method == "POST":
        try:
            request.POST["t&c"]
            pz = Cart.objects.get(id=pizza_id)
            pizzacount = int(request.POST["pizzacount"])
            total = pz.price * pizzacount
            if not OrderList.objects.filter(pizzaname=pz.details):
                OrderList.objects.create(name=request.user.username, pizzaname=pz.details, count=pizzacount, total=total)
            else:
                mypiz = OrderList.objects.get(name=request.user.username, pizzaname=pz.details)
                OrderList.objects.filter(name=request.user.username, pizzaname=pz.details).update(name=request.user.username, pizzaname=pz.details, count=mypiz.count + pizzacount, total=mypiz.total + total)
            messages.success(request, "Order placed successfully!")
            return HttpResponseRedirect(reverse("orders:cart_items"))
        except:
            messages.warning(request, "Please accept the Terms & Conditions.")
            return HttpResponseRedirect(reverse("orders:cart_items"))
    else:
        return HttpResponseRedirect(reverse("orders:cart_items"))


@login_required(login_url="user:login")
def orderall(request):
    if request.method == "POST":
        try:
            request.POST["T&C"]
            mycart = Cart.objects.filter(name=request.user.username)
            for pizza in mycart:
                total = pizza.price
                if OrderList.objects.filter(name=request.user.username, pizzaname=pizza.details):
                    mypiz = OrderList.objects.get(name=request.user.username, pizzaname=pizza.details)
                    OrderList.objects.filter(name=request.user.username, pizzaname=pizza.details).update(name=request.user.username, pizzaname=pizza.details, count=mypiz.count + 1, total=mypiz.total + total)

                if not OrderList.objects.filter(name=request.user.username, pizzaname=pizza.details):
                    OrderList.objects.create(name=request.user.username, pizzaname=pizza.details,count=1, total=total)
            messages.success(request, "Order placed successfully!")
            return HttpResponseRedirect(reverse("orders:cart_items"))
        except:
            messages.warning(request, "Please accept the Terms & Conditions.")
            return HttpResponseRedirect(reverse("orders:cart_items"))
    else:
        if OrderList.objects.all() != None:
            orders = OrderList.objects.filter(name=request.user.username)
            tp = 0
            for ordr in orders:
                tp += ordr.total
            context = {
                    "orders": orders,
                    "status": "Pending",
                    "tp": tp
                }
            return render(request, "orders/orders.html", context)
        else:
            messages.info(request, "No orders placed.Place your orders here.")
            return HttpResponseRedirect(reverse("orders:menu"))
            


@login_required(login_url="user:login")
def cancelorder(request, order_id):
    try:
        OrderList.objects.get(id=order_id).delete()
        messages.success(request, "Order cancelled successfully!")
        return HttpResponseRedirect(reverse("orders:orderall"))
    except:
        pass
