import streamlit as st
import pandas as pd
import requests
import io
import os

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="AI Web Intelligence Dashboard",
    page_icon="🤖",
    layout="wide"
)

# --- HELPER FUNCTIONS ---
def is_ollama_running():
    try:
        requests.get("http://localhost:11434", timeout=5)
        return True
    except:
        return False

def run_pipeline():
    progress_text = st.empty()
    progress_bar = st.progress(0)

    progress_text.text("Step 1/2: Scraping books.toscrape.com...")
    progress_bar.progress(10)
    from scraper import scrape_books
    df_raw = scrape_books(max_pages=5)
    df_raw.to_csv("books_raw.csv", index=False)
    progress_text.text(f"✅ Step 1 selesai — {len(df_raw)} buku ter-scrape")
    progress_bar.progress(50)

    progress_text.text("Step 2/2: AI menganalisis data... (tunggu 3-8 menit)")
    from analyzer import analyze_all
    df_analyzed = analyze_all(df_raw, batch_size=10)
    df_analyzed.to_csv("books_analyzed.csv", index=False)
    progress_bar.progress(100)
    progress_text.text("✅ Selesai! Data siap ditampilkan.")
    return df_analyzed

def apply_rating_color(series):
    colors = []
    for v in series:
        if v >= 4:
            colors.append("background-color: #d4edda; color: #155724")
        elif v == 3:
            colors.append("background-color: #fff3cd; color: #856404")
        else:
            colors.append("background-color: #f8d7da; color: #721c24")
    return colors

# --- HEADER ---
st.title("🤖 AI Web Intelligence Dashboard")
st.caption("Automated web scraper + Local LLM analysis | RTX 3060 GPU | Zero cloud API costs")
st.divider()

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Controls")

    if is_ollama_running():
        st.success("Ollama: Running ✅")
    else:
        st.error("Ollama: Not detected ❌")
        st.caption("Jalankan 'ollama serve' di terminal lain dulu")

    st.divider()

    run_btn = st.button(
        "🚀 Run Scraper + AI Analysis",
        use_container_width=True,
        disabled=not is_ollama_running()
    )

    st.divider()
    st.header("🔍 Filters")
    search_query = st.text_input("Search title", placeholder="Ketik judul buku...")
    rating_range = st.slider("Rating", 1, 5, (1, 5))
    max_price = st.slider("Max price (£)", 10, 60, 60)

# --- JALANKAN PIPELINE ---
if run_btn:
    df_result = run_pipeline()
    st.session_state["df"] = df_result

# --- LOAD DATA ---
if "df" in st.session_state:
    df = st.session_state["df"]
elif os.path.exists("books_analyzed.csv"):
    df = pd.read_csv("books_analyzed.csv")
else:
    df = None

# --- TAMPILKAN DASHBOARD ---
if df is not None:

    # Apply filters
    filtered = df.copy()
    if search_query:
        filtered = filtered[
            filtered["title"].str.contains(search_query, case=False, na=False)
        ]
    filtered = filtered[
        (filtered["rating"] >= rating_range[0]) &
        (filtered["rating"] <= rating_range[1]) &
        (filtered["price_gbp"] <= max_price)
    ]

    # METRICS
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("📚 Total Books", len(filtered))
    m2.metric("💷 Avg Price", f"£{filtered['price_gbp'].mean():.2f}")
    m3.metric("⭐ Avg Rating", f"{filtered['rating'].mean():.1f} / 5")
    in_stock = len(filtered[filtered["availability"].str.contains("In stock", na=False)])
    m4.metric("✅ In Stock", in_stock)

    st.divider()

    # CHARTS
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("⭐ Rating Distribution")
        rating_counts = (
            filtered["rating"]
            .value_counts()
            .sort_index()
            .rename_axis("Rating")
            .reset_index(name="Count")
            .set_index("Rating")
        )
        st.bar_chart(rating_counts)

    with col_right:
        st.subheader("💷 Price Range")
        def categorize_price(p):
            if p < 20: return "Budget (< £20)"
            elif p < 40: return "Mid (£20–40)"
            else: return "Premium (> £40)"
        price_dist = filtered["price_gbp"].apply(categorize_price).value_counts()
        st.bar_chart(price_dist)

    st.divider()

    # TABLE
    st.subheader(f"📋 Books Data ({len(filtered)} results)")

    display_df = filtered[
        ["title", "price_gbp", "rating", "availability", "ai_theme", "ai_market_insight"]
    ].copy()
    display_df.columns = ["Title", "Price (£)", "Rating", "Availability", "AI Theme", "AI Insight"]

    styled_df = display_df.style.apply(apply_rating_color, subset=["Rating"])
    st.dataframe(styled_df, use_container_width=True, height=450)

    st.divider()

    # DOWNLOAD EXCEL
    col_btn, col_info = st.columns([1, 3])
    with col_btn:
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            filtered.to_excel(writer, index=False, sheet_name="Books Data")
        st.download_button(
            label="⬇️ Download Excel",
            data=buffer.getvalue(),
            file_name="books_intelligence_report.xlsx",
            mime="application/vnd.ms-excel",
            use_container_width=True
        )
    with col_info:
        st.caption(f"Export {len(filtered)} buku beserta AI analysis ke file Excel.")

else:
    # EMPTY STATE
    st.info("👆 Klik **Run Scraper + AI Analysis** di sidebar untuk mulai.")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### 🕸️ Web Scraping")
        st.write("Otomatis scrape 100+ buku dari books.toscrape.com — harga, rating, ketersediaan.")
    with col2:
        st.markdown("### 🤖 Local AI")
        st.write("LLM lokal (llama3.1:8b) analisis tiap batch buku, hasilkan market insight.")
    with col3:
        st.markdown("### 📊 Dashboard")
        st.write("Filter interaktif, visualisasi, dan export Excel satu klik.")