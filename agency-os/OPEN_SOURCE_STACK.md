# Premium Instagram Agency OS — Open-source stack review

Date: 2026-10-07

## Goal
Build an outcome-driven premium Instagram growth agency. The system is optimized for measurable growth in reach, views, shares/reposts, saves, comments, profile actions and follower growth — not for producing a fixed number of posts.

## What we borrow and what we do not

### 1. builderz-labs/marketing-dashboard — MIT — adopt the control-center pattern
Use:
- operator-led mission control;
- CRM/content/analytics/approvals/automation in one interface;
- explicit human approval gates;
- local/private-first credential boundaries.

Do not depend on it as the whole product: it is alpha and broader than our Instagram-first use case.

### 2. tenfoldmarc/content-dashboard — MIT — adopt the growth loop
Use:
- own-post analytics;
- outlier detection;
- hook mining;
- content idea -> script -> publish -> measure loop;
- Google Drive production queue patterns;
- configurable brand voice.

Change:
- competitor collection must prefer Meta Business Discovery and compliant public web research; no fragile or ToS-risky scraping as a core dependency.
- replace creator-only assumptions with multi-client agency workspaces and approvals.

### 3. cbsshekhawat18-lab/social-stats-social-media-manager — MIT — adopt multi-client operations
Use:
- client workspaces;
- granular permissions;
- approval flows;
- analytics/reporting structure;
- unified inbox concepts;
- scheduled background sync.

Do not copy its breadth into MVP. WhatsApp bots, marketplace and unrelated modules are phase 3+.

### 4. gitroomhq/postiz-app — AGPL-3.0 — run as a separate publishing service
Use:
- social account connections;
- scheduling/publishing;
- API/webhooks;
- optional analytics surfaces;
- agent/MCP-ready publishing surface.

Boundary:
- do not vendor Postiz code into our proprietary core. Treat it as an external service behind a publishing adapter.

### 5. inovector/mixpost — MIT Lite — reference implementation / optional publisher
Use:
- calendar and queue patterns;
- post versions per network;
- media library;
- templates and hashtag groups.

Because the Lite code is MIT, specific implementation patterns may be reused with attribution where appropriate. Team/approval features may live in paid editions; verify before relying on them.

### 6. skeeven/Instagram-Analytics-Dashboard — reference analytics collector
Use the data model pattern:
- daily follower snapshots;
- post table;
- per-media per-day insight snapshots;
- current metrics such as views, reach, saves, shares and total interactions;
- resilient handling of metric differences by media type.

### 7. Meta Instagram API — source of truth for owned accounts
Use official OAuth and professional-account APIs for:
- own media and insights;
- publishing;
- comments where approved;
- profile/account insights;
- Business Discovery for public professional competitors where supported.

Never make unofficial scraping the primary data path.

### 8. Windsor.ai Instagram connector — production data adapter
Use as an optional fast connector for clients who connect their Instagram account:
- historical reads;
- account-specific fields;
- date filtering;
- scheduled exports;
- formula fields.

Keep our schema provider-neutral so we can switch between Windsor.ai and direct Meta API.

### 9. Activepieces — MIT core — preferred workflow automation layer
Why preferred over n8n for the product core:
- permissive MIT core;
- self-hostable;
- agent/MCP-friendly integration model.

n8n can still be used internally for agency-owned workflows, but its Sustainable Use License imposes restrictions if clients are allowed to configure automations through our product.

### 10. GrowthBook — MIT core — borrow experimentation discipline
Instagram organic content is not a true randomized A/B environment. We therefore borrow:
- hypothesis registry;
- experiment metadata;
- baseline comparison;
- sequential decision discipline;
- guardrails against declaring winners from one lucky post.

We do NOT label organic post comparisons as randomized A/B tests.

### 11. Langfuse — MIT core — AI quality layer
Use for:
- prompt/version tracing;
- agent traces;
- evaluation sets;
- comparing script/hook generation quality;
- cost/latency monitoring.

### 12. Open Agency OS (Aperture) — integration architecture pattern
Borrow the principle:
- mature services remain separate;
- events and APIs connect them;
- our core owns orchestration and client experience, not every commodity feature.

## Selected v1 architecture

Core application:
- Next.js/TypeScript UI and API;
- PostgreSQL/Supabase-compatible data model;
- object storage for media references;
- provider adapters for Instagram data and publishing.

External/adapted services:
- Instagram data: Windsor.ai first OR direct Meta Graph API;
- publishing: Postiz service adapter, with direct Meta publisher fallback;
- automation: Activepieces for product workflows;
- AI observability: Langfuse;
- files/assets: Google Drive integration;
- optional CRM later: Twenty as a separate AGPL service;
- optional nurture later: Mautic as a separate service.

## Non-negotiables
- No autonomous public publishing by default; client approval is required.
- No fake engagement, follow/unfollow bots, bought comments, purchased followers, engagement pods or credential scraping.
- No claim of causality from one post.
- Every recommendation must cite the data window, baseline and sample size.
- Client data is isolated per workspace.
- Tokens and secrets never live in Git.
- Growth decisions are based on normalized performance, not raw vanity metrics alone.

## Повторная проверка — 10 октября 2026

[Обзор v2](v2/research/OPEN_SOURCE_REVIEW.md) и [манифест источников](v2/research/SOURCE_MANIFEST.json) фиксируют прочитанные README, blob SHA и конкретные подходы. Проверка не включает установку, аудит кода или доказательство результата роста. Добавлены паттерны событийной аналитики PostHog, разделения загрузки/преобразования Airbyte и аналитики поста/аккаунта/ссылки Ayrshare; эти сервисы не подключались.
