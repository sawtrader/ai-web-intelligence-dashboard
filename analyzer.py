import requests
import json
import pandas as pd
from tqdm import tqdm
import time

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.1:8b"

def check_ollama():
    try:
        requests.get("http://localhost:11434", timeout=5)
        print("✅ Ollama berjalan.")
        return True
    except:
        print("❌ Ollama tidak terdeteksi. Pastikan 'ollama serve' berjalan di terminal lain.")
        return False

def analyze_batch(books_batch):
    books_text = "\n".join([
        f"- '{b['title']}' | Price: £{b['price_gbp']:.2f} | Rating: {b['rating']}/5"
        for b in books_batch
    ])

    prompt = f"""You are a book market analyst. Analyze these {len(books_batch)} books.

Books:
{books_text}

Respond ONLY with valid JSON, no explanation, no markdown:
{{
  "dominant_theme": "main theme in 3-5 words",
  "price_insight": "one sentence about pricing pattern",
  "market_insight": "one actionable business insight",
  "recommended_for": "target reader in 5 words"
}}"""

    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.2, "num_predict": 200}
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=120)
        response.raise_for_status()
        raw = response.json()["response"].strip()

        if "```" in raw:
            raw = raw.split("```")[1].replace("json", "").strip()

        return json.loads(raw)

    except json.JSONDecodeError:
        return {
            "dominant_theme": "Parse error - retry",
            "price_insight": "Could not parse response",
            "market_insight": "Run again to retry",
            "recommended_for": "Unknown"
        }
    except Exception as e:
        return {
            "dominant_theme": "Error",
            "price_insight": str(e)[:80],
            "market_insight": "Check ollama serve is running",
            "recommended_for": "Unknown"
        }

def analyze_all(df, batch_size=10):
    results = []
    total_batches = (len(df) + batch_size - 1) // batch_size
    print(f"Menganalisis {len(df)} buku dalam {total_batches} batch...")
    print(f"Estimasi waktu: {total_batches * 20}-{total_batches * 40} detik\n")

    for i in tqdm(range(0, len(df), batch_size), desc="Analisis AI"):
        batch = df.iloc[i:i + batch_size].to_dict("records")
        analysis = analyze_batch(batch)

        for book in batch:
            results.append({
                **book,
                "ai_theme": analysis.get("dominant_theme", ""),
                "ai_price_insight": analysis.get("price_insight", ""),
                "ai_market_insight": analysis.get("market_insight", ""),
                "ai_recommended_for": analysis.get("recommended_for", "")
            })

        time.sleep(0.5)

    return pd.DataFrame(results)


if __name__ == "__main__":
    if not check_ollama():
        exit(1)

    try:
        df = pd.read_csv("books_raw.csv")
        print(f"📂 Loaded {len(df)} buku dari books_raw.csv\n")
    except FileNotFoundError:
        print("❌ books_raw.csv tidak ditemukan. Jalankan scraper.py dulu!")
        exit(1)

    df_result = analyze_all(df, batch_size=10)

    df_result.to_csv("books_analyzed.csv", index=False)

    print(f"\n✅ Selesai! {len(df_result)} buku berhasil dianalisis.")
    print(f"💾 Hasil disimpan ke books_analyzed.csv")
    print(f"\nContoh output AI untuk buku pertama:")
    print(f"  Tema    : {df_result.iloc[0]['ai_theme']}")
    print(f"  Insight : {df_result.iloc[0]['ai_market_insight']}")