# datascience_template

Bu proje şablonu, veri bilimi projeleri için tipik bir klasör yapısı içerir.

## Klasör Yapısı

```
project_name/  # Proje kök dizini
│
├── data/  # Veri dosyalarını içeren klasör
│   ├── raw/  # İşlenmemiş veri dosyalarını içeren klasör
│   │   └── raw_data.csv  # İşlenmemiş veri dosyası (örneğin: kaynak veri)
│   ├── processed/  # İşlenmiş veri dosyalarını içeren klasör
│   │   └── processed_data.csv  # İşlenmiş veri dosyası (örneğin: ön işlenmiş veri)
│   └── external/  # Harici veri kaynaklarını içeren klasör
│       └── external_data.csv  # Harici veri dosyası (örneğin: internetten indirilen veri)
│
├── notebooks/  # Jupyter not defterlerini içeren klasör
│   ├── exploratory_analysis.ipynb  # Keşifsel veri analizi not defteri
│   ├── data_preprocessing.ipynb  # Veri ön işleme not defteri
│   └── modeling.ipynb  # Modelleme not defteri
│
├── src/  # Python betiklerini içeren klasör
│   ├── data/  # Veri işleme betiklerini içeren alt klasör
│   │   ├── load_data.py  # Veriyi yükleme betiği
│   │   └── preprocess_data.py  # Veriyi ön işleme betiği
│   ├── features/  # Özellik çıkarma betiklerini içeren alt klasör
│   │   └── feature_engineering.py  # Özellik mühendisliği betiği
│   ├── models/  # Modelleme betiklerini içeren alt klasör
│   │   └── train_model.py  # Model eğitim betiği
│   └── evaluation/  # Değerlendirme betiklerini içeren alt klasör
│       └── evaluate_model.py  # Model değerlendirme betiği
│   └── utils/  # Yardımcı işlevleri içeren alt klasör
│       └── helpers.py  # Genel amaçlı yardımcı fonksiyonlar betiği
│   └── main.py  # Ana giriş noktası betiği
│
├── visualization/  # Veri görselleştirme betiklerini içeren klasör
│   └── visualize_data.py  # Veri görselleştirme betiği
│
├── tests/  # Test betiklerini içeren klasör
│   ├── test_data.py  # Veri işleme betikleri için test betiği
│   └── test_models.py  # Modelleme betikleri için test betiği
│
└── README.md  # Proje açıklaması ve kullanım kılavuzu dosyası
```


