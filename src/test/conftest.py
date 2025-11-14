# src/test/conftest.py
# Injeta a RAIZ do repo no sys.path antes da coleta do pytest
import os, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
