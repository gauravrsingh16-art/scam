"""
FastAPI Serverless Application Entrypoint
Exports top-level ASGI variable: 'app' for Vercel Serverless Functions.
Provides RESTful API endpoints for Spam Intelligence AI ML inference.
"""

import os
import sys
import io
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from fastapi import FastAPI, UploadFile, File, Form, Query, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import pandas as pd
import numpy as np

from config import (
    MODEL_FILE,
    VECTORIZER_FILE,
    METRICS_FILE,
    RAW_DATASET_CSV,
    PROCESSED_DATASET_CSV,
    HISTORY_DB_PATH,
    COLORS
)
from src.prediction import SpamClassifierService
from src.explainability import analyze_heuristics
from src.database import (
    init_db,
    log_classification,
    get_history,
    get_history_filtered,
    get_dashboard_stats,
    delete_history_record,
    clear_history,
    is_history_enabled,
    set_history_enabled,
    is_preview_storage_enabled,
    set_preview_storage_enabled,
    reindex_database
)

# Initialize database schema if not present
try:
    init_db()
except Exception as e:
    print(f"Warning initializing database: {e}")

# Instantiate FastAPI application
app = FastAPI(
    title="Spam Intelligence API",
    description="Cybersecurity ML Defense Engine Serverless API",
    version="2.0.0",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json"
)

# Add CORS Middleware to allow requests from any frontend client
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Pydantic Schemas
# ---------------------------------------------------------------------------

class PredictRequest(BaseModel):
    text: str = Field(..., description="Message text payload to classify")
    message_type: str = Field(default="SMS", description="Source channel: SMS or Email")
    log_to_db: bool = Field(default=True, description="Whether to store record in database")


class EmailAnalysisRequest(BaseModel):
    subject: str = Field(default="", description="Email subject line")
    sender: str = Field(default="", description="Sender address/display")
    body: str = Field(default="", description="Email body content")
    log_to_db: bool = Field(default=True, description="Whether to store record in database")


class DeleteRecordRequest(BaseModel):
    record_id: int = Field(..., description="ID of the record to delete")


class SettingsUpdateRequest(BaseModel):
    history_enabled: Optional[bool] = None
    store_previews: Optional[bool] = None


# ---------------------------------------------------------------------------
# API Endpoints
# ---------------------------------------------------------------------------

@app.get("/api/health", summary="Service Health and Status")
@app.get("/api", summary="API Root Health Status")
@app.get("/", summary="Root Health Status")
def health_check() -> Dict[str, Any]:
    """Check API status, model loading status, and system metadata."""
    service = SpamClassifierService.get_instance()
    is_ready = service.is_model_ready()
    
    return {
        "status": "healthy" if is_ready else "degraded",
        "service": "Spam Intelligence AI Defense Engine",
        "version": "2.0.0",
        "model_loaded": is_ready,
        "model_path_exists": MODEL_FILE.exists(),
        "vectorizer_path_exists": VECTORIZER_FILE.exists(),
        "database_path": str(HISTORY_DB_PATH),
        "timestamp": datetime.now().isoformat()
    }


@app.get("/api/dashboard-stats", summary="Real-Time Dashboard Analytics")
def dashboard_stats() -> Dict[str, Any]:
    """Retrieve aggregate statistics, KPI card counts, and distribution data."""
    stats = get_dashboard_stats()
    
    # Calculate threat distribution
    total = stats.get("total_processed", 0)
    spam_count = stats.get("total_spam", 0)
    ham_count = stats.get("total_ham", 0)
    spam_rate = stats.get("spam_rate", 0.0)
    avg_conf = stats.get("avg_confidence", 0.0)
    
    # Recent activity preview
    try:
        recent_df = get_history(limit=5)
        recent_records = recent_df.to_dict(orient="records") if not recent_df.empty else []
    except Exception:
        recent_records = []
        
    return {
        "kpi": {
            "total_processed": total,
            "total_spam": spam_count,
            "total_ham": ham_count,
            "spam_rate": spam_rate,
            "avg_confidence": avg_conf,
            "sms_count": stats.get("sms_count", 0),
            "email_count": stats.get("email_count", 0),
            "bulk_count": stats.get("bulk_count", 0)
        },
        "distribution": {
            "spam": spam_count,
            "ham": ham_count,
            "spam_percentage": spam_rate,
            "ham_percentage": round(100.0 - spam_rate, 2) if total > 0 else 100.0
        },
        "recent_records": recent_records
    }


@app.post("/api/predict", summary="Classify Single SMS / Text Message")
def predict_message(payload: PredictRequest) -> Dict[str, Any]:
    """Classify a message text using the trained Multinomial Naive Bayes model."""
    if not payload.text.strip():
        raise HTTPException(status_code=400, detail="Message text cannot be empty.")
    
    service = SpamClassifierService.get_instance()
    try:
        result = service.predict_single(
            text=payload.text,
            message_type=payload.message_type,
            log_to_db=payload.log_to_db
        )
        return {
            "success": True,
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference error: {str(e)}")


@app.post("/api/email-analysis", summary="Analyze Structured Email Payload")
def email_analysis(payload: EmailAnalysisRequest) -> Dict[str, Any]:
    """Perform multi-field email threat analysis on Subject, Sender, and Body."""
    if not payload.body.strip() and not payload.subject.strip():
        raise HTTPException(status_code=400, detail="Provide at least an Email Subject or Email Body.")
    
    parts = []
    if payload.subject.strip():
        parts.append(f"Subject: {payload.subject.strip()}")
    if payload.sender.strip():
        parts.append(f"Sender: {payload.sender.strip()}")
    if payload.body.strip():
        parts.append(payload.body.strip())
        
    combined_text = " . ".join(parts)
    
    # Additional sender spoofing heuristics
    sender_flags = []
    sender_str = payload.sender.lower().strip()
    if sender_str:
        if any(brand in sender_str for brand in ["paypal", "apple", "google", "bank", "netflix", "amazon"]):
            if any(free in sender_str for free in ["@gmail.com", "@yahoo.com", "@hotmail.com", "@outlook.com"]):
                sender_flags.append("Free webmail address impersonating financial/tech brand")
        if any(sender_str.endswith(tld) for tld in [".xyz", ".top", ".click", ".win", ".bid"]):
            sender_flags.append("Sender uses high-risk / low-reputation top level domain (TLD)")
            
    service = SpamClassifierService.get_instance()
    try:
        result = service.predict_single(
            text=combined_text,
            message_type="Email",
            log_to_db=payload.log_to_db
        )
        
        # Combine heuristics with email-specific sender flags
        heuristics = result.get("heuristics", {})
        if sender_flags:
            heuristics["sender_spoof_flags"] = sender_flags
            heuristics["has_indicators"] = True
            heuristics["threat_score"] = min(100, heuristics.get("threat_score", 0) + 25)
            
        result["heuristics"] = heuristics
        result["email_fields"] = {
            "subject": payload.subject,
            "sender": payload.sender,
            "body_length": len(payload.body)
        }
        
        return {
            "success": True,
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Email analysis error: {str(e)}")


@app.post("/api/bulk-predict", summary="Batch Classification for CSV / TSV")
async def bulk_predict(
    file: UploadFile = File(...),
    text_column: Optional[str] = Form(None),
    log_to_db: bool = Form(False)
) -> Dict[str, Any]:
    """Upload a CSV or TSV file to run batch classification."""
    contents = await file.read()
    filename = file.filename or "bulk.csv"
    
    try:
        if filename.endswith(".tsv"):
            df = pd.read_csv(io.BytesIO(contents), sep="\t", on_bad_lines="skip")
        else:
            df = pd.read_csv(io.BytesIO(contents), on_bad_lines="skip")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Could not parse uploaded CSV/TSV: {str(e)}")
        
    if df.empty:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")
        
    # Auto-detect text column if not specified
    target_col = text_column
    if not target_col or target_col not in df.columns:
        candidates = ["text", "message", "sms", "email", "body", "content", "v2", "sms_text"]
        for c in df.columns:
            if c.lower() in candidates:
                target_col = c
                break
        if not target_col:
            target_col = df.columns[0]
            
    service = SpamClassifierService.get_instance()
    try:
        result_df = service.predict_bulk(df, text_col=target_col, log_to_db=log_to_db)
        
        total = len(result_df)
        spam_count = int((result_df["Prediction"] == "SPAM").sum())
        ham_count = total - spam_count
        spam_rate = round((spam_count / total) * 100, 2) if total > 0 else 0.0
        avg_conf = round(float(result_df["Confidence"].mean()) * 100, 2) if total > 0 else 0.0
        
        # Format top 100 rows for JSON preview
        preview_rows = result_df.head(100).to_dict(orient="records")
        
        return {
            "success": True,
            "filename": filename,
            "text_column": target_col,
            "summary": {
                "total": total,
                "spam_count": spam_count,
                "ham_count": ham_count,
                "spam_rate": spam_rate,
                "avg_confidence": avg_conf
            },
            "columns": list(result_df.columns),
            "rows": preview_rows
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch processing error: {str(e)}")


@app.get("/api/model-metrics", summary="Model Performance and Evaluation Metrics")
def model_metrics() -> Dict[str, Any]:
    """Retrieve actual metrics, confusion matrix, ROC-AUC, and hyperparameters."""
    if METRICS_FILE.exists():
        try:
            with open(METRICS_FILE, "r", encoding="utf-8") as f:
                metrics_data = json.load(f)
            return {"success": True, "metrics": metrics_data}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed reading metrics.json: {str(e)}")
    else:
        raise HTTPException(status_code=404, detail="Model metrics file not found. Please train model.")


@app.get("/api/history", summary="Query Classification History")
def query_history(
    search: str = Query(default="", description="Search keyword"),
    category: str = Query(default="ALL", description="Filter: ALL, SPAM, HAM"),
    message_type: str = Query(default="ALL", description="Filter: ALL, SMS, Email, Bulk"),
    limit: int = Query(default=100, ge=1, le=1000, description="Max rows to return")
) -> Dict[str, Any]:
    """Retrieve filtered classification audit records from SQLite."""
    try:
        df = get_history_filtered(
            search_query=search,
            category_filter=category,
            message_type_filter=message_type,
            limit=limit
        )
        records = df.to_dict(orient="records") if not df.empty else []
        return {
            "success": True,
            "total_returned": len(records),
            "records": records
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database query error: {str(e)}")


@app.post("/api/history/delete", summary="Delete Single History Record")
def delete_record(payload: DeleteRecordRequest) -> Dict[str, Any]:
    """Delete a specific classification record by ID."""
    success = delete_history_record(payload.record_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Record #{payload.record_id} not found.")
    return {"success": True, "deleted_id": payload.record_id}


@app.post("/api/history/clear", summary="Clear All History Records")
def clear_all_history() -> Dict[str, Any]:
    """Purge all classification history records."""
    deleted_count = clear_history()
    return {"success": True, "deleted_count": deleted_count}


@app.get("/api/dataset-info", summary="Dataset Metadata and Sample Rows")
def dataset_info() -> Dict[str, Any]:
    """Return dataset size, class distribution, and preview rows."""
    target_path = PROCESSED_DATASET_CSV if PROCESSED_DATASET_CSV.exists() else RAW_DATASET_CSV
    if not target_path.exists():
        raise HTTPException(status_code=404, detail="Dataset file not found.")
        
    try:
        df = pd.read_csv(target_path)
        total = len(df)
        label_col = "label" if "label" in df.columns else ("v1" if "v1" in df.columns else df.columns[0])
        
        spam_count = int((df[label_col].astype(str).str.lower().isin(["spam", "1"])).sum())
        ham_count = total - spam_count
        
        sample_rows = df.head(10).to_dict(orient="records")
        
        return {
            "success": True,
            "filename": target_path.name,
            "total_rows": total,
            "spam_count": spam_count,
            "ham_count": ham_count,
            "spam_percentage": round((spam_count / total) * 100, 2) if total > 0 else 0,
            "ham_percentage": round((ham_count / total) * 100, 2) if total > 0 else 0,
            "sample_rows": sample_rows
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading dataset: {str(e)}")


@app.get("/api/settings", summary="Get Privacy and System Settings")
def get_settings() -> Dict[str, Any]:
    """Retrieve current system and privacy settings."""
    return {
        "success": True,
        "history_enabled": is_history_enabled(),
        "store_previews": is_preview_storage_enabled()
    }


@app.post("/api/settings", summary="Update Privacy and System Settings")
def update_settings(payload: SettingsUpdateRequest) -> Dict[str, Any]:
    """Update privacy preferences."""
    if payload.history_enabled is not None:
        set_history_enabled(payload.history_enabled)
    if payload.store_previews is not None:
        set_preview_storage_enabled(payload.store_previews)
        
    return {
        "success": True,
        "history_enabled": is_history_enabled(),
        "store_previews": is_preview_storage_enabled()
    }
