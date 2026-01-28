from config.config import Config
from src.tracking.history_tracker import tracker
import streamlit as st
import pandas as pd
import numpy as np
import json
from pathlib import Path
from datetime import datetime
from src.model.model_validator import ModelValidator
from bokeh.plotting import figure
from bokeh.models import HoverTool, DateRangeSlider, CustomJS, ColumnDataSource
from bokeh.layouts import column
import streamlit.components.v1 as components


# Page configuration
st.set_page_config(
    page_title="Anomaly Detection Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.8; }
    }
    </style>
""", unsafe_allow_html=True)

