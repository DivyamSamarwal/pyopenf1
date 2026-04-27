# Advanced Usage

The `pyopenf1` client is designed for production use, meaning it includes robust defenses against API unreliability, strict rate limits, and network latency.

## Engine Architecture

When you make a request (e.g., `client.drivers.get_drivers()`), the request passes through several layers of defense before it actually hits the OpenF1 servers:

```mermaid
flowchart TD
    A[Your Code] --> B[Domain Endpoint (e.g., drivers)]
    B --> C{TTL Cache}
    C -->|Cache Hit| A
    C -->|Cache Miss| D[Token Bucket Rate Limiter]
    D --> E[Tenacity Retry Engine]
    E --> F[httpx AsyncClient]
    F -->|HTTP 429 / 503| E
    F -->|HTTP 200| G[Pydantic V2 Parser]
    G --> C
```

## Configuring the Client

You can tune the exact behavior of the engine by passing arguments to the Client constructor.

```python
async with AsyncOpenF1Client(
    cache_ttl=300.0,        # Cache responses for 5 minutes
    max_retries=5,          # Retry up to 5 times on errors
    max_per_second=6.0,     # Rate limit: 6 req/s
    max_per_minute=60.0,    # Rate limit: 60 req/min
) as client:
    pass
```

### Rate Limiting

The OpenF1 API heavily enforces rate limits (often resulting in `429 Too Many Requests`). 
To prevent your script from being temporarily banned, the client uses an internal **Token Bucket Algorithm**.

It will seamlessly `await asyncio.sleep()` to pause your code *just long enough* to comply with the rate limit, before releasing the request.

### TTL Caching

By default, caching is disabled (`cache_ttl=0.0`). 

If you are building a dashboard or running an analysis loop that fetches the same session data multiple times, you should enable the cache. 

> [!NOTE]
> Historical Formula 1 data is immutable (it never changes after the race is over). If you are fetching data from a past year, setting a massive `cache_ttl` will drastically speed up your scripts and reduce load on the OpenF1 servers.
