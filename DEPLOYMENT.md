# Deployment Guide for LaTeX Compilation Service

This service supports parallel LaTeX compilation and can be deployed to various cloud platforms.

## Features
- Parallel LaTeX compilation using ThreadPoolExecutor
- Automatic cleanup of temporary files
- Health check endpoint for monitoring
- CORS enabled for Cloudflare integration
- Unique job IDs to prevent conflicts

## Deployment Options

### 1. Railway (Recommended)
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway up
```

### 2. Fly.io
```bash
# Install Fly CLI
curl -L https://fly.io/install.sh | sh

# Deploy
fly auth login
fly launch
fly deploy
```

### 3. Render
1. Push your code to GitHub
2. Connect your GitHub repo to Render
3. Render will auto-deploy using render.yaml

## Cloudflare Integration

After deploying to any platform above:

1. Get your service URL (e.g., `https://your-app.railway.app`)
2. In Cloudflare Dashboard:
   - Add a CNAME record pointing to your service
   - Enable "Proxied" status
   - Configure Page Rules for caching if needed

### Cloudflare Workers (Optional)
Create a worker to add caching or rate limiting:

```javascript
export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    url.hostname = 'your-app.railway.app';
    
    // Add caching for GET requests
    if (request.method === 'GET') {
      const cache = caches.default;
      const cachedResponse = await cache.match(request);
      if (cachedResponse) return cachedResponse;
    }
    
    const response = await fetch(url.toString(), request);
    return response;
  },
};
```

## Performance Tuning

### Adjusting Parallelism
Edit `main.py` to change the number of workers:
```python
executor = ThreadPoolExecutor(max_workers=8)  # Increase for more parallelism
```

### Scaling
- **Railway**: Upgrade to Pro plan for horizontal scaling
- **Fly.io**: Adjust `min_machines_running` in fly.toml
- **Render**: Change `minInstances` and `maxInstances` in render.yaml

## Monitoring
- Health endpoint: `GET /health`
- Root endpoint: `GET /`
- Metrics: Consider adding Prometheus metrics for production

## Security Considerations
1. Add rate limiting to prevent abuse
2. Implement file size limits
3. Consider adding authentication for production use
4. Use environment variables for sensitive configuration