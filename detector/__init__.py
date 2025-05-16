
# detector/__init__.py

# Import từng hàm cụ thể từ các module tương ứng
from .checkbox import is_checkbox
from .checkbox_grid import is_checkbox_grid
from .date import is_date
from .dropdown import is_dropdown
from .linear_scale import is_linear_scale
from .multiple_choice import is_multiple_choice
from .multiple_choice_grid import is_multiple_choice_grid
from .paragraph_answer import is_paragraph_answer
from .short_answer import is_short_answer
from .star_rating import is_star_rating
from .time import is_time
from .file_upload import is_file_upload

# Liệt kê tất cả các hàm được export ra ngoài package
__all__ = [
    'is_checkbox',
    'is_checkbox_grid',
    'is_date',
    'is_dropdown',
    'is_linear_scale',
    'is_multiple_choice',
    'is_multiple_choice_grid',
    'is_paragraph_answer',
    'is_short_answer',
    'is_star_rating',
    'is_time',
    'is_file_upload'
]
