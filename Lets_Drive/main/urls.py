from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index),
    path('signin', views.signin),
    path('signup', views.signup),
    path('profile', views.profile),
    path('car', views.car),
    path('send_coord', views.send_coord, name='send_coord'),
    path('auth_session', views.auth_session, name='auth_session'),
    path('exit_user', views.exit_user, name='exit_user'),
    path('check_form', views.check_form, name='check_form'),
    path('selecttarif', views.selecttarif, name='selecttarif'),
    path('registerdrive', views.registerdrive, name='registerdrive'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
