# Premium Instagram Agency OS — Data Model

## Design principle
Multi-client, provider-neutral, evidence-first. Raw source data is retained separately from normalized metrics and strategic annotations.

## Workspace entities

### clients
- id
- name
- status
- timezone
- primary_market
- business_model
- primary_goal
- created_at

### brands
- id
- client_id
- brand_name
- positioning_summary
- audience_summary
- voice_rules
- visual_rules
- claim_rules
- prohibited_topics

### social_accounts
- id
- client_id
- provider
- platform
- external_account_id
- handle
- account_type
- connection_status
- data_provider
- publishing_provider

### account_daily_snapshots
- account_id
- snapshot_date
- followers
- follows
- media_count
- reach
- views
- profile_actions
- raw_payload_ref

### content_items
- id
- client_id
- platform
- external_media_id
- content_type
- published_at
- caption
- permalink
- duration_seconds
- campaign_id
- hypothesis_id
- approval_id

### content_feature_tags
- content_item_id
- topic
- pillar
- hook_family
- first_frame_type
- speaking_style
- emotional_driver
- audience_segment
- awareness_level
- cta_type
- offer_id
- production_level
- visual_setting
- trend_audio_id
- custom_tags

### media_insight_snapshots
- content_item_id
- captured_at
- content_age_hours
- reach
- views
- plays
- likes
- comments
- saves
- shares
- reposts
- total_interactions
- profile_actions
- watch_time
- avg_watch_time
- raw_payload_ref

### hypotheses
- id
- client_id
- statement
- audience_segment
- primary_metric
- secondary_metrics
- baseline_definition
- minimum_age_hours
- status
- created_at
- decision
- decision_notes

### experiments
Organic Instagram comparisons are observational unless a true randomized mechanism exists.
- id
- hypothesis_id
- design_type
- cohort_definition
- start_date
- end_date
- confidence
- confounders
- result_summary

### market_entities
- id
- client_id
- handle_or_name
- relationship_type: direct_competitor / aspirational / adjacent / reference
- public_source
- notes

### market_observations
- market_entity_id
- observed_at
- observation_type
- value
- source_url
- confidence

### creative_briefs
- id
- hypothesis_id
- audience_segment
- target_behavior
- hook_options
- core_tension
- payoff
- evidence
- format
- production_notes
- primary_metric
- status

### assets
- id
- client_id
- content_item_id
- provider
- external_file_id
- mime_type
- role
- checksum

### approvals
- id
- client_id
- object_type
- object_id
- requested_at
- approved_at
- approved_by
- state
- notes

### publications
- content_item_id
- provider
- scheduled_at
- published_at
- provider_job_id
- status
- error_code

### leads / outcomes
Optional business layer.
- id
- client_id
- occurred_at
- source_content_item_id
- source_confidence
- event_type
- value
- currency
- status

## Derived metrics
Derived metrics must be calculated from raw/normalized fields, not written as source truth.

Examples:
- shares_per_1000_reached = shares / reach * 1000
- saves_per_1000_reached = saves / reach * 1000
- comments_per_1000_reached = comments / reach * 1000
- interactions_per_1000_reached = total_interactions / reach * 1000
- follower_growth_rate = delta_followers / prior_followers
- content_percentile_within_format
- robust_outlier_score

All calculations must safely handle zero/null denominators and metric availability differences.

## Provenance
Every imported record stores:
- provider;
- ingestion timestamp;
- API/source version if available;
- raw payload reference;
- transformation version.

This allows us to reprocess data when Instagram metric definitions change.

## Tenant isolation
Every business object includes client_id/workspace scope. Credentials are not stored in content records and never committed to Git.
