from django.conf.urls import url, include
from .views import cart_home, cart_update

urlpatterns = [
    url(r'^$', cart_home, name='home'),
    url(r'^update/$', cart_update, name='update')
]
