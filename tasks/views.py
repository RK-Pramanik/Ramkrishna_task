from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Task, Submission
from .forms import TaskForm
from django.contrib import messages
from django.db.models import Count

@login_required
def task_list(request):
    user = request.user
    if user.is_admin() or user.is_superuser:
        tasks = Task.objects.all()
    elif user.is_teacher():
        tasks = Task.objects.filter(created_by=user)
    else:
        tasks = Task.objects.filter(assigned_to=user)
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'tasks/task_detail.html', {'task': task})

@login_required
def create_task(request):
    if not (request.user.is_teacher() or request.user.is_admin()):
        return HttpResponseForbidden("You don't have permission.")
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            task.save()
            messages.success(request, "Task created successfully.")
            return redirect('tasks:list')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form})

@login_required
def edit_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.user != task.created_by and not request.user.is_admin():
        return HttpResponseForbidden("Not allowed.")
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, "Task updated.")
            return redirect('tasks:detail', pk=pk)
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form})

@login_required
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.user != task.created_by and not request.user.is_admin():
        return HttpResponseForbidden("Not allowed.")
    if request.method == 'POST':
        task.delete()
        messages.success(request, "Task deleted.")
        return redirect('tasks:list')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})

@login_required
def update_status(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if request.user == task.assigned_to or request.user.is_teacher() or request.user.is_admin():
            task.status = new_status
            task.save()
            messages.success(request, "Status updated.")
        else:
            return HttpResponseForbidden("You cannot update this task.")
    return redirect('tasks:detail', pk=pk)

@login_required
def submit_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.user != task.assigned_to:
        return HttpResponseForbidden("Only the assigned student can submit.")
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        Submission.objects.create(task=task, student=request.user, file=file)
        messages.success(request, "File submitted successfully.")
    return redirect('tasks:detail', pk=pk)

@login_required
def dashboard(request):
    """Dashboard view showing task statistics and recent activities."""
    user = request.user
    
    # Base queryset for tasks
    if user.is_admin():
        tasks = Task.objects.all()
    elif user.is_teacher():
        tasks = Task.objects.filter(created_by=user)
    else:  # student
        tasks = Task.objects.filter(assigned_to=user)
    
    # Task statistics
    context = {
        'total_tasks': tasks.count(),
        'completed_tasks': tasks.filter(status='completed').count(),
        'in_progress_tasks': tasks.filter(status='in_progress').count(),
        'pending_tasks': tasks.filter(status='pending').count(),
        'recent_tasks': tasks.order_by('-created_at')[:5],
    }
    
    # Recent submissions (only for teachers and admins)
    if user.is_teacher() or user.is_admin():
        if user.is_teacher():
            submissions = Submission.objects.filter(task__created_by=user)
        else:  # admin
            submissions = Submission.objects.all()
        context['recent_submissions'] = submissions.order_by('-uploaded_at')[:5]
    
    return render(request, 'dashboard.html', context)
