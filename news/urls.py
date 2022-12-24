from django.urls import path
from .views import PostList, PostDetail, PostCreate, PostEdit, PostDelete, \
   news_filter, posts_in_category, Categories, logger_view
from django.views.decorators.cache import cache_page


urlpatterns = [
   path('', cache_page(60*1)(PostList.as_view()), name='posts'),
   path('<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('search', news_filter, name="news_filter"),
   path('create', PostCreate.as_view(), name='post_create'),
   path('success', PostCreate.send_emails, name='send_email'),
   path('<int:pk>/edit', PostEdit.as_view(), name='post_edit'),
   path('<int:pk>/delete', PostDelete.as_view(), name='post_delete'),
   path('category/<int:category_id>', posts_in_category, name='posts_in_category'),
   path('categories', Categories.as_view(), name='posts_by_category'),
   path('logger_view/', logger_view, name='logger_view')
]
