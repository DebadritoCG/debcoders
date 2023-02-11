from django.urls import path
from home import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register', views.register, name='register'),
    path('login', views.login_page, name='login'),
    path('about', views.about, name='about'),
    path('blog', views.blog, name='blog'),
    path('handleRegister', views.handleRegister, name='handleRegister'),
    path('handleLogin', views.handleLogin, name='handleLogin'),
    path('handleLogout', views.handleLogout, name='handleLogout'),
    path('blogPost/<sno>', views.blogPost, name='blogPost'),
    path('search', views.search, name='search'),
    path('postComment', views.postComment, name='postComment'),
    path('account_info', views.account_info, name='account_info'),
    path('deleteComment', views.deleteComment, name='deleteComment'),
]