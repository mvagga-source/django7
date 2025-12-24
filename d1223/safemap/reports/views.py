from django.db.models import Count
from django.db.models.functions import TruncDate
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db.utils import OperationalError
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta

from .models import Report
from .forms import ReportForm
from .services import classify_category, risk_score, one_line_summary

def map_view(request):
    return render(request, 'reports/map.html')

@login_required
def new_report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user

            # AI-ish auto fields (MVP heuristic)
            text = f"{obj.title} {obj.content}"
            cat = classify_category(text)
            risk = risk_score(cat, text)
            obj.category = cat
            obj.risk = risk
            obj.summary = one_line_summary(obj.title, cat, risk, obj.content)

            obj.save()
            messages.success(request, "제보가 등록됐어. 지도에서 확인 ㄱㄱ ✅")
            return redirect('reports:detail', pk=obj.pk)
        messages.error(request, "입력값을 확인해줘.")
    else:
        form = ReportForm()
    return render(request, 'reports/new.html', {'form': form})

@login_required
def my_reports(request):
    try:
        qs = Report.objects.filter(user=request.user).order_by('-created_at')
    except OperationalError:
        qs = []
    return render(request, 'reports/my.html', {'items': qs})

def detail(request, pk):
    obj = get_object_or_404(Report, pk=pk)
    return render(request, 'reports/detail.html', {'item': obj})

def api_list(request):
    """Return list of reports; supports days and bbox (minLng,minLat,maxLng,maxLat). Never 500."""
    days = int(request.GET.get('days', '7'))
    bbox = request.GET.get('bbox')
    now = timezone.now()
    try:
        qs = Report.objects.filter(created_at__gte=now - timedelta(days=days)).order_by('-created_at')

        if bbox:
            try:
                min_lng, min_lat, max_lng, max_lat = [float(x) for x in bbox.split(',')]
                qs = qs.filter(lat__gte=min_lat, lat__lte=max_lat, lng__gte=min_lng, lng__lte=max_lng)
            except Exception:
                pass

        qs = qs[:500]
        data = []
        for r in qs:
            data.append({
                'id': r.id,
                'title': r.title,
                'summary': (r.summary or ''),
                'category': r.category,
                'risk': r.risk,
            'status': getattr(r, 'status', 'received'),
            'status_label': dict(getattr(Report, 'STATUS_CHOICES', [('received','접수됨'),('processing','처리중'),('done','완료')])).get(getattr(r,'status','received'),'접수됨'),
                'lat': r.lat,
                'lng': r.lng,
                'happened_at': r.happened_at.isoformat(),
                'detail_url': f"/reports/{r.id}/",
            'address_text': getattr(r, 'address_text', ''),
            'sido': getattr(r, 'sido', ''),
            'sigungu': getattr(r, 'sigungu', ''),
            'dong': getattr(r, 'dong', ''),
            })
        return JsonResponse({'count': len(data), 'items': data})
    except OperationalError:
        return JsonResponse({'count': 0, 'items': [], 'warning': 'db_not_ready'})

def api_stats(request):
    """Return lightweight stats for charts. Supports days and bbox. Never 500."""
    days = int(request.GET.get('days', '30'))
    bbox = request.GET.get('bbox')
    now = timezone.now()
    start = now - timedelta(days=days)

    try:
        qs = Report.objects.filter(created_at__gte=start)

        if bbox:
            try:
                min_lng, min_lat, max_lng, max_lat = [float(x) for x in bbox.split(',')]
                qs = qs.filter(lat__gte=min_lat, lat__lte=max_lat, lng__gte=min_lng, lng__lte=max_lng)
            except Exception:
                pass

        daily = (qs.annotate(d=TruncDate('created_at'))
                   .values('d')
                   .annotate(c=Count('id'))
                   .order_by('d'))

        daily_labels = [str(x['d']) for x in daily]
        daily_counts = [x['c'] for x in daily]

        cat = (qs.values('category')
                 .annotate(c=Count('id'))
                 .order_by('-c'))
        cat_labels = [x['category'] for x in cat]
        cat_counts = [x['c'] for x in cat]

        risks = list(qs.values_list('risk', flat=True))
        risk_avg = round(sum(risks)/len(risks), 2) if risks else 0

        return JsonResponse({
            "days": days,
            "daily": {"labels": daily_labels, "counts": daily_counts},
            "categories": {"labels": cat_labels, "counts": cat_counts},
            "risk_avg": risk_avg,
        })
    except OperationalError:
        return JsonResponse({
            "days": days,
            "daily": {"labels": [], "counts": []},
            "categories": {"labels": [], "counts": []},
            "risk_avg": 0,
            "warning": "db_not_ready"
        })
