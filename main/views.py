from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm, ApplicationForm
from .models import Application

def index(request):
    #Главная: последни заявки + счетчик
    done_apps = Application.objects.filter(status='done').order_by('-created_at')[:4]
    in_work_count = Application.objects.filter(status='in_work').count()
    return render(request, 'main/index.html', {
        'done_apps': done_apps,
        'in_work_count': in_work_count,
    })
#если я не сдам все раньше среды я повешусь в туалете

def register(request):
    #Регистрация
    if request.user.is_authenticated:
        return redirect('profile')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Регистрация прошла успешно. Теперь войдите в систему.')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'main/register.html', {'form': form})


@login_required
def profile(request):
    applications = Application.objects.filter(user=request.user)
    status = request.GET.get('status', '')
    if status in ['new', 'in_work', 'done']:
        applications = applications.filter(status=status)
    return render(request, 'main/profile.html', {
        'applications': applications,
        'status': status,
        'statuses': Application.STATUS_CHOICES,
    })

@login_required
def create_application(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.save()
            messages.success(request, 'Заявка успешно создана.')
            return redirect('profile')
    else:
        form = ApplicationForm()
    return render(request, 'main/create_application.html', {'form': form})

@login_required
def delete_application(request, pk):
    application = get_object_or_404(Application, pk=pk, user=request.user)

    if application.status != 'new':
        messages.error(request, 'Нельзя удалить заявку, которая уже принята в работу или выполнена.')
        return redirect('profile')

    if request.method == 'POST':
        application.delete()
        messages.success(request, 'Заявка удалена.')
        return redirect('profile')

    return render(request, 'main/application_confirm_delete.html', {'application': application})