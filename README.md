# 🤖 AI Web Intelligence Dashboard

> Manually collecting and analyzing market data across hundreds of product pages takes hours — and sending that data to a cloud API means recurring costs plus privacy risk.
> This dashboard scrapes product data automatically, then analyzes it with an LLM that runs 100% locally on your own GPU, at zero API cost.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red)
![Ollama](https://img.shields.io/badge/Ollama-LLaMA3.1-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

📸 Demo

<img width="1912" height="936" alt="AI Web Intelligence Dashboard" src="https://github.com/user-attachments/assets/4be8105a-df74-4016-bc3a-064fd24a018d" />


## ✨ Features

- **Automated scraping** — extracts 100+ books (title, price, rating, availability) 
  from target website with pagination support
- **Local AI analysis** — each batch analyzed by LLaMA 3.1 8B running 
  on local GPU, generating market themes and business insights
- **Interactive dashboard** — real-time filters by title, rating, and price range
- **Visual analytics** — rating distribution and price range charts
- **One-click Excel export** — download filtered data with AI insights
- **100% private** — no data sent to external APIs, runs entirely on your machine

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Web Scraping | Python, Requests, BeautifulSoup4 |
| AI Analysis | Ollama, LLaMA 3.1 8B (local GPU) |
| Dashboard | Streamlit |
| Data Processing | Pandas |
| Export | OpenPyXL |
| Hardware | NVIDIA RTX 3060 (GPU-accelerated inference) |

---

## 🚀 Installation

**1. Clone the repository**
```bash
git clone https://github.com/sawtrader/ai-web-intelligence-dashboard.git
cd ai-web-intelligence-dashboard
```

**2. Install dependencies**
```bash
pip install streamlit requests beautifulsoup4 pandas tqdm openpyxl
```

**3. Install and run Ollama**

Download Ollama from [ollama.ai](https://ollama.ai), then:
```bash
ollama pull llama3.1:8b
ollama serve
```

**4. Run the dashboard**
```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`

---

## 📖 Usage

1. Open the dashboard in your browser
2. Click **🚀 Run Scraper + AI Analysis** in the sidebar
3. Wait 5–10 minutes for scraping and AI analysis to complete
4. Use filters (title search, rating slider, price range) to explore data
5. Click **⬇️ Download Excel** to export results

---

## 💼 Business Use Cases

- **E-commerce monitoring** — track competitor pricing and product ratings automatically
- **Market research** — identify trending themes and price patterns with AI insights
- **Inventory intelligence** — monitor stock availability across large product catalogs

---

## 📋 Project Structure
ai-web-intelligence-dashboard/

├── scraper.py

├── analyzer.py

├── app.py

└── README.md

---

## 📄 License

MIT License — free to use and modify.

---

*Built with Python + Local LLM | GPU-accelerated on NVIDIA RTX 3060*
