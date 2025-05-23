import json
import pandas as pd
from collections import Counter
from itertools import chain
import matplotlib.pyplot as plt

# 파일 불러오기
with open("live_cleaned_20250518_1716.json", "r", encoding="utf-8") as f:
    data = json.load(f)

df = pd.DataFrame(data)

df_sorted = df.sort_values(by="concurrentUserCount", ascending=False)
top_200 = df_sorted.head(200)
bottom_200 = df_sorted.tail(200)



# 상/하위 방송의 주요 특징 요약 함수
def summarize_group(group_df):
    return {
        "avg_viewers": int(group_df["concurrentUserCount"].mean()),
        "top_categories": group_df["liveCategoryValue"].value_counts().head(5).to_dict(),
        "top_tags": dict(Counter(chain.from_iterable(group_df["tags"])).most_common(10))
    }

summary = {
    "top_200_summary": summarize_group(top_200),
    "bottom_200_summary": summarize_group(bottom_200)
}

# 저장
with open("broadcast_group_summary.json", "w", encoding="utf-8") as f:
    json.dump(summary, f, indent=2, ensure_ascii=False)

print("✅ 상하위 방송 요약 broadcast_group_summary.json 저장 완료!")