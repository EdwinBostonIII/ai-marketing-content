# SPLANTS Marketing Engine - API Guide

## Quick Start

### 1. Authentication

All API requests require an API key in the header:

```bash
X-API-Key: your-api-key-here
```

### 2. Base URL

```
http://localhost:8080
```

### 3. Interactive Documentation

Visit `http://localhost:8080/docs` for interactive Swagger UI documentation.

## Core Endpoints

### Generate Content

**POST** `/v1/generate`

Generate AI-powered content with quality scoring and optimization.

#### Request Body

```json
{
  "content_type": "blog",
  "topic": "10 AI Marketing Tips for Small Business",
  "keywords": ["AI marketing", "small business", "automation"],
  "tone": "professional",
  "target_audience": "Small business owners",
  "platform": "blog",
  "length": 800,
  "include_hashtags": true,
  "seo_optimize": true,
  "generate_variants": false,
  "use_premium": false
}
```

#### Response

```json
{
  "id": 1,
  "content": "Your generated content here...",
  "quality_score": 0.92,
  "seo_score": 0.88,
  "metadata": {
    "word_count": 812,
    "reading_time": 4,
    "platform_optimized": "blog"
  },
  "generated_at": "2025-11-12T10:30:00Z",
  "cost_estimate": 0.03,
  "cached": false,
  "recommendations": [
    " Content quality is excellent!"
  ]
}
```

### List Content

**GET** `/v1/content`

Retrieve your generated content library.

#### Query Parameters

- `limit`: Number of results (1-100)
- `offset`: Pagination offset
- `content_type`: Filter by type
- `min_quality`: Minimum quality score (0-1)

### Publish Content

**POST** `/v1/publish`

Publish content to multiple platforms.

#### Request Body

```json
{
  "content_id": 1,
  "platforms": ["twitter", "linkedin"],
  "schedule_time": "2025-11-13T14:00:00Z",
  "auto_optimize_timing": true
}
```

## FREE Enhancement Endpoints

### Analytics Dashboard

**GET** `/v1/analytics/dashboard`

Get comprehensive analytics and ROI metrics.

#### Query Parameters

- `days`: Number of days to analyze (1-365)

#### Response Structure

```json
{
  "period_days": 30,
  "summary": {
    "total_content_generated": 150,
    "avg_quality_score": 0.87,
    "total_cost": 4.50
  },
  "content": {
    "by_type": [...],
    "by_platform": [...],
    "quality_distribution": {...}
  },
  "costs": {
    "total_cost": 4.50,
    "avg_cost_per_content": 0.03,
    "estimated_monthly": 45.00
  },
  "roi": {
    "cost_per_piece": 0.03,
    "pieces_per_dollar": 33.33,
    "estimated_time_saved_hours": 300
  }
}
```

### Content Templates

**GET** `/v1/templates`

List all available content templates.

**GET** `/v1/templates/{template_id}`

Get specific template details.

**POST** `/v1/templates/generate`

Generate content using a template.

### A/B Testing

**POST** `/v1/ab-test`

Create multiple content variants for testing.

**GET** `/v1/ab-test/{content_id}`

Get A/B test results and variants.

### Cost Control

**GET** `/v1/costs/usage`

Get detailed cost usage report with:
- Monthly spending
- Daily limits
- Projections
- Alerts

## Content Types

- `blog`: Blog posts (800-1500 words)
- `social_post`: Social media posts
- `email`: Email content
- `ad_copy`: Advertisement copy
- `landing_page`: Landing page content
- `video_script`: Video scripts
- `product_description`: E-commerce descriptions
- `press_release`: Press releases

## Platforms

- `blog`: Blog/website
- `twitter`: Twitter/X
- `linkedin`: LinkedIn
- `instagram`: Instagram
- `facebook`: Facebook
- `youtube`: YouTube
- `tiktok`: TikTok
- `pinterest`: Pinterest
- `email`: Email

## Tones

- `professional`: Business-appropriate
- `casual`: Relaxed and informal
- `enthusiastic`: Energetic and excited
- `conversational`: Natural dialogue
- `authoritative`: Expert and confident
- `friendly`: Warm and approachable
- `humorous`: Light and funny
- `inspirational`: Motivating

## Error Codes

| Code | Description | Solution |
|------|-------------|----------|
| 403 | Invalid API key | Check X-API-Key header |
| 404 | Resource not found | Verify endpoint/ID |
| 402 | Budget limit reached | Increase MONTHLY_AI_BUDGET |
| 429 | Rate limit exceeded | Wait before retrying |
| 500 | Server error | Check logs |

## Rate Limits

- Default: 100 requests/day (configurable via `DAILY_API_LIMIT`)
- Burst: 10 requests/minute

## Webhooks

Configure webhook URLs in `.env`:

```env
WEBHOOK_CONTENT_GENERATED_URL=https://hooks.zapier.com/...
WEBHOOK_CONTENT_PUBLISHED_URL=https://hooks.zapier.com/...
```

Events sent:
- `content_generated`: When content is created
- `content_published`: When content is published
- `budget_alert`: When approaching limits

## Best Practices

1. **Always include keywords** for better SEO scores
2. **Specify target audience** for more relevant content
3. **Use templates** for consistent quality
4. **Enable A/B testing** for emails and ads
5. **Monitor costs** regularly via `/v1/costs/usage`
6. **Use caching** (Redis) to reduce costs by 30-50%

## Example: Complete Workflow

```python
import requests

API_KEY = "your-api-key"
BASE_URL = "http://localhost:8080"

headers = {
    "X-API-Key": API_KEY,
    "Content-Type": "application/json"
}

# 1. Generate content
response = requests.post(
    f"{BASE_URL}/v1/generate",
    headers=headers,
    json={
        "content_type": "blog",
        "topic": "AI Marketing for Small Business",
        "keywords": ["AI", "marketing", "small business"],
        "tone": "professional",
        "length": 800
    }
)
content = response.json()
content_id = content["id"]

# 2. Publish to platforms
response = requests.post(
    f"{BASE_URL}/v1/publish",
    headers=headers,
    json={
        "content_id": content_id,
        "platforms": ["twitter", "linkedin"],
        "auto_optimize_timing": True
    }
)

# 3. Check analytics
response = requests.get(
    f"{BASE_URL}/v1/analytics/dashboard?days=7",
    headers=headers
)
analytics = response.json()
print(f"Total content: {analytics['summary']['total_content_generated']}")
print(f"Average quality: {analytics['summary']['avg_quality_score']}")
```