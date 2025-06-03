import subprocess
import os

def compile_latex(tex_path: str) -> str:
    # Use the same directory as the input file for output
    output_dir = os.path.dirname(tex_path)
    os.makedirs(output_dir, exist_ok=True)

    cmd = [
        "tectonic",
        "--outdir", output_dir,
        tex_path
    ]

    result = subprocess.run(cmd, capture_output=True)
    if result.returncode != 0:
        print("Tectonic failed:", result.stderr.decode())
        return None

    # Get the base filename without extension
    base_name = os.path.splitext(os.path.basename(tex_path))[0]
    pdf_path = os.path.join(output_dir, f"{base_name}.pdf")
    
    if os.path.exists(pdf_path):
        return pdf_path
    else:
        print(f"PDF not found at {pdf_path}")
        # List files in output directory for debugging
        print("Files in output directory:", os.listdir(output_dir))
        return None
