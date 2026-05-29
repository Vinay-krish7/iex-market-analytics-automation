from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR/"data"
REPORT_DIR = BASE_DIR/"reports"
PLOT_DIR = BASE_DIR/"plots"
LOG_DIR = BASE_DIR/"logs"


CHROMEDRIVER_PATH = r"C:\Users\komaravolu.vinay\chromedriver.exe"

EMAIL_RECIPIENTS = [
    "abhishek.agarwal@feplglobal.com",
    