# Premium Instagram Agency OS — Implementation Roadmap

## Phase 0 — Foundation
Goal: one client can be onboarded, measured and reviewed end-to-end.

Deliverables:
- multi-client workspace schema;
- client/brand/account registry;
- Instagram data adapter interface;
- Windsor.ai adapter;
- direct Meta adapter specification;
- daily account and media insight snapshots;
- content taxonomy;
- baseline and outlier calculations;
- approval model;
- executive dashboard specification.

Exit criteria:
- historical and current owned-account data ingest successfully;
- every analyzed post has comparable normalized metrics;
- system can identify top/bottom recent content without manual spreadsheet work.

## Phase 1 — Growth Intelligence MVP
Goal: the system recommends what to create next using evidence.

Deliverables:
- account audit report;
- rolling baseline engine;
- outlier detector;
- market/reference registry;
- compliant competitor research workflow;
- comment/audience-language clustering;
- hypothesis registry;
- next-best-content recommender;
- weekly Growth Director report.

Exit criteria:
- every recommendation cites observed evidence and confidence;
- every planned content item is linked to a hypothesis and primary metric;
- weekly review can explain what changed and what will be tested next.

## Phase 2 — Creative Production OS
Goal: turn growth hypotheses into production-ready content.

Deliverables:
- Creative Director agent;
- Reels/script agent;
- carousel agent;
- hook library and hook-performance history;
- shot list and edit-map generator;
- Google Drive production pack integration;
- versioning and client approval queue.

Exit criteria:
- approved brief can become a complete production pack without losing the hypothesis or target metric;
- content versions remain traceable from idea to published post.

## Phase 3 — Publishing + Measurement Loop
Goal: close the loop automatically after human approval.

Deliverables:
- Postiz publishing adapter;
- direct Meta publishing fallback;
- scheduled publishing jobs;
- snapshot collection at defined content ages;
- matched-cohort postmortem;
- winning-pattern library;
- scale / iterate / retire decisions.

Exit criteria:
- published content is automatically linked to its hypothesis, exact version and later results;
- no public post can publish without a valid approval state.

## Phase 4 — Premium Agency Operations
Goal: support 3-10 simultaneous premium clients.

Deliverables:
- client portal;
- permissions;
- approval SLA dashboard;
- team workload view;
- CRM adapter (Twenty optional);
- lead/outcome tracking;
- monthly client reports;
- billing/service package metadata;
- reusable agency playbooks by niche.

## Phase 5 — Optimization and AI Evaluation
Goal: make the agency smarter with every client while preserving client isolation.

Deliverables:
- Langfuse prompt/agent tracing;
- quality eval sets for hooks/scripts/strategy;
- prompt version comparison;
- experiment registry inspired by GrowthBook;
- model/cost monitoring;
- retrieval of proven mechanisms by niche, audience and goal;
- privacy-safe cross-client pattern library using abstractions rather than exposing client data.

## First dashboard screens
1. Agency Command Center
2. Client Overview
3. Account Audit
4. Content Performance
5. Market Map
6. Winning Patterns
7. Hypotheses
8. Creative Lab
9. Approval Queue
10. Calendar / Publishing
11. Weekly Growth Review
12. Business Outcomes

## First algorithms to implement

### Matched baseline
Filter by format and recent time window. Use median and percentiles before mean.

### Outlier detection
Use robust z-like score based on median absolute deviation plus percentile rank. Require minimum content age and denominator thresholds.

### Next-best-content score
Rank candidate hypotheses using:
- evidence confidence;
- expected metric upside;
- strategic relevance;
- audience fit;
- novelty;
- production cost;
- saturation penalty;
- risk penalty.

The score is a prioritization aid, not an autonomous publishing decision.

## Success criteria for the agency itself
The agency must be judged by client growth, not deliverable volume.

Track per client:
- rolling median reach by format;
- shares per 1,000 reached;
- saves per 1,000 reached;
- comments per 1,000 reached;
- follower growth;
- proportion of posts above prior-period median;
- percentage of hypotheses that produced actionable learning;
- qualified leads/revenue where connected.

Agency-level quality:
- time from insight to approved content;
- percentage of recommendations backed by evidence;
- publishing error rate;
- client approval turnaround;
- percentage of winning mechanisms successfully repeated without audience fatigue.

## Build principle
Do not build commodity infrastructure when a mature service can sit behind an adapter. Own the decision layer, growth intelligence, client experience, creative methodology and evidence graph.
