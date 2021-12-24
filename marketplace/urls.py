from django.urls import path
from . import views

app_name = 'marketplace'

urlpatterns = [
    path('', views.marketplace_views_home, name='marketplace_home_page'),
    path('list.html', views.marketplace_views_list, name='marketplace_list_items'),
    path('<int:item_id>', views.detail, name='marketplace_detail_item'),
    path('add.html', views.add, name='marketplace_add_item'),
    path('edit/<int:item_id>', views.edit, name='edit'),
    path('editted/<int:item_id>', views.edit_item, name='edit_item'),
    path('delete/<int:item_id>', views.delete, name='delete'),
    path('deleted', views.delete_item, name='delete_item'),
    path('search.html', views.search_result, name='search_result'),
    path('itemcomment/<int:item_id>', views.add_comment, name='product_add_comment'),
    path('editcomment', views.edit_comment_page, name='product_edit_comment'),
    path('deletecomment', views.delete_comment, name='product_delete_comment'),
    path('readcomment/<int:item_id>', views.read_comment, name='product_read_comment'),
    path('sorted', views.sort_by_item, name='sort_item'),
]