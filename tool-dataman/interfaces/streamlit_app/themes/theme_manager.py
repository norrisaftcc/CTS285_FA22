#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
theme_manager.py - Theme management for the Dataman Streamlit app

This module provides functionality for managing themes in the Streamlit app,
including Little Professor and Dataman themes.
"""
import base64
import os
from typing import Dict, Tuple

import streamlit as st

# ASCII art for simple theme representations when images are not available
DATAMAN_ASCII = """
  _____        _                           
 |  __ \      | |                          
 | |  | | __ _| |_ __ _ _ __ ___   __ _ _ __
 | |  | |/ _` | __/ _` | '_ ` _ \ / _` | '_ \\
 | |__| | (_| | || (_| | | | | | | (_| | | | |
 |_____/ \__,_|\__\__,_|_| |_| |_|\__,_|_| |_|
                                            
"""

LITTLE_PROFESSOR_ASCII = """
  _     _ _   _   _        _____            __                          
 | |   (_) | | | | |      |  __ \          / _|                         
 | |    _| |_| |_| | ___  | |__) | __ ___ | |_ ___  ___ ___  ___  _ __ 
 | |   | | __| __| |/ _ \ |  ___/ '__/ _ \|  _/ _ \/ __/ __|/ _ \| '__|
 | |___| | |_| |_| |  __/ | |   | | | (_) | ||  __/\__ \__ \ (_) | |   
 |______\_\__|\__|_|\___| |_|   |_|  \___/|_| \___||___/___/\___/|_|   
                                                                      
"""

# Theme colors
THEME_COLORS = {
    "dataman": {
        "primary": "#4A90E2",      # Blue
        "secondary": "#50E3C2",    # Teal
        "background": "#2D3E50",   # Dark blue
        "text": "#FFFFFF",         # White
        "accent": "#F5A623",       # Orange
    },
    "little_professor": {
        "primary": "#D64541",      # Red
        "secondary": "#F9690E",    # Orange
        "background": "#F5D76E",   # Yellow
        "text": "#34495E",         # Dark blue
        "accent": "#674172",       # Purple
    }
}

def get_base64_encoded_image(image_path: str) -> str:
    """
    Get base64 encoded image for embedding in HTML.
    
    Args:
        image_path (str): Path to the image
        
    Returns:
        str: Base64 encoded image
    """
    if not os.path.exists(image_path):
        return ""
    
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

def set_theme(theme_name: str) -> None:
    """
    Set the theme for the Streamlit app.
    
    Args:
        theme_name (str): Name of the theme to set ('dataman' or 'little_professor')
    """
    if theme_name not in ["dataman", "little_professor"]:
        theme_name = "dataman"  # Default to dataman
    
    # Store theme in session state
    st.session_state.theme = theme_name
    
    # Apply theme colors
    colors = THEME_COLORS[theme_name]
    
    # Apply theme using CSS
    st.markdown(f"""
    <style>
        :root {{
            --primary-color: {colors["primary"]};
            --secondary-color: {colors["secondary"]};
            --background-color: {colors["background"]};
            --text-color: {colors["text"]};
            --accent-color: {colors["accent"]};
        }}
        
        /* Top bar */
        header {{
            background-color: var(--primary-color) !important;
        }}
        
        /* Sidebar */
        section[data-testid="stSidebar"] {{
            background-color: var(--background-color) !important;
            color: var(--text-color) !important;
        }}
        
        section[data-testid="stSidebar"] .css-17lntkn {{
            color: var(--text-color) !important;
        }}
        
        /* Buttons */
        button[kind="primary"] {{
            background-color: var(--primary-color) !important;
        }}
        
        button[kind="secondary"] {{
            background-color: var(--secondary-color) !important;
        }}
        
        /* Links */
        a {{
            color: var(--accent-color) !important;
        }}
        
        /* Headers */
        h1, h2, h3, h4, h5 {{
            color: var(--primary-color) !important;
        }}
        
        /* Correct/incorrect feedback */
        .correct-answer {{
            color: #28a745 !important;
            font-weight: bold;
        }}
        
        .incorrect-answer {{
            color: #dc3545 !important;
            font-weight: bold;
        }}
        
        /* Logo */
        .theme-logo {{
            text-align: center;
            font-family: monospace;
            white-space: pre;
            font-size: 10px;
            line-height: 10px;
            margin-bottom: 20px;
            color: var(--primary-color);
        }}
        
        /* Achievement badges */
        .achievement-badge {{
            background-color: var(--accent-color);
            color: white;
            padding: 5px 10px;
            border-radius: 15px;
            margin: 5px 0;
            display: inline-block;
        }}
    </style>
    """, unsafe_allow_html=True)

def display_logo() -> None:
    """Display the logo for the current theme."""
    theme = st.session_state.get("theme", "dataman")
    
    if theme == "dataman":
        st.markdown(f'<div class="theme-logo">{DATAMAN_ASCII}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="theme-logo">{LITTLE_PROFESSOR_ASCII}</div>', unsafe_allow_html=True)

def theme_correct_answer(message: str) -> None:
    """
    Display a correct answer message with themed styling.
    
    Args:
        message (str): Message to display
    """
    st.markdown(f'<div class="correct-answer">✓ {message}</div>', unsafe_allow_html=True)

def theme_incorrect_answer(message: str) -> None:
    """
    Display an incorrect answer message with themed styling.
    
    Args:
        message (str): Message to display
    """
    st.markdown(f'<div class="incorrect-answer">✗ {message}</div>', unsafe_allow_html=True)

def display_achievement_badge(name: str, description: str) -> None:
    """
    Display an achievement badge.
    
    Args:
        name (str): Name of the achievement
        description (str): Description of the achievement
    """
    st.markdown(f'<div class="achievement-badge">🏆 {name}: {description}</div>', unsafe_allow_html=True)

def get_theme_colors() -> Dict[str, str]:
    """
    Get the colors for the current theme.
    
    Returns:
        Dict[str, str]: Dictionary of theme colors
    """
    theme = st.session_state.get("theme", "dataman")
    return THEME_COLORS[theme]