"""Ponto de entrada mantido; a bateria atual está em verificar_interpretacao.py."""
import runpy
from pathlib import Path

runpy.run_path(str(Path(__file__).with_name('verificar_interpretacao.py')))
