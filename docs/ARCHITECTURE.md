# Trending Tokens System Design

This document outlines a core architecture to support **displaying trending tokens** on the Bubblemaps homepage.
The goal is to compute and serve a "ranked list of tokens" based on "recent user interactions", specifically views of token maps via the frontend.

---

## Problem Statement

- Every time, we have a user view a token map on the homepage, a backend API call is made.
- These views reflect interest and engagement - we treat them as the basis for a "trending" score.
- We want to aggregate and score these views to identify <em>"trending tokens"</em>.
- Therefore our system must/should:
  - Aggregate these interactions (in this case, we may treat them as events) in near real-time and expose a lightweight API that the homepage can call to display trending tokens.
  - Handle high-volume, bursty traffic.
  - Update rankings in near- or true-real-time.
  - Serve a lightweight endpoint or WebSocket stream to power the homepage UI.
  - Our system should be fast enough to handle spikes in traffic and provide a smooth user experience (<10sec max., and ideally < a few ms).

---

## High-Level Architecture

<em>To be added later - Whimscial perhaps, Vim buffer isn't rendering my ascii on readme</em>

---

## Components

### 1. View Ingestion API
- **The Design**: API would follow a simple REST pattern, for example, `POST /api/v1/tokens/{token_address}/view`
- Then a lightweight handler (endpoint function) pushes view events into a queue.
- Keeps the request-response cycle fast — doesn’t block on processing.

### 2. Queue System (Ingestion Buffer)
- **Redis Streams**, **RabbitMQ**, or **Celery** (with Redis broker).
- Buffers incoming view events.
- Absorbs spikes in traffic and decouples ingestion from aggregation logic,
therefore we protects downstream systems.

### 3. Aggregation & Processing Worker
- Dequeues view events and increments counters in Redis.
- Uses keys like `trending:{hour}:{token_address} → count`.
- Enables time-based anaylsis (e.g., per-hour, per day).

### 4. Trending Ranking Service
- Periodic job (e.g., every 3-5 minutes) to compute trending scores.
- Computes trending scores using one or more of:
  - Total views in last N hours
  - Rate of change compared to previous period
  - Weighted scores based on freshness or uniqueness
- Writes ranked list to a Redis key like: `homepage:trending_tokens`.

### 5. Public Interface - Trending API Endpoint (API + WebSocket)

Here we have two ways of exposing the trending tokens to the frontend - each
with its own pros and cons. We may either  go with:

- **REST**: `GET /api/v1/tokens/trending`
  - Returns top-N tokens based on latest Redis result.
  - Fast enough to serve homepage directly.
- **WebSocket**: `WS /ws/trending`
  - Streams new trending updates to subscribed clients.
  - Enables real-time UX without polling.

---

## Tech Stack

| Component             | Tech                         | Why?                                                 |
|----------------------|------------------------------|------------------------------------------------------|
| API Layer            | FastAPI                      | Async, lightweight, perfect for high-throughput APIs |
| Queue/Broker         | Redis Streams / RabbitMQ     | Handles bursty traffic, decouples ingestion; simple and scalable     |
| Worker / Aggregator  | Python (Celery or custom)    | Scalable logic layer, flexible processing            |
| Store (trending)     | Redis | in-memory, fast counters, supports TTL/time windows    |
| Cache for homepage   | Redis | minimal latency access to top tokens                   |
| [Optional] long-term storage | PostgreSQL or ClickHouse | analytics, history, dashboards    |
| WebSocket Layer      | FastAPI w/ `websockets` or Starlette | Real-time client updates, minimal latency       |

---

## System Design Decisions

- **Event-driven ingestion** ensures write performance under load.
- **Time-based keys** allow for stronger trend scoring over time windows.
- **Redis-based aggregation** supports fast reads and real-time visibility.
- **WebSocket support** enables live updates without frontend polling.
- **Separation of concerns** (ingestion, aggregation, ranking, delivery) makes the system maintainable and scalable.

---

## Scaling Considerations

In the context of scaling, the following are some considerations we may yet make based on the information we have of the current progress of the system.
We are assumption that latency is although a 'primary' concern, throughput is our focus here, as we would be injesting the lots of this information and analzing it
alongside the user interaction (yes think of both as data sources for our injestion pipeline).

- Redis keys use TTLs or rolling window logic to bound memory usage.
- Queue depth and processing lag can be monitored and auto-scaled.
- API & workers can be containerized and deployted across replicas or (orchestrated with Kubernetes).
- WebSocket layer uses publish/subscribe (FastAPI's websocket's with a bit of tweaking) to fan out trending changes, and handle reconnecting sockets to connected clients.

---

## Future Considerations

- Normalize view scores (e.g. by token age, popularity baseline).
- Capture more metadata (for example, geo, session info, device type, or anything into our weighting algorithm).
- Ranking Algorithms, per-chain or per-category (DeFi, NFTs, etc.).
- Implement custom algorithms to track anomalies (such as sudden pump of obscure token).
- Persist historical trends to our ClickHouse storage for faster analytical throughput. We are also open to any other analytical DB for long-term insight.

---

## Summary

With our proposed design, the system enables us to dynamically surface trending tokens based on user engagement — with real-time responsiveness, high write throughput, and fast read access.

By relying on fast in-memory data structures for short-term analytics (Redis) and optionally streaming to longer-term storage (our ClickHouse db), we can support near real-time responsiveness for the user-facing homepage without sacrificing the ability to analyze trends over time. A beautiful step further is our WebSockets API,
**WebSockets**, of which we go beyond static updates and unlock a live, streaming experience that keeps the homepage fresh without unnecessary polling.
