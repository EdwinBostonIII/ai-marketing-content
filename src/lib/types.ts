export type ContentType = 'blog_post' | 'social_post' | 'email' | 'ad_copy'

export type Tone = 'professional' | 'casual' | 'friendly' | 'persuasive' | 'informative'

export interface GenerateRequest {
  topic: string
  keywords: string[]
  content_type: ContentType
  tone: Tone
  use_premium?: boolean
}

export interface GeneratedContent {
  id: string
  content: string
  quality_score: number
  seo_score: number
  content_type: ContentType
  topic: string
  created_at: string
  tone: Tone
  cost: number
}

export interface AnalyticsData {
  total_content: number
  avg_quality_score: number
  avg_seo_score: number
  total_cost: number
  monthly_cost: number
  content_by_type: Record<ContentType, number>
  quality_trend: Array<{ date: string; score: number }>
  roi: number
}

export interface Settings {
  apiKey: string
  monthlyBudget: number
  webhookUrls: string[]
  apiEndpoint: string
}
