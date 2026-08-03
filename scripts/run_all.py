#!/usr/bin/env python3
import subprocess, sys
from pathlib import Path
root = Path(__file__).resolve().parents[1]
for name in ["generate_exports.py", "generate_site.py", "generate_llms.py", "generate_sitemap.py", "validate_data.py"]:
    subprocess.run([sys.executable, str(root / "scripts" / name)], check=True)
