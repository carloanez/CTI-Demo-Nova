"""Run the whole replay pipeline with all Python network socket creation disabled."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from pytest_socket import disable_socket
disable_socket()
from cti_lab.cli import run
run("replay")
