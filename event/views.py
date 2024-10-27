from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.shortcuts import reverse
from .models import Event
from .forms import EventForm

def show_event(request):
    events = Event.objects.all()
    return render(request, "event.html", {
        "events": events,
    })

def create_event(request):
    form = EventForm(request.POST or None, request.FILES or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect("event:show_event")

    context = { "form": form }
    return render(request, "create_event.html", context)

def edit_event(request, id):
    event = Event.objects.get(pk = id)
    form = EventForm(request.POST or None, request.FILES or None, instance=event)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect("event:show_event")

    context = { "form": form }
    return render(request, "edit_event.html", context)

def delete_event(request, id):
    event = Event.objects.get(pk = id)
    event.delete()
    return HttpResponseRedirect(reverse('event:show_event'))