"""
🛒 Shop — Books, Gear, Downloads & Support
"""
import streamlit as st
from utils import init_session_state, apply_brand_theme, render_sidebar
from auth import render_auth, render_logout_sidebar
from shop import render_full_shop_page

st.set_page_config(
    page_title="Shop — Rocen Homesteady",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="auto"
)

init_session_state()
apply_brand_theme()
user = render_auth()
render_logout_sidebar()
render_sidebar()

render_full_shop_page()
