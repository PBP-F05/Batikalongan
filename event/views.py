from logging import warn
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import reverse
from .models import Event
from .forms import EventForm
from .decorators import admin_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

def show_event(request):
    events = Event.objects.all()
    return render(request, "event.html", {
        "events": events,
    })

@admin_required
def create_event(request):
    form = EventForm(request.POST or None, request.FILES or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect("event:show_event")

    context = { "form": form }
    return render(request, "create_event.html", context)

@admin_required
def edit_event(request, id):
    event = Event.objects.get(pk = id)
    form = EventForm(request.POST or None, request.FILES or None, instance=event)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect("event:show_event")

    context = { "form": form }
    return render(request, "edit_event.html", context)

@admin_required
def delete_event(request, id):
    event = Event.objects.get(pk = id)
    event.delete()
    return HttpResponseRedirect(reverse('event:show_event'))

@csrf_exempt
@require_POST
@admin_required
def create_event_ajax(request):
    form = EventForm(request.POST or None, request.FILES or None)
    form.save()

    return HttpResponse(b"CREATED", status=201)
