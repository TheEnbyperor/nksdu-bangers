from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponseForbidden
from django.utils import timezone
from django.core.files.base import ContentFile
from django.conf import settings
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
import uuid
from . import models, tasks
import requests
import dateutil.parser


def index(request):
    if "show" in request.GET:
        url = f"https://nkd.su/api/week/{request.GET['show']}/"
    else:
        url = "https://nkd.su/api/"

    r = requests.get(url)
    if r.status_code == 404:
        raise Http404()

    r.raise_for_status()
    data = r.json()

    songs = []

    for song in data["playlist"]:
        existing_banger = models.Banger.objects.filter(nkdsu_id=song["track"]["id"]).first()
        songs.append({
            "title": song["track"]["title"],
            "role": song["track"]["role"],
            "artist": song["track"]["artist"],
            "id": song["track"]["id"],
            "existing_banger": existing_banger,
            "time": dateutil.parser.parse(song["time"])
        })

    return render(request, "banger/index.html", {
        "songs": songs,
        "next_show": dateutil.parser.parse(data["showtime"]),
        "site_key": settings.RECAPTCHA_SITE_KEY
    })


def bangers(request):
    banger_list = models.Banger.objects.all()
    paginator = Paginator(banger_list, 25)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'banger/bangers.html', {'page_obj': page_obj})


@require_POST
def make_banger(request, nkdsu_id):
    existing_banger = models.Banger.objects.filter(nkdsu_id=nkdsu_id).first()
    if existing_banger:
        return redirect('view_banger', existing_banger.id)

    recaptcha_resp = request.POST.get("g-recaptcha-response")
    recaptcha_r = requests.post("https://www.google.com/recaptcha/api/siteverify", data={
        "secret": settings.RECAPTCHA_SECRET_KEY,
        "response": recaptcha_resp
    })
    recaptcha_r.raise_for_status()
    recaptcha_data = recaptcha_r.json()

    if not recaptcha_data["success"]:
        return HttpResponseForbidden()

    r = requests.get(f"https://nkd.su/api/track/{nkdsu_id}")
    if r.status_code == 404:
        raise Http404()

    r.raise_for_status()
    data = r.json()

    cert_bytes = tasks.draw_cert(data["title"], data["artist"], data["role"])
    banger_id = uuid.uuid4()
    new_banger = models.Banger(
        id=banger_id,
        nkdsu_id=data["id"],
        title=data["title"],
        artist=data["artist"],
        role=data["role"],
        certified_timestamp=timezone.now(),
        certificate=ContentFile(cert_bytes, f"banger_{banger_id}.png")
    )
    new_banger.save()

    return redirect('view_banger', new_banger.id)


def view_banger(request, banger_id):
    banger = get_object_or_404(models.Banger, id=banger_id)

    return render(request, "banger/banger.html", {
        "banger": banger
    })
