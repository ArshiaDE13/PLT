"""Persian variants of the whole Tutorial section (chapters 1-16).

English content in chapters_a.py / chapters_b.py stays the canonical source;
this module only adds the fa fields the browser picks when Persian is active.
Merged by content.py at build time.
"""

from fa_tutorial_a import FA_A
from fa_tutorial_b import FA_B

FA_CONTENT = {}
FA_CONTENT.update(FA_A)
FA_CONTENT.update(FA_B)
