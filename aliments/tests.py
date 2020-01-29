from django.test import TestCase, Client
from aliments.models import Category
from aliments.models import Store
from aliments.models import Products
from aliments.models import Foodsave
from django.urls import reverse
from django.contrib.auth.models import User
from .forms import RegistrationForm
from django.views.generic import TemplateView


# creations test
class CategoryTest(TestCase):

    def create_Category(self, nameCategory='Cat1', idCategory='idCat1'):
        return Category.objects.create(nameCategory=nameCategory,
                                       idCategory=idCategory)

    def create_Store(self, nameStore='Sto1', idStore='idSto1'):
        return Store.objects.create(nameStore=nameStore, idStore=idStore)

    def create_Products(self, idprod):
        c = self.create_Category()
        s = self.create_Store()
        self.assertTrue(isinstance(c, Category))
        self.assertTrue(isinstance(s, Store))

        nameAlim = "Gazpacho"
        image = "https://static.openfoodfacts.org/images/products/541/018/" \
                "803/1072/front_fr.30.200.jpg"
        url = "https://world.openfoodfacts.org/product/5410188031072/"\
              "gazpacho-alvalle"
        descriptionAlim = "Tomate, poivron, concombre, oignon, huile d'olive"\
                          "extra vierge, eau, vinaigre de vin, sel, ail"\
                          "et jus de citron."
        nutritionGrade = "a"
        idCategory = (c)
        idStore = (s)
        return Products.objects.create(id=idprod,
                                       nameAlim=nameAlim,
                                       image=image, url=url,
                                       descriptionAlim=descriptionAlim,
                                       nutritionGrade=nutritionGrade,
                                       idCategory=idCategory,
                                       idStore=idStore)

    def setUp(self):
        self.client = Client()
        self.results_detail = reverse('results_details', args=[4])
        self.results = reverse('results')

        self.c = self.create_Category()
        self.s = self.create_Store()

        self.instc = self.assertTrue(isinstance(self.c, Category))
        self.assertEqual(self.c.__str__(), self.c.nameCategory)
        self.insts = self.assertTrue(isinstance(self.s, Store))
        self.assertEqual(self.s.__str__(), self.s.nameStore)

    def test_Category_creation(self):
        c = self.create_Category()
        s = self.create_Store()
        p = self.create_Products(2)

        self.assertTrue(isinstance(c, Category))
        self.assertEqual(c.__str__(), c.nameCategory)
        self.assertTrue(isinstance(s, Store))
        self.assertEqual(s.__str__(), s.nameStore)
        self.assertTrue(isinstance(p, Products))
        self.assertEqual(p.__str__(), p.nameAlim)

    def test_text_content(self):
        p = self.create_Products(3)
        expected_object_name = f'{p.nameAlim}'
        self.assertEquals(expected_object_name, 'Gazpacho')

    # views (uses reverse)
    def test_get_absolute_url(self):
        p = self.create_Products(4)
        response = self.client.get(self.results_detail)

        product_detail = Products.objects.get(id=4)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'aliments/results_details.html')  

    """def test_results_POST(self):
        p = self.create_Products(5)

        response = self.client.post(self.results, {"nameAlim":"Gazpacho",
                                                   "image":"https://static.openfoodfacts.org/images/products/541/018/803/1072/front_fr.30.200.jpg",
                                                   "url" : "https://world.openfoodfacts.org/product/5410188031072/gazpacho-alvalle",
                                                   "descriptionAlim" : "Tomate, poivron, concombre, oignon, huile d'olive extra vierge, eau, vinaigre de vin, sel, ail et jus de citron.",
                                                   "nutritionGrade": "a",
                                                   "idCategory": (self.c),
                                                   "idStore": (self.s)})

        self.assertEquals(response.status_code, 302)"""


class CategoryCreateTest(TestCase):

    def create_category(self, idCategory="idcategory",
                        nameCategory="namecategory"):
        return Category.objects.create(idCategory=idCategory, nameCategory=nameCategory)

    def test_category_creation(self):
        w = self.create_category()
        self.assertTrue(isinstance(w, Category))
        self.assertEqual(w.__str__(), w.nameCategory)


class StoreCreateTest(TestCase):

    def create_store(self, idStore="idstore", 
                     nameStore="namecstore"):
        return Store.objects.create(idStore=idStore, nameStore=nameStore)

    def test_store_creation(self):
        w = self.create_store()
        self.assertTrue(isinstance(w, Store))
        self.assertEqual(w.__str__(), w.nameStore)

# form test
class CommentFormTest(TestCase):

    def test_valid_data(self):
        form = RegistrationForm(data={"username" : "jspurbeurre",
                                      "email" : "purbeurre@example.com",
                                      "password1" : "pass1234.",
                                      "password2" : "pass1234."
                                      })

        self.assertTrue(form.is_valid())

    def test_non_valid_data(self):
        form = RegistrationForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)


class HomeView(TemplateView):
    template_name = 'aliments/index.html'

    def get_context_data(self, **kwargs):
        kwargs['environment'] = 'Production'
        return super().get_context_data(**kwargs)

# views test
class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.login = reverse('login')
        self.mentions = reverse('mentions')
        self.contact = reverse('contact')
        self.logout = reverse('logout')
        self.connected = reverse('connected')
        self.index = reverse('index')
        self.results_detail = reverse('results_details', args=[4])
        self.signup = reverse('signup')

    def test_login_GET(self):
        response = self.client.get(self.login)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'aliments/user.html')

    def test_mentions_GET(self):
        response = self.client.get(self.mentions)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'aliments/mentions.html')

    def test_contact_GET(self):
        response = self.client.get(self.contact)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'aliments/base.html')

    def test_logout_POST(self):
        response = self.client.post(self.logout)

        self.assertEquals(response.status_code, 200)

    def test_index_GET(self):
        response = self.client.post(self.index)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'aliments/index.html')

    def test_connected_GET(self):
        response = self.client.post(self.connected)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'aliments/aliments.html')

    def test_signup_POST(self):
        response = self.client.post(self.signup)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'aliments/signup.html')

