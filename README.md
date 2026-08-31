# AI Plant Doctor (AI پਲਾਂټ ډاکټر / اے آئی پلانٹ ڈاکٹر)

A production-oriented Computer Vision platform for plant health monitoring, disease classification, U-Net lesion segmentation, severity estimation, RAG AI Assistant, and multi-lingual crop care recommendations.

---

## 🌟 Key Features

- 🔬 **Dual-Head PyTorch AI Engine**: 
  - **Plant Disease Classification**: ResNet backbone classifying disease types across major crops.
  - **Lesion Segmentation**: Decoupled U-Net architecture predicting precise pixel-level leaf infection masks.
  - **Configurable Severity Estimation**: Automated calculation of infected leaf area percentage with tolerance thresholding.
- 📈 **Plant Monitoring & Health Progression**:
  - Repeated scanning against plant profiles (`GET /api/plants/{id}/scans`, `GET /api/plants/{id}/progress`).
  - Side-by-side Before/After scan comparison and visual lesion coverage trend charts.
  - Progression classification (`Improving`, `Worsening`, `Stable`, `Insufficient Data`).
- 🔔 **Monitoring Notifications & Safety Safeguards**:
  - Non-alarming photo quality tips on low-confidence predictions ($<60\%$).
  - High-priority worsening trend alerts.
  - Customizable quiet hours and reminder frequencies (`Daily`, `Weekly`, `Bi-weekly`).
- 🤖 **RAG-Driven AI Plant Health Assistant**:
  - 5-step RAG pipeline retrieving current diagnosis, plant history, and verified knowledge base.
  - Enforced safety guardrails against inventing unverified chemical pesticide doses.
- 🌐 **Multi-Lingual Support**: Native support for **English (`en`)**, **Urdu (`ur`)**, and **Pashto (`ps`)** with Right-to-Left (RTL) layout switching while preserving scientific names (*Alternaria solani*) and safety rules.
- 📊 **Admin Dashboard**: System analytics, low-confidence rate monitoring, user account management, model version control, and security audit logs.

---

## 📁 Repository Architecture

```
AI_Plant_Doctor/
├── mobile/             # Flutter + Dart Material 3 App (Mobile/Web)
│   ├── lib/            # Clean Architecture (Core, Features, l10n, Providers)
│   └── pubspec.yaml
├── backend/            # FastAPI REST API Backend
│   ├── app/            # Routers, Services, Schemas, Core
│   └── requirements.txt
├── ai/                 # PyTorch Computer Vision Pipeline
│   ├── dataset/        # Data loader & augmentation
│   ├── models/         # ResNet Classifier & U-Net Segmentor
│   ├── training/       # PyTorch Training Loop & Checkpoints
│   ├── evaluation/     # Metrics (F1, Precision, Confusion Matrix)
│   ├── segmentation/   # Decoupled U-Net Lesion Pipeline
│   ├── severity.py     # Configurable Severity Engine
│   └── pipeline.py     # Unified AI Engine Singleton
├── database/           # Database Setup & Migrations
│   ├── models/         # SQLAlchemy ORM Models (User, Plant, PlantScan, Disease, AuditLog)
│   ├── alembic/        # Database Migrations
│   └── seeds/          # Multi-lingual Knowledge Base Seed Data
├── admin/              # Admin Dashboard Web Client (index.html)
├── tests/              # Test Suite (Backend, AI, Frontend)
├── docker-compose.yml  # Docker Container Setup
├── .env.example        # Environment Variables Template
└── README.md
```

---

## ⚙️ Clean Installation & Setup Instructions

### Prerequisites
- **Python**: 3.11+
- **Flutter SDK**: 3.19+ / 3.44+
- **Database**: PostgreSQL (or automatic fallback to local SQLite `plant_doctor.db`)

### 1. Environment Configuration

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Ensure `.env` contains your target database connection string, storage configuration (`STORAGE_TYPE=local` or `STORAGE_TYPE=s3`), and model paths.

---

### 2. Database Setup & Migration Instructions

Install backend dependencies and run Alembic migrations / seed scripts:

```bash
cd backend
python -m venv venv

# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt

# Run database migrations
alembic upgrade head

# Seed multi-lingual knowledge base (EN, UR, PS)
python -m database.seeds.seed_data
```

---

### 3. PyTorch Model Setup & Training Instructions

Model weights (`.pt`) are automatically managed via the `ModelLoader` singleton in `backend/app/services/model_loader.py`.

To train custom PyTorch classification weights on your dataset (e.g., PlantVillage):

```bash
# Train PyTorch disease classifier
python -m ai.training.trainer --dataset_dir path/to/dataset --epochs 25 --batch_size 32

# Evaluate model performance & generate metrics (JSON, Confusion Matrix)
python -m ai.evaluation.evaluator --weights ai/weights/best_model.pt
```

---

### 4. Running Backend Server

Start the FastAPI application:

```bash
# From AI_Plant_Doctor root directory
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

FastAPI Interactive OpenAPI Docs are available at: `http://localhost:8000/docs`

---

### 5. Flutter Mobile / Web App Instructions

```bash
cd mobile

# Install Flutter dependencies
flutter pub get

# Generate localizations (English, Urdu, Pashto)
flutter gen-l10n

# Run on Web Chrome
flutter run -d chrome

# Run on Android / iOS Emulator
flutter run
```

#### Build Instructions:

```bash
# Build Android APK
flutter build apk --release

# Build Android App Bundle
flutter build appbundle --release

# Build Web Version
flutter build web --release
```

---

## 📡 API Documentation Summary

| Endpoint | Method | Description |
| :--- | :---: | :--- |
| `/api/v1/auth/register` | `POST` | User registration |
| `/api/v1/auth/login` | `POST` | User login & JWT token generation |
| `/api/diagnosis/analyze` | `POST` | Image upload $\rightarrow$ CV inference $\rightarrow$ Severity estimation |
| `/api/diagnosis/history` | `GET` | Scan history search & filtering |
| `/api/plants` | `GET / POST` | User plant profiles CRUD |
| `/api/plants/{id}/scans` | `GET` | Plant monitoring scan timeline |
| `/api/plants/{id}/progress` | `GET` | Disease progression analytics & trend |
| `/api/v1/notifications/settings` | `GET / PUT` | Notification preferences & quiet hours |
| `/api/v1/assistant` | `POST` | RAG AI Plant Health Assistant |
| `/api/v1/admin/metrics` | `GET` | Admin dashboard analytics |
| `/api/v1/admin/models` | `GET` | AI model status & evaluation metrics |
| `/api/v1/admin/audit-logs` | `GET` | Security audit trail logs |

---

## 🧪 Testing Instructions

Run the automated unittest suite (18 test suites covering backend API, PyTorch inference, U-Net segmentation, severity engine, RAG assistant, and admin security):

```bash
# Run backend & AI pipeline test suite
python -m unittest discover -s tests

# Run Flutter static analyzer
cd mobile
flutter analyze
```

---

## 🚢 Docker Deployment Instructions

Deploy the complete PostgreSQL + FastAPI container stack via Docker Compose:

```bash
docker-compose up --build -d
```

---

## 🌐 Multilingual Matrix

| Language | Code | Text Direction | Status |
| :--- | :---: | :---: | :---: |
| **English** | `en` | Left-to-Right (LTR) | Fully Supported |
| **Urdu (اردو)** | `ur` | Right-to-Left (RTL) | Fully Supported |
| **Pashto (پښتو)** | `ps` | Right-to-Left (RTL) | Fully Supported |

---

## 🛡️ License

Distributed under the MIT License. See `LICENSE` for details.
