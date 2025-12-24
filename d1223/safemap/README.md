# SafeMap (홈페이지형 MVP)

## 기능
- 메인 홈페이지(랜딩) + 서비스 소개 페이지
- 회원가입/로그인/로그아웃/프로필
- 사건·사고 제보 등록(로그인 필요)
- 제보 저장 시 자동 요약/분류/위험도(룰 기반 MVP)
- 지도 화면(Leaflet + OSM)에서 최근 7일/30일 필터로 마커 표시
- 안전 챗봇(룰 기반 MVP, API 엔드포인트 포함)

## 실행
```bash
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## URL
- / : 홈
- /about/ : 소개
- /reports/map/ : 지도
- /reports/new/ : 제보 등록
- /chat/ : 챗봇
- /accounts/signup/ : 회원가입
- /accounts/login/ : 로그인


## 내 근처 약국/병원(챗봇)
- 옵션 기능: Google Places API 키가 있으면 근처 약국/병원 + 영업시간을 보여줍니다.
- 키가 없거나 외부 호출이 실패해도 서버는 절대 안 터지고 안내만 합니다.
- Windows PowerShell 예시:
```powershell
$env:GOOGLE_MAPS_API_KEY="YOUR_KEY"
python manage.py runserver
```

## 실행(필수)
반드시 `manage.py`가 있는 폴더에서 실행하세요.

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## 로그인/회원가입이 “안 되는 것처럼 보일 때”
- 사실은 로그인 성공 후 이동한 페이지(/)에서 DB migrate가 안 되어 오류가 나는 경우가 많아요.
- 이 템플릿은 홈에서 DB가 없으면 0으로 표시하도록 방어처리 했습니다.
- 그래도 기본은 `python manage.py migrate`가 정답입니다.


## 지도 지역 필터(bbox)
- 지도에서 지역 선택 시 `/reports/api/list/?days=7&bbox=minLng,minLat,maxLng,maxLat` 형태로 해당 지역 데이터만 로딩합니다.


## 제보 등록: 지도에서 위치 선택
- 위도/경도 입력은 숨김 처리됨.
- 지도 클릭 또는 주소 검색으로 위치 선택 → 주소(시/구/동) 자동 채움.
- 적용 후 `python manage.py migrate` 필수.


## 상태값(필수)
- Report 상태: 접수됨 / 처리중 / 완료 (색상 배지로 표시)
- 관리자 페이지: `/admin/` 에서 상태 변경 가능(일괄 변경 액션 포함)
- 적용 후 `python manage.py migrate` 필수.
