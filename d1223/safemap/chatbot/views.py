import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.conf import settings

# requests is optional at runtime (guarded) so the server never crashes because of it.
try:
    import requests
except Exception:
    requests = None

def chat_page(request):
    return render(request, 'chatbot/chat.html')

def _rule_based_reply(msg: str) -> str:
    m = (msg or '').strip()
    low = m.lower()
    if not m:
        return "메시지가 비어있음. 나랑 말 걸어줘 😼"
    if any(x in low for x in ['화재','불','연기','폭발']):
        return "🔥 화재 관련이면: 119 신고가 최우선. 연기 흡입 위험 크면 즉시 대피 + 주변 공유."
    if any(x in low for x in ['폭행','위협','칼','흉기','강도','스토킹']):
        return "🚨 위험하면 즉시 112. 가능하면 안전한 곳으로 이동하고, 시간/장소/특징 메모해둬."
    if any(x in low for x in ['교통','사고','추돌','접촉','차']):
        return "🚗 교통사고면: 1) 2차 사고 방지 2) 부상 확인 3) 필요시 119/112 4) 사진/블랙박스 확보."
    if any(x in low for x in ['분실','도난','지갑','휴대폰']):
        return "🧳 분실/도난이면: 최근 동선 정리 → 분실물 센터/경찰서 문의. 휴대폰이면 통신사 분실신고도 ㄱㄱ."
    return "오케이. 상황을 '언제/어디서/무슨 일이/누가/지금 위험한지' 순서로 말해주면 더 정확히 안내할게."

def _safe_float(v):
    try:
        return float(v)
    except Exception:
        return None

def _places_nearby(lat: float, lng: float, place_type: str, radius_m: int = 1500, limit: int = 5):
    """Google Places API(선택)로 근처 장소 + 영업시간을 조회.
    - API 키 없거나 requests 없으면 error로 반환
    - 외부 호출/파싱 오류도 전부 잡아서 error로 반환
    """
    if not getattr(settings, "GOOGLE_MAPS_API_KEY", ""):
        return {"error": "NO_API_KEY"}
    if requests is None:
        return {"error": "NO_REQUESTS"}

    key = settings.GOOGLE_MAPS_API_KEY
    nearby_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    details_url = "https://maps.googleapis.com/maps/api/place/details/json"

    try:
        r = requests.get(
            nearby_url,
            params={
                "key": key,
                "location": f"{lat},{lng}",
                "radius": radius_m,
                "type": place_type,
                "language": "ko",
            },
            timeout=10,
        )
        data = r.json() if r.ok else {}
    except Exception:
        return {"error": "NETWORK_FAIL"}

    results = (data.get("results") or [])[:limit]
    out = []

    for p in results:
        place_id = p.get("place_id")
        name = p.get("name")
        vicinity = p.get("vicinity") or p.get("formatted_address") or ""
        open_now = None
        if isinstance(p.get("opening_hours"), dict):
            open_now = p["opening_hours"].get("open_now")

        details = {}
        if place_id:
            try:
                d = requests.get(
                    details_url,
                    params={
                        "key": key,
                        "place_id": place_id,
                        "fields": "name,formatted_address,opening_hours,international_phone_number,website,url",
                        "language": "ko",
                    },
                    timeout=10,
                )
                details = d.json().get("result", {}) if d.ok else {}
            except Exception:
                details = {}

        opening = details.get("opening_hours") or {}
        weekday_text = opening.get("weekday_text") or []

        out.append({
            "name": details.get("name") or name or "(이름 없음)",
            "address": details.get("formatted_address") or vicinity or "(주소 없음)",
            "open_now": open_now if open_now is not None else opening.get("open_now"),
            "weekday_text": weekday_text,
            "maps_url": details.get("url"),
            "phone": details.get("international_phone_number"),
            "website": details.get("website"),
        })

    return {"items": out, "raw_status": data.get("status")}

def _format_places(kind_ko: str, payload: dict) -> str:
    err = payload.get("error")
    if err == "NO_API_KEY":
        return (
            f"{kind_ko} 영업시간 검색 기능은 꺼져있어(API 키 없음).\n"
            f"서버 환경변수 GOOGLE_MAPS_API_KEY 설정하면 바로 동작함."
        )
    if err == "NO_REQUESTS":
        return (
            f"{kind_ko} 검색에 필요한 requests 패키지가 없어.\n"
            f"`pip install -r requirements.txt` 하고 다시 실행해줘."
        )
    if err == "NETWORK_FAIL":
        return "지금은 외부 지도 API 호출이 실패했어. 네트워크/키 제한/요금 설정을 확인해줘."

    items = payload.get("items") or []
    if not items:
        return f"근처 {kind_ko}를 못 찾았어. 반경을 늘리거나(기본 1.5km) 다시 시도해봐."

    lines = [f"📍 내 근처 {kind_ko} Top {len(items)}"]
    for i, it in enumerate(items, 1):
        open_now = it.get("open_now")
        status = "영업중" if open_now is True else ("영업종료" if open_now is False else "영업상태 미상")
        lines.append(f"{i}) {it.get('name')} — {status}")
        lines.append(f"   주소: {it.get('address')}")
        wt = it.get("weekday_text") or []
        if wt:
            lines.append(f"   시간: {wt[0]} (요일별 전체는 지도 링크에서)")
        if it.get("phone"):
            lines.append(f"   전화: {it.get('phone')}")
        if it.get("maps_url"):
            lines.append(f"   지도: {it.get('maps_url')}")
    return "\n".join(lines)

@require_POST
def chat_api(request):
    """챗봇 API: 어떤 상황에서도 500 안 나게 방어."""
    try:
        body = json.loads(request.body.decode("utf-8"))
    except Exception:
        body = {}

    msg = (body.get("message") or "").strip()
    low = msg.lower()

    lat = _safe_float(body.get("lat"))
    lng = _safe_float(body.get("lng"))

    wants_near = any(k in low for k in ["근처", "주변", "near"])
    wants_pharmacy = any(k in low for k in ["약국", "pharmacy"])
    wants_hospital = any(k in low for k in ["병원", "hospital"])

    if wants_near and (wants_pharmacy or wants_hospital):
        if lat is None or lng is None:
            return JsonResponse({
                "reply": "내 근처 찾기는 위치가 필요해. 브라우저 위치 허용하고 다시 말해줘 🙏",
                "mode": "places"
            })
        if wants_pharmacy:
            payload = _places_nearby(lat, lng, "pharmacy")
            return JsonResponse({"reply": _format_places("약국", payload), "mode": "places"})
        payload = _places_nearby(lat, lng, "hospital")
        return JsonResponse({"reply": _format_places("병원", payload), "mode": "places"})

    return JsonResponse({"reply": _rule_based_reply(msg), "mode": "rules"})
