# GG_FORM_TOOL/__init__.py

# Import các module chính ở thư mục gốc
from .scanform import scan_form
from .detect import detect_main  # nếu có hàm main xử lý chính
from .app import run_app         # nếu app.py có hàm chính

# Nếu muốn expose thư mục con như package:
from . import action
from . import data
from . import detector
