from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import *
urlpatterns = [
	path('', views.landingpage, name='landingpage'),
	path('gallery/', views.gallery, name="gallery"),
	path('feeds/', views.follow_gallery, name='follow-gallery'),
	path('videos-gallery', views.videos_gallery, name="videos-lab"),
	path('videos-gallery/<int:pk>/like', Addvideolike.as_view(), name='like'),
	path('gallery/<int:pk>/like', Addpostlike.as_view(), name='photolike'),
	path('feeds/<int:pk>/like', Addfeedlike.as_view(), name='feedlike'),
	path('login/', views.loginpage, name="login"),
	path('setting/', views.settings, name='settings'),
	path('upload/', views.upload, name='upload'),
	# path('vidupload/', views.vidupload, name='vidupload'),
	path('post/', views.imgupload, name='imgupload'),
	path('signup/', views.signup, name="signup"),
	path('detail/<int:pk>/', postdetails.as_view(), name='post-detail'),
	path('detail/edit/<int:pk>/', Posteditview.as_view(), name="post-edit"),
	path('detail/delete/<int:pk>/', PostDeleteView.as_view(), name='post-delete'),
	path('detail/<int:detail_pk>/comment/delete/<int:pk>/', CommentDeleteView.as_view(), name='comment-delete'),
	path('detail/<int:detail_pk>/comment/<int:pk>/like', addcommentlike.as_view(), name="comment-like"),
	path('detail/<int:detail_pk>/comment/<int:pk>/dislike', adddislikecomments.as_view(), name="comment-dislike"),
	path('detail/<int:post_pk>/comment/<int:pk>/reply', commentreplyview.as_view(), name='comment-reply'),
	path('logout/', views.logoutuser, name="logout"),
	path('profile/<str:pk>/', views.pro, name="pro"),
	path('chat', views.chat, name="chat"),
	path('friend/<str:pk>', views.userschat, name="userschat"),
	path('follow', views.follow, name="follow"),
	path('search', views.search, name="search"),

]