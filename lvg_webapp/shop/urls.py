from django.urls import path
from django.contrib.auth import views as auth_views  # Import auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),  # home page
    path('features/', views.features, name='features'),  # features page
    path('support/', views.support, name='support'),  # support page
    path('shop/', views.shop, name='shop'),  # shop page   
    path('register/', views.register, name='register'),  # register page
    path('login/', views.login_view, name='login'),  # login page
    path('logout/', views.logout_view, name='logout'), # logout
    path('template/', views.template, name='template'), # logout
    path('profile/', views.profile, name='profile'), # profile
    path('update_profile/', views.update_profile, name='update_profile'),
    path('change_password/', views.change_password, name='change_password'),
    path('support_profile/', views.support_profile, name='support_profile'),
    path('password_reset/', views.password_reset_request, name='forgot_password'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    path('request_email_change/', views.request_email_change, name='request_email_change'),
    path('confirm_email_change/<uidb64>/<token>/', views.confirm_email_change, name='confirm_email_change'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('lvg-collection/', views.lvg_collection, name='lvg_collection'),
    path('lvgdesign-collection/', views.lvgdesign_collection, name='lvgdesign_collection'),
    path('lvgwear-collection/', views.lvgwear_collection, name='lvgwear_collection'),
    path('search/', views.search, name='search'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)