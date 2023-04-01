from django.db import models
from django.contrib.auth import get_user_model
import uuid
from django.utils import timezone
from datetime import datetime
from .validators import file_size

# Create your models here.
User = get_user_model()

class profile(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	id_user = models.IntegerField(default=True)
	bio = models.TextField(blank=True)
	location = models.CharField(max_length=100, blank=True)
	profileimg = models.ImageField(upload_to='profile-images', default='icon.png')

	def __str__(self):
		return self.user.username


class post(models.Model):
	user = models.CharField(max_length=100)
	image = models.ImageField(upload_to="post-images")
	video = models.FileField(upload_to='video/%y')
	caption = models.TextField()
	created_at = models.DateTimeField(default=datetime.now)
	likes = models.ManyToManyField(User, blank=True, related_name='likes')
	dislikes = models.ManyToManyField(User, blank=True, related_name='dislikes')


	def __str__(self):
		return self.user

class Video(models.Model):
	#user = models.ForeignKey(User, on_delete=models.CASCADE)
	created_at = models.DateTimeField(default=datetime.now)
	caption = models.CharField(max_length=100)
	video = models.FileField(upload_to="video/%y", validators=[file_size])
	likes = models.ManyToManyField(User, blank=True, related_name='videolikes')
	dislikes = models.ManyToManyField(User, blank=True, related_name='videodislikes')


	def __str__(self):
		return self.caption[:50]



class likepost(models.Model):
	post_id = models.CharField(max_length=500)
	username = models.CharField(max_length=100)


	def __str__(self):
		return self.username


class Comment(models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	content = models.TextField()
	created_on = models.DateField(auto_now_add=True)
	posted = models.ForeignKey('post', on_delete=models.CASCADE)
	likes = models.ManyToManyField(User, blank=True, related_name='comment_likes')
	dislikes = models.ManyToManyField(User, blank=True, related_name='comment_dislikes')
	parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='+')


	@property
	def children(self):
		return Comment.objects.filter(parent=self).order_by('-created_on').all()

	@property
	def is_parent(self):
		if self.parent is None:
			return True
		return False

	def __str__(self):
		return self.content[:50]


		

class followerscount(models.Model):
	follower = models.CharField(max_length=100)
	user = models.CharField(max_length=100)

	def __str__(self):
		return self.user

class Notification(models.Model):
	#1 = like, 2 = comments, 3=follow
	notification_type = models.IntegerField()
	to_user = models.ForeignKey(User, related_name="notification_to", on_delete=models.CASCADE, null=True)
	from_user = models.ForeignKey(User, related_name="notification_from", on_delete=models.CASCADE, null=True)
	posts = models.ForeignKey('post', on_delete=models.CASCADE, related_name="+", blank=True, null=True)
	date = models.DateTimeField(default=timezone.now)
	user_has_seen = models.BooleanField(default=False)





class Chat(models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	message = models.TextField()
	created_at = models.DateField(default=timezone.now)

	def __str__(self):
		return self.author
