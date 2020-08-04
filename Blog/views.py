from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from .models import Post,Comments
from .forms import Comment_form
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import (
	ListView,
	DetailView,
	CreateView,
	UpdateView,
	DeleteView
	)

# Create your views here.
def home(request):
	posts = Post.objects.all()
	return render(request,'home/home.html',{'posts':posts})

def about(request):
	return render(request,'home/about.html',{'title':'Django-About'})

class PostListView(ListView):
	model = Post
	template_name = 'home/home.html'
	context_object_name = 'posts'
	ordering = ['-date_posted']
	paginate_by = 5

class UserPostListView(ListView):
    model = Post
    template_name = 'home/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 2

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):
	model = Post
	template_name = 'home/post_detail.html'
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['Comments'] = Comments.objects.filter(post=pk)
		context['form'] = Comment_form()
		return context
def PostDetail(request,pk):
	object_post = get_object_or_404(Post, pk=pk)
	comment_list = Comments.objects.filter(post=pk).order_by('-date_posted')
	if request.method == 'POST':
		form = Comment_form(request.POST)
		if form.is_valid():
			comment = form.save(commit=False)
			comment.post = object_post
			comment.user = request.user
			comment.save()
			#return redirect('/')
	else:
		form = Comment_form()
	context = {'object_post':object_post,'comment_list':comment_list,'form':form}
	return render(request,'home/post_detail.html',context)
		

class PostCreateView(LoginRequiredMixin, CreateView):
	model = Post
	fields = ['title','content']
	template_name = 'home/post_create.html'

	def form_valid(self, form):
		form.instance.author = self.request.user
		form.instance.post = self.request.post
		return super().form_valid(form)

class CommentCreateView(LoginRequiredMixin, CreateView):
	model = Comments
	fields = ['comment']
	template_name = 'home/post_detail.html'

	def form_valid(self, form):
		form.instance.user = self.request.user
		return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	fields = ['title','content']
	template_name = 'home/post_create.html'

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		else:
			return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post
	template_name = 'home/post_delete_confirm.html'
	success_url = '/'

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		else:
			return False