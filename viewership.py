import json
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt

# 파일 불러오기
with open("live_cleaned_20250518_1716.json", "r", encoding="utf-8") as f:
    data = json.load(f)

df = pd.DataFrame(data)

# 카테고리별 시청자 수 총합
category_view_sum = df.groupby("liveCategoryValue")["concurrentUserCount"].sum().sort_values(ascending=False)
# 시리즈를 딕셔너리로 변환 후 JSON 저장
category_view_sum.to_dict()

with open("category_view_sum2.json", "w", encoding="utf-8") as f:
    json.dump(category_view_sum.to_dict(), f, indent=2, ensure_ascii=False)

print("✅ 'category_view_sum.json' 파일로 저장 완료!")
