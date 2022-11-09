from django.urls import path
from .views import PostList, PostDetail, PostCreate, PostEdit, PostDelete, \
   news_filter, send_emails_to_subscribers, posts_in_category, Categories


urlpatterns = [
   path('', PostList.as_view(), name='posts'),
   path('<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('search', news_filter, name="news_filter"),
   path('create', PostCreate.as_view(), name='post_create'),
   path('success', send_emails_to_subscribers, name='send_email'),
   path('<int:pk>/edit', PostEdit.as_view(), name='post_edit'),
   path('<int:pk>/delete', PostDelete.as_view(), name='post_delete'),
   path('category/<int:category_id>', posts_in_category, name='posts_in_category'),
   path('categories', Categories.as_view(), name='posts_by_category' )

]
