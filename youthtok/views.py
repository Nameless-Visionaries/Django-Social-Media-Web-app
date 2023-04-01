from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .decorator import *
from .models import *
from .models import post as Post
import datetime
from itertools import chain
import random
from .forms import CommentForm, Video_form
from django.views import View
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin

# Create your views here.
#--------------------authuntication sections------------------------#
@unauthenticated_user
def landingpage(request):
	context = {}
	return render(request, 'landing.html', context)

@unauthenticated_user
def loginpage(request):
	if request.method == "POST":
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('gallery')
		else:
			messages.error(request, "login failed, password or username is incorrect")

	return render(request, 'login.html')

def signup(request):
	if request.method == "POST":
		first_name = request.POST.get('first_name')
		last_name = request.POST.get('last_name')
		username = request.POST.get('username')
		email = request.POST.get('email')
		gender = request.POST.get('gender')
		password = request.POST.get('password')
		password2 = request.POST.get('password2')



		if User.objects.filter(email=email).exists():
			messages.info(request, 'email already exists')
			return redirect('signup')
		elif User.objects.filter(username=username).exists():
			messages.info(request, 'username taken')
			return redirect('signup')
		if password != password2:
			messages.error(request, 'Error! passwords do not match')
		elif len(password) < 8:
			messages.error(request, 'password is too short') 

		else:
			new_user = User.objects.create_user(username, email, password)
			new_user.first_name = first_name
			new_user.last_name = last_name
			new_user.save()

			user_login = authenticate(username=username, password=password)
			login(request, user_login)

			#
			user_model = User.objects.get(username=username)
			new_profile = profile.objects.create(user=user_model, id_user=user_model.id)
			new_profile.save()

			return redirect('gallery')
	
	context = {'user': request.user,}
	return render(request, 'signup.html')

def logoutuser(request):
	logout(request)
	return redirect('login')


#-----------------end of authuntication sections------------------------------#

					#############################

#----------inner app functions and views---------_#
#random posts
@login_required
def gallery(request):
	video = Video.objects.all()

	user_object = User.objects.get(username=request.user.username)
	prof_user = profile.objects.get(user=user_object)
	posts = post.objects.all()

	user_following_list = []
	posted_feed = []

	user_following = followerscount.objects.filter(follower=request.user.username)

	for users in user_following:
		user_following_list.append(users.user)

	for username in user_following_list:
		feed_lists = post.objects.filter(user=username)
		posted_feed.append(feed_lists)
	feed_lists = list(chain(*posted_feed))


	#user suggestion statrts here!!!
	all_users = User.objects.all()
	user_following_all = []

	for user in user_following:
		user_list = User.objects.get(username=user.user)
		user_following_all.append(user_list)

	new_suggestions_list = [x for x in list(all_users) if (x not in list(user_following_all))]
	current_user = User.objects.filter(username=request.user.username)
	final_suggestions_list = [x for x in list(new_suggestions_list) if (x not in list(current_user))]
	random.shuffle(final_suggestions_list)

	username_profile = []
	username_profile_list = []

	for users in final_suggestions_list:
		username_profile.append(users.id)

	for ids in username_profile:
		profile_lists = profile.objects.filter(id_user=ids)
		username_profile_list.append(profile_lists)

	suggestions_username_profile_list = list(chain(*username_profile_list))

	#colloecting only captions empty for now

	#comments section

	context = {
		'posts': posts,
		'followingfeeds': feed_lists[:4], 
		'user_profile': prof_user,
		'suggestions_username_profile_list': suggestions_username_profile_list[:9],
	}
	return render(request, 'gallery.html', context)

#following only
@login_required
def follow_gallery(request):
	video = Video.objects.all()
	
	user_object = User.objects.get(username=request.user.username)
	prof_user = profile.objects.get(user=user_object)
	posts = post.objects.all()

	user_following_list = []
	posted_feed = []

	user_following = followerscount.objects.filter(follower=request.user.username)

	for users in user_following:
		user_following_list.append(users.user)

	for username in user_following_list:
		feed_lists = post.objects.filter(user=username)
		posted_feed.append(feed_lists)
	feed_lists = list(chain(*posted_feed))


	#user suggestion statrts here!!!
	all_users = User.objects.all()
	user_following_all = []

	for user in user_following:
		user_list = User.objects.get(username=user.user)
		user_following_all.append(user_list)

	new_suggestions_list = [x for x in list(all_users) if (x not in list(user_following_all))]
	current_user = User.objects.filter(username=request.user.username)
	final_suggestions_list = [x for x in list(new_suggestions_list) if (x not in list(current_user))]
	random.shuffle(final_suggestions_list)

	username_profile = []
	username_profile_list = []

	for users in final_suggestions_list:
		username_profile.append(users.id)

	for ids in username_profile:
		profile_lists = profile.objects.filter(id_user=ids)
		username_profile_list.append(profile_lists)

	suggestions_username_profile_list = list(chain(*username_profile_list))

	#colloecting only captions empty for now

	#comments section

	context = {
		'posts': feed_lists,
		'user_profile': prof_user,
		'suggestions_username_profile_list': suggestions_username_profile_list[:9],
	}
	return render(request, 'follow_posts.html', context)


#videos only
@login_required
def videos_gallery(request):
	
	user_object = User.objects.get(username=request.user.username)
	prof_user = profile.objects.get(user=user_object)
	posts = post.objects.all()

	user_following_list = []
	posted_feed = []

	user_following = followerscount.objects.filter(follower=request.user.username)

	for users in user_following:
		user_following_list.append(users.user)

	for username in user_following_list:
		feed_lists = post.objects.filter(user=username)
		posted_feed.append(feed_lists)
	feed_lists = list(chain(*posted_feed))


	#user suggestion statrts here!!!
	all_users = User.objects.all()
	user_following_all = []

	for user in user_following:
		user_list = User.objects.get(username=user.user)
		user_following_all.append(user_list)

	new_suggestions_list = [x for x in list(all_users) if (x not in list(user_following_all))]
	current_user = User.objects.filter(username=request.user.username)
	final_suggestions_list = [x for x in list(new_suggestions_list) if (x not in list(current_user))]
	random.shuffle(final_suggestions_list)

	username_profile = []
	username_profile_list = []

	for users in final_suggestions_list:
		username_profile.append(users.id)

	for ids in username_profile:
		profile_lists = profile.objects.filter(id_user=ids)
		username_profile_list.append(profile_lists)

	suggestions_username_profile_list = list(chain(*username_profile_list))
	
	#colloecting videos
	video = Video.objects.all() 
	if request.method == "POST":
		form = Video_form(data=request.POST, files=request.FILES)
		if form.is_valid():
			form.save()
			return redirect('videos-lab')
	else:
		form = Video_form()

	#comments section
	context = {
		'form' : form,
		'all_videos' : video,
		'user_profile': prof_user,
		'suggestions_username_profile_list': suggestions_username_profile_list[:9],
	}
	return render(request, 'video_lab.html', context)


#details for specific user page and funcunalities
class postdetails(LoginRequiredMixin, View):

	def get(self, request, pk, *args, **kwargs):
		user_posts = post.objects.get(id=pk)
		form = CommentForm()

		comments = Comment.objects.filter(posted=user_posts).order_by('created_on')

		context = {
			'form': form,
			'posts' : user_posts,
			'comments': comments,
		}
		return render(request, 'post&comments.html', context)
	def post(self, request, pk ,*args, **awargs):
		user_posts = post.objects.get(id=pk)
		form = CommentForm(request.POST)
		if form.is_valid():
			new_comment = form.save(commit=False)
			new_comment.author = request.user
			new_comment.posted = user_posts
			new_comment.save()

		comments = Comment.objects.filter(posted=user_posts).order_by('created_on')

		context = {
			'form': form,
			'posts' : user_posts,
			'comments': comments,
			}

		
		return render(request, 'post&comments.html', context)


#edit options for specific user page and funcunalities
class Posteditview(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = post
	fields = ['image', 'caption']
	template_name = 'postedit.html'

	def get_success_url(self):
		pk = self.kwargs['pk']
		return reverse_lazy('post-detail', kwargs={'pk':pk})

	def test_func(self):
		posti = self.get_object()
		return self.request.user == posti.user


#delete options for specific user page and funcunalities
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = post
	template_name = 'postdelete.html'
	success_url = reverse_lazy('gallery')

	def test_func(self):
		posti = self.get_object()
		return self.request.user == posti.user

#deleting a comment
class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Comment
	template_name = 'comment-delete.html'

	def get_success_url(self):
		pk = self.kwargs['detail_pk']
		return reverse_lazy('post-detail', kwargs={'pk': pk})
	
	def test_func(self):
		posti = self.get_object()
		return self.request.user == posti.author


#adding likes to post
class Addvideolike(LoginRequiredMixin, View):
	def post(self, request, pk, *args, **awargs):
		post = Video.objects.get(pk=pk)

		is_like = False
		for like in post.likes.all():
			if like == request.user:
				is_like = True
				break

		if not is_like:
			post.likes.add(request.user)

		if is_like:
			post.likes.remove(request.user)

		next = request.POST.get('next')
		return HttpResponseRedirect(next)

class Addpostlike(LoginRequiredMixin, View):
	def post(self, request, pk, *args, **awargs):
		post = Post.objects.get(pk=pk)

		is_like = False
		for like in post.likes.all():
			if like == request.user:
				is_like = True
				break

		if not is_like:
			post.likes.add(request.user)

		if is_like:
			post.likes.remove(request.user)

		next = request.POST.get('next')
		return HttpResponseRedirect(next)

class Addfeedlike(LoginRequiredMixin, View):
	def post(self, request, pk, *args, **awargs):
		post = Post.objects.get(pk=pk)

		is_like = False
		for like in post.likes.all():
			if like == request.user:
				is_like = True
				break

		if not is_like:
			post.likes.add(request.user)

		if is_like:
			post.likes.remove(request.user)

		next = request.POST.get('next')
		return HttpResponseRedirect(next)



#comment like
class addcommentlike(LoginRequiredMixin, View):
	def post(self, request, pk, *arg, **kwargs):
		comment = Comment.objects.get(pk=pk)
		is_dislike = False
		for dislike in comment.dislikes.all():
			if dislike == request.user:
				is_dislike = True
				break

		if is_dislike:
			comment.dislikes.remove(request.user)
		is_like = False

		for like in comment.likes.all():
			if like == request.user:
				is_like = True
				break

		if not is_like:
			comment.likes.add(request.user)
		if is_like:
			comment.likes.remove(request.user)

		next = request.POST.get('next', '/')
		return redirect(next)

#comments dislike
class adddislikecomments(LoginRequiredMixin, View):
	def post(self, request, pk, *arg, **kwargs):
		comment = Comment.objects.get(pk=pk)
		is_like = False
		for like in comment.likes.all():
			if like == request.user:
				is_like = True
				break

		if is_like:
			comment.likes.remove(request.user)
		is_dislike = False

		for dislike in comment.dislikes.all():
			if dislike == request.user:
				is_dislike = True
				break

		if not is_dislike:
			comment.dislikes.add(request.user)
		if is_dislike:
			comment.dislikes.remove(request.user)

		next = request.POST.get('next', '/')
		return redirect(next)

#replying to comments
class commentreplyview(LoginRequiredMixin, View):
	def post(self, request, post_pk, pk, *args, **awargs):
		post = Post.objects.get(pk=post_pk)
		parent_comment = Comment.objects.get(pk=pk)
		form = CommentForm(request.POST)

		if form.is_valid():
			new_comment = form.save(commit=False)
			new_comment.author = request.user
			new_comment.user = post
			new_comment.parent = parent_comment
			new_comment.save()

		return redirect('post-detail', pk=post_pk) 



@login_required
def pro(request, pk):
	video = Video.objects.all()
	user_object = User.objects.get(username=pk)
	prof_user = profile.objects.get(user=user_object)
	user_post = post.objects.filter(user=pk)
	user_post_length = len(user_post)

	follower = request.user.username
	user = pk


	if followerscount.objects.filter(follower=follower, user=user).first():
		button_text = 'Unfollow'
	else:
		button_text = 'follow'
	

	user_followers = len(followerscount.objects.filter(user=pk))
	user_following = len(followerscount.objects.filter(follower=pk))

	context = {
		'video': video,
		'user': request.user,
		'user_object': user_object,
		'user_profile': prof_user,
		'user_post': user_post,
		'user_post_length': user_post_length,
		'button_text': button_text,
		'user_followers': user_followers,
		'user_following': user_following 

	}
	return render(request, 'user_profile.html', context)

#-----------------------chat applications---------#
@login_required
def chat(request, pk):
	chat = Chat.objects.get(pk=pk)
	context = {
		'chat':chat,
	}
	return render(request, 'chat.html', context)

@login_required
def userschat(request, pk):
	context = {
		'user': request.user,
	}
	return render(request, 'users_chat.html', context)

#################################
@login_required
def settings(request):
	prof_user = profile.objects.get(user=request.user)


	if request.method == "POST":
		if request.FILES.get('image') == None:
			image = prof_user.profileimg
			bio = request.POST['bio']
			location = request.POST['location']

			prof_user.profileimg = image
			prof_user.bio = bio
			prof_user.location = location
			prof_user.save()

		if request.FILES.get('image') != None:
			image = request.FILES.get('image')
			bio = request.POST['bio']
			location = request.POST['location']

			prof_user.profileimg = image
			prof_user.bio = bio
			prof_user.location = location
			prof_user.save()
		return redirect('settings')

	context = {
		'user': request.user,
		'user_profile': prof_user,
	}
	return render(request, 'settings.html', context)

@login_required
def upload(request):	

	if request.method == 'POST':
		user = request.user.username
		image = request.FILES.get('image-upload')
		caption = request.POST['caption']


		new_post = post.objects.create(user=user, image=image, caption=caption)
		new_post.save()
		return redirect('/')


		
@login_required
def imgupload(request):
	return render(request, 'upload.html')

@login_required
def like_post(request):
	username = request.user.username
	post_id = request.GET.get('post_id')
	posts = post.objects.all()
	like_filter = likepost.objects.filter(post_id=post_id, username=username).first()
	if like_filter == None:
		new_like = likepost.objects.create(post_id=post_id, username=username)
		new_like.save()
		posts.no_of_likes = posts.no_of_likes+1
		posts.save()
		return redirect('gallery')
	else:
		like_filter.delete()
		posts.no_of_likes = posts.no_of_likes-1
		posts.save()
		return redirect('gallery')



@login_required
def follow(request):
	if request.method == 'POST':
		follower = request.POST['follower']
		user = request.POST['user']

		if followerscount.objects.filter(follower=follower, user=user).first():
			delete_follower = followerscount.objects.get(follower=follower, user=user)
			delete_follower.delete()
			return redirect('/profile/'+user)
		else:
			new_follower = followerscount.objects.create(follower=follower, user=user)
			new_follower.save()
			return redirect('/profile/'+user)
	else:
		return redirect('/')

@login_required
def search(request):

	user_object = User.objects.get(username=request.user.username)
	user_profile = profile.objects.get(user=user_object)
	if request.method == 'POST':
		username = request.POST['username']
		username_object = User.objects.filter(username__icontains=username)


		username_profile = []
		username_profile_list = []



		for users in username_object:
			username_profile.append(users.id)

		for ids in username_profile:
			profile_lists = profile.objects.filter(id_user=ids)
			username_profile_list.append(profile_lists)

		username_profile_list = list(chain(*username_profile_list))


	context = {
	'username_profile_list': username_profile_list,
	'user_object':user_object,
	'user_profile': user_profile,
	}
	return render(request, 'search-users.html', context)




