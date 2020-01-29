from django.conf.urls import url
from .import views  # import views so we can use them in urls.
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    url(r'^$', views.index),
    url(r'^index', views.index, name="index"),
    url(r'^login/$', LoginView.as_view(template_name='aliments/user.html'), name='login'),
    url(r'^results/$', views.results, name="results"),
    url(r'^results_details/(?P<pk>\d+)/$', views.results_details, name="results_details"),
    url(r'^aliment/', views.aliment, name="aliment"),
    url(r'^logout/$', LogoutView.as_view(template_name='aliments/index.html'), name='logout'),
    url(r'^mentions/', views.mentions, name="mentions"),
    url(r'^contact/', views.index, name="contact"),
    url(r'^signup/', views.signup, name="signup"),
    url(r'^connected/', views.connected, name="connected"),
]
