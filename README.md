# LaTeX Compilation Service

A high-performance LaTeX to PDF compilation service with parallel processing support.

## Features

- 🚀 Parallel LaTeX compilation using ThreadPoolExecutor
- 📊 Built-in Prometheus metrics
- 🔄 Auto-cleanup of temporary files
- 🌐 CORS enabled for web integration
- 🏭 Production-ready with health checks
- 🐳 Dockerized with Tectonic engine

## API Endpoints

- `POST /compile` - Upload a .tex file and get a PDF back
- `GET /health` - Health check endpoint
- `GET /metrics` - Prometheus metrics
- `GET /` - Service info

## Quick Start

### Local Development
```bash
docker-compose up --build
```

### Production Deployment on Render

1. Push this repository to GitHub
2. Connect your GitHub account to Render
3. Click "New Web Service" and select your repository
4. Render will automatically detect the `render.yaml` configuration
5. Deploy!

## Usage Example

```bash
# Compile a LaTeX file
curl -X POST "https://your-app.onrender.com/compile" \
  -H "accept: application/pdf" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@document.tex" \
  --output document.pdf
```

## Environment Variables

- `PORT` - Server port (default: 8000)
- `PYTHONUNBUFFERED` - Disable Python output buffering
- `TECTONIC_CACHE_DIR` - Tectonic package cache directory

## Monitoring

Access metrics at `/metrics` endpoint for Prometheus scraping.

## License

MIT