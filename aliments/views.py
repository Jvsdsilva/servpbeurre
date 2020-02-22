from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .forms import RegistrationForm
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from aliments.models import Products
from aliments.models import Foodsave
from aliments import dbInsert
from aliments import dbRequests
from django.contrib.auth.models import User
from django.db import transaction
from aliments.models import Category
from aliments.models import Store
from aliments.models import Products
import logging
from django.urls import reverse


# Get an instance of a logger
logger = logging.getLogger(__name__)


# go to home
def index(request):
    logger.info('index', exc_info=True, extra={
        # Optionally pass a request and we'll grab any information we can
        'request': request,
    })

    try:
        cat = Category.objects.all()

        if cat.exists():
            logger.info("Table category not empty")
        else:
            dbInsert.insertCategory()

            store = Store.objects.all()
            if store.exists():
                logger.info("Table store not empty")
            else:
                dbInsert.insertStore()

                products = Products.objects.all()
                if products.exists():
                    logger.info("Table products not empty")
                else:
                    dbInsert.insertProducts()
        logger.info("Data insert into db")
    except Exception:
        logging.exception(
            "We get some problems with data insert into db")

    template = loader.get_template('aliments/index.html')
    return HttpResponse(template.render(request=request))


# loged in
def login(request):
    logger.info('login', exc_info=True, extra={
        # Optionally pass a request and we'll grab any information we can
        'request': request,
    })
    template = loader.get_template('aliments/login.html')
    return HttpResponse(template.render(request=request))


# redirect to user connected page
def connected(request):
    logger.info('connected', exc_info=True, extra={
        # Optionally pass a request and we'll grab any information we can
        'request': request,
    })
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

    logger.info('results', exc_info=True, extra={
        # Optionally pass a request and we'll grab any information we can
        'request': request,
    })

    result_res = []
    query_index = ""
    query = ""
    query_nav = ""
    search = ""

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
            try:
                results = dbInsert.get_Results(query)
                logger.info('get results', exc_info=True, extra={
                    # Optionally pass a request and we'll grab any information
                    # we can
                    'request': results,
                })
            except Exception:
                logging.exception(
                    "We get some problems with request results: ")

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
    logger.info('results_details', exc_info=True, extra={
        # Optionally pass a request and we'll grab any information we can
        'request': request,
    })

    try:
        obj_aliment = Products.objects.get(pk=pk)
        logger.info('get results details', exc_info=True, extra={
            # Optionally pass a request and we'll grab any information we can
            'request': obj_aliment,
        })
    except Exception:
        logging.exception(
            "We get some problems with request results details: ")

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
    logger.info('foodsave', exc_info=True, extra={
        # Optionally pass a request and we'll grab any information we can
        'request': request,
    })

    foodsave = request.POST.get('foodsavebtn', None)

    if foodsave == 'foodsavebtn':
        pk = request.POST['id']
        current_user = request.user

        try:
            obj_aliment = Products.objects.get(pk=pk)
            logger.info('get results details', exc_info=True, extra={
                # Optionally pass a request and we'll grab any information
                # we can
                'request': obj_aliment,
            })
        except Exception:
            logging.exception(
                "We get some problems with request foodsave")

        obj_user = User(id=current_user.id)

        try:
            dbInsert.insertFoodsave(obj_aliment, obj_user)
            logger.info('insert foodsave')
        except Exception:
            logging.exception(
                "We get some problems with insert foodsave")

    current_user_id = request.user

    try:
        saved_products = dbInsert.get_saved_products(current_user_id.id)
        logger.info('get foodsave', exc_info=True, extra={
            # Optionally pass a request and we'll grab any information we can
            'request': saved_products,
        })
    except Exception:
        logging.exception(
            "We get some problems with get foodsave")

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
