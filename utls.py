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
        "-Z", "continue-on-errors",  # Keep compiling even when recoverable errors occur
        "--outdir", output_dir,
        tex_path
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    
    # Capture any warnings or errors from output
    output_msg = result.stderr or result.stdout or ""
    
    if result.returncode != 0:
        print("Tectonic failed:", output_msg)
        return None, output_msg

    # Get the base filename without extension
    base_name = os.path.splitext(os.path.basename(tex_path))[0]
    pdf_path = os.path.join(output_dir, f"{base_name}.pdf")
    
    if os.path.exists(pdf_path):
        # Return warnings/errors even on successful compilation
        warnings = output_msg if output_msg.strip() else None
        return pdf_path, warnings
    else:
        error_msg = f"PDF not found at {pdf_path}. Files in output directory: {os.listdir(output_dir)}"
        print(error_msg)
        return None, error_msg
