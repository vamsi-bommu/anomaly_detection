"""
Master Pipeline Orchestrator
Runs the complete anomaly detection pipeline
"""
import traceback
from pathlib import Path


# ============================================================================
# IMPORT CONFIGURATION - All paths managed in config.py
# ============================================================================
from config.config import Config

# Use centralized configuration
INVOICE_DATA = Config.INVOICE_DATA
FESTIVALS_DATA = Config.FESTIVALS_DATA
HIERARCHICAL_DATA_DIR = Config.HIERARCHICAL_DATA_DIR
LOGS_DIR = Config.LOGS_DIR
MIN_RECORDS = Config.MIN_RECORDS

print("Using configuration from config.py")
print(f"Data Dir: {HIERARCHICAL_DATA_DIR}")
print(f"Logs Dir: {LOGS_DIR}")
# ============================================================================


def ensure_directories_exist():
    """Create all necessary directories"""
    dirs = [HIERARCHICAL_DATA_DIR, LOGS_DIR]
    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f" Directory ready: {dir_path}")


def run_preprocessing(invoice_data_path: str, output_dir: str, min_records: int = 1200):
    """Stage 1: Data Preprocessing"""
    print("\n" + "="*80)
    print("STAGE 1: DATA PREPROCESSING")
    print("="*80)
    
    # Validate input file exists
    if not Path(invoice_data_path).exists():
        print(f" Invoice data file not found: {invoice_data_path}")
        return False
    
    print(f" Using invoice data: {invoice_data_path}")
    print(f" Saving hierarchical data to: {output_dir}")
    
    try:
        from preprocessor import DataPreprocessor
        
        preprocessor = DataPreprocessor(
            base_output_dir=output_dir,
            min_records=min_records
        )
        
        metadata = preprocessor.process_invoice_data(invoice_data_path)
        
        print("\nStage 1 Complete: Data Preprocessing")
        return True
        
    except Exception as e:
        print(f"\n Stage 1 Failed: {str(e)}")
        traceback.print_exc()
        return False
