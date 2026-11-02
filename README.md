# AI-Powered Email/SMS Spam Detection System
### Production-Quality AIML Mini Project — Cybersecurity Threat Defense Engine

[![Python Version](https://img.shields.io/badge/Python-3.14%2B-blue.svg)](https://www.python.org/)
[![Frontend](https://img.shields.io/badge/Frontend-React%20%2B%20Vite%20%7C%20Streamlit-8B35F6.svg)](https://vitejs.dev/)
[![Backend](https://img.shields.io/badge/API-FastAPI%20ASGI-009688.svg)](https://fastapi.tiangolo.com/)
[![Deployment](https://img.shields.io/badge/Deploy-Vercel%20%7C%20Streamlit%20Cloud-black.svg)](https://vercel.com/)
[![Machine Learning](https://img.shields.io/badge/ML-Scikit--Learn-F7931E.svg)](https://scikit-learn.org/)
[![Database](https://img.shields.io/badge/Storage-SQLite3-003B57.svg)](https://www.sqlite.org/)
[![Tests](https://img.shields.io/badge/Tests-32%20Passing-20C997.svg)](https://pytest.org/)
[![License](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)

---

## 🚀 Vercel Deployment Architecture & Fix

### The Root Cause of `[PYTHON_ENTRYPOINT_NOT_FOUND]`
When deploying Python repositories on Vercel, the `@vercel/python` serverless builder automatically inspects the repository root. If it discovers `requirements.txt` and `app.py`, Vercel assumes `app.py` is an ASGI/WSGI serverless function and expects it to export a top-level `app`, `application`, or `handler` variable.

Because the original project is a **Streamlit application**, `app.py` runs a continuous WebSocket event loop (`streamlit run app.py`) and does not export an ASGI handler. Streamlit cannot run directly as a stateless Vercel Serverless Function.

### The Solution: Production Dual Architecture
Rather than hacking `app.py` with dummy variables or deleting Streamlit, this repository adopts a **Dual-Deployment Architecture**:

1. **Vercel Serverless Architecture (React + FastAPI):**
   - **Backend:** `api/index.py` exports a top-level ASGI `app = FastAPI(...)` serverless endpoint that reuses the exact same trained scikit-learn models (`models/spam_model.pkl`, `models/vectorizer.pkl`) and preprocessing logic.
   - **Frontend:** A high-performance React 18 SPA built with Vite in `web/` (compiling to `dist/`) adhering strictly to the premium dark-purple cybersecurity SaaS design system.
   - **Routing:** `vercel.json` maps `/api/(.*)` to `api/index.py` and serves the static frontend from `dist/`.
   - **Vercel Ignore:** `.vercelignore` prevents Vercel's Python builder from scanning `app.py`, `views/`, and `tests/`.

2. **Streamlit Community Cloud Architecture:**
   - The full, interactive Streamlit application (`app.py`, `views/`) is **100% preserved**.
   - Running `streamlit run app.py` continues to execute the multi-page Streamlit application locally or on Streamlit Community Cloud.

---

---

## 1. Project Introduction
The **AI-Powered Email/SMS Spam Detection System** is an enterprise-grade cybersecurity application engineered to classify incoming electronic mail and Short Message Service (SMS) transmissions in real-time. Designed with a modern dark navy and purple glassmorphic interface, the system leverages Natural Language Processing (NLP) feature extraction pipelines combined with a **Multinomial Naive Bayes (MNB)** statistical classifier to intercept unwanted commercial advertisements, advance-fee frauds, credential phishing attempts, lottery scams, and malicious URLs.

Unlike superficial prototypes, this application is backed by an end-to-end machine learning pipeline, persistent SQLite telemetry, rigorous train/test evaluation on canonical datasets, and explainable heuristic threat signals.

---

## 2. Problem Statement
Electronic messaging represents the backbone of modern personal and corporate collaboration. However, the open nature of email protocols (SMTP) and cellular SMS gateways has resulted in massive threat vectors:
- **Financial Fraud & Scams:** Fake lottery prizes, deceptive loan offers, and impersonation extortion schemes.
- **Credential Harvesting (Phishing):** Spoofed banking alerts prompting users to submit credentials on fraudulent login portals.
- **Productivity Drain:** Legitimate inboxes inundated with unsolicited bulk promotions.

Traditional static keyword filters fail because cybercriminals bypass rigid rules using homoglyphs, deliberate typos (`c@sh`, `fr33`), and conversational disguises. Conversely, overly strict rules flag legitimate business invoices as spam. An intelligent, probabilistic NLP solution is required to evaluate contextual word co-occurrences and class likelihoods.

---

## 3. Project Objectives
1. **Automated Probabilistic Classification:** Classify user-submitted text as `SPAM` or `NOT SPAM (HAM)` using an empirical machine learning model rather than hardcoded rules.
2. **Dual-Channel Flexibility:** Support both short-form SMS messages and structured emails (Subject + Sender + Body).
3. **High-Throughput Batch Processing:** Enable bulk CSV uploads with automatic column mapping, vectorized inference, and CSV export.
4. **Transparent Explainability & Security:** Expose heuristic threat triggers (urgency cues, prize terms, shortcodes, link shorteners) alongside model probabilities while providing clear disclaimers that HAM classification is not a blanket guarantee of security.
5. **Auditable Local Telemetry:** Store classification metadata in SQLite with configurable privacy controls (zero-content retention mode).
6. **Academic Rigor:** Display genuine, un-fabricated test-set evaluation metrics (Accuracy, Precision, Recall, F1, ROC-AUC, and Confusion Matrix).

---

## 4. System Architecture

```
[ Incoming SMS / Email / CSV ]
               │
               ▼
┌──────────────────────────────────────────────┐
│       1. Text Preprocessing Engine           │
│  - Unicode NFKC normalization                │
│  - HTML tag stripping                        │
│  - Regex tokenization (URL, Email, Phone, £) │
│  - Case folding & whitespace trimming        │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│       2. Feature Extraction Pipeline         │
│  - Sublinear TF-IDF / CountVectorizer        │
│  - N-gram Range: (1, 2) [Unigram + Bigram]   │
│  - Vocabulary Dimension: 5,000 features      │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│     3. Multinomial Naive Bayes Model         │
│  - Laplace Smoothing (α = 0.1)               │
│  - Posterior Class Probability Calculation   │
└──────────────┬───────────────────────────────┘
               │
      ┌────────┴──────────────────────────┐
      ▼                                   ▼
┌────────────────────────┐      ┌───────────────────────────┐
│ 4. Heuristic Analyzer  │      │ 5. SQLite Audit History   │
│  - Urgency triggers    │      │  - Timestamp, Channel     │
│  - Financial lures     │      │  - Prediction, Confidence │
│  - Actionable advice   │      │  - Zero-retention option  │
└─────────────┬──────────┘      └─────────────┬─────────────┘
              │                               │
              └───────────────┬───────────────┘
                              │
                              ▼
┌───────────────────────────────────────────────────────────┐
│        6. Streamlit Cybersecurity UI Design System        │
│  - Dark Navy & Purple Glassmorphic Interface              │
│  - Interactive Plotly Visualizations & Live Gauges        │
└───────────────────────────────────────────────────────────┘
```

---

## 5. Machine Learning Methodology

### Mathematical Formulation
The classifier models message categories $y \in \{\text{SPAM}, \text{HAM}\}$ given a document feature vector $\mathbf{x} = (x_1, x_2, \dots, x_n)$ via **Bayes' Theorem**:

$$P(y \mid \mathbf{x}) = \frac{P(y) \cdot P(\mathbf{x} \mid y)}{P(\mathbf{x})}$$

Under the **Naive Bayes conditional independence assumption**:

$$P(\mathbf{x} \mid y) = \prod_{i=1}^n P(x_i \mid y)$$

### Laplace Smoothing
To avoid zero probabilities for words observed during testing that did not appear in a specific class training fold:

$$\hat{\theta}_{yi} = \frac{N_{yi} + \alpha}{N_y + \alpha \cdot |V|}$$

Where:
- $N_{yi}$ is the count of feature $i$ in class $y$.
- $N_y$ is the total count of all features in class $y$.
- $\alpha = 0.1$ is the smoothing constant.
- $|V|$ is the total vocabulary size ($5,000$).

### Term Frequency - Inverse Document Frequency (TF-IDF)
Features are weighted using sublinear term frequency scaling:

$$\text{TF-IDF}(t, d, D) = (1 + \log(\text{TF}(t, d))) \times \log\left(\frac{1 + |D|}{1 + |\{d \in D : t \in d\}|}\right) + 1$$

---

## 6. Real Model Evaluation Results
Evaluated strictly on held-out test data ($20\%$ stratified split of $5,572$ records):

| Evaluation Metric | Academic Report Reference | Actual Trained System |
| :--- | :--- | :--- |
| **Test Accuracy** | `91.20%` | **98.92%** |
| **Spam Precision** | `—` | **97.26%** |
| **Spam Recall** | `—` | **94.67%** |
| **F1-Score** | `—` | **95.95%** |
| **ROC-AUC Score** | `0.9420` | **0.9929** |
| **Training Accuracy**| `96.00%` | **99.53%** |
| **Confusion Matrix** | `[[58, 11], [4, 98]]` | `[[961, 4], [8, 142]]` |

*Note: The actual production model utilizes sublinear TF-IDF with bigrams and optimized Laplace smoothing, achieving superior performance compared to the historical baseline.*

---

## 7. Technology Stack

- **Runtime:** Python 3.14+
- **Frontend / Web UI:** Streamlit with Custom Glassmorphism CSS & Cyber Theme
- **Data Engineering:** Pandas, NumPy, Regular Expressions
- **Machine Learning:** Scikit-learn (`MultinomialNB`, `TfidfVectorizer`, `CountVectorizer`, `train_test_split`)
- **Data Visualizations:** Plotly (`Heatmap`, `Scatter`, `Pie`, `Bar`), Matplotlib, Seaborn
- **Persistence:** SQLite3 (`classification_history.db`), Joblib (`spam_model.pkl`, `vectorizer.pkl`)
- **Testing:** Pytest (23 unit and integration tests)

---

## 8. Project Folder Structure

```
email-sms-spam-detection/
├── app.py                     # Master Streamlit UI & Navigation Controller
├── train.py                   # Standalone Model Training CLI Tool
├── config.py                  # Project Paths, Palette & ML Constants
├── requirements.txt           # Verified Package Dependencies
├── README.md                  # Complete Academic & Engineering Documentation
├── .gitignore                 # Version Control Ignore Rules
│
├── .streamlit/
│   └── config.toml            # Streamlit Theme & Server Configurations
│
├── data/
│   ├── raw/                   # Raw Datasets (UCI SMS Collection & Samples)
│   │   ├── sms_spam_collection.csv
│   │   ├── sms_spam_collection.tsv
│   │   └── sample_bulk_messages.csv
│   ├── processed/             # Cleaned Corpus for Model Training
│   │   └── cleaned_dataset.csv
│   └── classification_history.db  # SQLite Telemetry Database
│
├── models/
│   ├── spam_model.pkl         # Serialized MultinomialNB Model Artifact
│   ├── vectorizer.pkl         # Serialized TF-IDF Feature Pipeline
│   └── metrics.json           # Actual Empirical Evaluation Results & Metadata
│
├── src/
│   ├── __init__.py            # Package Init
│   ├── data_loader.py         # Multi-format CSV/TSV Loader & Schema Inference
│   ├── preprocessing.py       # Text Cleaning, Label Normalization & Filtering
│   ├── feature_extraction.py  # TF-IDF and CountVectorizer Pipelines
│   ├── model_training.py      # Stratified Train/Test Split & Training Engine
│   ├── evaluation.py          # Metric Computations & Plotly Visualizations
│   ├── prediction.py          # Singleton Inference Service & Batch Prediction
│   ├── explainability.py      # Heuristic Urgency/Phishing Pattern Detectors
│   ├── database.py            # SQLite Telemetry, Analytics & Privacy Controls
│   └── analytics.py           # Dashboard Plotly Figures & Time Series
│
├── views/
│   ├── __init__.py            # Views Package Init
│   ├── dashboard.py           # Page 1: Operations Dashboard
│   ├── message_detection.py   # Page 2: Single Message Spam Detection
│   ├── email_analysis.py      # Page 3: Full Email Threat Analysis
│   ├── bulk_detection.py      # Page 4: Bulk CSV Batch Processor
│   ├── model_performance.py   # Page 5: Empirical Model Evaluation Metrics
│   ├── dataset_management.py  # Page 6: Corpus Health & Retraining Workstation
│   ├── history.py             # Page 7: Classification History & Audit Logs
│   ├── project_information.py # Page 8: Academic Documentation & Architecture
│   └── settings.py            # Page 9: System Settings & Preferences
│
├── assets/
│   └── styles.css             # Exact Reference SaaS Dark-Purple Design System
│
└── tests/
    ├── test_preprocessing.py      # Preprocessing & Regex Unit Tests
    ├── test_dataset.py            # Loader & Column Inference Tests
    ├── test_feature_extraction.py # TF-IDF & Bag-of-Words Tests
    ├── test_training.py           # Model Training Lifecycle Tests
    ├── test_prediction.py         # Prediction Benchmark & Boundary Tests
    ├── test_database.py           # SQLite Operations & Privacy Tests
    └── test_evaluation.py         # Metric Calculations Tests
```

---

## 9. Installation & Setup Instructions

### Prerequisites
- Python 3.10+ (Tested up to Python 3.14)
- Git (optional)
- Windows PowerShell, Command Prompt, or Linux/macOS Terminal

### Step 1: Open Project Directory
```powershell
cd d:\Desktop\unmani
```

### Step 2: Install Required Dependencies
```powershell
# For Vercel Serverless & FastAPI API:
pip install -r requirements.txt

# For Streamlit Application & Visualization Suite:
pip install -r requirements-streamlit.txt
```

---

## 10. Execution & Deployment Instructions

### A. Deploy to Vercel (Production Serverless)
1. **Prerequisites:** Push changes to GitHub repository [https://github.com/gauravrsingh16-art/scam](https://github.com/gauravrsingh16-art/scam).
2. **Via Vercel Web Dashboard:**
   - Go to [vercel.com](https://vercel.com) and click **"Add New Project"**.
   - Select GitHub repository `gauravrsingh16-art/scam`.
   - Vercel will automatically detect `vercel.json` and the `vite` framework.
   - Build Command: `npm run build`
   - Output Directory: `dist`
   - Click **"Deploy"**.
3. **Via Vercel CLI:**
   ```powershell
   npm install -g vercel
   vercel --prod
   ```
   *Note: `.vercelignore` guarantees that `app.py` is ignored by the Python serverless scanner, and `api/index.py` handles all `/api/*` routes with genuine ML inference.*

### B. Run Modern Stack Locally (React + FastAPI)
1. **Terminal 1 — Start FastAPI Serverless Backend:**
   ```powershell
   python -m uvicorn api.index:app --reload --port 8000
   ```
   API Documentation available at: `http://localhost:8000/api/docs`
2. **Terminal 2 — Start React/Vite Frontend:**
   ```powershell
   npm run dev
   ```
   Open browser at: `http://localhost:3000`

### C. Run Streamlit Application (Local & Streamlit Cloud)
Launch the multi-page Streamlit application:
```powershell
streamlit run app.py
```
Open browser at: `http://localhost:8501`

### D. Train / Retrain Model via Command Line
```powershell
# Retrain model on active dataset
python train.py
```

---

## 11. Automated Testing Instructions
Run the full automated test suite using Pytest:
```powershell
python -m pytest -v
```
All **32 unit, integration, and API tests** execute and pass:
- Preprocessing & regex tests (`test_preprocessing.py`)
- Dataset loader & column inference tests (`test_dataset.py`)
- Feature extraction & TF-IDF tests (`test_feature_extraction.py`)
- Training lifecycle & artifact tests (`test_training.py`)
- Prediction & boundary tests (`test_prediction.py`)
- SQLite database & privacy tests (`test_database.py`)
- Metric calculation tests (`test_evaluation.py`)
- FastAPI serverless endpoint tests (`test_api.py`)

---

## 12. REST API Endpoints Specification

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/health` | Service health status, model readiness, and version |
| `GET` | `/api/dashboard-stats` | Real-time KPI counts, threat distribution, recent audits |
| `POST` | `/api/predict` | Classifies single message text with confidence & heuristics |
| `POST` | `/api/email-analysis` | Analyzes structured email (Subject, Sender, Body) |
| `POST` | `/api/bulk-predict` | Batch classification for uploaded CSV/TSV files |
| `GET` | `/api/model-metrics` | Actual test metrics (Accuracy, Precision, Recall, Confusion Matrix) |
| `GET` | `/api/history` | Filterable SQLite audit records |
| `POST` | `/api/history/delete` | Deletes specific audit record by ID |
| `POST` | `/api/history/clear` | Purges all audit history records |
| `GET` | `/api/dataset-info` | Corpus rows, class balance, and sample rows |
| `GET` | `/api/settings` | Retrieves privacy settings (audit logging & preview storage) |
| `POST` | `/api/settings` | Updates privacy settings |

---

---

## 12. Application Features Across All 7 Pages

1. **Dashboard:** Live KPI counters (Total Processed, Spam Intercepted, Legitimate Ham, Model Test Accuracy), interactive Plotly Donut chart, channel distribution, and recent activity feed.
2. **Message Detection:** Instant SMS/email classifier with character counter, quick benchmark buttons (Lottery scam, phishing, campus meeting, clinic confirmation), confidence meter, and heuristic indicators.
3. **Email Analysis:** Multi-field analyzer taking Subject, optional Sender Address, and Email Body with unified NLP vectorization, credential theft alerts, and security guidance.
4. **Bulk Detection:** High-speed batch processor accepting CSV files, auto-detecting message columns, generating downloadable classified CSVs, and offering a one-click sample loader.
5. **Model Performance:** Real evaluation dashboard displaying actual Test Accuracy, Precision, Recall, F1, ROC-AUC, interactive Confusion Matrix heatmap, ROC Curve, and top distinguishing vocabulary terms.
6. **Dataset Management:** Corpus health dashboard reporting total rows, spam/ham counts, missing values, duplicates, and an interactive retraining workstation.
7. **Project Information:** Academic-level documentation containing problem formulation, architecture diagrams, Bayes Theorem equations, Laplace smoothing proofs, and future research directions.

---

## 13. Data Privacy and Security Design
- **Zero-Content Retention:** The application does not store message plaintext by default. Users can toggle message preview storage on/off in the sidebar.
- **Local SQLite Audit:** Telemetry records only message channel, prediction outcome, confidence score, and timestamp.
- **Input Sanitization:** Uploaded CSVs are capped at 15MB, parsed safely with encoding fallbacks, and never executed as code.
- **Model Limitation Disclaimers:** HAM classifications are explicitly stated as statistical predictions, not absolute guarantees of safety.

---

## 14. Future Scope
- **Transformer Fine-Tuning:** Integrate DistilBERT or RoBERTa for contextual sequence modeling.
- **Active URL Sandboxing:** Implement headless URL redirects and domain reputation checks.
- **Multilingual Support:** Incorporate multilingual embeddings (mBERT) for regional language spam campaigns.
- **Mobile Integration:** Develop on-device daemon for Android SMS spam interception.

---

## 15. Academic Project Credits
- **Project Title:** Email/SMS Spam Detection System
- **Domain:** Artificial Intelligence, Machine Learning, Natural Language Processing, Cybersecurity
- **Dataset Source:** [UCI Machine Learning Repository — SMS Spam Collection](https://archive.ics.uci.edu/dataset/228/sms+spam+collection)
