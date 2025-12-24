from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from django.db.utils import OperationalError
from django.http import JsonResponse, HttpResponseBadRequest
import requests
from functools import lru_cache
import time

try:
    from .models import Board
except Exception:
    Board = None

try:
    from reports.models import Report
except Exception:
    Report = None

def home(request):
    now = timezone.now()
    last7 = 0
    last30 = 0
    avg_risk_7 = 0

    if Report is not None:
        try:
            last7 = Report.objects.filter(created_at__gte=now - timedelta(days=7)).count()
            last30 = Report.objects.filter(created_at__gte=now - timedelta(days=30)).count()
            risks = list(Report.objects.filter(created_at__gte=now - timedelta(days=7)).values_list('risk', flat=True))
            avg_risk_7 = round(sum(risks) / len(risks), 2) if risks else 0
        except OperationalError:
            last7 = last30 = 0
            avg_risk_7 = 0

    return render(request, 'pages/home.html', {'last7': last7, 'last30': last30, 'avg_risk_7': avg_risk_7})

def about(request):
    return render(request, 'pages/about.html')

# --- KR Admin Proxy (Overpass) ---

# Simple in-process TTL cache
_cache_store = {}
_CACHE_TTL_SEC = 60 * 60  # 1 hour

def _cache_get(key):
    item = _cache_store.get(key)
    if not item:
        return None
    ts, value = item
    if time.time() - ts > _CACHE_TTL_SEC:
        _cache_store.pop(key, None)
        return None
    return value

def _cache_set(key, value):
    _cache_store[key] = (time.time(), value)

OVERPASS_URL = "https://overpass-api.de/api/interpreter"

def _overpass(query):
    try:
        r = requests.post(OVERPASS_URL, data={"data": query}, timeout=25)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"elements": []}

def _list_sido():
    key = "sido:list"
    cached = _cache_get(key)
    if cached is not None:
        return cached
    q = (
        "[out:json][timeout:25];"
        "rel[boundary=administrative][admin_level=2][name=\"대한민국\"];"
        "map_to_area->.kr;"
        "rel(area.kr)[boundary=administrative][admin_level=4][name];"
        "out tags;"
    )
    j = _overpass(q)
    names = sorted({(e.get('tags') or {}).get('name') for e in j.get('elements', []) if (e.get('tags') or {}).get('name')})
    _cache_set(key, names)
    return names

def _list_sigungu(sido_name: str):
    key = f"sigungu:{sido_name}"
    cached = _cache_get(key)
    if cached is not None:
        return cached
    q = (
        "[out:json][timeout:25];"
        f"rel[boundary=administrative][admin_level=4][name=\"{sido_name}\"];"
        "map_to_area->.a;"
        "rel(area.a)[boundary=administrative][admin_level=6][name];"
        "out tags;"
    )
    j = _overpass(q)
    names = sorted({(e.get('tags') or {}).get('name') for e in j.get('elements', []) if (e.get('tags') or {}).get('name')})
    _cache_set(key, names)
    return names

def _list_dong(sido_name: str, sigungu_name: str):
    key = f"dong:{sido_name}:{sigungu_name}"
    cached = _cache_get(key)
    if cached is not None:
        return cached
    # Find area for the given sigungu within the sido, then list admin_level 8/9/10 names
    q = (
        "[out:json][timeout:25];"
        f"rel[boundary=administrative][admin_level=4][name=\"{sido_name}\"];"
        "map_to_area->.sido;"
        f"rel(area.sido)[boundary=administrative][admin_level=6][name=\"{sigungu_name}\"];"
        "map_to_area->.sgg;"
        "rel(area.sgg)[boundary=administrative][admin_level~\"8|9|10\"][name];"
        "out tags;"
    )
    j = _overpass(q)
    names = sorted({(e.get('tags') or {}).get('name') for e in j.get('elements', []) if (e.get('tags') or {}).get('name')})
    _cache_set(key, names)
    return names

def kr_admin(request):
    # Modes:
    #  - GET /pages/api/kr-admin/?level=sido -> [sido]
    #  - GET /pages/api/kr-admin/?sido=서울특별시 -> [sigungu]
    #  - GET /pages/api/kr-admin/?sido=서울특별시&sigungu=강남구 -> [dong]
    level = request.GET.get('level')
    sido = request.GET.get('sido')
    sigungu = request.GET.get('sigungu')

    if level == 'sido' or (not sido and not sigungu):
        return JsonResponse({"level": "sido", "items": _list_sido()})

    if sido and not sigungu:
        items = _list_sigungu(sido)
        return JsonResponse({"level": "sigungu", "sido": sido, "items": items})

    if sido and sigungu:
        items = _list_dong(sido, sigungu)
        return JsonResponse({"level": "dong", "sido": sido, "sigungu": sigungu, "items": items})

    return HttpResponseBadRequest("Invalid parameters")


def board_list(request):
    items = []
    if Board is not None:
        try:
            items = Board.objects.order_by('-created_at')
        except OperationalError:
            items = []
    return render(request, 'board_list.html', {'items': items})
