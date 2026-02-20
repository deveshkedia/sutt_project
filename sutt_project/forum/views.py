from django.shortcuts import render, get_object_or_404,redirect
from django.views.generic import TemplateView, DetailView, ListView,CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from .models import Category, Tags, Thread, Replies, Likes, Report, ThreadResource
from forum.emails import send_thread_like_notification
from django.contrib.postgres.search import TrigramSimilarity
import markdown 
import bleach


ALLOWED_TAGS = [
    "p", "h1", "h2", "h3", "h4", "h5", "h6",
    "ul", "ol", "li",
    "strong", "em", "blockquote",
    "code", "pre",
    "a",
    "img",
]

ALLOWED_ATTRIBUTES = {
    "a": ["href", "title"],
    "img": ["src", "alt", "width", "height"],
}

# Create your views here.
def forum_home(request):
    return render(request, 'forum/home.html')

class ReportView(LoginRequiredMixin, CreateView):
    model = Report
    login_url  = '/accounts/login/'
    template_name = 'forum/threads/report.html'
    fields = ['reason', 'description']
    
    def form_valid(self, form):
        thread_id = self.kwargs['thread_id']
        thread = get_object_or_404(Thread, id=thread_id)
        
        existing_report = Report.objects.filter(thread=thread, reporter=self.request.user).exists()
        if existing_report:
            form.add_error(None, "You have already reported this thread.")
            return self.form_invalid(form)
        
        report = form.save(commit=False)
        report.thread = thread
        report.reporter = self.request.user
        report.save()
        
        return redirect('thread-detail', pk=thread_id)

class ThreadView(LoginRequiredMixin,CreateView):
    model = Thread
    login_url  = '/accounts/login/'
    template_name = 'forum/threads/create.html'
    success_url = reverse_lazy('thread-list')
    fields = ['title', 'content', 'category']
    
    def form_valid(self,form):
        thread = form.save(commit=False)
        thread.author = self.request.user
        thread.save()
        
        raw_tags = self.request.POST.get("tags", "")
        tag_names = [tag.strip() for tag in raw_tags.split(",") if tag.strip()]
        for tag_name in tag_names:
            tag, created = Tags.objects.get_or_create(name=tag_name)
            thread.tags.add(tag)
        
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

        

class ThreadListView(ListView):
    model = Thread
    template_name = 'forum/threads/list.html'
    context_object_name = 'threads'
    paginate_by = 10
    ordering = ['-created_at']
    def get_queryset(self):
        queryset = Thread.objects.annotate().select_related('author', 'category').prefetch_related('thread_resources')
        q = self.request.GET.get("q")
        category=self.request.GET.get("category")
        if q:
            queryset = queryset.annotate(similarity=TrigramSimilarity("title", q) + TrigramSimilarity("content", q)).filter(similarity__gt=0.1).order_by("-similarity")
        if category:
            queryset = queryset.filter(category__id=category)

        return queryset
            
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['tags'] = Tags.objects.all()
        return context

class MyThreadsListView(LoginRequiredMixin, ListView):
    model = Thread
    template_name = 'forum/threads/my_threads.html'
    context_object_name = 'threads'
    paginate_by = 10
    ordering = ['-created_at']
    login_url = '/accounts/login/'
    
    def get_queryset(self):
        queryset = Thread.objects.filter(author=self.request.user).select_related('author', 'category').prefetch_related('thread_resources')
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['tags'] = Tags.objects.all()
        return context

class ThreadDetailView(LoginRequiredMixin, DetailView):
    model = Thread
    template_name = 'forum/threads/detail.html'
    context_object_name = 'thread'
    login_url = '/accounts/login/'
    
    def get_queryset(self):
        return Thread.objects.select_related('author', 'category').prefetch_related('thread_resources')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['replies'] = Replies.objects.filter(
            thread=self.object, 
            is_deleted=False
        ).select_related('author').order_by('created_at')
        context['thread_resources'] = ThreadResource.objects.filter(thread=self.object)
        context['is_moderator'] = self.request.user.groups.filter(name='Moderator').exists()
        context['is_author'] = self.request.user == self.object.author
        context['liked'] = Likes.objects.filter(thread=self.object, user=self.request.user).exists()
        context['content_html'] = bleach.clean(
            markdown.markdown(self.object.content, extensions=['fenced_code', 'codehilite']),
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        strip=True
    )
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

        if thread.author and thread.author != request.user:
            try:
                send_thread_like_notification(
                    thread_author_email=thread.author.email,
                    liker_name=request.user.get_full_name() or request.user.username,
                    thread_title=thread.title
                )
            except Exception as e:
                pass
    
    thread.save()
    return redirect('thread-detail', pk=pk)

@login_required
def report_thread(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    existing_report = Report.objects.filter(thread=thread, reporter=request.user).exists()
    
    if request.method == 'POST':
        if existing_report:
            return render(request, 'forum/threads/report.html', {
                'thread': thread,
                'error': 'You have already reported this thread.'
            })
        
        reason = request.POST.get('reason')
        description = request.POST.get('description')
        
        if reason and description:
            Report.objects.create(
                thread=thread,
                reporter=request.user,
                reason=reason,
                description=description
            )
            return redirect('thread-detail', pk=thread_id)
    
    return render(request, 'forum/reports/create.html', {
        'thread': thread,
        'existing_report': existing_report,
        'reason_choices': Report.REASON_CHOICES
    })

class ReportListView(LoginRequiredMixin, ListView):
    model = Report
    template_name = 'forum/reports/list.html'
    context_object_name = 'reports'
    paginate_by = 10
    ordering = ['-created_at']
    login_url = '/accounts/login/'
    
    def get_queryset(self):
        if not self.request.user.groups.filter(name='Moderator').exists():
            return Report.objects.none()
        
        queryset = Report.objects.select_related('thread', 'reporter').order_by('-created_at')
        status = self.request.GET.get('status')
        reason = self.request.GET.get('reason')
        
        if status:
            queryset = queryset.filter(status=status)
        if reason:
            queryset = queryset.filter(reason=reason)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = Report.STATUS_CHOICES
        context['reason_choices'] = Report.REASON_CHOICES
        context['selected_status'] = self.request.GET.get('status', '')
        context['selected_reason'] = self.request.GET.get('reason', '')
        return context

@login_required
def update_report_status(request, report_id, status):
    if not (request.user.is_staff or request.user.groups.filter(name='Moderator').exists()):
        return redirect('report-list')
    
    report = get_object_or_404(Report, id=report_id)
    valid_statuses = [choice[0] for choice in Report.STATUS_CHOICES]
    if status in valid_statuses:
        report.status = status
        report.save()
    
    return redirect('report-list')

@login_required
def review_report(request, report_id):
    return update_report_status(request, report_id, 'reviewed')

@login_required
def resolve_report(request, report_id):
    return update_report_status(request, report_id, 'resolved')

@login_required
def upload_thread_resource(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    if request.user != thread.author:
        return redirect('thread-detail', pk=thread_id)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        file_type = request.POST.get('file_type', 'other')
        description = request.POST.get('description')
        file = request.FILES.get('file')
        
        if title and file:
            ThreadResource.objects.create(
                thread=thread,
                title=title,
                file=file,
                file_type=file_type,
                description=description,
                uploaded_by=request.user
            )
    
    return redirect('thread-detail', pk=thread_id)

@login_required
def delete_thread_resource(request, resource_id):
    resource = get_object_or_404(ThreadResource, id=resource_id)
    thread_id = resource.thread.id
    if request.user != resource.uploaded_by and request.user != resource.thread.author:
        return redirect('thread-detail', pk=thread_id)
    
    resource.file.delete()
    resource.delete()
    
    return redirect('thread-detail', pk=thread_id)