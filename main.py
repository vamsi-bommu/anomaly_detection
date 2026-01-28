"""
Master Pipeline Orchestrator
Runs the complete hierarchical anomaly detection pipeline
Structure: Global â†’ Branches
"""
import os
import sys
import argparse
import subprocess
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
print(f"   Data Dir: {HIERARCHICAL_DATA_DIR}")
print(f"   Logs Dir: {LOGS_DIR}")
# ============================================================================