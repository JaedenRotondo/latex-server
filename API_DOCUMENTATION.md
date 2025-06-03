# LaTeX Compilation API Documentation

## Overview

This API provides a high-performance LaTeX to PDF compilation service powered by Tectonic. It accepts LaTeX files and returns compiled PDF documents, with support for parallel processing and automatic package management.

## Base URL

```
https://latex-compiler.onrender.com
```

## API Endpoints

### 1. Compile LaTeX to PDF

**Endpoint:** `POST /compile`

**Description:** Converts a LaTeX (.tex) file to PDF format

**Request:**
- Method: `POST`
- Content-Type: `multipart/form-data`
- Body: Form data with a file field named `file`

**Response:**
- Success (200): Returns the compiled PDF file
- Error (400): Invalid file format (not .tex)
- Error (500): Compilation failed

**Example Request:**

```bash
# Using curl
curl -X POST "https://latex-compiler.onrender.com/compile" \
  -H "accept: application/pdf" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@document.tex" \
  --output document.pdf

# Using Python
import requests

with open('document.tex', 'rb') as f:
    files = {'file': ('document.tex', f, 'text/plain')}
    response = requests.post('https://latex-compiler.onrender.com/compile', files=files)
    
if response.status_code == 200:
    with open('output.pdf', 'wb') as pdf:
        pdf.write(response.content)
```

**JavaScript/Fetch Example:**

```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);

fetch('https://latex-compiler.onrender.com/compile', {
    method: 'POST',
    body: formData
})
.then(response => response.blob())
.then(blob => {
    // Create download link
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'output.pdf';
    a.click();
});
```

### 2. Health Check

**Endpoint:** `GET /health`

**Description:** Check if the service is running

**Response:**
```json
{
    "status": "healthy"
}
```

### 3. Service Info

**Endpoint:** `GET /`

**Description:** Get basic service information

**Response:**
```json
{
    "message": "LaTeX Compilation Service",
    "status": "healthy"
}
```

## Technical Specifications

### Infrastructure
- **Hosting:** Render.com (Oregon region)
- **Container:** Docker with Python 3.11 slim
- **LaTeX Engine:** Tectonic 0.15.0
- **Web Framework:** FastAPI with Uvicorn

### Performance
- **Parallel Processing:** 4 concurrent workers
- **Request Isolation:** Each compilation runs in a unique directory
- **Auto-cleanup:** Temporary files deleted after 5 minutes
- **Memory:** 512MB (free tier) / 2GB (paid tier)
- **CPU:** 0.1 vCPU (free tier) / 1 vCPU (paid tier)

### Limitations
- **File Size:** 10MB maximum per request (configurable)
- **Timeout:** 30 seconds per compilation
- **Rate Limits:** 
  - Free tier: ~100 requests/minute
  - Paid tier: Higher limits available

### Supported LaTeX Features
- **Full LaTeX Support:** All standard LaTeX commands
- **Package Management:** Automatic package downloads via Tectonic
- **Fonts:** System fonts + LaTeX fonts
- **Graphics:** TikZ, PGFPlots, includegraphics
- **Bibliography:** BibTeX/BibLaTeX support
- **Unicode:** Full UTF-8 support

## Error Handling

### Common Error Responses

**400 Bad Request**
```json
{
    "detail": "File must be a .tex file"
}
```

**500 Internal Server Error**
```json
{
    "detail": "LaTeX compilation failed"
}
```

## Usage Examples

### Basic Document
```latex
\documentclass{article}
\begin{document}
Hello, World!
\end{document}
```

### With Packages
```latex
\documentclass{article}
\usepackage{amsmath}
\usepackage{graphicx}
\usepackage{tikz}

\begin{document}
\section{Mathematics}
$E = mc^2$

\begin{tikzpicture}
  \draw (0,0) circle (1cm);
\end{tikzpicture}
\end{document}
```

## Integration Guide

### React Component Example
```jsx
function LaTeXCompiler() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleCompile = async () => {
    if (!file) return;
    
    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('https://latex-compiler.onrender.com/compile', {
        method: 'POST',
        body: formData
      });

      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        window.open(url, '_blank');
      } else {
        alert('Compilation failed');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <input 
        type="file" 
        accept=".tex" 
        onChange={(e) => setFile(e.target.files[0])}
      />
      <button onClick={handleCompile} disabled={loading}>
        {loading ? 'Compiling...' : 'Compile to PDF'}
      </button>
    </div>
  );
}
```

### CORS Configuration
The API has CORS enabled for all origins. You can make requests from any domain.

## Monitoring & Status

- **Uptime Monitoring:** https://latex-compiler.onrender.com/health
- **Response Time:** Typically 1-5 seconds for standard documents
- **Service Status:** Check Render status page

## Security

- **Input Validation:** Only .tex files accepted
- **Sandboxed Execution:** Each compilation runs in isolation
- **No Persistent Storage:** Files are deleted after processing
- **HTTPS Only:** All connections are encrypted

## Rate Limiting & Scaling

### Free Tier
- Suitable for personal projects
- May experience cold starts
- Shared resources

### Scaling Options
1. **Upgrade Render Plan:** For dedicated resources
2. **Deploy Multiple Instances:** For high availability
3. **Add CDN:** Use Cloudflare for caching static resources

## Support & Troubleshooting

### Common Issues

1. **Compilation Timeout**
   - Simplify complex documents
   - Split into smaller files
   - Check for infinite loops in LaTeX

2. **Missing Packages**
   - Tectonic downloads packages automatically
   - First compilation may be slower

3. **Font Issues**
   - Use standard LaTeX fonts
   - Or specify system fonts available in Linux

### Debug Your LaTeX
Test your LaTeX locally first:
```bash
tectonic document.tex
```

## License & Terms

This API is provided as-is for educational and personal use. For commercial use or SLA requirements, please deploy your own instance using the provided source code.

## Source Code

Full source code available at: https://github.com/JaedenRotondo/latex-server