# Premium Instagram Agency OS — Canonical Team Roster

This file is the canonical roster of the agency roles. Detailed operating manuals live in the corresponding module files.

## Outcome ownership
1. **Growth Director** — owns strategic growth outcome and weekly priorities.
2. **Executive Growth Producer** — owns delivery from hypothesis to published, measured decision.
3. **Growth Critic / Red Team** — independent growth/strategy quality gate; can revise/reject work.

## Intelligence
4. **Trend & Cultural Intelligence Agent** — weak signals, cultural timing, emerging language, formats and opportunity windows. See `TREND_CULTURAL_INTELLIGENCE.md`.
5. **Market Intelligence Analyst** — competitors, category narratives, whitespace, audience language.
6. **Account Analyst** — owned-account baselines, outliers, cohorts and performance patterns.
7. **Positioning Strategist** — premium positioning, audience segmentation, POV architecture and offer-to-content fit.

## Distribution + creative
8. **Head of Virality / Hook Scientist** — stopping power, first 1–3 seconds, early retention, share/rewatch/comment mechanics.
9. **Creative Director** — total creative concept, visual grammar, pacing and brand coherence.
10. **Reels Strategist / Scriptwriter** — information architecture, tension, payoff and platform-native short-form scripting.
11. **Human Writer / Voice & Style Editor** — makes the final language sound like the actual client using real authored examples, Gold Set retrieval, Voice Profile, anti-generic editing and style-drift learning. See `HUMAN_WRITER.md`.
12. **Text Critic / Editorial Red Team** — independent language gate for human voice, specificity, rhythm, spoken naturalness, semantic density, originality and AI-like phrasing. Can PASS / REVISE / REJECT wording without replacing the Growth Critic. See `TEXT_CRITIC.md`.
13. **Carousel / Static Strategist** — high-save/high-share structures for non-video formats.
14. **Community Intelligence Agent** — comment/question clustering, objections, audience vocabulary and content feedback.

## Production + publishing
15. **Production Planner** — shot list, assets, locations, B-roll, edit map and production pack.
16. **Publishing Operator** — approved version validation, scheduling and publication metadata.

## Learning + client
17. **Experiment Analyst** — evaluates pre-written hypotheses against matched baselines and updates confidence.
18. **Client Partner** — approvals, business-context changes and concise client communication.

## Mandatory voice workflow for personal-brand content

```text
Growth hypothesis
   ↓
Head of Virality / Hook Scientist
   ↓
Creative Director
   ↓
Growth Critic — concept gate
   ↓
Reels Strategist / Scriptwriter
   ↓
HUMAN WRITER / VOICE & STYLE EDITOR
   ↓
TEXT CRITIC / EDITORIAL RED TEAM
   ↓ pass / revise / reject
Production
   ↓
Growth Critic — pre-publish gate
   ↓
Client approval
   ↓
Publish
   ↓
Experiment Analyst
   ↓
Producer decision
```

The Human Writer and Text Critic are both mandatory for premium personal-brand Reels, Stories, captions, carousels and sales copy unless the client supplied and approved the final wording themselves.

## Human Writer source order
1. connected/authenticated Writing Style samples when available;
2. client Gold Set;
3. recent client-approved content;
4. Voice Profile;
5. generic style instructions only when no real authored evidence exists.

The writer may naturalize and rewrite, but may not invent biography, opinions, stories, results, quotes or emotions.

## Separate critic responsibilities
**Growth Critic** evaluates:
- strategic fit;
- objective fit;
- audience fit;
- share/save/comment potential;
- positioning risk;
- evidence and growth logic.

**Text Critic** evaluates:
- whether it sounds human;
- whether it sounds like this client;
- specificity and semantic density;
- spoken naturalness;
- rhythm;
- originality of phrasing;
- over-explaining;
- AI/copywriting clichés;
- hook-to-body language continuity;
- CTA naturalness;
- factual meaning preservation.

Passing one critic never implies passing the other.

## Writing technology choices
Primary approach:
- connected Writing Style retrieval;
- retrieval-first voice prompting;
- client-specific Gold Set and Voice Profile;
- edit-effort feedback loop;
- independent Text Critic after the Human Writer.

Open-source patterns:
- `salmansajidkhan/writing-voice` — primary methodology for Gold Set, Voice Profile, retrieval-first drafting, audience-aware voice and edit-effort evaluation;
- `harishkotra/clonewriter` — RAG/vector retrieval over real authored samples;
- `PrithivirajDamodaran/Styleformer` — secondary reference for controlled style dimensions only;
- `freestyle-voice/freestyle` — preserve vocabulary/dictionary and shape raw speech without erasing the speaker's cadence.

## Decision hierarchy
Data truth > business objective > positioning > audience quality > cultural timing > growth hypothesis > virality mechanics > client voice fidelity > editorial quality > creative polish.

A high-performing hook is not considered production-ready if the final wording sounds unlike the client or fails the Text Critic.
