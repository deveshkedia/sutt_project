from django.shortcuts import render, get_object_or_404,redirect
from django.views.generic import TemplateView, DetailView, ListView,CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from .models import Category, Resource, Thread, Replies,Likes

# Create your views here.
def forum_home(request):
    return render(request, 'forum/home.html')

class ThreadView(LoginRequiredMixin,CreateView):
    model = Thread
    login_url  = '/accounts/login/'
    template_name = 'forum/threads/create.html'
    success_url = 'forum:thread_list'
    fields = ['title', 'content', 'category', 'resources']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['resources'] = Resource.objects.all()
        return context

class ThreadListView(ListView):
    model = Thread
    template_name = 'forum/threads/list.html'
    context_object_name = 'threads'
    paginate_by = 10
    ordering = ['-created_at']
    
    def get_queryset(self):
        return Thread.objects.annotate().select_related('author', 'category').prefetch_related('resources')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        # context['reply_count'] = Replies.objects.filter(is_deleted=False,thread__in=self.get_queryset()).count()
        return context

class ThreadDetailView(DetailView):
    model = Thread
    template_name = 'forum/threads/detail.html'
    context_object_name = 'thread'
    
    def get_queryset(self):
        return Thread.objects.select_related('author', 'category').prefetch_related('resources')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['replies'] = Replies.objects.filter(
            thread=self.object, 
            is_deleted=False
        ).select_related('author').order_by('created_at')
        context['is_moderator'] = self.request.user.groups.filter(name='Moderator').exists()
        context['liked'] = Likes.objects.filter(thread=self.object, user=self.request.user).exists()
        return context
    
@login_required 
def reply_to_thread(request,thread_id):
    if request.method == 'POST':
        thread = get_object_or_404(Thread, id=thread_id)
        content = request.POST.get('content')
        if content:
            Replies.objects.create(
                thread=thread,
                content=content,
                author=request.user
            )
    return redirect('thread-detail', pk=thread_id)

@login_required
def delete_reply(request, reply_id):
    if request.user.groups.filter(name='Moderator').exists():
        reply = get_object_or_404(Replies, id=reply_id)
    else:
        reply = get_object_or_404(Replies, id=reply_id, author=request.user)
    reply.is_deleted = True
    reply.save()
    return redirect('thread-detail', pk=reply.thread.id)

@login_required
def like_thread(request, pk):
    thread = get_object_or_404(Thread, id=pk)
    if Likes.objects.filter(thread=thread, user=request.user).exists():
        Likes.objects.filter(thread=thread, user=request.user).delete()
        thread.likes_count = thread.likes_count - 1
    else:
        Likes.objects.create(thread=thread, user=request.user)
        thread.likes_count = thread.likes_count + 1
    thread.save()
    return redirect('thread-detail', pk=pk)