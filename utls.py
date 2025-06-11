import subprocess
import os
from typing import Tuple, Optional

def compile_latex(tex_path: str) -> Tuple[Optional[str], Optional[str]]:
    # Use the same directory as the input file for output
    output_dir = os.path.dirname(tex_path)
    os.makedirs(output_dir, exist_ok=True)

    cmd = [
        "tectonic",
        "--print",  # Get detailed error output
        "--outdir", output_dir,
        tex_path
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        error_msg = result.stderr or result.stdout or "Unknown compilation error"
        print("Tectonic failed:", error_msg)
        return None, error_msg

    # Get the base filename without extension
    base_name = os.path.splitext(os.path.basename(tex_path))[0]
    pdf_path = os.path.join(output_dir, f"{base_name}.pdf")
    
    if os.path.exists(pdf_path):
        return pdf_path, None
    else:
        error_msg = f"PDF not found at {pdf_path}. Files in output directory: {os.listdir(output_dir)}"
        print(error_msg)
        return None, error_msg
