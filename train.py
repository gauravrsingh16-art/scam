"""
Standalone Model Training CLI Script
EMAIL/SMS SPAM DETECTION SYSTEM

Usage:
    python train.py
    python train.py --vectorizer count --max-features 4000
    python train.py --vectorizer tfidf --ngram 1 2 --alpha 0.1
"""

import argparse
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from src.database import init_db
from src.model_training import train_model


def main():
    parser = argparse.ArgumentParser(description="Train Multinomial Naive Bayes model for Spam Detection.")
    parser.add_argument(
        "--vectorizer",
        type=str,
        default="tfidf",
        choices=["tfidf", "count"],
        help="Feature extraction technique: 'tfidf' (default) or 'count'"
    )
    parser.add_argument(
        "--ngram",
        type=int,
        nargs=2,
        default=[1, 2],
        help="N-gram range as two integers: min_n max_n (default: 1 2)"
    )
    parser.add_argument(
        "--max-features",
        type=int,
        default=5000,
        help="Maximum vocabulary features to extract (default: 5000)"
    )
    parser.add_argument(
        "--min-df",
        type=int,
        default=2,
        help="Minimum document frequency for terms (default: 2)"
    )
    parser.add_argument(
        "--alpha",
        type=float,
        default=0.1,
        help="Laplace smoothing parameter for MultinomialNB (default: 0.1)"
    )
    parser.add_argument(
        "--drop-duplicates",
        action="store_true",
        help="Drop duplicate message texts before training"
    )

    args = parser.parse_args()

    print("=" * 60)
    print("   AI-POWERED EMAIL/SMS SPAM DETECTION — MODEL TRAINING   ")
    print("=" * 60)
    print(f"Vectorizer Type   : {args.vectorizer.upper()}")
    print(f"N-gram Range      : ({args.ngram[0]}, {args.ngram[1]})")
    print(f"Max Features      : {args.max_features}")
    print(f"Min Doc Frequency : {args.min_df}")
    print(f"Laplace Alpha     : {args.alpha}")
    print(f"Drop Duplicates   : {args.drop_duplicates}")
    print("-" * 60)

    # Initialize SQLite database
    init_db()

    try:
        print("[*] Loading dataset and executing training pipeline...")
        result = train_model(
            vectorizer_type=args.vectorizer,
            ngram_range=(args.ngram[0], args.ngram[1]),
            max_features=args.max_features,
            min_df=args.min_df,
            alpha=args.alpha,
            drop_duplicates=args.drop_duplicates
        )

        test_metrics = result["test_metrics"]
        print("\n" + "=" * 60)
        print("                 TRAINING COMPLETED SUCCESSFULLY           ")
        print("=" * 60)
        print(f"Training Samples  : {result['dataset_statistics']['train_samples']}")
        print(f"Holdout Test Size : {result['dataset_statistics']['test_samples']}")
        print(f"Vocabulary Size   : {result['hyperparameters']['vocabulary_size']}")
        print("-" * 60)
        print(f"Training Accuracy : {result['train_accuracy'] * 100:.2f}%")
        print(f"Test Accuracy     : {test_metrics['accuracy'] * 100:.2f}%")
        print(f"Spam Precision    : {test_metrics['precision'] * 100:.2f}%")
        print(f"Spam Recall       : {test_metrics['recall'] * 100:.2f}%")
        print(f"F1-Score          : {test_metrics['f1_score'] * 100:.2f}%")
        if test_metrics.get("roc_auc"):
            print(f"ROC-AUC Score     : {test_metrics['roc_auc']:.4f}")
        print(f"Confusion Matrix  : {test_metrics['confusion_matrix']}")
        print("-" * 60)
        print("Model saved to     : models/spam_model.pkl")
        print("Vectorizer saved to: models/vectorizer.pkl")
        print("Metrics saved to   : models/metrics.json")
        print("=" * 60)

    except Exception as e:
        print(f"\n[ERROR] Model training failed: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
