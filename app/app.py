import streamlit as st
from st_pages import show_pages_from_config
import os
import subprocess
import platform

if platform.system() != 'Windows':
    setup_script = 'app/setup.sh'
    if os.path.exists(setup_script):
        subprocess.run(['bash', setup_script])

show_pages_from_config()
