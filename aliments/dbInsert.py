from aliments import dbRequests
from aliments.models import Category
from aliments.models import Store
from aliments.models import Products
from aliments.models import Foodsave


# insert list category into database
def insertCategory():
    category_list = {}
    cat_list = []
    request = dbRequests.DbRequests()

    category_list = request.Request_categories()

    for i in category_list[:100]:
        idcat = i['id']
        name = i['nameCategory']
        cat = Category(nameCategory=name, idCategory=idcat)

        cat_list.append(cat)

    # Call bulk_create to create records in a single call
    Category.objects.bulk_create(cat_list)


# insert list store into database
def insertStore():
    store_list = {}
    sto_list = []

    request = dbRequests.DbRequests()

    store_list = request.Request_stores()

    for i in store_list[:100]:
        idSto = i['id']
        name = i['nameStore']
        store = Store(nameStore=name, idStore=idSto)

        sto_list.append(store)

    # Call bulk_create to create records in a single call
    Store.objects.bulk_create(sto_list)


# Insert list of products into database
def insertProducts():
    list_prod_obj = []

    request = dbRequests.DbRequests()

    product_list = request.Request_products()

    for i in product_list[:100]:
        nameAlim = i["nameAlim"]
        image = i["image"]
        url = i["url"]
        descriptionAlim = i["descriptionAlim"]
        nutritionGrade = i["nutritionGrade"]
        idCategory = i["idCategory"]
        idStore = i["idStore"]
        # get id category for this product
        idCat = getidCategory(idCategory)
        # get id store for this product
        idSto = getidStore(idStore)

        if (idCat is not None) and (idSto is not None):
            product = Products(nameAlim=nameAlim, image=image, url=url,
                               descriptionAlim=descriptionAlim,
                               nutritionGrade=nutritionGrade, idCategory=idCat,
                               idStore=idSto)

            list_prod_obj.append(product)

    # Call bulk_create to create records in a single call
    Products.objects.bulk_create(list_prod_obj)


# get primary key for category
def getidCategory(category):
    ob_Category = Category.objects.filter(nameCategory=category)
    if ob_Category.first():
        obj_cat = Category(id=ob_Category.first().id,
                           idCategory=ob_Category.first().idCategory,
                           nameCategory=ob_Category.first().nameCategory)
    else:
        obj_cat = None

    return(obj_cat)


# get primary key for store
def getidStore(store):
    ob_Store = Store.objects.filter(nameStore=store)
    if ob_Store.first():
        obj_store = Store(id=ob_Store.first().id,
                          idStore=ob_Store.first().idStore,
                          nameStore=ob_Store.first().nameStore)
    else:
        obj_store = None

    return(obj_store)


# insert save product into database
def insertFoodsave(idAlim, idUser):
    list_food = []

    if (idAlim != "") and (idUser != ""):
        obj_foodsave = Foodsave(idAliment=idAlim, idUser=idUser)

        list_food.append(obj_foodsave)
        # Call bulk_create to create records in a single call
        Foodsave.objects.bulk_create(list_food)
        # obj_foodsave.save()
    return(list_food)


# get products from table products
def get_Results(product):
    ob_Product = Products.objects.filter(nameAlim=product)

    if ob_Product.first():
        obj_prods_by_cat = get_products_by_cat(ob_Product.first().idCategory)
    else:
        obj_prods_by_cat = list()
    
    return(obj_prods_by_cat)


# get products from the same category
def get_products_by_cat(category):
    ob_cat_prod = Products.objects.filter(idCategory=category)[:6]
    json_res = []

    for obj in ob_cat_prod:
        product = Products(id=obj.id,
                           nameAlim=obj.nameAlim,
                           image=obj.image,
                           url=obj.url,
                           descriptionAlim=obj.descriptionAlim,
                           nutritionGrade=obj.nutritionGrade,
                           idCategory=obj.idCategory,
                           idStore=obj.idStore
                           )
        json_res.append(product)

    return(json_res)


# get saved products
def get_saved_products(idUser):
    result_res = []
    aliment_save = Foodsave.objects.filter(idUser=idUser)

    for result in aliment_save.values():
        context = {}

        obj_aliment = Products.objects.filter(pk=result['idAliment_id'])

        if obj_aliment.first() != "":
            context['nameAlim'] = obj_aliment.first().nameAlim
            context['image'] = obj_aliment.first().image
            context['nutritionGrade'] = obj_aliment.first().nutritionGrade

            result_res.append(context)
        else:
            result_res = list()

    return(result_res)