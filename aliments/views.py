from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .forms import RegistrationForm
from django import forms
from django.http import HttpResponse
from django.template import loader
from .models import Products
from .models import Foodsave
from aliments import dbInsert
from aliments import dbRequests
from django.contrib.auth.models import User
from django.db import transaction
from .models import Category
from .models import Store
from .models import Products


# go to home
def index(request):

    cat = Category.objects.all()
    if cat.exists():
        print("exist")
    else:
        dbInsert.insertCategory()

        store = Store.objects.all()
        if store.exists():
            print("exist")
        else:
            dbInsert.insertStore()
            products = Products.objects.all()
            if products.exists():
                print("exist")
            else:
                dbInsert.insertProducts()
    template = loader.get_template('aliments/index.html')
    return HttpResponse(template.render(request=request))


# loged in
def login(request):
    template = loader.get_template('aliments/user.html')
    return HttpResponse(template.render(request=request))


# redirect to user connected page
def connected(request):
    template = loader.get_template('aliments/aliments.html')
    return HttpResponse(template.render(request=request))


# logout user
def logout(request):
    template = loader.get_template('aliments/index.html')
    return HttpResponse(template.render(request=request))


# Create new user
def signup(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('login')
    else:
        form = RegistrationForm()

    return render(request, 'aliments/signup.html', {'form': form})


# request results
def results(request):
    result_res = []
    query_index = ""
    query = ""
    query_nav = ""

    if request.method == "POST":
        search = request.POST.get('searchbtn')
        if search is None:
            query_nav = request.POST['query_nav']

            if query_nav != "":
                query_nav = query_nav
            else:
                query_nav = ""
    
    if search == 'searchbtn' or query_nav != "":
        if search == 'searchbtn':
            query_index = request.POST['query_index']

        if query_index != "" or query_nav != "":
            if query_index != "":
                query = query_index

            if query_nav != "":
                query = query_nav

            results = dbInsert.get_Results(query)
        else:
            text = "Veiullez saisir un produit"
            return render(request, 'aliments/index.html', {'text': text})

        if len(results) == 0:
            text = "Nous n'avons pas ce produit, veiullez reessayer!"
            return render(request, 'aliments/results.html', {'text': text})
        else:
            for result in results:
                contexts = {}
                contexts['id'] = result.id
                contexts['nameAlim'] = result.nameAlim
                contexts['image'] = result.image
                contexts['nutritionGrade'] = result.nutritionGrade

                result_res.append(contexts)

            return render(request, 'aliments/results.html',
                         {'results': result_res})


# redirect to page details for a specific product
def results_details(request, pk):
    obj_aliment = Products.objects.get(pk=pk)

    context = {
        'id': obj_aliment.id,
        'image': obj_aliment.image,
        'nameAlim': obj_aliment.nameAlim,
        "descriptionAlim": obj_aliment.descriptionAlim,
        "nutritionGrade": obj_aliment.nutritionGrade
    }

    return render(request, 'aliments/results_details.html', context)


# page of products
def aliment(request):

    foodsave = request.POST.get('foodsavebtn', None)

    if foodsave == 'foodsavebtn':
        pk = request.POST['id']
        current_user = request.user

        obj_aliment = Products.objects.get(pk=pk)

        obj_user = User(id=current_user.id)

        dbInsert.insertFoodsave(obj_aliment, obj_user)
    current_user_id = request.user
    saved_products = dbInsert.get_saved_products(current_user_id.id)

    if len(saved_products) == 0:
        text = "Vous n'avez pas de produits enregistrées!"
        return render(request, 'aliments/aliments.html', {'text': text})
    else:
        args = {'foodsave': saved_products}

        return render(request, 'aliments/aliments.html', args)


# page of condictions
def mentions(request):
    template = loader.get_template('aliments/mentions.html')
    return HttpResponse(template.render(request=request))


# page contact
def contact(request):
    template = loader.get_template('aliments/based.html')
    return HttpResponse(template.render(request=request))
