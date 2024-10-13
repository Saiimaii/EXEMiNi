from . import views
from django.urls import path
from django.contrib.auth import views as auth_views


urlpatterns = [
    #login signup index base
    path('', views.index),
    path('contact/', views.contact),
    path('about/', views.about,name="about"),
    path('signup/', views.signup),
    path('login/', views.login),
    path('addUser/' , views.addUser),
    path('loginFrom/' , views.loginFrom),
    path('backend/' , views.backend),
    path('logout/' , views.logout),
    # path('change/<id>', views.change),
    #reset-password
    path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
    path('change/<int:id>/', views.change, name='change'),
    path('change-password/<int:id>/', views.change_password, name='change_password'),
    #Preorder page
    path('porder/', views.porder),
    path('new/', views.new),
    path('myorder/', views.myorder),
    path('edit/<datashop_id>', views.edit),
    path('delete/<datashop_id>/', views.delete),
    #admin page
    path('all_order/', views.all_order), 
    path('list_name/', views.list_name),  
    path('chart_view/', views.chart_view, name='chart_view'),
    path('weekly-product-data/', views.weekly_product_data, name='weekly_product_data'),
    path('update_status/', views.update_status),
    path('edit_user/<user_id>', views.edit),
    path('delete_user/<user_id>/', views.delete),

   
       
    
]


