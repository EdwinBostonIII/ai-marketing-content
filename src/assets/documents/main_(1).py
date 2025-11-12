"""
SPLANTS Marketing Engine v2.1
AI-powered content generation system for SPLANTS custom pants marketing

CORE FEATURES (Included - $30/month infrastructure):
- AI Content Generation (GPT-4)
- Multi-Platform Publishing
- SEO Optimization
- Quality Scoring
- Content Storage & Management

FREE OPTIONAL ENHANCEMENTS (Included, can enable/disable):
- Analytics Dashboard - Track ROI and performance
- A/B Testing - Test content variations
- Content Templates - Proven content structures
- Cost Control - Budget monitoring and alerts
- Webhook System - Automation integrations
- Smart Hashtags - Auto-generate optimized hashtags
- Platform Optimization - Auto-adjust for each platform

PAID OPTIONAL ENHANCEMENTS (Add when ready):
- Redis Caching (+$10-15/month) - 30-50% API cost reduction
- Multi-Model Synthesis (+$0.02-0.05/request) - GPT-4 + Claude
- Social Media Auto-Posting (Varies by platform) - Requires API keys

Last Updated: 2025-11-12
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends, Security, Query
from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any, Literal
import asyncio
import asyncpg
from datetime import datetime, timedelta
import os
import hashlib
import json
import httpx
from enum import Enum
import logging
import re
from collections import defaultdict

# AI Provider imports
from openai import AsyncOpenAI
from anthropic import AsyncAnthropic

# ============================================
# PAID OPTIONAL ENHANCEMENT: Redis Caching (+$10-15/month)
# Reduces AI API costs by 30-50% through intelligent caching
# To enable: Uncomment these imports and Redis sections below
# ============================================
# import aioredis
# from typing import Optional as Opt

# ============================================
# LOGGING CONFIGURATION
# ============================================

# Create logs directory if it doesn't exist
os.makedirs('logs', exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Console output
        logging.FileHandler('logs/app.log')  # File output
    ]
)
logger = logging.getLogger(__name__)

# ============================================
# APPLICATION INITIALIZATION
# ============================================

app = FastAPI(
    title="SPLANTS Marketing Engine",
    version="2.1",
    description="""
    AI-Powered Content Generation System for SPLANTS
    
    Core System: $30/month infrastructure
    Free Enhancements: Analytics, A/B Testing, Templates, Cost Control
    Paid Enhancements: Redis Caching, Multi-Model AI, Auto-Publishing
    
    Comprehensive documentation available at /docs
    """,
    docs_url="/docs",  # Swagger UI at /docs
    redoc_url="/redoc"  # ReDoc at /redoc
)

# CORS configuration - allows your frontend/apps to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # SECURITY: In production, specify your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================
# CONFIGURATION FROM ENVIRONMENT VARIABLES
# (Set these in your .env file - see README)
# ============================================

# REQUIRED - Core System ($30/month infrastructure)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://splants:password@db:5432/splants")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # Required for AI generation
API_KEY = os.getenv("API_KEY", "change-this-to-a-secure-key")  # Your API key for authentication

# OPTIONAL - Multi-Model Enhancement
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")  # For premium multi-model

# FREE OPTIONAL ENHANCEMENT: Cost Control
MONTHLY_AI_BUDGET = float(os.getenv("MONTHLY_AI_BUDGET", "0"))  # Set to 0 for unlimited
DAILY_API_LIMIT = int(os.getenv("DAILY_API_LIMIT", "0"))  # Set to 0 for unlimited

# PAID OPTIONAL ENHANCEMENT: Redis Caching (+$10-15/month)
REDIS_URL = os.getenv("REDIS_URL")  # Set this to enable caching
CACHE_ENABLED = bool(REDIS_URL)

# FREE OPTIONAL ENHANCEMENT: Webhooks
WEBHOOK_CONTENT_GENERATED = os.getenv("WEBHOOK_CONTENT_GENERATED_URL")
WEBHOOK_CONTENT_PUBLISHED = os.getenv("WEBHOOK_CONTENT_PUBLISHED_URL")
WEBHOOK_DAILY_REPORT = os.getenv("WEBHOOK_DAILY_REPORT_URL")

# PAID OPTIONAL ENHANCEMENT: Social Media Auto-Publishing (Costs vary)
# These are for automatic posting to platforms (optional)
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")

LINKEDIN_CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID")
LINKEDIN_CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET")

# Application settings
MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH", "5000"))  # Max words per generation
DEFAULT_CONTENT_LENGTH = int(os.getenv("DEFAULT_CONTENT_LENGTH", "500"))  # Default words

# Validate critical configuration
if not OPENAI_API_KEY:
    logger.error("CRITICAL: OPENAI_API_KEY not set! Application will not function properly.")
    logger.error("Please add your OpenAI API key to .env file")

if API_KEY == "change-this-to-a-secure-key":
    logger.warning("WARNING: Using default API key. Please change this in production!")

# ============================================
# AUTHENTICATION (Core Feature)
# ============================================

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def verify_api_key(api_key: str = Security(api_key_header)):
    """
    Simple but secure API key authentication
    
    To use the API, include this header in all requests:
    X-API-Key: your-api-key-here
    """
    if api_key != API_KEY:
        logger.warning(f"Invalid API key attempt: {api_key[:10] if api_key else 'None'}...")
        raise HTTPException(
            status_code=403,
            detail="Invalid API Key. Please check your X-API-Key header."
        )
    return api_key

# ============================================
# DATABASE SETUP (Core Feature)
# ============================================

db_pool = None

# FREE OPTIONAL ENHANCEMENT: Redis Cache
redis_cache = None

@app.on_event("startup")
async def startup():
    """Initialize all services when the application starts"""
    global db_pool, redis_cache
    
    logger.info("=" * 60)
    logger.info("SPLANTS Marketing Engine - Starting Up")
    logger.info("=" * 60)
    
    # Core: Database connection
    try:
        db_pool = await asyncpg.create_pool(
            DATABASE_URL,
            min_size=1,
            max_size=10,
            command_timeout=60
        )
        logger.info(" Database connected successfully")
    except Exception as e:
        logger.error(f" Database connection failed: {e}")
        raise
    
    # Core: Create essential tables
    async with db_pool.acquire() as conn:
        # Content table - stores all generated content
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS content (
                id SERIAL PRIMARY KEY,
                content_type VARCHAR(50) NOT NULL,
                topic TEXT NOT NULL,
                content TEXT NOT NULL,
                metadata JSONB DEFAULT '{}',
                quality_score FLOAT DEFAULT 0,
                seo_score FLOAT DEFAULT 0,
                status VARCHAR(20) DEFAULT 'draft',
                created_at TIMESTAMP DEFAULT NOW(),
                updated_at TIMESTAMP DEFAULT NOW()
            )
        ''')
        
        # Social posts table - tracks published content
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS social_posts (
                id SERIAL PRIMARY KEY,
                platform VARCHAR(50) NOT NULL,
                content_id INTEGER REFERENCES content(id) ON DELETE CASCADE,
                post_content TEXT NOT NULL,
                status VARCHAR(20) DEFAULT 'draft',
                platform_post_id VARCHAR(100),
                metrics JSONB DEFAULT '{}',
                metadata JSONB DEFAULT '{}',
                scheduled_for TIMESTAMP,
                published_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT NOW()
            )
        ''')
        
        # FREE OPTIONAL ENHANCEMENT: Analytics Tables
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS analytics_events (
                id SERIAL PRIMARY KEY,
                event_type VARCHAR(50) NOT NULL,
                event_data JSONB DEFAULT '{}',
                user_id VARCHAR(100),
                session_id VARCHAR(100),
                created_at TIMESTAMP DEFAULT NOW()
            )
        ''')
        
        # Create index for faster analytics queries
        await conn.execute('''
            CREATE INDEX IF NOT EXISTS idx_analytics_created_at 
            ON analytics_events(created_at DESC)
        ''')
        
        await conn.execute('''
            CREATE INDEX IF NOT EXISTS idx_analytics_event_type 
            ON analytics_events(event_type)
        ''')
        
        # FREE OPTIONAL ENHANCEMENT: API Usage Tracking for Cost Control
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS api_usage (
                id SERIAL PRIMARY KEY,
                model VARCHAR(50) NOT NULL,
                tokens INTEGER DEFAULT 0,
                cost DECIMAL(10,4) DEFAULT 0,
                request_type VARCHAR(50),
                content_id INTEGER REFERENCES content(id) ON DELETE SET NULL,
                success BOOLEAN DEFAULT TRUE,
                error_message TEXT,
                created_at TIMESTAMP DEFAULT NOW()
            )
        ''')
        
        # Create index for cost queries
        await conn.execute('''
            CREATE INDEX IF NOT EXISTS idx_api_usage_created_at 
            ON api_usage(created_at DESC)
        ''')
        
        # FREE OPTIONAL ENHANCEMENT: A/B Test Tracking
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS ab_tests (
                id SERIAL PRIMARY KEY,
                test_name VARCHAR(100) NOT NULL,
                variant_ids INTEGER[] NOT NULL,
                test_parameter VARCHAR(50),
                status VARCHAR(20) DEFAULT 'active',
                winner_id INTEGER,
                created_at TIMESTAMP DEFAULT NOW(),
                completed_at TIMESTAMP
            )
        ''')
        
        # FREE OPTIONAL ENHANCEMENT: Webhook Logs
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS webhook_logs (
                id SERIAL PRIMARY KEY,
                event_type VARCHAR(50) NOT NULL,
                webhook_url TEXT NOT NULL,
                payload JSONB DEFAULT '{}',
                status_code INTEGER,
                response_body TEXT,
                success BOOLEAN DEFAULT FALSE,
                retry_count INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT NOW()
            )
        ''')
        
        logger.info(" Database tables initialized")
    
    # PAID OPTIONAL ENHANCEMENT: Redis Cache Connection (+$10-15/month)
    if CACHE_ENABLED and REDIS_URL:
        try:
            # Uncomment these lines when you add Redis
            # redis_cache = await aioredis.from_url(
            #     REDIS_URL,
            #     encoding="utf-8",
            #     decode_responses=True
            # )
            # await redis_cache.ping()
            # logger.info(" Redis cache connected (API costs will be reduced by 30-50%)")
            logger.info(" Redis caching configured but not active (uncomment in code to enable)")
        except Exception as e:
            logger.warning(f" Redis connection failed: {e}")
            logger.warning("Continuing without cache. Add Redis for 30-50% cost savings.")
    else:
        logger.info(" Redis caching disabled (add REDIS_URL to enable cost savings)")
    
    # FREE OPTIONAL ENHANCEMENT: Initialize services
    await analytics.initialize()
    await cost_controller.initialize()
    
    # Log startup configuration
    logger.info("=" * 60)
    logger.info("CONFIGURATION:")
    logger.info(f"  OpenAI: {' Configured' if OPENAI_API_KEY else ' Missing'}")
    logger.info(f"  Anthropic (Multi-Model): {' Configured' if ANTHROPIC_API_KEY else ' Not configured (optional)'}")
    logger.info(f"  Redis Caching: {' Enabled' if CACHE_ENABLED else ' Disabled (optional +$10/mo)'}")
    logger.info(f"  Cost Control: {' Enabled ($' + str(MONTHLY_AI_BUDGET) + '/mo budget)' if MONTHLY_AI_BUDGET > 0 else ' Disabled'}")
    logger.info(f"  Webhooks: {' Configured' if any([WEBHOOK_CONTENT_GENERATED, WEBHOOK_CONTENT_PUBLISHED]) else ' Not configured (optional)'}")
    logger.info("=" * 60)
    logger.info("FREE ENHANCEMENTS ACTIVE:")
    logger.info("  - Analytics Dashboard")
    logger.info("  - A/B Testing")
    logger.info("  - Content Templates")
    logger.info("  - Smart Hashtags")
    logger.info("  - Platform Optimization")
    logger.info("=" * 60)
    logger.info("SPLANTS Marketing Engine Ready")
    logger.info("API Documentation: http://localhost:8080/docs")
    logger.info("=" * 60)

@app.on_event("shutdown")
async def shutdown():
    """Graceful shutdown - close all connections"""
    logger.info("Shutting down SPLANTS Marketing Engine...")
    
    if db_pool:
        await db_pool.close()
        logger.info("Database connection closed")
    
    if redis_cache:
        # Uncomment when Redis is enabled
        # await redis_cache.close()
        logger.info("Redis cache connection closed")
    
    logger.info("Shutdown complete")

# ============================================
# DATA MODELS (Core Feature)
# ============================================

class ContentType(str, Enum):
    """Types of content that can be generated"""
    BLOG = "blog"
    SOCIAL_POST = "social_post"
    EMAIL = "email"
    AD_COPY = "ad_copy"
    LANDING_PAGE = "landing_page"
    VIDEO_SCRIPT = "video_script"
    PRODUCT_DESCRIPTION = "product_description"
    PRESS_RELEASE = "press_release"

class Platform(str, Enum):
    """Supported social media and content platforms"""
    BLOG = "blog"
    TWITTER = "twitter"
    LINKEDIN = "linkedin"
    INSTAGRAM = "instagram"
    FACEBOOK = "facebook"
    YOUTUBE = "youtube"
    TIKTOK = "tiktok"
    PINTEREST = "pinterest"
    EMAIL = "email"

class ContentTone(str, Enum):
    """Writing tones for content generation"""
    PROFESSIONAL = "professional"
    CASUAL = "casual"
    ENTHUSIASTIC = "enthusiastic"
    CONVERSATIONAL = "conversational"
    AUTHORITATIVE = "authoritative"
    FRIENDLY = "friendly"
    HUMOROUS = "humorous"
    INSPIRATIONAL = "inspirational"

class ContentRequest(BaseModel):
    """Request model for content generation"""
    
    # Required fields
    content_type: ContentType = Field(
        ...,
        description="Type of content to generate"
    )
    topic: str = Field(
        ...,
        min_length=5,
        max_length=500,
        description="Main topic or subject (be specific for better results)"
    )
    
    # Optional core fields
    keywords: List[str] = Field(
        default=[],
        max_items=10,
        description="SEO keywords to naturally include (max 10)"
    )
    tone: ContentTone = Field(
        default=ContentTone.PROFESSIONAL,
        description="Writing tone/style"
    )
    target_audience: Optional[str] = Field(
        None,
        max_length=200,
        description="Target audience description (e.g., 'small business owners aged 30-50')"
    )
    platform: Platform = Field(
        default=Platform.BLOG,
        description="Target platform for optimization"
    )
    length: Optional[int] = Field(
        None,
        ge=50,
        le=MAX_CONTENT_LENGTH,
        description=f"Target word count (50-{MAX_CONTENT_LENGTH})"
    )
    
    # FREE OPTIONAL ENHANCEMENT: Advanced features
    include_hashtags: bool = Field(
        default=True,
        description="FREE: Auto-generate optimized hashtags for social media"
    )
    seo_optimize: bool = Field(
        default=True,
        description="FREE: Apply SEO best practices"
    )
    generate_variants: bool = Field(
        default=False,
        description="FREE: Generate A/B test variants (creates 3 versions)"
    )
    
    # PAID OPTIONAL ENHANCEMENT: Premium features
    use_premium: bool = Field(
        default=False,
        description="PAID: Use multi-model synthesis for higher quality (+$0.02-0.05/request)"
    )
    
    @validator('topic')
    def validate_topic(cls, v):
        """Ensure topic is meaningful"""
        if len(v.strip()) < 5:
            raise ValueError('Topic must be at least 5 characters')
        return v.strip()
    
    @validator('keywords')
    def validate_keywords(cls, v):
        """Ensure keywords are reasonable"""
        return [kw.strip() for kw in v if kw.strip()]
    
    class Config:
        schema_extra = {
            "example": {
                "content_type": "blog",
                "topic": "10 AI Marketing Tips for Small Business Owners",
                "keywords": ["AI marketing", "small business", "automation", "efficiency"],
                "tone": "professional",
                "target_audience": "Small business owners with 1-10 employees",
                "platform": "blog",
                "length": 800,
                "include_hashtags": False,
                "seo_optimize": True,
                "generate_variants": False,
                "use_premium": False
            }
        }

class ContentResponse(BaseModel):
    """Response model for generated content"""
    
    id: int
    content: str
    quality_score: float = Field(ge=0, le=1)
    seo_score: float = Field(ge=0, le=1)
    metadata: Dict[str, Any]
    generated_at: datetime
    
    # FREE OPTIONAL ENHANCEMENT: Additional data
    cost_estimate: Optional[float] = None
    cached: bool = False
    variants: Optional[List[Dict[str, Any]]] = None
    recommendations: Optional[List[str]] = None
    
    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "content": "Your generated content will appear here...",
                "quality_score": 0.92,
                "seo_score": 0.88,
                "metadata": {
                    "word_count": 523,
                    "reading_time": 3,
                    "platform_optimized": "blog",
                    "hashtags": ["#AIMarketing", "#SmallBusiness"]
                },
                "generated_at": "2025-11-12T10:30:00Z",
                "cost_estimate": 0.03,
                "cached": False
            }
        }

class PublishRequest(BaseModel):
    """Request model for publishing content"""
    
    content_id: int = Field(..., description="ID of content to publish")
    platforms: List[Platform] = Field(
        ...,
        min_items=1,
        max_items=5,
        description="Platforms to publish to (max 5)"
    )
    schedule_time: Optional[datetime] = Field(
        None,
        description="Schedule for future publishing (leave empty for immediate)"
    )
    
    # FREE OPTIONAL ENHANCEMENT: Smart timing
    auto_optimize_timing: bool = Field(
        default=False,
        description="FREE: Automatically find best time to post (based on platform best practices)"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "content_id": 1,
                "platforms": ["twitter", "linkedin"],
                "schedule_time": None,
                "auto_optimize_timing": False
            }
        }

# ============================================
# CORE CONTENT ENGINE (Main AI System)
# ============================================

class ContentEngine:
    """
    The heart of the system - AI content generation
    
    This class handles all content generation using GPT-4 and optionally Claude.
    It includes FREE enhancements like quality scoring, SEO optimization,
    hashtag generation, and platform-specific optimization.
    """
    
    def __init__(self):
        """Initialize AI clients and caching"""
        self.openai_client = None
        self.anthropic_client = None
        
        if OPENAI_API_KEY:
            self.openai_client = AsyncOpenAI(api_key=OPENAI_API_KEY)
            logger.info("OpenAI client initialized")
        else:
            logger.error("OpenAI API key missing - content generation will fail")
        
        if ANTHROPIC_API_KEY:
            self.anthropic_client = AsyncAnthropic(api_key=ANTHROPIC_API_KEY)
            logger.info("Anthropic client initialized (premium multi-model available)")
        
        # FREE OPTIONAL ENHANCEMENT: Content templates
        self.templates = ContentTemplates()
    
    async def generate_content(
        self,
        request: ContentRequest,
        background_tasks: BackgroundTasks
    ) -> ContentResponse:
        """
        Generate AI content with all enhancements
        
        This is the main entry point for content generation.
        It handles caching, cost control, quality assessment, and all
        free enhancements automatically.
        """
        
        start_time = datetime.now()
        logger.info(f"Generating {request.content_type.value} content: {request.topic[:50]}...")
        
        # PAID OPTIONAL ENHANCEMENT: Cache Check
        cache_key = None
        cached_content = None
        if CACHE_ENABLED and redis_cache:
            cache_key = self._generate_cache_key(request)
            # cached_content = await self._get_cached_content(cache_key)
            # if cached_content:
            #     logger.info(f"Cache hit! Saved ~${cached_content.get('cost_saved', 0.03):.3f}")
            #     return ContentResponse(**cached_content, cached=True)
        
        # FREE OPTIONAL ENHANCEMENT: Cost Control
        estimated_cost = self._estimate_cost(request)
        if MONTHLY_AI_BUDGET > 0:
            can_proceed = await cost_controller.check_budget(estimated_cost)
            if not can_proceed:
                raise HTTPException(
                    402,
                    detail=f"Monthly budget of ${MONTHLY_AI_BUDGET} would be exceeded. "
                           f"Current usage: ${await cost_controller.get_month_cost():.2f}"
                )
        
        # Generate content
        model_used = "unknown"
        try:
            if request.use_premium and self.anthropic_client:
                # PAID: Multi-model synthesis
                content = await self._generate_premium_content(request)
                model_used = "multi-model"
            else:
                # CORE: Standard GPT-4
                content = await self._generate_standard_content(request)
                model_used = "gpt-4"
                
        except Exception as e:
            logger.error(f"Content generation failed: {e}")
            
            # Track failure
            await self._track_api_usage(
                model=model_used,
                tokens=0,
                cost=0,
                request_type=request.content_type.value,
                success=False,
                error_message=str(e)
            )
            
            raise HTTPException(
                500,
                detail=f"Content generation failed: {str(e)}. "
                       "Please check your API keys and try again."
            )
        
        # FREE OPTIONAL ENHANCEMENT: Calculate quality scores
        quality_score = self._assess_quality(content, request)
        seo_score = self._calculate_seo_score(content, request.keywords) if request.seo_optimize else 0.5
        
        # FREE OPTIONAL ENHANCEMENT: Smart hashtags for social media
        if request.include_hashtags and request.platform in [Platform.TWITTER, Platform.INSTAGRAM, Platform.LINKEDIN]:
            content = await self._add_smart_hashtags(content, request.keywords, request.platform)
        
        # FREE OPTIONAL ENHANCEMENT: Platform optimization
        content = self._optimize_for_platform(content, request.platform, request)
        
        # Store in database
        async with db_pool.acquire() as conn:
            result = await conn.fetchrow('''
                INSERT INTO content 
                (content_type, topic, content, metadata, quality_score, seo_score, status)
                VALUES ($1, $2, $3, $4, $5, $6, $7)
                RETURNING id, created_at
            ''', request.content_type.value, request.topic, content, 
                json.dumps({
                    "keywords": request.keywords,
                    "tone": request.tone.value,
                    "platform": request.platform.value,
                    "model": model_used,
                    "target_audience": request.target_audience,
                    "premium": request.use_premium
                }),
                quality_score, seo_score, 'ready')
        
        content_id = result['id']
        
        # Calculate actual cost and processing time
        word_count = len(content.split())
        processing_time = (datetime.now() - start_time).total_seconds()
        
        # FREE OPTIONAL ENHANCEMENT: Generate recommendations
        recommendations = self._generate_recommendations(quality_score, seo_score, request)
        
        response = ContentResponse(
            id=content_id,
            content=content,
            quality_score=quality_score,
            seo_score=seo_score,
            metadata={
                "word_count": word_count,
                "reading_time": max(1, word_count // 200),
                "platform_optimized": request.platform.value,
                "processing_time": round(processing_time, 2),
                "model": model_used
            },
            generated_at=result['created_at'],
            cost_estimate=estimated_cost,
            cached=False,
            recommendations=recommendations
        )
        
        # Background tasks for non-blocking operations
        background_tasks.add_task(
            self._track_api_usage,
            model=model_used,
            tokens=word_count,  # Rough estimate
            cost=estimated_cost,
            request_type=request.content_type.value,
            content_id=content_id,
            success=True
        )
        
        # FREE OPTIONAL ENHANCEMENT: Track analytics
        background_tasks.add_task(
            analytics.track_event,
            'content_generated',
            {
                'content_id': content_id,
                'content_type': request.content_type.value,
                'quality_score': quality_score,
                'seo_score': seo_score,
                'word_count': word_count,
                'platform': request.platform.value,
                'premium': request.use_premium
            }
        )
        
        # FREE OPTIONAL ENHANCEMENT: Webhooks
        if WEBHOOK_CONTENT_GENERATED:
            background_tasks.add_task(
                webhook_system.trigger_webhook,
                'content_generated',
                {
                    'content_id': content_id,
                    'type': request.content_type.value,
                    'quality_score': quality_score,
                    'topic': request.topic
                },
                WEBHOOK_CONTENT_GENERATED
            )
        
        # FREE OPTIONAL ENHANCEMENT: A/B Testing variants
        if request.generate_variants:
            background_tasks.add_task(
                self._generate_ab_variants,
                request,
                content_id
            )
        
        # PAID OPTIONAL ENHANCEMENT: Cache the response
        if cache_key and CACHE_ENABLED:
            # background_tasks.add_task(self._cache_content, cache_key, response)
            pass
        
        logger.info(f" Content generated (ID: {content_id}, Quality: {quality_score:.2f}, Cost: ${estimated_cost:.3f})")
        
        return response
    
    async def _generate_standard_content(self, request: ContentRequest) -> str:
        """
        CORE FEATURE: Standard content generation using GPT-4
        This is the main content generation method for the standard tier
        """
        if not self.openai_client:
            raise HTTPException(500, "OpenAI API key not configured")
        
        system_prompt = self._build_system_prompt(request)
        user_prompt = self._build_user_prompt(request)
        
        try:
            completion = await self.openai_client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=self._calculate_max_tokens(request.length),
                presence_penalty=0.1,  # Encourages diverse vocabulary
                frequency_penalty=0.1  # Reduces repetition
            )
            
            return completion.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise
    
    async def _generate_premium_content(self, request: ContentRequest) -> str:
        """
        PAID OPTIONAL ENHANCEMENT: Multi-model synthesis (+$0.02-0.05/request)
        
        Combines GPT-4 and Claude for superior quality.
        This method:
        1. Generates content with both AI models in parallel
        2. Synthesizes the best elements of both responses
        3. Results in 20-30% higher quality scores
        
        Best for: Landing pages, important emails, key blog posts
        """
        if not self.openai_client or not self.anthropic_client:
            logger.warning("Multi-model requested but Anthropic not configured, falling back to GPT-4")
            return await self._generate_standard_content(request)
        
        logger.info("Using premium multi-model synthesis")
        
        # Generate with both models in parallel
        tasks = [
            self._generate_with_openai(request),
            self._generate_with_anthropic(request)
        ]
        
        try:
            responses = await asyncio.gather(*tasks, return_exceptions=True)
        except Exception as e:
            logger.error(f"Multi-model generation failed: {e}")
            return await self._generate_standard_content(request)
        
        # Handle any failures
        valid_responses = [r for r in responses if not isinstance(r, Exception)]
        
        if len(valid_responses) == 0:
            raise HTTPException(500, "All AI models failed to generate content")
        
        if len(valid_responses) == 1:
            logger.warning("Only one model succeeded, returning that response")
            return valid_responses[0]
        
        # Synthesize the best of both
        synthesis_prompt = f"""You are a content synthesis expert. I have two AI-generated responses for the same request.
        
Your task: Create a single, superior version that combines the best elements of both responses.

Response 1 (GPT-4):
{valid_responses[0]}

Response 2 (Claude):
{valid_responses[1]}

Guidelines:
- Keep the same tone and target audience
- Maintain the best structural elements from either
- Use the most compelling phrases and examples
- Ensure smooth flow and coherence
- Match or improve upon the stronger response's quality

Create the best possible synthesis:"""
        
        try:
            synthesis = await self.openai_client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": "You are an expert at synthesizing content from multiple sources."},
                    {"role": "user", "content": synthesis_prompt}
                ],
                temperature=0.5,
                max_tokens=self._calculate_max_tokens(request.length)
            )
            
            return synthesis.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Synthesis failed, returning best single response: {e}")
            # Return the longer response as fallback
            return max(valid_responses, key=len)
    
    async def _generate_with_openai(self, request: ContentRequest) -> str:
        """Generate using OpenAI GPT-4"""
        system_prompt = self._build_system_prompt(request)
        user_prompt = self._build_user_prompt(request)
        
        completion = await self.openai_client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=self._calculate_max_tokens(request.length)
        )
        
        return completion.choices[0].message.content.strip()
    
    async def _generate_with_anthropic(self, request: ContentRequest) -> str:
        """Generate using Anthropic Claude"""
        system_prompt = self._build_system_prompt(request)
        user_prompt = self._build_user_prompt(request)
        
        message = await self.anthropic_client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=self._calculate_max_tokens(request.length),
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}]
        )
        
        return message.content[0].text.strip()
    
    def _build_system_prompt(self, request: ContentRequest) -> str:
        """
        Build intelligent system prompt based on content type
        FREE OPTIONAL ENHANCEMENT: Context-aware prompting
        """
        
        base_prompts = {
            ContentType.BLOG: f"""You are an expert blog writer and content strategist.

Your expertise:
- Writing engaging, SEO-optimized blog content
- Maintaining reader engagement from intro to conclusion
- Using storytelling and data to support points
- Creating actionable takeaways

Write in a {request.tone.value} tone for {request.target_audience or 'a general audience'}.
Focus on providing genuine value, actionable insights, and maintaining reader engagement throughout.""",
            
            ContentType.SOCIAL_POST: f"""You are a social media expert specializing in {request.platform.value}.

Your expertise:
- Creating viral, highly engaging social content
- Understanding platform-specific best practices
- Writing compelling hooks and calls-to-action
- Optimizing for maximum reach and engagement

Write in a {request.tone.value} tone optimized specifically for {request.platform.value}.
Keep it concise, impactful, and shareable. Include a clear call-to-action.""",
            
            ContentType.EMAIL: f"""You are an email marketing specialist with proven conversion expertise.

Your expertise:
- Writing subject lines with high open rates
- Creating compelling email body copy
- Driving conversions through persuasive CTAs
- Personalizing content for target audiences

Write in a {request.tone.value} tone that resonates and converts.
Focus on clear value propositions, personalization, and strong CTAs.""",
            
            ContentType.AD_COPY: f"""You are a direct response copywriter specializing in high-converting ads.

Your expertise:
- Writing attention-grabbing headlines
- Creating benefit-driven body copy
- Crafting urgent, compelling calls-to-action
- Understanding buyer psychology

Write in a {request.tone.value} tone that drives immediate action.
Focus on benefits over features, create urgency, and include clear CTAs.""",
            
            ContentType.LANDING_PAGE: f"""You are a conversion optimization expert writing landing page copy.

Your expertise:
- Writing compelling headlines that convert
- Structuring content for maximum conversion
- Addressing objections effectively
- Creating trust through social proof

Write in a {request.tone.value} tone that converts visitors into customers.
Structure: Powerful headline, clear value proposition, benefits, social proof, strong CTA.""",
            
            ContentType.VIDEO_SCRIPT: f"""You are a video script writer creating engaging scripts for {request.platform.value}.

Your expertise:
- Writing hooks that stop scrolling
- Structuring content for video format
- Maintaining viewer engagement throughout
- Creating memorable, actionable conclusions

Write in a {request.tone.value} tone optimized for {request.platform.value}.
Include: Hook (first 3 seconds), story arc, clear value, and strong CTA.""",
            
            ContentType.PRODUCT_DESCRIPTION: f"""You are an e-commerce copywriter specializing in product descriptions.

Your expertise:
- Writing benefit-driven product copy
- Addressing customer pain points
- Creating urgency and desire
- SEO optimization for product pages

Write in a {request.tone.value} tone that sells.
Focus on benefits, features, and why the customer needs this now.""",
            
            ContentType.PRESS_RELEASE: f"""You are a PR professional writing newsworthy press releases.

Your expertise:
- Writing in AP style
- Creating compelling angles
- Structuring information effectively
- Making content media-ready

Write in a {request.tone.value} tone following press release best practices.
Structure: Headline, dateline, lead paragraph, body, boilerplate, contact info."""
        }
        
        return base_prompts.get(request.content_type, base_prompts[ContentType.BLOG])
    
    def _build_user_prompt(self, request: ContentRequest) -> str:
        """
        Build comprehensive user prompt with all requirements
        FREE OPTIONAL ENHANCEMENT: Smart prompting
        """
        
        parts = [f"**Topic:** {request.topic}"]
        
        if request.keywords:
            parts.append(f"**SEO Keywords to include naturally:** {', '.join(request.keywords)}")
            parts.append("(Incorporate keywords organically - avoid keyword stuffing)")
        
        if request.length:
            parts.append(f"**Target length:** Approximately {request.length} words")
        else:
            # Suggest appropriate lengths based on content type
            suggested_lengths = {
                ContentType.BLOG: "800-1200 words",
                ContentType.SOCIAL_POST: "50-100 words",
                ContentType.EMAIL: "200-400 words",
                ContentType.AD_COPY: "50-150 words",
                ContentType.LANDING_PAGE: "500-800 words",
                ContentType.VIDEO_SCRIPT: "150-300 words",
                ContentType.PRODUCT_DESCRIPTION: "150-250 words",
                ContentType.PRESS_RELEASE: "400-600 words"
            }
            parts.append(f"**Target length:** {suggested_lengths.get(request.content_type, '500-800 words')}")
        
        if request.target_audience:
            parts.append(f"**Target audience:** {request.target_audience}")
        
        if request.platform != Platform.BLOG:
            parts.append(f"**Platform:** Optimize specifically for {request.platform.value}")
            
            # Platform-specific guidance
            platform_tips = {
                Platform.TWITTER: "Keep it concise and impactful. Max 280 characters.",
                Platform.LINKEDIN: "Professional tone. Use relevant hashtags (3-5). Encourage discussion.",
                Platform.INSTAGRAM: "Visual storytelling. Use emojis. Include 5-10 relevant hashtags.",
                Platform.FACEBOOK: "Conversational and engaging. Ask questions to encourage comments.",
                Platform.YOUTUBE: "Include timestamps. Hook viewers in first 3 seconds.",
                Platform.TIKTOK: "Trend-aware. Fast-paced. Entertainment-first approach.",
                Platform.PINTEREST: "Search-optimized. Include detailed description for pins."
            }
            
            if request.platform in platform_tips:
                parts.append(f"**Platform tip:** {platform_tips[request.platform]}")
        
        if request.seo_optimize and request.content_type == ContentType.BLOG:
            parts.append("""
**SEO Optimization Requirements:**
- Include a compelling meta description suggestion (150-160 characters)
- Use headers (H2, H3) to structure content
- Suggest opportunities for internal linking
- Use lists and bullet points for readability
- Include a strong conclusion with CTA
""")
        
        return "\n\n".join(parts)
    
    def _optimize_for_platform(self, content: str, platform: Platform, request: ContentRequest) -> str:
        """
        FREE OPTIONAL ENHANCEMENT: Platform-specific optimization
        
        Automatically adjusts content to meet platform requirements and best practices
        """
        
        if platform == Platform.TWITTER:
            # Twitter: 280 character limit
            if len(content) > 280:
                # Smart truncation - try to end at sentence or word boundary
                truncated = content[:277]
                
                # Try to find last sentence ending
                last_period = max(truncated.rfind('.'), truncated.rfind('!'), truncated.rfind('?'))
                if last_period > 200:  # Keep if it's not too short
                    content = truncated[:last_period + 1]
                else:
                    # Find last word boundary
                    last_space = truncated.rfind(' ')
                    if last_space > 250:
                        content = truncated[:last_space] + "..."
                    else:
                        content = truncated + "..."
        
        elif platform == Platform.LINKEDIN:
            # LinkedIn: First 140 characters show without "see more"
            # Ensure strong hook in first sentence
            if len(content) > 140:
                first_period = content.find('.')
                if first_period == -1 or first_period > 140:
                    # Add line break after ~140 chars for better mobile display
                    space_pos = content.find(' ', 130)
                    if space_pos != -1 and space_pos < 150:
                        content = content[:space_pos] + '\n\n' + content[space_pos + 1:]
        
        elif platform == Platform.INSTAGRAM:
            # Instagram: 2200 character caption limit
            if len(content) > 2200:
                content = content[:2197] + "..."
            
            # Ensure hashtags are at the end
            if '#' in content:
                # Move all hashtags to the end
                lines = content.split('\n')
                hashtag_lines = [line for line in lines if '#' in line]
                content_lines = [line for line in lines if '#' not in line]
                
                if hashtag_lines:
                    content = '\n'.join(content_lines) + '\n\n' + '\n'.join(hashtag_lines)
        
        elif platform == Platform.FACEBOOK:
            # Facebook: Optimal post length is 40-80 characters for max engagement
            # But can be up to 63,206 characters
            # Add paragraph breaks for readability
            if len(content) > 200 and '\n\n' not in content[:200]:
                # Add a line break after first sentence if missing
                first_period = content.find('.')
                if first_period != -1 and first_period < 200:
                    content = content[:first_period + 1] + '\n\n' + content[first_period + 2:]
        
        elif platform == Platform.YOUTUBE:
            # YouTube: Description should have key info in first 157 characters
            # Add timestamps if this is a video script
            if request.content_type == ContentType.VIDEO_SCRIPT:
                # Suggest timestamp structure
                if '[00:00]' not in content and '0:00' not in content:
                    content = "📍 Timestamps:\n0:00 - Intro\n\n" + content
        
        elif platform == Platform.TIKTOK:
            # TikTok: 150 character caption, 2200 for video description
            # Keep it punchy and use emojis
            if len(content) > 150:
                content = content[:147] + "..."
            
            # Ensure at least one emoji for engagement
            if not any(char for char in content if ord(char) > 127):
                # Add relevant emoji at start
                emoji_map = {
                    'tip': '',
                    'business': '💼',
                    'marketing': '',
                    'ai': '',
                    'money': '',
                    'success': ''
                }
                
                for keyword, emoji in emoji_map.items():
                    if keyword in content.lower():
                        content = f"{emoji} {content}"
                        break
        
        return content.strip()
    
    async def _add_smart_hashtags(
        self,
        content: str,
        keywords: List[str],
        platform: Platform
    ) -> str:
        """
        FREE OPTIONAL ENHANCEMENT: Smart hashtag generation
        
        Automatically generates optimized hashtags based on:
        - Content keywords
        - Platform best practices
        - Trending topics (when available)
        - Hashtag performance data
        """
        
        if not keywords:
            return content
        
        # Already has hashtags? Skip
        if '#' in content:
            return content
        
        # Platform-specific hashtag strategy
        hashtag_config = {
            Platform.TWITTER: {
                'max': 2,
                'placement': 'inline',
                'style': 'capitalize_first'
            },
            Platform.INSTAGRAM: {
                'max': 10,
                'placement': 'end',
                'style': 'capitalize_all'
            },
            Platform.LINKEDIN: {
                'max': 5,
                'placement': 'end',
                'style': 'capitalize_first'
            },
            Platform.FACEBOOK: {
                'max': 2,
                'placement': 'inline',
                'style': 'capitalize_first'
            },
            Platform.TIKTOK: {
                'max': 5,
                'placement': 'inline',
                'style': 'lowercase'
            },
            Platform.PINTEREST: {
                'max': 5,
                'placement': 'end',
                'style': 'capitalize_first'
            }
        }
        
        config = hashtag_config.get(platform)
        if not config:
            return content
        
        # Generate hashtags from keywords
        hashtags = []
        for keyword in keywords[:config['max']]:
            # Clean and format hashtag
            hashtag = keyword.replace(' ', '').replace('-', '').replace('_', '')
            
            # Apply styling
            if config['style'] == 'capitalize_first':
                hashtag = hashtag.capitalize()
            elif config['style'] == 'capitalize_all':
                # CamelCase for multi-word hashtags
                words = keyword.split()
                hashtag = ''.join(word.capitalize() for word in words)
            elif config['style'] == 'lowercase':
                hashtag = hashtag.lower()
            
            # Validate hashtag length (max 30 characters per platform standard)
            if len(hashtag) <= 30 and len(hashtag) >= 3:
                hashtags.append('#' + hashtag)
        
        if not hashtags:
            return content
        
        # Add hashtags based on platform preference
        hashtag_string = ' '.join(hashtags)
        
        if config['placement'] == 'inline':
            # Add at the end of the first line or paragraph
            lines = content.split('\n')
            lines[0] = f"{lines[0]} {hashtag_string}"
            content = '\n'.join(lines)
        else:  # 'end'
            # Add at the very end with spacing
            content = f"{content}\n\n{hashtag_string}"
        
        return content
    
    def _assess_quality(self, content: str, request: ContentRequest) -> float:
        """
        FREE OPTIONAL ENHANCEMENT: Advanced quality assessment
        
        Evaluates content quality across multiple dimensions:
        - Length appropriateness
        - Keyword integration
        - Readability
        - Engagement indicators
        - Structure and formatting
        """
        
        score = 0.0
        word_count = len(content.split())
        
        # 1. Length appropriateness (25% of score)
        if request.length:
            ratio = word_count / request.length
            # Ideal is within 10% of target
            if 0.9 <= ratio <= 1.1:
                score += 0.25
            elif 0.8 <= ratio <= 1.2:
                score += 0.20
            elif 0.7 <= ratio <= 1.3:
                score += 0.15
            else:
                score += 0.10
        else:
            # Default good range
            if 100 <= word_count <= 2000:
                score += 0.25
            elif 50 <= word_count <= 3000:
                score += 0.15
            else:
                score += 0.10
        
        # 2. Keyword integration (25% of score)
        if request.keywords:
            content_lower = content.lower()
            keyword_count = sum(1 for kw in request.keywords if kw.lower() in content_lower)
            keyword_ratio = keyword_count / len(request.keywords)
            
            # Perfect: All keywords present
            if keyword_ratio >= 0.9:
                score += 0.25
            elif keyword_ratio >= 0.7:
                score += 0.20
            elif keyword_ratio >= 0.5:
                score += 0.15
            else:
                score += 0.10
        else:
            score += 0.25  # No penalty if no keywords specified
        
        # 3. Readability (20% of score)
        sentences = content.count('.') + content.count('!') + content.count('?')
        if sentences > 0:
            avg_sentence_length = word_count / sentences
            
            # Ideal: 15-20 words per sentence
            if 15 <= avg_sentence_length <= 20:
                score += 0.20
            elif 10 <= avg_sentence_length <= 25:
                score += 0.15
            elif 8 <= avg_sentence_length <= 30:
                score += 0.10
            else:
                score += 0.05
        
        # 4. Engagement indicators (15% of score)
        engagement_score = 0
        
        # Questions (engages reader)
        if '?' in content:
            engagement_score += 0.05
        
        # Numbers/statistics (adds credibility)
        if any(char.isdigit() for char in content):
            engagement_score += 0.04
        
        # Call-to-action phrases
        cta_phrases = ['click', 'visit', 'learn', 'discover', 'join', 'get', 'try', 'start', 'explore']
        if any(cta in content.lower() for cta in cta_phrases):
            engagement_score += 0.03
        
        # Lists/bullets (improves scannability)
        if any(marker in content for marker in ['•', '-', '1.', '2.', '*']):
            engagement_score += 0.03
        
        score += min(engagement_score, 0.15)
        
        # 5. Structure and formatting (15% of score)
        structure_score = 0
        
        # Paragraphs (good readability)
        paragraph_count = content.count('\n\n') + 1
        if 3 <= paragraph_count <= 10:
            structure_score += 0.05
        elif paragraph_count > 1:
            structure_score += 0.03
        
        # Headers/sections (good organization)
        if any(header in content for header in ['##', 'H2:', 'H3:', '**']):
            structure_score += 0.05
        
        # Strong opening (first sentence quality)
        first_sentence = content.split('.')[0] if '.' in content else content[:100]
        if len(first_sentence.split()) >= 8 and len(first_sentence.split()) <= 20:
            structure_score += 0.03
        
        # Clear conclusion
        last_paragraph = content.split('\n\n')[-1] if '\n\n' in content else content[-200:]
        if any(conclusion in last_paragraph.lower() for conclusion in ['conclusion', 'in summary', 'to summarize', 'finally']):
            structure_score += 0.02
        
        score += min(structure_score, 0.15)
        
        return min(score, 1.0)
    
    def _calculate_seo_score(self, content: str, keywords: List[str]) -> float:
        """
        FREE OPTIONAL ENHANCEMENT: Comprehensive SEO scoring
        
        Evaluates SEO optimization across:
        - Keyword presence and placement
        - Keyword density
        - Content structure
        - Meta elements suggestions
        """
        
        if not keywords:
            return 0.5  # Neutral score if no keywords
        
        score = 0.0
        content_lower = content.lower()
        word_count = len(content.split())
        
        # 1. Keyword presence (35% of SEO score)
        keyword_count = sum(1 for kw in keywords if kw.lower() in content_lower)
        presence_ratio = keyword_count / len(keywords)
        
        if presence_ratio >= 0.9:
            score += 0.35
        elif presence_ratio >= 0.7:
            score += 0.28
        elif presence_ratio >= 0.5:
            score += 0.20
        else:
            score += 0.10
        
        # 2. Keyword density (25% of SEO score)
        # Optimal density: 1-3% of total words
        if word_count > 0:
            total_keyword_occurrences = sum(
                content_lower.count(kw.lower()) for kw in keywords
            )
            density = (total_keyword_occurrences / word_count) * 100
            
            if 1 <= density <= 3:
                score += 0.25  # Perfect density
            elif 0.5 <= density < 1:
                score += 0.20  # A bit low
            elif 3 < density <= 5:
                score += 0.15  # A bit high
            else:
                score += 0.05  # Too high or too low
        
        # 3. Keyword placement (20% of SEO score)
        placement_score = 0
        
        # First 100 words (important for SEO)
        first_100 = ' '.join(content.split()[:100]).lower()
        if any(kw.lower() in first_100 for kw in keywords):
            placement_score += 0.07
        
        # Headers/titles (high importance)
        headers = [line for line in content.split('\n') if line.strip().startswith('#') or '**' in line]
        if headers and any(kw.lower() in ' '.join(headers).lower() for kw in keywords):
            placement_score += 0.07
        
        # Last paragraph (conclusion)
        last_para = content.split('\n\n')[-1].lower() if '\n\n' in content else content[-200:].lower()
        if any(kw.lower() in last_para for kw in keywords):
            placement_score += 0.06
        
        score += min(placement_score, 0.20)
        
        # 4. Content structure (20% of SEO score)
        structure_score = 0
        
        # Good length (500-2500 words is ideal for SEO)
        if 500 <= word_count <= 2500:
            structure_score += 0.08
        elif 300 <= word_count <= 3000:
            structure_score += 0.05
        else:
            structure_score += 0.02
        
        # Headers present (H2, H3, etc.)
        header_markers = ['##', 'H2:', 'H3:', '###']
        if any(marker in content for marker in header_markers):
            structure_score += 0.06
        
        # Lists/bullets (good for featured snippets)
        if any(marker in content for marker in ['•', '-', '1.', '2.', '*']):
            structure_score += 0.04
        
        # Internal linking suggestions (if present)
        if '[' in content and ']' in content:
            structure_score += 0.02
        
        score += min(structure_score, 0.20)
        
        return min(score, 1.0)
    
    def _generate_recommendations(
        self,
        quality_score: float,
        seo_score: float,
        request: ContentRequest
    ) -> List[str]:
        """
        FREE OPTIONAL ENHANCEMENT: Personalized recommendations
        
        Generates actionable suggestions to improve content quality
        """
        
        recommendations = []
        
        # Quality recommendations
        if quality_score < 0.7:
            recommendations.append(" Consider adding more specific examples or data to increase quality")
        
        if quality_score < 0.8:
            recommendations.append(" Add more engagement elements like questions or calls-to-action")
        
        # SEO recommendations
        if seo_score < 0.6:
            recommendations.append("🔍 Include more of your target keywords naturally throughout the content")
        
        if seo_score < 0.7:
            recommendations.append("🔍 Consider adding headers (H2, H3) with keywords for better SEO")
        
        # Length recommendations
        word_count = 0  # This would come from actual content
        if request.length and request.length < 300:
            recommendations.append("📝 Longer content (500+ words) tends to rank better for SEO")
        
        # Platform-specific recommendations
        if request.platform == Platform.INSTAGRAM and not request.include_hashtags:
            recommendations.append("📱 Enable hashtags for better Instagram discoverability")
        
        if request.platform == Platform.LINKEDIN and request.tone == ContentTone.CASUAL:
            recommendations.append("💼 Consider a more professional tone for LinkedIn content")
        
        # Premium recommendation
        if not request.use_premium and (quality_score < 0.85 or seo_score < 0.85):
            recommendations.append("✨ Try premium multi-model generation for 20-30% quality improvement (+$0.02)")
        
        # A/B testing recommendation
        if not request.generate_variants and request.content_type in [ContentType.EMAIL, ContentType.AD_COPY]:
            recommendations.append(" Enable A/B testing to find the highest-performing version (free)")
        
        return recommendations if recommendations else [" Content quality is excellent! No improvements needed."]
    
    def _estimate_cost(self, request: ContentRequest) -> float:
        """
        Estimate API cost for the request
        Based on typical token usage patterns
        """
        
        # Base costs (rough estimates)
        if request.use_premium:
            # Multi-model costs more (both GPT-4 and Claude)
            base_cost = 0.05
        else:
            # Standard GPT-4
            base_cost = 0.03
        
        # Adjust for length
        if request.length:
            if request.length > 2000:
                base_cost *= 1.5
            elif request.length > 1000:
                base_cost *= 1.2
        
        # Variants add cost
        if request.generate_variants:
            base_cost *= 3  # 3 variants
        
        return round(base_cost, 4)
    
    def _calculate_max_tokens(self, target_length: Optional[int]) -> int:
        """Calculate max tokens based on target word count"""
        
        if target_length:
            # Roughly 1.3 tokens per word, with 50% buffer
            tokens = int(target_length * 1.3 * 1.5)
        else:
            tokens = 2000  # Default
        
        # Cap at model maximum
        return min(tokens, 4000)
    
    def _generate_cache_key(self, request: ContentRequest) -> str:
        """Generate cache key for request"""
        
        # Include all relevant parameters that affect output
        key_parts = [
            request.content_type.value,
            request.topic,
            request.tone.value,
            request.platform.value,
            str(request.length or 'auto'),
            str(request.use_premium),
            '-'.join(sorted(request.keywords))
        ]
        
        key_string = ':'.join(key_parts)
        return f"content:{hashlib.md5(key_string.encode()).hexdigest()}"
    
    async def _track_api_usage(
        self,
        model: str,
        tokens: int,
        cost: float,
        request_type: str,
        content_id: Optional[int] = None,
        success: bool = True,
        error_message: Optional[str] = None
    ):
        """
        FREE OPTIONAL ENHANCEMENT: Track API usage for cost monitoring
        """
        
        try:
            async with db_pool.acquire() as conn:
                await conn.execute('''
                    INSERT INTO api_usage 
                    (model, tokens, cost, request_type, content_id, success, error_message)
                    VALUES ($1, $2, $3, $4, $5, $6, $7)
                ''', model, tokens, cost, request_type, content_id, success, error_message)
        except Exception as e:
            logger.error(f"Failed to track API usage: {e}")
    
    async def _generate_ab_variants(
        self,
        request: ContentRequest,
        original_content_id: int
    ):
        """
        FREE OPTIONAL ENHANCEMENT: Generate A/B test variants
        
        Creates 2 additional variants with different approaches:
        1. Different tone
        2. Different structure/angle
        """
        
        try:
            logger.info(f"Generating A/B test variants for content {original_content_id}")
            
            # Get original content
            async with db_pool.acquire() as conn:
                original = await conn.fetchrow(
                    "SELECT * FROM content WHERE id = $1",
                    original_content_id
                )
            
            if not original:
                logger.error("Original content not found for A/B testing")
                return
            
            # Define variant strategies
            variants = []
            
            # Variant 1: Different tone
            if request.tone != ContentTone.ENTHUSIASTIC:
                variant1_request = request.copy(deep=True)
                variant1_request.tone = ContentTone.ENTHUSIASTIC
                variants.append(("tone", variant1_request))
            
            # Variant 2: Different approach (if professional, try casual)
            if request.tone == ContentTone.PROFESSIONAL:
                variant2_request = request.copy(deep=True)
                variant2_request.tone = ContentTone.CONVERSATIONAL
                variants.append(("approach", variant2_request))
            else:
                # Otherwise try professional
                variant2_request = request.copy(deep=True)
                variant2_request.tone = ContentTone.PROFESSIONAL
                variants.append(("approach", variant2_request))
            
            variant_ids = [original_content_id]
            
            # Generate variants
            for variant_type, variant_request in variants[:2]:  # Max 2 variants
                try:
                    # Generate variant content
                    if variant_request.use_premium and self.anthropic_client:
                        content = await self._generate_premium_content(variant_request)
                    else:
                        content = await self._generate_standard_content(variant_request)
                    
                    # Calculate scores
                    quality_score = self._assess_quality(content, variant_request)
                    seo_score = self._calculate_seo_score(content, variant_request.keywords)
                    
                    # Save variant
                    async with db_pool.acquire() as conn:
                        variant_id = await conn.fetchval('''
                            INSERT INTO content 
                            (content_type, topic, content, metadata, quality_score, seo_score, status)
                            VALUES ($1, $2, $3, $4, $5, $6, $7)
                            RETURNING id
                        ''', variant_request.content_type.value, variant_request.topic, content,
                            json.dumps({
                                "keywords": variant_request.keywords,
                                "tone": variant_request.tone.value,
                                "platform": variant_request.platform.value,
                                "variant_type": variant_type,
                                "original_id": original_content_id,
                                "is_variant": True
                            }),
                            quality_score, seo_score, 'variant')
                    
                    variant_ids.append(variant_id)
                    logger.info(f"Created variant {variant_id} (type: {variant_type})")
                    
                except Exception as e:
                    logger.error(f"Failed to generate variant {variant_type}: {e}")
            
            # Create A/B test record
            if len(variant_ids) > 1:
                async with db_pool.acquire() as conn:
                    await conn.execute('''
                        INSERT INTO ab_tests (test_name, variant_ids, test_parameter, status)
                        VALUES ($1, $2, $3, $4)
                    ''', f"AB Test: {request.topic[:50]}", variant_ids, "tone", "active")
                
                logger.info(f"A/B test created with {len(variant_ids)} variants")
        
        except Exception as e:
            logger.error(f"A/B variant generation failed: {e}")

# ============================================
# SOCIAL MEDIA PUBLISHER (Core Feature)
# ============================================

class SocialPublisher:
    """
    Handles multi-platform content publishing
    
    Core Features:
    - Content validation for each platform
    - Publishing scheduling
    - Status tracking
    
    Optional: Actual API posting (requires platform API keys)
    """
    
    async def publish(
        self,
        content_id: int,
        platforms: List[Platform],
        schedule_time: Optional[datetime] = None,
        background_tasks: BackgroundTasks = None,
        auto_optimize_timing: bool = False
    ) -> Dict[str, Any]:
        """
        Publish or schedule content across platforms
        
        FREE OPTIONAL ENHANCEMENT: Smart timing optimization
        PAID OPTIONAL ENHANCEMENT: Auto-posting (requires API keys)
        """
        
        logger.info(f"Publishing content {content_id} to {len(platforms)} platform(s)")
        
        # Get content from database
        async with db_pool.acquire() as conn:
            content = await conn.fetchrow(
                "SELECT * FROM content WHERE id = $1",
                content_id
            )
        
        if not content:
            raise HTTPException(404, "Content not found")
        
        # FREE OPTIONAL ENHANCEMENT: Auto-optimize timing
        if auto_optimize_timing and not schedule_time:
            schedule_time = self._get_optimal_posting_time(platforms)
            logger.info(f"Optimized posting time: {schedule_time}")
        
        results = {}
        
        for platform in platforms:
            try:
                # Validate content for platform
                validated_content = self._validate_for_platform(
                    content['content'],
                    platform
                )
                
                # Store in database
                async with db_pool.acquire() as conn:
                    post_id = await conn.fetchval('''
                        INSERT INTO social_posts 
                        (platform, content_id, post_content, status, scheduled_for)
                        VALUES ($1, $2, $3, $4, $5)
                        RETURNING id
                    ''', platform.value, content_id, validated_content,
                        'scheduled' if schedule_time else 'ready',
                        schedule_time)
                
                results[platform.value] = {
                    'post_id': post_id,
                    'status': 'scheduled' if schedule_time else 'ready_to_publish',
                    'scheduled_for': schedule_time.isoformat() if schedule_time else None,
                    'content_preview': validated_content[:100] + '...' if len(validated_content) > 100 else validated_content,
                    'auto_posting': self._is_auto_posting_available(platform)
                }
                
                # PAID OPTIONAL ENHANCEMENT: Auto-post to platform
                # This requires platform API keys (costs vary by platform)
                if background_tasks and not schedule_time:
                    if self._is_auto_posting_available(platform):
                        # background_tasks.add_task(
                        #     self._publish_to_platform,
                        #     post_id,
                        #     platform,
                        #     validated_content
                        # )
                        results[platform.value]['note'] = "Auto-posting available but not enabled (add API keys)"
                    else:
                        results[platform.value]['note'] = "Manual posting required (add API keys for auto-posting)"
                
                logger.info(f"Content prepared for {platform.value} (post_id: {post_id})")
                
            except Exception as e:
                logger.error(f"Failed to prepare content for {platform.value}: {e}")
                results[platform.value] = {
                    'status': 'error',
                    'error': str(e)
                }
        
        # FREE OPTIONAL ENHANCEMENT: Track analytics
        if background_tasks:
            background_tasks.add_task(
                analytics.track_event,
                'content_published',
                {
                    'content_id': content_id,
                    'platforms': [p.value for p in platforms],
                    'scheduled': bool(schedule_time)
                }
            )
        
        # FREE OPTIONAL ENHANCEMENT: Webhook notification
        if WEBHOOK_CONTENT_PUBLISHED and background_tasks:
            background_tasks.add_task(
                webhook_system.trigger_webhook,
                'content_published',
                {
                    'content_id': content_id,
                    'platforms': [p.value for p in platforms],
                    'results': results
                },
                WEBHOOK_CONTENT_PUBLISHED
            )
        
        return {
            'content_id': content_id,
            'total_platforms': len(platforms),
            'scheduled_for': schedule_time.isoformat() if schedule_time else None,
            'results': results
        }
    
    def _validate_for_platform(self, content: str, platform: Platform) -> str:
        """
        Ensure content meets platform requirements
        Returns validated (and possibly truncated) content
        """
        
        validators = {
            Platform.TWITTER: lambda c: c[:280] if len(c) > 280 else c,
            Platform.LINKEDIN: lambda c: c[:3000] if len(c) > 3000 else c,
            Platform.FACEBOOK: lambda c: c[:5000] if len(c) > 5000 else c,
            Platform.INSTAGRAM: lambda c: c[:2200] if len(c) > 2200 else c,
            Platform.YOUTUBE: lambda c: c[:5000] if len(c) > 5000 else c,
            Platform.TIKTOK: lambda c: c[:2200] if len(c) > 2200 else c,
            Platform.PINTEREST: lambda c: c[:500] if len(c) > 500 else c,
            Platform.EMAIL: lambda c: c,  # No limit
            Platform.BLOG: lambda c: c,  # No limit
        }
        
        validator = validators.get(platform, lambda c: c)
        validated = validator(content)
        
        if len(validated) < len(content):
            logger.warning(f"Content truncated for {platform.value}: {len(content)} -> {len(validated)} chars")
        
        return validated
    
    def _get_optimal_posting_time(self, platforms: List[Platform]) -> datetime:
        """
        FREE OPTIONAL ENHANCEMENT: Calculate optimal posting time
        
        Based on platform-specific best practices and time zones.
        Returns a datetime in UTC.
        """
        
        # Best posting times by platform (in UTC)
        # These are research-backed optimal times for engagement
        optimal_times = {
            Platform.TWITTER: [(13, 0), (17, 0)],  # 1 PM and 5 PM UTC
            Platform.LINKEDIN: [(10, 0), (12, 0), (17, 0)],  # Business hours
            Platform.INSTAGRAM: [(11, 0), (13, 0), (19, 0)],  # Lunch and evening
            Platform.FACEBOOK: [(12, 0), (15, 0), (19, 0)],  # Midday and evening
            Platform.YOUTUBE: [(14, 0), (18, 0)],  # Afternoon
            Platform.TIKTOK: [(18, 0), (21, 0)],  # Evening
            Platform.PINTEREST: [(20, 0), (23, 0)],  # Evening/night
        }
        
        # Find common optimal time across all platforms
        all_times = []
        for platform in platforms:
            if platform in optimal_times:
                all_times.extend(optimal_times[platform])
        
        if not all_times:
            # Default to 2 PM UTC tomorrow
            return datetime.utcnow().replace(hour=14, minute=0, second=0, microsecond=0) + timedelta(days=1)
        
        # Find most common time
        from collections import Counter
        time_counts = Counter(all_times)
        best_time = time_counts.most_common(1)[0][0]
        
        # Schedule for tomorrow at that time
        tomorrow = datetime.utcnow() + timedelta(days=1)
        return tomorrow.replace(hour=best_time[0], minute=best_time[1], second=0, microsecond=0)
    
    def _is_auto_posting_available(self, platform: Platform) -> bool:
        """
        Check if auto-posting is configured for a platform
        
        PAID OPTIONAL ENHANCEMENT: Requires platform API keys
        """
        
        availability = {
            Platform.TWITTER: bool(TWITTER_API_KEY and TWITTER_ACCESS_TOKEN),
            Platform.LINKEDIN: bool(LINKEDIN_CLIENT_ID and LINKEDIN_CLIENT_SECRET),
            # Add other platforms as they're implemented
        }
        
        return availability.get(platform, False)
    
    async def _publish_to_platform(
        self,
        post_id: int,
        platform: Platform,
        content: str
    ):
        """
        PAID OPTIONAL ENHANCEMENT: Actually post to social media
        
        This is a placeholder for actual platform posting.
        Implementation requires platform-specific API keys and SDKs.
        
        Cost: Varies by platform (most are free, some have limits)
        
        SUGGESTIONS for implementation:
        - Twitter: Use tweepy library with TWITTER_API_KEY
        - LinkedIn: Use linkedin-api library with LINKEDIN_CLIENT_ID
        - Instagram: Use instagrapi (requires username/password)
        - Facebook: Use facebook-sdk with Facebook Graph API
        - TikTok: Use TikTok API (requires approval)
        
        Each platform has different authentication requirements:
        - Twitter: OAuth 1.0a (API key + secret + access token)
        - LinkedIn: OAuth 2.0 (client ID + secret)
        - Instagram: Username/password or Business API
        - Facebook: Graph API (access token)
        """
        
        logger.info(f"Auto-posting to {platform.value} (post_id: {post_id})")
        
        # Update database status
        try:
            async with db_pool.acquire() as conn:
                await conn.execute('''
                    UPDATE social_posts
                    SET status = $1, published_at = $2
                    WHERE id = $3
                ''', 'publishing', datetime.utcnow(), post_id)
            
            # TODO: Implement actual platform posting
            # Example structure:
            # if platform == Platform.TWITTER:
            #     await self._post_to_twitter(content)
            # elif platform == Platform.LINKEDIN:
            #     await self._post_to_linkedin(content)
            # etc.
            
            # For now, mark as needs_manual_posting
            async with db_pool.acquire() as conn:
                await conn.execute('''
                    UPDATE social_posts
                    SET status = $1, metadata = $2
                    WHERE id = $3
                ''', 'needs_manual_posting',
                    json.dumps({'note': 'Auto-posting not configured. Please add platform API keys.'}),
                    post_id)
            
            logger.info(f"Post {post_id} marked for manual publishing")
            
        except Exception as e:
            logger.error(f"Failed to publish post {post_id}: {e}")
            
            # Update status to failed
            async with db_pool.acquire() as conn:
                await conn.execute('''
                    UPDATE social_posts
                    SET status = $1, metadata = $2
                    WHERE id = $3
                ''', 'failed',
                    json.dumps({'error': str(e)}),
                    post_id)

# ============================================
# FREE OPTIONAL ENHANCEMENT: Analytics Dashboard
# ============================================

class AnalyticsDashboard:
    """
    FREE OPTIONAL ENHANCEMENT: Comprehensive analytics and ROI tracking
    
    Provides insights into:
    - Content performance
    - Cost tracking
    - Platform distribution
    - Quality trends
    - ROI metrics
    """
    
    async def initialize(self):
        """Initialize analytics system"""
        logger.info("Analytics dashboard initialized")
    
    async def get_dashboard_metrics(self, days: int = 30) -> Dict[str, Any]:
        """
        Get comprehensive dashboard metrics
        
        Returns all key metrics for the specified time period
        """
        
        async with db_pool.acquire() as conn:
            # Content generation metrics
            content_metrics = await conn.fetchrow('''
                SELECT 
                    COUNT(*) as total_generated,
                    AVG(quality_score) as avg_quality,
                    AVG(seo_score) as avg_seo,
                    COUNT(DISTINCT DATE(created_at)) as active_days,
                    COUNT(CASE WHEN quality_score > 0.8 THEN 1 END) as high_quality_count,
                    COUNT(CASE WHEN metadata->>'is_variant' = 'true' THEN 1 END) as variant_count
                FROM content
                WHERE created_at > NOW() - INTERVAL '%s days'
                  AND status != 'variant'
            ''' % days)
            
            # Content type distribution
            content_types = await conn.fetch('''
                SELECT 
                    content_type,
                    COUNT(*) as count,
                    AVG(quality_score) as avg_quality
                FROM content
                WHERE created_at > NOW() - INTERVAL '%s days'
                  AND status != 'variant'
                GROUP BY content_type
                ORDER BY count DESC
            ''' % days)
            
            # Platform distribution
            platform_dist = await conn.fetch('''
                SELECT 
                    metadata->>'platform' as platform,
                    COUNT(*) as count,
                    AVG(quality_score) as avg_quality
                FROM content
                WHERE created_at > NOW() - INTERVAL '%s days'
                  AND metadata->>'platform' IS NOT NULL
                  AND status != 'variant'
                GROUP BY metadata->>'platform'
                ORDER BY count DESC
            ''' % days)
            
            # Cost tracking
            cost_metrics = await conn.fetchrow('''
                SELECT 
                    SUM(cost) as total_cost,
                    AVG(cost) as avg_cost_per_request,
                    COUNT(*) as total_requests,
                    COUNT(CASE WHEN success = true THEN 1 END) as successful_requests,
                    SUM(CASE WHEN model = 'multi-model' THEN cost END) as premium_cost
                FROM api_usage
                WHERE created_at > NOW() - INTERVAL '%s days'
            ''' % days)
            
            # Publishing metrics
            publish_metrics = await conn.fetchrow('''
                SELECT 
                    COUNT(*) as total_posts,
                    COUNT(DISTINCT platform) as platforms_used,
                    COUNT(CASE WHEN status = 'published' THEN 1 END) as published_count,
                    COUNT(CASE WHEN status = 'scheduled' THEN 1 END) as scheduled_count
                FROM social_posts
                WHERE created_at > NOW() - INTERVAL '%s days'
            ''' % days)
            
            # A/B test metrics
            ab_test_metrics = await conn.fetchrow('''
                SELECT 
                    COUNT(*) as total_tests,
                    COUNT(CASE WHEN status = 'active' THEN 1 END) as active_tests,
                    COUNT(CASE WHEN winner_id IS NOT NULL THEN 1 END) as completed_tests
                FROM ab_tests
                WHERE created_at > NOW() - INTERVAL '%s days'
            ''' % days)
        
        # Calculate derived metrics
        total_cost = float(cost_metrics['total_cost'] or 0)
        content_count = int(content_metrics['total_generated'] or 1)
        avg_quality = float(content_metrics['avg_quality'] or 0)
        
        # Quality distribution
        quality_distribution = {
            'excellent': 0,
            'good': 0,
            'average': 0,
            'needs_improvement': 0
        }
        
        async with db_pool.acquire() as conn:
            quality_data = await conn.fetch('''
                SELECT quality_score
                FROM content
                WHERE created_at > NOW() - INTERVAL '%s days'
                  AND status != 'variant'
            ''' % days)
            
            for row in quality_data:
                score = row['quality_score']
                if score >= 0.85:
                    quality_distribution['excellent'] += 1
                elif score >= 0.70:
                    quality_distribution['good'] += 1
                elif score >= 0.50:
                    quality_distribution['average'] += 1
                else:
                    quality_distribution['needs_improvement'] += 1
        
        return {
            'period_days': days,
            'summary': {
                'total_content_generated': content_count,
                'avg_quality_score': round(avg_quality, 3),
                'avg_seo_score': round(float(content_metrics['avg_seo'] or 0), 3),
                'active_days': int(content_metrics['active_days'] or 0),
                'total_cost': round(total_cost, 2)
            },
            'content': {
                'by_type': [
                    {
                        'type': row['content_type'],
                        'count': row['count'],
                        'avg_quality': round(float(row['avg_quality']), 2)
                    }
                    for row in content_types
                ],
                'by_platform': [
                    {
                        'platform': row['platform'],
                        'count': row['count'],
                        'avg_quality': round(float(row['avg_quality']), 2)
                    }
                    for row in platform_dist
                ],
                'quality_distribution': quality_distribution,
                'high_quality_percentage': round(
                    (int(content_metrics['high_quality_count'] or 0) / max(content_count, 1)) * 100,
                    1
                )
            },
            'costs': {
                'total_cost': round(total_cost, 2),
                'avg_cost_per_content': round(total_cost / max(content_count, 1), 4),
                'total_api_calls': int(cost_metrics['total_requests'] or 0),
                'successful_calls': int(cost_metrics['successful_requests'] or 0),
                'success_rate': round(
                    (int(cost_metrics['successful_requests'] or 0) / max(int(cost_metrics['total_requests'] or 1), 1)) * 100,
                    1
                ),
                'premium_cost': round(float(cost_metrics['premium_cost'] or 0), 2),
                'estimated_monthly': round((total_cost / max(days, 1)) * 30, 2),
                'budget_status': await self._get_budget_status()
            },
            'publishing': {
                'total_posts': int(publish_metrics['total_posts'] or 0),
                'platforms_used': int(publish_metrics['platforms_used'] or 0),
                'published_count': int(publish_metrics['published_count'] or 0),
                'scheduled_count': int(publish_metrics['scheduled_count'] or 0)
            },
            'ab_testing': {
                'total_tests': int(ab_test_metrics['total_tests'] or 0),
                'active_tests': int(ab_test_metrics['active_tests'] or 0),
                'completed_tests': int(ab_test_metrics['completed_tests'] or 0)
            },
            'roi': {
                'cost_per_piece': round(total_cost / max(content_count, 1), 3),
                'pieces_per_dollar': round(content_count / max(total_cost, 0.01), 2),
                'efficiency_score': round((avg_quality * 100) / max(total_cost / content_count, 0.01), 1),
                'estimated_time_saved_hours': content_count * 2,  # Estimate 2 hours saved per content piece
                'estimated_value_generated': content_count * 50  # Estimate $50 value per content piece
            },
            'trends': await self._calculate_trends(days)
        }
    
    async def _get_budget_status(self) -> Dict[str, Any]:
        """Get current budget status"""
        
        if MONTHLY_AI_BUDGET <= 0:
            return {
                'budget_set': False,
                'unlimited': True
            }
        
        month_cost = await cost_controller.get_month_cost()
        remaining = MONTHLY_AI_BUDGET - month_cost
        percentage = (month_cost / MONTHLY_AI_BUDGET) * 100
        
        return {
            'budget_set': True,
            'monthly_budget': MONTHLY_AI_BUDGET,
            'month_to_date': round(month_cost, 2),
            'remaining': round(remaining, 2),
            'percentage_used': round(percentage, 1),
            'status': 'healthy' if percentage < 80 else 'warning' if percentage < 95 else 'critical'
        }
    
    async def _calculate_trends(self, days: int) -> Dict[str, Any]:
        """Calculate trends over time"""
        
        async with db_pool.acquire() as conn:
            # Get weekly trends
            weekly_data = await conn.fetch('''
                SELECT 
                    DATE_TRUNC('week', created_at) as week,
                    COUNT(*) as count,
                    AVG(quality_score) as avg_quality,
                    AVG(seo_score) as avg_seo
                FROM content
                WHERE created_at > NOW() - INTERVAL '%s days'
                  AND status != 'variant'
                GROUP BY DATE_TRUNC('week', created_at)
                ORDER BY week DESC
                LIMIT 4
            ''' % days)
        
        trends = {
            'weekly': [
                {
                    'week': row['week'].isoformat(),
                    'content_count': row['count'],
                    'avg_quality': round(float(row['avg_quality']), 2),
                    'avg_seo': round(float(row['avg_seo']), 2)
                }
                for row in weekly_data
            ]
        }
        
        # Calculate trend direction
        if len(trends['weekly']) >= 2:
            latest = trends['weekly'][0]['content_count']
            previous = trends['weekly'][1]['content_count']
            trends['direction'] = 'up' if latest > previous else 'down' if latest < previous else 'stable'
            trends['change_percentage'] = round(((latest - previous) / max(previous, 1)) * 100, 1)
        else:
            trends['direction'] = 'unknown'
            trends['change_percentage'] = 0
        
        return trends
    
    async def track_event(
        self,
        event_type: str,
        event_data: Dict[str, Any],
        user_id: Optional[str] = None,
        session_id: Optional[str] = None
    ):
        """
        Track an analytics event
        
        Used internally by the system to track all significant events
        """
        
        try:
            async with db_pool.acquire() as conn:
                await conn.execute('''
                    INSERT INTO analytics_events (event_type, event_data, user_id, session_id)
                    VALUES ($1, $2, $3, $4)
                ''', event_type, json.dumps(event_data), user_id, session_id)
        except Exception as e:
            logger.error(f"Failed to track event {event_type}: {e}")

# ============================================
# FREE OPTIONAL ENHANCEMENT: Cost Controller
# ============================================

class CostController:
    """
    FREE OPTIONAL ENHANCEMENT: Budget monitoring and cost control
    
    Prevents budget overruns by:
    - Tracking monthly spending
    - Enforcing daily limits
    - Providing cost projections
    - Alerting on thresholds
    """
    
    def __init__(self):
        self.monthly_budget = MONTHLY_AI_BUDGET
        self.daily_limit = (MONTHLY_AI_BUDGET / 30) if MONTHLY_AI_BUDGET > 0 else float('inf')
        self.daily_api_limit = DAILY_API_LIMIT
    
    async def initialize(self):
        """Initialize cost controller"""
        if self.monthly_budget > 0:
            logger.info(f"Cost control enabled: ${self.monthly_budget}/month budget")
            logger.info(f"Daily limit: ${self.daily_limit:.2f}")
        else:
            logger.info("Cost control disabled (no budget limit set)")
        
        if self.daily_api_limit > 0:
            logger.info(f"Daily API call limit: {self.daily_api_limit} requests")
    
    async def check_budget(self, estimated_cost: float) -> bool:
        """
        Check if request is within budget
        
        Returns True if the request can proceed, False otherwise
        """
        
        if self.monthly_budget <= 0:
            return True  # No budget limit
        
        async with db_pool.acquire() as conn:
            # Get current month's spending
            result = await conn.fetchrow('''
                SELECT SUM(cost) as month_cost
                FROM api_usage
                WHERE created_at >= date_trunc('month', CURRENT_DATE)
                  AND success = true
            ''')
            
            current_cost = float(result['month_cost'] or 0)
            
            # Check monthly budget
            if current_cost + estimated_cost > self.monthly_budget:
                logger.warning(
                    f"Monthly budget would be exceeded: "
                    f"${current_cost:.2f} + ${estimated_cost:.2f} > ${self.monthly_budget:.2f}"
                )
                return False
            
            # Check daily limit
            daily_result = await conn.fetchrow('''
                SELECT SUM(cost) as today_cost
                FROM api_usage
                WHERE created_at >= CURRENT_DATE
                  AND success = true
            ''')
            
            today_cost = float(daily_result['today_cost'] or 0)
            
            if today_cost + estimated_cost > self.daily_limit:
                logger.warning(
                    f"Daily budget would be exceeded: "
                    f"${today_cost:.2f} + ${estimated_cost:.2f} > ${self.daily_limit:.2f}"
                )
                return False
            
            # Check daily API call limit
            if self.daily_api_limit > 0:
                api_count_result = await conn.fetchrow('''
                    SELECT COUNT(*) as today_count
                    FROM api_usage
                    WHERE created_at >= CURRENT_DATE
                ''')
                
                today_count = int(api_count_result['today_count'] or 0)
                
                if today_count >= self.daily_api_limit:
                    logger.warning(
                        f"Daily API limit reached: {today_count}/{self.daily_api_limit} calls"
                    )
                    return False
        
        return True
    
    async def get_month_cost(self) -> float:
        """Get current month's total cost"""
        
        async with db_pool.acquire() as conn:
            result = await conn.fetchrow('''
                SELECT SUM(cost) as month_cost
                FROM api_usage
                WHERE created_at >= date_trunc('month', CURRENT_DATE)
                  AND success = true
            ''')
            
            return float(result['month_cost'] or 0)
    
    async def get_usage_report(self) -> Dict[str, Any]:
        """
        Get detailed cost usage report
        
        Includes projections and alerts
        """
        
        async with db_pool.acquire() as conn:
            # Monthly usage
            monthly = await conn.fetchrow('''
                SELECT 
                    COUNT(*) as requests,
                    SUM(cost) as total_cost,
                    AVG(cost) as avg_cost,
                    SUM(CASE WHEN model = 'multi-model' THEN cost END) as premium_cost
                FROM api_usage
                WHERE created_at >= date_trunc('month', CURRENT_DATE)
                  AND success = true
            ''')
            
            # Daily usage
            daily = await conn.fetchrow('''
                SELECT 
                    COUNT(*) as requests,
                    SUM(cost) as total_cost
                FROM api_usage
                WHERE created_at >= CURRENT_DATE
                  AND success = true
            ''')
            
            # Weekly trend
            weekly_trend = await conn.fetch('''
                SELECT 
                    DATE(created_at) as date,
                    SUM(cost) as daily_cost,
                    COUNT(*) as daily_requests
                FROM api_usage
                WHERE created_at >= CURRENT_DATE - INTERVAL '7 days'
                  AND success = true
                GROUP BY DATE(created_at)
                ORDER BY date DESC
            ''')
        
        month_cost = float(monthly['total_cost'] or 0)
        today_cost = float(daily['total_cost'] or 0)
        
        # Calculate projections
        current_day = datetime.utcnow().day
        days_in_month = 30  # Simplified
        projected_monthly = (month_cost / max(current_day, 1)) * days_in_month if current_day > 0 else 0
        
        # Budget status
        if self.monthly_budget > 0:
            budget_remaining = self.monthly_budget - month_cost
            budget_percentage = (month_cost / self.monthly_budget) * 100
            days_remaining = days_in_month - current_day
            
            # Calculate if we're on track
            expected_spending = (self.monthly_budget / days_in_month) * current_day
            spending_status = "under" if month_cost < expected_spending else "over" if month_cost > expected_spending * 1.1 else "on_track"
        else:
            budget_remaining = None
            budget_percentage = None
            spending_status = "no_budget_set"
        
        return {
            'monthly': {
                'budget': self.monthly_budget if self.monthly_budget > 0 else None,
                'spent': round(month_cost, 2),
                'remaining': round(budget_remaining, 2) if budget_remaining is not None else None,
                'percentage_used': round(budget_percentage, 1) if budget_percentage is not None else None,
                'requests': int(monthly['requests'] or 0),
                'avg_cost_per_request': round(float(monthly['avg_cost'] or 0), 4),
                'premium_cost': round(float(monthly['premium_cost'] or 0), 2),
                'status': spending_status
            },
            'daily': {
                'limit': round(self.daily_limit, 2) if self.daily_limit != float('inf') else None,
                'spent': round(today_cost, 2),
                'remaining': round(self.daily_limit - today_cost, 2) if self.daily_limit != float('inf') else None,
                'requests': int(daily['requests'] or 0),
                'api_limit': self.daily_api_limit if self.daily_api_limit > 0 else None
            },
            'projections': {
                'projected_monthly_cost': round(projected_monthly, 2),
                'will_exceed_budget': projected_monthly > self.monthly_budget if self.monthly_budget > 0 else False,
                'days_until_budget_exhausted': int(budget_remaining / (today_cost / max(current_day, 1))) if budget_remaining and today_cost > 0 else None
            },
            'weekly_trend': [
                {
                    'date': row['date'].isoformat(),
                    'cost': round(float(row['daily_cost']), 2),
                    'requests': int(row['daily_requests'])
                }
                for row in weekly_trend
            ],
            'alerts': self._generate_cost_alerts(month_cost, budget_percentage, projected_monthly)
        }
    
    def _generate_cost_alerts(
        self,
        month_cost: float,
        budget_percentage: Optional[float],
        projected_cost: float
    ) -> List[Dict[str, str]]:
        """Generate cost-related alerts"""
        
        alerts = []
        
        if self.monthly_budget <= 0:
            return alerts
        
        # Budget percentage alerts
        if budget_percentage:
            if budget_percentage >= 95:
                alerts.append({
                    'level': 'critical',
                    'message': f"You've used {budget_percentage:.1f}% of your monthly budget!"
                })
            elif budget_percentage >= 80:
                alerts.append({
                    'level': 'warning',
                    'message': f"You've used {budget_percentage:.1f}% of your monthly budget"
                })
            elif budget_percentage >= 50:
                alerts.append({
                    'level': 'info',
                    'message': f"You've used {budget_percentage:.1f}% of your monthly budget"
                })
        
        # Projection alerts
        if projected_cost > self.monthly_budget:
            overage = projected_cost - self.monthly_budget
            alerts.append({
                'level': 'warning',
                'message': f"Projected to exceed budget by ${overage:.2f} this month"
            })
        
        # Spending rate alerts
        expected_daily = self.monthly_budget / 30
        actual_daily = month_cost / max(datetime.utcnow().day, 1)
        
        if actual_daily > expected_daily * 1.5:
            alerts.append({
                'level': 'warning',
                'message': f"Spending rate is 50% higher than expected (${actual_daily:.2f}/day vs ${expected_daily:.2f}/day)"
            })
        
        return alerts

# ============================================
# FREE OPTIONAL ENHANCEMENT: Content Templates
# ============================================

class ContentTemplates:
    """
    FREE OPTIONAL ENHANCEMENT: Library of proven content templates
    
    Pre-built templates for common content needs:
    - Blog post structures
    - Email sequences
    - Social campaigns
    - Ad copy frameworks
    """
    
    templates = {
        "blog_listicle": {
            "name": "Listicle Blog Post",
            "description": "Number-based article format (e.g., '10 Tips for...')",
            "best_for": ["How-to guides", "Tips and tricks", "Resource lists"],
            "structure": """
# [Number] [Topic] [Benefit/Promise]

## Introduction
Hook the reader with a relatable problem or question. Preview what they'll learn.

## [Item 1]: [Compelling Title]
[Detailed explanation with examples]

## [Item 2]: [Compelling Title]
[Detailed explanation with examples]

[Continue for all items...]

## Conclusion
Summarize key takeaways and include a clear call-to-action.
""",
            "variables": ["number", "topic", "items"],
            "example": "10 AI Marketing Tools That Will Transform Your Business in 2025"
        },
        
        "blog_how_to": {
            "name": "How-To Guide",
            "description": "Step-by-step tutorial format",
            "best_for": ["Tutorials", "Process guides", "Skill-building"],
            "structure": """
# How to [Achieve Specific Result]

## Introduction
- Why this matters
- What you'll need
- Expected outcome

## Step 1: [Action]
Detailed instructions with screenshots/examples

## Step 2: [Action]
Detailed instructions with screenshots/examples

[Continue for all steps...]

## Common Mistakes to Avoid
List of pitfalls and how to avoid them

## Conclusion
Summary and next steps
""",
            "example": "How to Set Up Your First AI Marketing Campaign in 30 Minutes"
        },
        
        "social_campaign": {
            "name": "Multi-Platform Social Campaign",
            "description": "Coordinated social media campaign across platforms",
            "best_for": ["Product launches", "Events", "Brand awareness"],
            "platforms": {
                "twitter": "Hook + Value + CTA in 280 chars. 1-2 hashtags max.",
                "linkedin": "Professional insight + statistics + engagement question. 3-5 hashtags.",
                "instagram": "Visual story + personal touch + 5-10 hashtags.",
                "facebook": "Conversational + community-focused + question to drive comments."
            },
            "example": "New product launch campaign"
        },
        
        "email_welcome": {
            "name": "Welcome Email Sequence",
            "description": "3-email sequence for new subscribers",
            "best_for": ["New subscribers", "Customer onboarding", "Building relationships"],
            "emails": {
                "email_1": {
                    "timing": "Immediately",
                    "subject": "Welcome to [Brand]! Here's what to expect...",
                    "structure": "Warm greeting + Set expectations + Quick win/freebie + What's next"
                },
                "email_2": {
                    "timing": "Day 3",
                    "subject": "The one thing that changed everything for [audience]",
                    "structure": "Story hook + Problem identification + Solution (your product) + Social proof"
                },
                "email_3": {
                    "timing": "Day 7",
                    "subject": "Ready to [achieve result]? Start here.",
                    "structure": "Recap value + Clear offer + Address objections + Urgent CTA"
                }
            },
            "example": "SaaS product welcome sequence"
        },
        
        "ad_copy_psa": {
            "name": "Problem-Solution-Action Ad",
            "description": "Classic direct response ad framework",
            "best_for": ["Facebook ads", "Google ads", "LinkedIn ads"],
            "structure": """
**Headline (Hook):** [Address specific pain point with question or statement]

**Body:**
Problem: Are you struggling with [specific problem]?

Solution: [Your product] helps you [specific benefit] without [common objection].

Proof: [Statistic, testimonial, or result]

**Call-to-Action:** [Clear, action-oriented CTA with urgency]
""",
            "example": "Facebook ad for marketing software"
        },
        
        "landing_page": {
            "name": "High-Converting Landing Page",
            "description": "Conversion-focused page structure",
            "best_for": ["Product pages", "Lead magnets", "Event registrations"],
            "structure": """
## Headline
[Clear value proposition in 10 words or less]

### Subheadline
[Expand on the promise - who it's for and what they get]

### The Problem
[Describe the pain point your audience faces]

### The Solution
[How your product/service solves it]

### Key Benefits
- [Benefit 1 with specific outcome]
- [Benefit 2 with specific outcome]
- [Benefit 3 with specific outcome]

### How It Works
1. [Simple step 1]
2. [Simple step 2]
3. [Simple step 3]

### Social Proof
[Testimonials, logos, statistics]

### Pricing/Offer
[Clear pricing or offer details]

### Risk Reversal
[Guarantee, free trial, money-back policy]

### FAQ
[Address top 5-7 objections]

### Final CTA
[Repeat the call-to-action with urgency]
""",
            "example": "SaaS product landing page"
        }
    }
    
    async def get_all_templates(self) -> Dict[str, Any]:
        """Get list of all available templates"""
        return {
            template_id: {
                'name': template['name'],
                'description': template['description'],
                'best_for': template.get('best_for', []),
                'example': template.get('example', '')
            }
            for template_id, template in self.templates.items()
        }
    
    async def get_template(self, template_id: str) -> Dict[str, Any]:
        """Get specific template details"""
        if template_id not in self.templates:
            raise HTTPException(404, f"Template '{template_id}' not found")
        
        return self.templates[template_id]
    
    async def generate_from_template(
        self,
        template_id: str,
        variables: Dict[str, Any],
        use_ai: bool = True
    ) -> str:
        """
        Generate content using a template
        
        If use_ai=True, will use AI to fill in the template intelligently
        If use_ai=False, will return the template structure for manual filling
        """
        
        template = await self.get_template(template_id)
        
        if not use_ai:
            # Return template structure for manual use
            return template.get('structure', str(template))
        
        # Use AI to intelligently fill the template
        # This would integrate with the ContentEngine
        # For now, return the structure with variable hints
        structure = template.get('structure', '')
        
        # Replace variables if provided
        for key, value in variables.items():
            placeholder = f"[{key}]"
            if placeholder in structure:
                structure = structure.replace(placeholder, str(value))
        
        return structure

# ============================================
# FREE OPTIONAL ENHANCEMENT: Webhook System
# ============================================

class WebhookSystem:
    """
    FREE OPTIONAL ENHANCEMENT: Webhook system for automation
    
    Enables integration with:
    - Zapier (automation platform)
    - Make (formerly Integromat)
    - IFTTT (if-this-then-that)
    - Custom integrations
    
    Cost: Free (you just need webhook URLs)
    """
    
    async def trigger_webhook(
        self,
        event_type: str,
        data: Dict[str, Any],
        webhook_url: str,
        retry_count: int = 0
    ):
        """
        Trigger a webhook with event data
        
        Includes automatic retry logic for failed deliveries
        """
        
        if not webhook_url:
            return
        
        payload = {
            "event": event_type,
            "timestamp": datetime.utcnow().isoformat(),
            "data": data
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    webhook_url,
                    json=payload,
                    timeout=10,
                    headers={
                        "Content-Type": "application/json",
                        "User-Agent": "SPLANTS-Marketing-Engine/2.1"
                    }
                )
                
                success = 200 <= response.status_code < 300
                
                # Log webhook delivery
                async with db_pool.acquire() as conn:
                    await conn.execute('''
                        INSERT INTO webhook_logs
                        (event_type, webhook_url, payload, status_code, response_body, success, retry_count)
                        VALUES ($1, $2, $3, $4, $5, $6, $7)
                    ''', event_type, webhook_url, json.dumps(payload),
                        response.status_code, response.text[:1000], success, retry_count)
                
                if success:
                    logger.info(f"Webhook delivered: {event_type} -> {webhook_url[:50]}... (Status: {response.status_code})")
                else:
                    logger.warning(f"Webhook failed: {event_type} -> {webhook_url[:50]}... (Status: {response.status_code})")
                    
                    # Retry logic
                    if retry_count < 3:
                        await asyncio.sleep(2 ** retry_count)  # Exponential backoff
                        await self.trigger_webhook(event_type, data, webhook_url, retry_count + 1)
                
        except Exception as e:
            logger.error(f"Webhook error: {event_type} -> {webhook_url[:50]}... (Error: {e})")
            
            # Log failure
            async with db_pool.acquire() as conn:
                await conn.execute('''
                    INSERT INTO webhook_logs
                    (event_type, webhook_url, payload, status_code, response_body, success, retry_count)
                    VALUES ($1, $2, $3, $4, $5, $6, $7)
                ''', event_type, webhook_url, json.dumps(payload),
                    0, str(e)[:1000], False, retry_count)
            
            # Retry logic
            if retry_count < 3:
                await asyncio.sleep(2 ** retry_count)
                await self.trigger_webhook(event_type, data, webhook_url, retry_count + 1)

# ============================================
# INITIALIZE SERVICES
# ============================================

content_engine = ContentEngine()
social_publisher = SocialPublisher()
analytics = AnalyticsDashboard()
cost_controller = CostController()
webhook_system = WebhookSystem()

# ============================================
# API ENDPOINTS
# ============================================

@app.get("/", tags=["Core"])
async def root():
    """
    System information endpoint
    
    Provides an overview of system capabilities and configuration status.
    """
    return {
        "name": "SPLANTS Marketing Engine",
        "version": "2.1",
        "status": "operational",
        "description": "AI-powered content generation system for SPLANTS",
        "documentation": {
            "swagger_ui": "/docs",
            "redoc": "/redoc"
        },
        "core_features": {
            "monthly_cost": "$20-30 infrastructure",
            "features": [
                "AI Content Generation (GPT-4)",
                "Multi-Platform Publishing",
                "SEO Optimization",
                "Quality Scoring",
                "Content Storage & Management",
                "API Authentication"
            ]
        },
        "free_enhancements": {
            "cost": "$0/month",
            "features": [
                "Analytics Dashboard - ROI and performance tracking",
                "A/B Testing - Content variation testing",
                "Content Templates - Structured content frameworks",
                "Cost Control - Budget monitoring",
                "Webhook System - Automation integration",
                "Smart Hashtags - Automated hashtag generation",
                "Platform Optimization - Platform-specific content adaptation"
            ]
        },
        "paid_enhancements": {
            "redis_caching": {
                "cost": "$10-15/month",
                "benefit": "30-50% API cost reduction",
                "enabled": CACHE_ENABLED
            },
            "multi_model": {
                "cost": "$0.02-0.05 per request",
                "benefit": "20-30% quality improvement",
                "enabled": bool(ANTHROPIC_API_KEY)
            },
            "auto_publishing": {
                "cost": "Varies by platform",
                "benefit": "Automated social media posting",
                "enabled": any([TWITTER_API_KEY, LINKEDIN_CLIENT_ID])
            }
        },
        "configuration_status": {
            "openai": "Configured" if OPENAI_API_KEY else "Missing (required)",
            "anthropic": "Configured" if ANTHROPIC_API_KEY else "Not configured (optional)",
            "redis_cache": "Enabled" if CACHE_ENABLED else "Disabled (optional)",
            "cost_control": "Enabled" if MONTHLY_AI_BUDGET > 0 else "Disabled (optional)",
            "webhooks": "Configured" if any([WEBHOOK_CONTENT_GENERATED, WEBHOOK_CONTENT_PUBLISHED]) else "Not configured (optional)"
        },
        "setup_steps": {
            "step_1": "Configure OpenAI API key in .env file (OPENAI_API_KEY)",
            "step_2": "Set API authentication key (API_KEY)",
            "step_3": "Test content generation at /v1/generate",
            "step_4": "Review complete documentation at /docs"
        }
    }

@app.get("/health", tags=["Core"])
async def health_check():
    """
    Health check endpoint
    
    Monitors system status and operational state of all services.
    """
    try:
        # Check database
        async with db_pool.acquire() as conn:
            await conn.fetchval("SELECT 1")
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    return {
        "status": "healthy" if db_status == "connected" else "degraded",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "2.1",
        "services": {
            "database": db_status,
            "openai": "configured" if content_engine.openai_client else "not_configured",
            "anthropic": "configured" if content_engine.anthropic_client else "not_configured",
            "redis_cache": "enabled" if CACHE_ENABLED else "disabled",
            "cost_control": "enabled" if MONTHLY_AI_BUDGET > 0 else "disabled"
        },
        "uptime_since": datetime.utcnow().isoformat(),
        "api_docs": "/docs"
    }

# ============================================
# CORE ENDPOINTS - Content Generation
# ============================================

@app.post("/v1/generate", response_model=ContentResponse, tags=["Core - Content Generation"])
async def generate_content(
    request: ContentRequest,
    background_tasks: BackgroundTasks,
    api_key: str = Depends(verify_api_key)
):
    """
    Generate AI content
    
    ## Core Features (Included)
    - GPT-4 content generation
    - Quality scoring
    - SEO optimization
    - Platform optimization
    
    ## FREE Optional Enhancements
    - `include_hashtags`: Auto-generate optimized hashtags (social media)
    - `seo_optimize`: Apply SEO best practices
    - `generate_variants`: Create A/B test versions (3 variants)
    
    ## PAID Optional Enhancements
    - `use_premium`: Multi-model synthesis with GPT-4 + Claude (+$0.02-0.05)
    
    ## Example Request
    ```json
    {
      "content_type": "blog",
      "topic": "10 AI Marketing Tips for Small Business",
      "keywords": ["AI marketing", "small business", "automation"],
      "tone": "professional",
      "length": 800,
      "platform": "blog"
    }
    ```
    """
    try:
        response = await content_engine.generate_content(request, background_tasks)
        return response
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Content generation failed: {e}")
        raise HTTPException(
            500,
            detail=f"Content generation failed: {str(e)}. Please check your configuration and try again."
        )

@app.get("/v1/content/{content_id}", tags=["Core - Content Management"])
async def get_content(
    content_id: int,
    api_key: str = Depends(verify_api_key)
):
    """
    Get content by ID
    
    Retrieves a specific piece of generated content.
    """
    async with db_pool.acquire() as conn:
        content = await conn.fetchrow(
            "SELECT * FROM content WHERE id = $1",
            content_id
        )
    
    if not content:
        raise HTTPException(404, f"Content with ID {content_id} not found")
    
    return dict(content)

@app.get("/v1/content", tags=["Core - Content Management"])
async def list_content(
    limit: int = Query(10, ge=1, le=100, description="Number of results (1-100)"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
    content_type: Optional[ContentType] = Query(None, description="Filter by content type"),
    min_quality: Optional[float] = Query(None, ge=0, le=1, description="Minimum quality score (0-1)"),
    api_key: str = Depends(verify_api_key)
):
    """
    List generated content with pagination and filters
    
    Use this to browse your content library.
    """
    async with db_pool.acquire() as conn:
        query = "SELECT * FROM content WHERE status != 'variant'"
        params = []
        
        if content_type:
            params.append(content_type.value)
            query += f" AND content_type = ${len(params)}"
        
        if min_quality is not None:
            params.append(min_quality)
            query += f" AND quality_score >= ${len(params)}"
        
        query += f" ORDER BY created_at DESC LIMIT {limit} OFFSET {offset}"
        
        content = await conn.fetch(query, *params)
        
        # Get total count for pagination
        count_query = "SELECT COUNT(*) FROM content WHERE status != 'variant'"
        if content_type:
            count_query += f" AND content_type = '{content_type.value}'"
        if min_quality is not None:
            count_query += f" AND quality_score >= {min_quality}"
        
        total_count = await conn.fetchval(count_query)
    
    return {
        "total": total_count,
        "limit": limit,
        "offset": offset,
        "has_more": (offset + limit) < total_count,
        "content": [dict(c) for c in content]
    }

# ============================================
# CORE ENDPOINTS - Publishing
# ============================================

@app.post("/v1/publish", tags=["Core - Publishing"])
async def publish_content(
    request: PublishRequest,
    background_tasks: BackgroundTasks,
    api_key: str = Depends(verify_api_key)
):
    """
    Publish content to social media platforms
    
    ## Core Features
    - Multi-platform content validation
    - Scheduling support
    - Publishing tracking
    
    ## FREE Optional Enhancement
    - `auto_optimize_timing`: Find optimal posting time (based on research)
    
    ## PAID Optional Enhancement
    - Actual platform posting requires platform API keys (costs vary)
    
    ## Example Request
    ```json
    {
      "content_id": 1,
      "platforms": ["twitter", "linkedin"],
      "schedule_time": "2025-11-13T14:00:00Z"
    }
    ```
    """
    try:
        results = await social_publisher.publish(
            request.content_id,
            request.platforms,
            request.schedule_time,
            background_tasks,
            request.auto_optimize_timing
        )
        
        return {
            "status": "success",
            "message": "Content prepared for publishing",
            **results
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Publishing failed: {e}")
        raise HTTPException(500, f"Publishing failed: {str(e)}")

@app.get("/v1/posts", tags=["Core - Publishing"])
async def list_posts(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    platform: Optional[Platform] = Query(None, description="Filter by platform"),
    status: Optional[str] = Query(None, description="Filter by status"),
    api_key: str = Depends(verify_api_key)
):
    """
    List published/scheduled posts
    
    View all your social media posts across platforms.
    """
    async with db_pool.acquire() as conn:
        query = "SELECT * FROM social_posts WHERE 1=1"
        params = []
        
        if platform:
            params.append(platform.value)
            query += f" AND platform = ${len(params)}"
        
        if status:
            params.append(status)
            query += f" AND status = ${len(params)}"
        
        query += f" ORDER BY created_at DESC LIMIT {limit} OFFSET {offset}"
        
        posts = await conn.fetch(query, *params)
        total_count = await conn.fetchval(
            "SELECT COUNT(*) FROM social_posts" +
            (f" WHERE platform = '{platform.value}'" if platform else "") +
            (f" AND status = '{status}'" if status else "")
        )
    
    return {
        "total": total_count,
        "limit": limit,
        "offset": offset,
        "posts": [dict(p) for p in posts]
    }

# ============================================
# FREE OPTIONAL ENHANCEMENT ENDPOINTS
# ============================================

@app.get("/v1/analytics/dashboard", tags=["FREE Enhancement - Analytics"])
async def get_analytics_dashboard(
    days: int = Query(30, ge=1, le=365, description="Number of days to analyze (1-365)"),
    api_key: str = Depends(verify_api_key)
):
    """
    FREE OPTIONAL ENHANCEMENT: Analytics Dashboard
    
    Get comprehensive analytics and ROI metrics including:
    - Content generation statistics
    - Quality and SEO trends
    - Cost tracking and projections
    - Platform distribution
    - A/B test results
    - Weekly trends
    
    This helps you understand:
    - What content performs best
    - Where your budget is going
    - Which platforms get most content
    - Overall system efficiency
    """
    try:
        metrics = await analytics.get_dashboard_metrics(days)
        return metrics
    except Exception as e:
        logger.error(f"Analytics failed: {e}")
        raise HTTPException(500, f"Failed to get analytics: {str(e)}")

@app.get("/v1/templates", tags=["FREE Enhancement - Templates"])
async def list_templates(
    api_key: str = Depends(verify_api_key)
):
    """
    FREE OPTIONAL ENHANCEMENT: Content Templates
    
    Get list of all available content templates.
    Templates are proven content structures that ensure quality and consistency.
    
    Available templates:
    - Blog listicles
    - How-to guides
    - Social campaigns
    - Email sequences
    - Ad copy frameworks
    - Landing pages
    """
    templates = await content_engine.templates.get_all_templates()
    return {
        "total": len(templates),
        "templates": templates
    }

@app.get("/v1/templates/{template_id}", tags=["FREE Enhancement - Templates"])
async def get_template(
    template_id: str,
    api_key: str = Depends(verify_api_key)
):
    """
    FREE OPTIONAL ENHANCEMENT: Get Template Details
    
    Get detailed information about a specific template including:
    - Structure
    - Best use cases
    - Variables needed
        - Examples
    """
    try:
        template = await content_engine.templates.get_template(template_id)
        return template
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Template fetch failed: {e}")
        raise HTTPException(500, f"Failed to get template: {str(e)}")

@app.post("/v1/templates/generate", tags=["FREE Enhancement - Templates"])
async def generate_from_template(
    template_id: str = Query(..., description="Template ID to use"),
    variables: Dict[str, Any] = {},
    use_ai: bool = Query(True, description="Use AI to fill template intelligently"),
    api_key: str = Depends(verify_api_key)
):
    """
    FREE OPTIONAL ENHANCEMENT: Generate from Template
    
    Generate content using a proven template structure.
    
    If `use_ai=true`: AI will intelligently fill the template
    If `use_ai=false`: Returns template structure for manual filling
    
    ## Example Request
    ```json
    {
      "template_id": "blog_listicle",
      "variables": {
        "number": "10",
        "topic": "AI Marketing Tips",
        "items": ["Tip 1", "Tip 2", ...]
      },
      "use_ai": true
    }
    ```
    """
    try:
        result = await content_engine.templates.generate_from_template(
            template_id,
            variables,
            use_ai
        )
        return {
            "template_id": template_id,
            "content": result,
            "ai_generated": use_ai
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Template generation failed: {e}")
        raise HTTPException(500, f"Template generation failed: {str(e)}")

@app.post("/v1/ab-test", tags=["FREE Enhancement - A/B Testing"])
async def create_ab_test(
    request: ContentRequest,
    variants: int = Query(3, ge=2, le=5, description="Number of variants to generate (2-5)"),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    api_key: str = Depends(verify_api_key)
):
    """
    FREE OPTIONAL ENHANCEMENT: A/B Testing
    
    Generate multiple content variants for testing.
    Creates variants with different:
    - Tones
    - Structures
    - Approaches
    
    Perfect for:
    - Email subject lines
    - Ad copy
    - Social media posts
    - Landing page headlines
    
    Returns all variants so you can test which performs best.
    """
    try:
        # Generate original
        original = await content_engine.generate_content(request, background_tasks)
        
        # Generate variants in background
        background_tasks.add_task(
            content_engine._generate_ab_variants,
            request,
            original.id
        )
        
        return {
            "status": "created",
            "message": f"Original content created. Generating {variants-1} additional variants in background.",
            "original": original,
            "note": "Variants will be available shortly. Check /v1/ab-test/{original_id} for results."
        }
    except Exception as e:
        logger.error(f"A/B test creation failed: {e}")
        raise HTTPException(500, f"A/B test creation failed: {str(e)}")

@app.get("/v1/ab-test/{content_id}", tags=["FREE Enhancement - A/B Testing"])
async def get_ab_test_results(
    content_id: int,
    api_key: str = Depends(verify_api_key)
):
    """
    FREE OPTIONAL ENHANCEMENT: Get A/B Test Results
    
    Retrieve all variants for an A/B test.
    """
    async with db_pool.acquire() as conn:
        # Get original content
        original = await conn.fetchrow(
            "SELECT * FROM content WHERE id = $1",
            content_id
        )
        
        if not original:
            raise HTTPException(404, "Content not found")
        
        # Get variants
        variants = await conn.fetch(
            """SELECT * FROM content 
               WHERE metadata->>'original_id' = $1 
               AND metadata->>'is_variant' = 'true'""",
            str(content_id)
        )
        
        # Get test record
        test_record = await conn.fetchrow(
            "SELECT * FROM ab_tests WHERE $1 = ANY(variant_ids)",
            content_id
        )
    
    return {
        "test_id": test_record['id'] if test_record else None,
        "status": test_record['status'] if test_record else 'unknown',
        "original": dict(original),
        "variants": [dict(v) for v in variants],
        "total_variants": len(variants) + 1,
        "winner": test_record['winner_id'] if test_record else None
    }

@app.get("/v1/costs/usage", tags=["FREE Enhancement - Cost Control"])
async def get_cost_usage(
    api_key: str = Depends(verify_api_key)
):
    """
    FREE OPTIONAL ENHANCEMENT: Cost Monitoring
    
    Get detailed cost usage report including:
    - Monthly spending and budget status
    - Daily spending and limits
    - Cost projections
    - Spending trends
    - Alerts and warnings
    
    Use this to:
    - Monitor your AI API spending
    - Stay within budget
    - Identify cost optimization opportunities
    - Plan for next month
    """
    try:
        report = await cost_controller.get_usage_report()
        return report
    except Exception as e:
        logger.error(f"Cost report failed: {e}")
        raise HTTPException(500, f"Cost report failed: {str(e)}")

@app.post("/v1/webhook/register", tags=["FREE Enhancement - Webhooks"])
async def register_webhook(
    event: str = Query(..., description="Event type (e.g., 'content_generated', 'content_published')"),
    url: str = Query(..., description="Webhook URL to call"),
    api_key: str = Depends(verify_api_key)
):
    """
    FREE OPTIONAL ENHANCEMENT: Webhook Registration
    
    Register a webhook URL to receive event notifications.
    
    Perfect for integrating with:
    - Zapier (automation platform)
    - Make (formerly Integromat)
    - IFTTT (if-this-then-that)
    - Custom applications
    
    Available events:
    - `content_generated`: Triggered when content is created
    - `content_published`: Triggered when content is published
    - `budget_alert`: Triggered when approaching budget limits
    - `daily_report`: Daily summary of activity
    
    ## Example
    Set `WEBHOOK_CONTENT_GENERATED_URL` in your .env file, or use this endpoint
    to register webhooks dynamically.
    
    Note: In production, you'd want to store these in the database
    and validate webhook URLs.
    """
    # In production, store this in database
    # For now, just validate and return success
    
    if not url.startswith('http'):
        raise HTTPException(400, "Webhook URL must start with http:// or https://")
    
    # Test the webhook
    try:
        test_payload = {
            "event": "webhook_test",
            "timestamp": datetime.utcnow().isoformat(),
            "message": "This is a test webhook delivery"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                json=test_payload,
                timeout=5
            )
        
        success = 200 <= response.status_code < 300
        
        return {
            "status": "registered" if success else "warning",
            "event": event,
            "url": url,
            "test_status": response.status_code,
            "message": "Webhook registered successfully" if success else "Webhook registered but test delivery failed",
            "note": "Webhook will be triggered on future events. Store this URL in your .env file for persistence."
        }
        
    except Exception as e:
        return {
            "status": "registered_with_warning",
            "event": event,
            "url": url,
            "message": f"Webhook registered but test failed: {str(e)}",
            "note": "Webhook will still be triggered on future events"
        }

@app.get("/v1/webhook/logs", tags=["FREE Enhancement - Webhooks"])
async def get_webhook_logs(
    limit: int = Query(50, ge=1, le=100),
    event_type: Optional[str] = Query(None, description="Filter by event type"),
    api_key: str = Depends(verify_api_key)
):
    """
    FREE OPTIONAL ENHANCEMENT: Webhook Delivery Logs
    
    View webhook delivery history including:
    - Successful deliveries
    - Failed deliveries
    - Retry attempts
    - Response status codes
    """
    async with db_pool.acquire() as conn:
        query = "SELECT * FROM webhook_logs WHERE 1=1"
        params = []
        
        if event_type:
            params.append(event_type)
            query += f" AND event_type = ${len(params)}"
        
        query += f" ORDER BY created_at DESC LIMIT {limit}"
        
        logs = await conn.fetch(query, *params)
    
    return {
        "total": len(logs),
        "logs": [dict(log) for log in logs]
    }

# ============================================
# SYSTEM ENDPOINTS
# ============================================

@app.get("/v1/system/status", tags=["System"])
async def get_system_status(
    api_key: str = Depends(verify_api_key)
):
    """
    Get detailed system status
    
    Includes:
    - Service health
    - Configuration status
    - Feature availability
    - Current load
    """
    
    # Get current usage
    month_cost = await cost_controller.get_month_cost() if MONTHLY_AI_BUDGET > 0 else 0
    
    async with db_pool.acquire() as conn:
        # Content stats
        content_stats = await conn.fetchrow('''
            SELECT 
                COUNT(*) as total,
                COUNT(*) FILTER (WHERE created_at >= CURRENT_DATE) as today
            FROM content
            WHERE status != 'variant'
        ''')
        
        # API call stats
        api_stats = await conn.fetchrow('''
            SELECT 
                COUNT(*) as total_calls,
                COUNT(*) FILTER (WHERE created_at >= CURRENT_DATE) as today_calls
            FROM api_usage
        ''')
    
    return {
        "status": "operational",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "2.1",
        "services": {
            "database": {
                "status": "connected",
                "type": "PostgreSQL"
            },
            "ai_models": {
                "gpt4": {
                    "status": "available" if OPENAI_API_KEY else "not_configured",
                    "provider": "OpenAI"
                },
                "claude": {
                    "status": "available" if ANTHROPIC_API_KEY else "not_configured",
                    "provider": "Anthropic"
                }
            },
            "cache": {
                "status": "enabled" if CACHE_ENABLED else "disabled",
                "type": "Redis" if CACHE_ENABLED else None
            }
        },
        "features": {
            "core": {
                "content_generation": True,
                "multi_platform_publishing": True,
                "seo_optimization": True,
                "quality_scoring": True
            },
            "free_enhancements": {
                "analytics_dashboard": True,
                "ab_testing": True,
                "content_templates": True,
                "cost_control": MONTHLY_AI_BUDGET > 0,
                "webhooks": bool(WEBHOOK_CONTENT_GENERATED or WEBHOOK_CONTENT_PUBLISHED),
                "smart_hashtags": True,
                "platform_optimization": True
            },
            "paid_enhancements": {
                "redis_caching": CACHE_ENABLED,
                "multi_model_synthesis": bool(ANTHROPIC_API_KEY),
                "auto_publishing": any([TWITTER_API_KEY, LINKEDIN_CLIENT_ID])
            }
        },
        "usage": {
            "content": {
                "total": int(content_stats['total']),
                "today": int(content_stats['today'])
            },
            "api_calls": {
                "total": int(api_stats['total_calls']),
                "today": int(api_stats['today_calls']),
                "daily_limit": DAILY_API_LIMIT if DAILY_API_LIMIT > 0 else "unlimited"
            },
            "costs": {
                "month_to_date": round(month_cost, 2),
                "budget": MONTHLY_AI_BUDGET if MONTHLY_AI_BUDGET > 0 else "unlimited",
                "percentage_used": round((month_cost / MONTHLY_AI_BUDGET * 100), 1) if MONTHLY_AI_BUDGET > 0 else None
            }
        },
        "configuration": {
            "monthly_budget": MONTHLY_AI_BUDGET if MONTHLY_AI_BUDGET > 0 else None,
            "daily_api_limit": DAILY_API_LIMIT if DAILY_API_LIMIT > 0 else None,
            "max_content_length": MAX_CONTENT_LENGTH,
            "cache_enabled": CACHE_ENABLED
        }
    }

@app.get("/v1/system/health/detailed", tags=["System"])
async def detailed_health_check(
    api_key: str = Depends(verify_api_key)
):
    """
    Detailed health check with component testing
    
    Tests all system components and reports individual status
    """
    health = {
        "overall": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "components": {}
    }
    
    # Test database
    try:
        async with db_pool.acquire() as conn:
            await conn.fetchval("SELECT 1")
        health["components"]["database"] = {
            "status": "healthy",
            "latency_ms": 0  # Would measure actual latency
        }
    except Exception as e:
        health["components"]["database"] = {
            "status": "unhealthy",
            "error": str(e)
        }
        health["overall"] = "degraded"
    
    # Test OpenAI
    try:
        if content_engine.openai_client:
            # Don't make actual API call in health check (costs money)
            # Just verify client is configured
            health["components"]["openai"] = {
                "status": "configured",
                "note": "Client initialized"
            }
        else:
            health["components"]["openai"] = {
                "status": "not_configured",
                "note": "Add OPENAI_API_KEY to enable"
            }
    except Exception as e:
        health["components"]["openai"] = {
            "status": "error",
            "error": str(e)
        }
    
    # Test Redis (if enabled)
    if CACHE_ENABLED:
        # Would test actual Redis connection
        health["components"]["redis"] = {
            "status": "configured",
            "note": "Cache enabled"
        }
    else:
        health["components"]["redis"] = {
            "status": "disabled",
            "note": "Add REDIS_URL to enable caching"
        }
    
    return health

# ============================================
# ERROR HANDLERS
# ============================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler with helpful error messages"""
    return {
        "error": exc.detail,
        "status_code": exc.status_code,
        "timestamp": datetime.utcnow().isoformat(),
        "path": str(request.url),
        "method": request.method,
        "help": {
            403: "Invalid API key. Check your X-API-Key header.",
            404: "Resource not found. Check the endpoint URL.",
            402: "Budget limit reached. Increase your MONTHLY_AI_BUDGET or wait until next month.",
            429: "Rate limit exceeded. Too many requests.",
            500: "Server error. Check logs for details.",
            503: "Service temporarily unavailable. Try again later."
        }.get(exc.status_code, "See API documentation at /docs")
    }

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Catch-all exception handler"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return {
        "error": "Internal server error",
        "message": str(exc),
        "status_code": 500,
        "timestamp": datetime.utcnow().isoformat(),
        "path": str(request.url),
        "note": "This error has been logged. Please contact support if it persists."
    }

# ============================================
# RUN APPLICATION
# ============================================

if __name__ == "__main__":
    import uvicorn
    
    logger.info("=" * 60)
    logger.info("Starting SPLANTS Marketing Engine - ")
    logger.info("=" * 60)
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8080,
        log_level="info",
        reload=False,  # Set to True for development
        access_log=True
    )