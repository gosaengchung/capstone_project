import requests
import json
import schedule
import time
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

url = "https://openapi.chzzk.naver.com/open/v1/lives"
headers = {
    "Client-Id": CLIENT_ID,
    "Client-Secret": CLIENT_SECRET,
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0"
}

def fetch_all_lives():
    all_lives = []
    next_cursor = None
    page_count = 0

    while page_count < 50:
        params = {"size": 20}
        if next_cursor:
            params["next"] = next_cursor

        res = requests.get(url, headers=headers, params=params)
        print(f"\n📡 요청 {page_count + 1}페이지 | Status: {res.status_code}")

        if res.status_code == 200:
            try:
                data = res.json()

                # ✅ 방송 목록 수집
                content = data.get("content", {})
                lives = content.get("data", [])
                print(f"📦 수집된 방송 수: {len(lives)}개")
                all_lives.extend(lives)

                # ✅ 다음 페이지 커서
                next_cursor = content.get("page", {}).get("next")
                if not next_cursor:
                    print("🚫 다음 페이지 없음")
                    break

            except ValueError as e:
                print("❌ JSON 파싱 오류:", e)
                break

        else:
            print(f"❌ 요청 실패: {res.status_code}")
            break

        page_count += 1
        time.sleep(0.1)

    print(f"\n✅ 최종 수집된 방송 수: {len(all_lives)}개")
    return all_lives

def save_lives():
    result = fetch_all_lives()
    if result:
        now_str = datetime.now().strftime("%Y%m%d_%H%M")
        filename = f"live_channels_all_{now_str}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"📁 저장 완료: {filename}")
    else:
        print("⚠️ 저장할 방송 데이터가 없습니다.")

def filter_lives(data):
    return [
        {
            "channelName": d.get("channelName"),
            "liveTitle": d.get("liveTitle"),
            "concurrentUserCount": d.get("concurrentUserCount"),
            "liveCategoryValue": d.get("liveCategoryValue"),
            "openDate": d.get("openDate"),
            "tags": d.get("tags"),
            "channelId": d.get("channelId"),
            "liveId": d.get("liveId")
        }
        for d in data
    ]

def save_to_json(data):
    now_str = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"live_cleaned_{now_str}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"📁 저장 완료: {filename}")

def run_job():
    raw = fetch_all_lives()
    filtered = filter_lives(raw)
    save_to_json(filtered)

if __name__ == "__main__":
    run_job()
