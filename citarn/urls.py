from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from references import views as reference_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("conta/entrar/", auth_views.LoginView.as_view(), name="login"),
    path("conta/sair/", auth_views.LogoutView.as_view(), name="logout"),
    path(
        "conta/senha/",
        auth_views.PasswordChangeView.as_view(template_name="registration/password_change_form.html"),
        name="password_change",
    ),
    path(
        "conta/senha/concluido/",
        auth_views.PasswordChangeDoneView.as_view(template_name="registration/password_change_done.html"),
        name="password_change_done",
    ),
    path("conta/criar/", reference_views.register, name="register"),
    path("", include("references.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
