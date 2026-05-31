# LLM Orchestration — Advanced RAG

LangGraph tabanlı, adaptif yönlendirme ve kalite kontrol mekanizmalarına sahip gelişmiş bir RAG (Retrieval-Augmented Generation) sistemi.

## Mimari

```
Soru
 │
 ▼
[Router] ──── vectorstore? ───▶ [Retrieve] ──▶ [Grade Documents]
    │                                                   │
    └──── websearch? ─────────────────────────▶ [Web Search]
                                                        │
                                              ◀─────────┘
                                         [Generate]
                                              │
                                    [Hallucination Check]
                                    ┌─────────┴──────────┐
                                  useful            not useful
                                    │                    │
                                   END             [Web Search]
```

Graf görselleştirmesi için `graph.png` dosyasına bakabilirsiniz.

## Özellikler

- **Akıllı Yönlendirme**: Soru, vektör veritabanına mı yoksa web aramasına mı gidecek otomatik karar verilir
- **Doküman Kalite Kontrolü**: Alınan belgeler soruyla ilgililik açısından puanlanır
- **Halüsinasyon Tespiti**: Üretilen cevabın belgelere dayalı olup olmadığı kontrol edilir
- **Cevap Kalite Kontrolü**: Cevabın soruyu gerçekten yanıtlayıp yanıtlamadığı değerlendirilir
- **Otomatik Geri Dönüş**: Yetersiz cevaplar web aramasına yönlendirilir

## Kurulum

### Gereksinimler

- Python 3.9+
- OpenAI API anahtarı
- Tavily API anahtarı (web arama için)

### Bağımlılıkları Yükle

```bash
pip install -r requirements.txt
```

### Ortam Değişkenleri

`.env` dosyası oluşturup şu değerleri ekleyin:

```
OPENAI_API_KEY=your_openai_api_key
TAVILY_API_KEY=your_tavily_api_key
```

## Kullanım

### 1. Vektör Veritabanını Oluştur

```bash
python ingestion.py
```

Bu adım web kaynaklarından (LLM ajanları, prompt engineering, adversarial attacks) doküman çekerek Chroma vektör veritabanına yükler.

### 2. Uygulamayı Çalıştır

```bash
python main.py
```

## Proje Yapısı

```
├── main.py                         # Uygulama giriş noktası
├── ingestion.py                    # Doküman yükleme ve vektör DB oluşturma
├── requirements.txt
├── .env                            # API anahtarları (git'e eklenmez)
└── graph/
    ├── graph.py                    # LangGraph iş akışı tanımı
    ├── state.py                    # Graf durum modeli
    ├── node_constants.py           # Node isim sabitleri
    ├── chains/
    │   ├── rooter.py               # Soru yönlendirme zinciri
    │   ├── generation.py           # Cevap üretme zinciri
    │   ├── retrieval_grader.py     # Doküman puanlama zinciri
    │   ├── hallucination_grader.py # Halüsinasyon kontrol zinciri
    │   └── answer_grader.py        # Cevap kalite zinciri
    └── nodes/
        ├── retrieve.py             # Vektör DB'den doküman çekme
        ├── grade_documents.py      # Doküman filtreleme
        ├── generate.py             # Cevap üretme
        └── web_search.py           # Tavily web araması
```

## Vektör Veritabanı Kaynakları

Sistem aşağıdaki konularda eğitilmiş dokümanlara sahiptir:

- [LLM Powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/)
- [Prompt Engineering](https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/)
- [Adversarial Attacks on LLMs](https://lilianweng.github.io/posts/2023-10-25-adv-attack-llm/)

Bu konular dışındaki sorular otomatik olarak web aramasına yönlendirilir.

## Teknolojiler

| Teknoloji | Kullanım |
|-----------|----------|
| LangGraph | Graf tabanlı iş akışı |
| LangChain | LLM zincirleri ve araçlar |
| OpenAI GPT | Dil modeli |
| Chroma | Vektör veritabanı |
| Tavily | Web arama API |
