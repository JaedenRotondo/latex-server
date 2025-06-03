from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks, Request
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import asyncio
import uuid
from concurrent.futures import ThreadPoolExecutor
from utls import compile_latex
import shutil
from monitoring import metrics_middleware, metrics_endpoint

app = FastAPI(title="LaTeX Compilation Service")

# Add CORS middleware for Cloudflare
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Thread pool for parallel LaTeX compilation
executor = ThreadPoolExecutor(max_workers=4)  # Adjust based on your server capacity

# Add metrics middleware
@app.middleware("http")
async def add_metrics_middleware(request: Request, call_next):
    return await metrics_middleware(request, call_next)

@app.get("/metrics")
async def get_metrics():
    return await metrics_endpoint()

@app.get("/")
async def root():
    return {"message": "LaTeX Compilation Service", "status": "healthy"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/compile")
async def compile_latex_endpoint(file: UploadFile = File(...)):
    if not file.filename.endswith('.tex'):
        raise HTTPException(status_code=400, detail="File must be a .tex file")
    
    # Generate unique ID for this compilation
    job_id = str(uuid.uuid4())
    job_dir = f"/tmp/jobs/{job_id}"
    os.makedirs(job_dir, exist_ok=True)
    
    tex_path = os.path.join(job_dir, file.filename)
    
    # Save uploaded file
    with open(tex_path, "wb") as f:
        content = await file.read()
        f.write(content)
    
    # Run compilation in thread pool for parallelism
    loop = asyncio.get_event_loop()
    pdf_path = await loop.run_in_executor(executor, compile_latex, tex_path)
    
    if not pdf_path:
        # Clean up on failure
        shutil.rmtree(job_dir, ignore_errors=True)
        raise HTTPException(status_code=500, detail="LaTeX compilation failed")
    
    # Schedule cleanup after response
    async def cleanup():
        await asyncio.sleep(300)  # Keep files for 5 minutes
        shutil.rmtree(job_dir, ignore_errors=True)
    
    asyncio.create_task(cleanup())
    
    return FileResponse(
        pdf_path, 
        media_type="application/pdf", 
        filename=f"{os.path.splitext(file.filename)[0]}.pdf"
    )
