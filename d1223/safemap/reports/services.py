import re

CATEGORY_KEYWORDS = {
    'traffic': ['교통', '사고', '추돌', '접촉', '충돌', '차', '오토바이', '자전거', '신호', '횡단보도', '급정거'],
    'violence': ['폭행', '칼', '흉기', '위협', '싸움', '폭력', '난동', '강도', '성추행', '스토킹'],
    'fire': ['화재', '불', '연기', '폭발', '타는', '불길', '소방'],
    'lost': ['분실', '도난', '훔', '잃어', '지갑', '휴대폰', '가방', '열쇠'],
}

def classify_category(text: str) -> str:
    t = text.lower()
    scores = {k:0 for k in CATEGORY_KEYWORDS}
    for cat, kws in CATEGORY_KEYWORDS.items():
        for kw in kws:
            if kw in t:
                scores[cat] += 1
    best = max(scores.items(), key=lambda x: x[1])
    return best[0] if best[1] > 0 else 'etc'

def risk_score(category: str, text: str) -> int:
    t = text.lower()
    base = {'violence':4, 'fire':5, 'traffic':3, 'lost':2, 'etc':1}.get(category, 1)
    if any(x in t for x in ['사망', '중상', '피', '의식', '대형', '다수']):
        base = min(5, base + 1)
    if any(x in t for x in ['경미', '가벼운', '작은']):
        base = max(1, base - 1)
    return int(max(1, min(5, base)))

def one_line_summary(title: str, category: str, risk: int, text: str) -> str:
    # crude but effective MVP summary
    snippet = re.sub(r'\s+', ' ', text.strip())
    snippet = snippet[:60] + ('…' if len(snippet) > 60 else '')
    cat_ko = {'traffic':'교통사고','violence':'폭력/위협','fire':'화재/연기','lost':'분실/도난','etc':'기타'}.get(category,'기타')
    return f"[{cat_ko} | 위험도 {risk}] {title} - {snippet}"
