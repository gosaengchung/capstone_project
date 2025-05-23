import json
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
# 파일 불러오기
with open("live_cleaned_20250518_1716.json", "r", encoding="utf-8") as f:
    data = json.load(f)

df = pd.DataFrame(data)

from itertools import chain

# 태그 추출 및 개수 세기
all_tags = list(chain.from_iterable(df["tags"]))
tag_counter = Counter(all_tags)
top_50_tags = tag_counter.most_common(50)

# JSON 형태로 저장
with open("top_50_tags2.json", "w", encoding="utf-8") as f:
    json.dump(top_50_tags, f, indent=2, ensure_ascii=False)

print("✅ 인기 태그 top_50_tags2.json 저장 완료!")