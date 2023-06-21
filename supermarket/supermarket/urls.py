from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.index.urls',namespace='index')),
    path('accounts/', include('apps.accounts.urls',namespace='accounts')),
    path('about_us/',include('apps.about_us.urls',namespace='about_us')),
    path('search/',include('apps.search.urls',namespace='search')),
    path('contact_us/',include('apps.contact_us.urls',namespace='contact_us')),
    path('products/',include('apps.products.urls',namespace='products')),
    path('orders/',include('apps.orders.urls',namespace='orders')),
    path('payments/',include('apps.payments.urls',namespace='payments')),
    path('scoring/',include('apps.scoring.urls',namespace='scoring')),
    path('comments/',include('apps.comments.urls',namespace='comments')),
    path('favorite/',include('apps.favorite.urls',namespace='favorite')),
    path('compare/',include('apps.compare.urls',namespace='compare')),
    path('blogs/',include('apps.blogs.urls',namespace='blogs')),
    path('ckeditor',include('ckeditor_uploader.urls')),




]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
