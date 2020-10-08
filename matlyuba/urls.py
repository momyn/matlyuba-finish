from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from app import views
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from matlyuba import settings
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url



urlpatterns = [
    path('admin/', admin.site.urls),
    path('cart/', include('cart.urls', namespace='cart')),
    path('shop/',  views.products, name='shop'),
    path('about/',  views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('lookbook/',  views.lookbook, name='lookbook'),
    path('lookbook/<slug:slug>', views.look, name='look'),
    path('', views.product_list, name='home'),
    path(r'product_list/', views.product_list,
         name='product_list'
         ),
    path(r'<slug:category_slug>/', views.product_list,
         name='product_list_by_category'
         ),
    path(r'<int:id>/<slug:slug>', views.product_detail,
         name='product_detail'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# if settings.DEBUG:
#     urlpatterns = static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#     urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
