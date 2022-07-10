from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt
import netflix

urlpatterns = [
	path('',views.index_view,name='index_view'),
	path('checkout',views.checkout, name='checkout'),
	path('success_payment',views.success_payment, name='success_payment'),
	#path('success_payment',csrf_exempt(netflix.views.success_payment)),
]
