
from django.conf.urls import url
from . import views

app_name = 'tkartapp'
urlpatterns = [
        url(r'^$', views.store, name='store'),
        url(r'^store/$', views.store, name='store'),
        url(r'^store/viewcart/$',views.viewcart,name='viewcart'),
        url(r'^store/checkout/$',views.checkout,name='checkout'),
        url(r'^store/invalid_session/$',views.invalid_session,name='invalid_session'),
        # url(r'^store/outofstock/$',views.outofstock,name='outofstock'),
        # url(r'^admin/index/$',views.shirt_list,name='shirt_list'),
        # url(r'^admin/create/$',views.shirt_create,name='shirt_create'),
        # url(r'^admin/update/(?P<pk>\d+)$',views.shirt_update,name='shirt_update'),
        # url(r'^admin/delete/(?P<pk>\d+)$',views.shirt_delete,name='shirt_delete'),
        url(r'^store/add_to_cart/$',views.add_to_cart,name='add_to_cart'),
        url(r'^login/$',  views.login,name='login'),
        url(r'^auth/$',  views.auth_view,name='auth_view'),
        url(r'^logout/$', views.logout,name='logout'),
        url(r'^loggedin/$', views.loggedin,name='loggedin'),
        url(r'^invalid/$', views.invalid_login,name='invalid_login'),
        url(r'^register/$', views.register_user,name='register_user'),
        url(r'^register_success/$', views.register_success,name='register_success')
]
