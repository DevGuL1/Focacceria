from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('login/', views.dashboard_login, name='dashboard_login'),
    path('logout/', views.dashboard_logout, name='dashboard_logout'),

    # Home
    path('', views.dashboard_home, name='dashboard_home'),

    # Site Settings
    path('settings/', views.site_settings, name='site_settings'),
    path('fonts/', views.font_settings, name='font_settings'),
    path('home-video/', views.home_video_settings, name='home_video_settings'),

    # Sliders
    path('sliders/', views.sliders, name='sliders'),
    path('sliders/add/', views.slider_add, name='slider_add'),
    path('sliders/<int:pk>/edit/', views.slider_edit, name='slider_edit'),
    path('sliders/<int:pk>/delete/', views.slider_delete, name='slider_delete'),

    # Navigation
    path('navigation/', views.navigation, name='navigation'),
    path('navigation/add/', views.nav_add, name='nav_add'),
    path('navigation/<int:pk>/edit/', views.nav_edit, name='nav_edit'),
    path('navigation/<int:pk>/delete/', views.nav_delete, name='nav_delete'),
    path('navigation/reorder/', views.nav_reorder, name='nav_reorder'),

    # Footer
    path('footer/', views.footer, name='footer'),
    path('footer/column/add/', views.footer_column_add, name='footer_column_add'),
    path('footer/column/<int:pk>/delete/', views.footer_column_delete, name='footer_column_delete'),
    path('footer/link/add/', views.footer_link_add, name='footer_link_add'),
    path('footer/link/<int:pk>/delete/', views.footer_link_delete, name='footer_link_delete'),

    # SEO
    path('seo/', views.seo_settings, name='seo_settings'),

    # Menu Categories
    path('menu/categories/', views.menu_categories, name='menu_categories'),
    path('menu/categories/add/', views.category_add, name='category_add'),
    path('menu/categories/<int:pk>/edit/', views.category_edit, name='category_edit'),
    path('menu/categories/<int:pk>/delete/', views.category_delete, name='category_delete'),
    path('menu/categories/reorder/', views.category_reorder, name='category_reorder'),

    # Menu Items
    path('menu/items/', views.menu_items, name='menu_items'),
    path('menu/items/category/<int:category_pk>/', views.menu_items, name='menu_items_by_category'),
    path('menu/items/add/', views.item_add, name='item_add'),
    path('menu/items/<int:pk>/edit/', views.item_edit, name='item_edit'),
    path('menu/items/<int:pk>/delete/', views.item_delete, name='item_delete'),
    path('menu/items/reorder/', views.item_reorder, name='item_reorder'),

    # Add-ons
    path('menu/addons/', views.addons, name='addons'),
    path('menu/addons/add/', views.addon_add, name='addon_add'),
    path('menu/addons/<int:pk>/delete/', views.addon_delete, name='addon_delete'),
]
