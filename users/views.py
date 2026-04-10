from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib.auth.decorators import login_required
from django.conf import settings
from urllib.parse import urlparse
from .forms import CustomRegistrationForm, ChangePasswordForm
from main.models import UserMedia
from main.services.recommendations import get_recommendations_for_media


def register(request):
    form = CustomRegistrationForm()
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.email = user.email.lower()
            user.save()
            login(request, user, backend="users.backends.EmailBackend")
            return redirect('home')
        messages.error(request, 'Registration failed. Please correct the errors below.')

    return render(request, 'users/auth.html', {'form': form,'page': 'register'})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user, backend='users.backends.EmailBackend')
            
            # Get next from POST and validate it
            next_url = request.POST.get('next', '')
            if next_url and len(next_url) <= 500 and url_has_allowed_host_and_scheme(next_url, allowed_hosts=None):
                return redirect(next_url)
            return redirect('home')
        else:
            messages.error(request, 'Invalid email or password.')

    return render(request, 'users/auth.html', {'page': 'login'})

def change_password(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ChangePasswordForm(user=request.user, data=request.POST)
            if form.is_valid():
                form.save()
                login(request, request.user)
                messages.success(request, 'Your password has been changed successfully.')
                return redirect('home') 
            else:
                for error in list(form.errors.values()):
                    messages.error(request, ', '.join([str(e) for e in error]))
        else:
            form = ChangePasswordForm(user=request.user)
        return render(request, 'users/password.html', {'form': form})
    messages.error(request, 'You need to be logged in to change your password.')
    return redirect('login')


def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url="login")
def update_user(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            full_name = request.POST.get('full_name')
            username = request.POST.get('username')
            email = request.POST.get('email')
            user = request.user
            user.full_name = full_name
            user.username = username
            user.email = email
            user.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('home') 
        return render(request, 'users/update_user.html', {'user': request.user})
    messages.error(request, 'You need to be logged in to update your profile.')
    return redirect('login')


@login_required(login_url="login")
def profile(request):
    status_filter = request.GET.get("status")

    watching = UserMedia.objects.filter(user=request.user, status="watching").select_related("media")
    completed = UserMedia.objects.filter(user=request.user, status="completed").select_related("media")
    plan = UserMedia.objects.filter(user=request.user, status="plan").select_related("media")

    sections = [
        {
            "title": "Watching / Reading",
            "icon": "play-circle",
            "key": "watching",
            "items": watching
        },
        {
            "title": "Completed",
            "icon": "check-circle",
            "key": "completed",
            "items": completed
        },
        {
            "title": "Plan to Watch / Read",
            "icon": "bookmark",
            "key": "plan",
            "items": plan
        }
    ]

    if status_filter:
        sections = [s for s in sections if s["key"] == status_filter]

    all_items = UserMedia.objects.filter(user=request.user).select_related("media")
    
    return render(request, "users/profile.html", {
        "sections": sections,
        "watching": watching,
        "completed": completed,
        "plan": plan,
        "current_filter": status_filter,
        "all_items": all_items,
    })


@login_required(login_url="login")
def profile(request):
    status_filter = request.GET.get('status')
    user_media = UserMedia.objects.filter(user=request.user).select_related('media')
    
    watching = [m for m in user_media if m.status == 'watching']
    completed = [m for m in user_media if m.status == 'completed']
    plan = [m for m in user_media if m.status == 'plan']
    
    all_sections = [
        {"key": "watching", "title": "Watching / Reading", "items": watching, "icon": "play-circle"},
        {"key": "completed", "title": "Completed", "items": completed, "icon": "check-circle"},
        {"key": "plan", "title": "Plan to Watch / Read", "items": plan, "icon": "bookmark"},
    ]

    if status_filter in ['watching', 'completed', 'plan']:
        sections = [s for s in all_sections if s['key'] == status_filter]
    else:
        sections = all_sections
    
    return render(request, "users/profile.html", {
        "sections": sections,
        "watching": watching,
        "completed": completed,
        "plan": plan,
        "current_filter": status_filter,
    })


@login_required(login_url="login")
def recommendations_view(request,):
    completed = (
        UserMedia.objects.filter(user=request.user, status="completed")
        .select_related("media").order_by("-updated_at")
    )

    if not completed.exists():
        return render(request, "main/recommendations.html", {
            "recommendations": [],
            "empty_reason": "Complete something first to get personalized recommendations!"
        })

    tracked_media = set(UserMedia.objects.filter(user=request.user).values_list("media_id", flat=True))

    seen_external_ids = set()
    recommendations = []

    for user_media in completed:
        media = user_media.media
        recs = get_recommendations_for_media(
            source=media.source,
            external_id=media.external_id,
            media_type=media.media_type,
        )

        for rec in recs:
            ext_id = rec["external_id"]

            if ext_id in tracked_media or ext_id in seen_external_ids:
                continue

            seen_external_ids.add(ext_id)
            rec["because_of"] = media.title
            recommendations.append(rec)
    
    recommendations.sort(key=lambda x: x.get("score") or 0, reverse=True)

    return render(request, "main/recommendations.html", {"recommendations": recommendations[:20], "empty_reason": None})
