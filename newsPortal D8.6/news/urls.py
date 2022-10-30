from django.urls import path
from .views import PostList, PostDetail, PostCreate, PostEdit, PostDelete, news_filter


urlpatterns = [
   path('', PostList.as_view(), name='posts'),
   path('<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('search', news_filter, name="news_filter"),
   path('create', PostCreate.as_view(), name='post_create'),
   path('<int:pk>/edit', PostEdit.as_view(), name='post_edit'),
   path('<int:pk>/delete', PostDelete.as_view(), name='post_delete'),

]
