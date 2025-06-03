from prometheus_client import Counter, Histogram, Gauge, generate_latest
from fastapi import Request, Response
import time
import psutil

# Metrics
compilation_requests = Counter('latex_compilation_requests_total', 'Total LaTeX compilation requests')
compilation_errors = Counter('latex_compilation_errors_total', 'Total LaTeX compilation errors')
compilation_duration = Histogram('latex_compilation_duration_seconds', 'LaTeX compilation duration')
active_compilations = Gauge('latex_active_compilations', 'Number of active compilations')
cpu_usage = Gauge('latex_cpu_usage_percent', 'CPU usage percentage')
memory_usage = Gauge('latex_memory_usage_percent', 'Memory usage percentage')

def track_system_metrics():
    """Update system metrics"""
    cpu_usage.set(psutil.cpu_percent())
    memory_usage.set(psutil.virtual_memory().percent)

async def metrics_middleware(request: Request, call_next):
    """Middleware to track metrics"""
    if request.url.path == "/compile":
        compilation_requests.inc()
        start_time = time.time()
        active_compilations.inc()
        
        try:
            response = await call_next(request)
            if response.status_code >= 400:
                compilation_errors.inc()
            return response
        finally:
            compilation_duration.observe(time.time() - start_time)
            active_compilations.dec()
    else:
        return await call_next(request)

async def metrics_endpoint():
    """Prometheus metrics endpoint"""
    track_system_metrics()
    return Response(generate_latest(), media_type="text/plain")