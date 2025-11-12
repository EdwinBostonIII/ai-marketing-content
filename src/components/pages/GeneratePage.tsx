import { useState } from 'react'
import { Sparkle, TrendUp, Copy, WarningCircle } from '@phosphor-icons/react'
import { Button } from '@/components/ui/button'
import { Card } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Switch } from '@/components/ui/switch'
import { Badge } from '@/components/ui/badge'
import { toast } from 'sonner'
import { ContentType, Tone, GeneratedContent } from '@/lib/types'
import { useSettings, createApiRequest } from '@/lib/api'

export default function GeneratePage() {
  const { settings } = useSettings()
  const [topic, setTopic] = useState('')
  const [keywords, setKeywords] = useState('')
  const [contentType, setContentType] = useState<ContentType>('blog_post')
  const [tone, setTone] = useState<Tone>('professional')
  const [usePremium, setUsePremium] = useState(false)
  const [isGenerating, setIsGenerating] = useState(false)
  const [generatedContent, setGeneratedContent] = useState<GeneratedContent | null>(null)

  const handleGenerate = async () => {
    if (!topic.trim()) {
      toast.error('Please enter a topic')
      return
    }

    if (!settings?.apiKey) {
      toast.error('Please configure your API key in Settings')
      return
    }

    setIsGenerating(true)
    setGeneratedContent(null)

    try {
      const apiRequest = await createApiRequest(settings)
      const result = await apiRequest<GeneratedContent>('/v1/generate', {
        method: 'POST',
        body: JSON.stringify({
          topic,
          keywords: keywords.split(',').map(k => k.trim()).filter(k => k),
          content_type: contentType,
          tone,
          use_premium: usePremium
        })
      })

      setGeneratedContent(result)
      toast.success('Content generated successfully!')
    } catch (error) {
      toast.error(error instanceof Error ? error.message : 'Failed to generate content')
    } finally {
      setIsGenerating(false)
    }
  }

  const handleCopy = () => {
    if (generatedContent?.content) {
      navigator.clipboard.writeText(generatedContent.content)
      toast.success('Content copied to clipboard!')
    }
  }

  const getQualityColor = (score: number) => {
    if (score >= 80) return 'bg-green-500'
    if (score >= 60) return 'bg-accent'
    return 'bg-destructive'
  }

  const getQualityLabel = (score: number) => {
    if (score >= 80) return 'Excellent'
    if (score >= 60) return 'Good'
    return 'Needs Work'
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-semibold tracking-tight">Generate Content</h1>
        <p className="text-muted-foreground mt-2">
          Create AI-powered marketing content with built-in quality and SEO scoring
        </p>
      </div>

      <div className="grid lg:grid-cols-2 gap-6">
        <Card className="p-6">
          <div className="space-y-6">
            <div className="space-y-2">
              <Label htmlFor="topic" className="text-base font-medium">Topic</Label>
              <Input
                id="topic"
                placeholder="e.g., The benefits of remote work"
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
                disabled={isGenerating}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="keywords" className="text-base font-medium">Keywords</Label>
              <Input
                id="keywords"
                placeholder="e.g., remote, productivity, work-life balance"
                value={keywords}
                onChange={(e) => setKeywords(e.target.value)}
                disabled={isGenerating}
              />
              <p className="text-sm text-muted-foreground">Separate keywords with commas</p>
            </div>

            <div className="grid sm:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="content-type" className="text-base font-medium">Content Type</Label>
                <Select value={contentType} onValueChange={(value) => setContentType(value as ContentType)} disabled={isGenerating}>
                  <SelectTrigger id="content-type">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="blog_post">Blog Post</SelectItem>
                    <SelectItem value="social_post">Social Post</SelectItem>
                    <SelectItem value="email">Email</SelectItem>
                    <SelectItem value="ad_copy">Ad Copy</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="tone" className="text-base font-medium">Tone</Label>
                <Select value={tone} onValueChange={(value) => setTone(value as Tone)} disabled={isGenerating}>
                  <SelectTrigger id="tone">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="professional">Professional</SelectItem>
                    <SelectItem value="casual">Casual</SelectItem>
                    <SelectItem value="friendly">Friendly</SelectItem>
                    <SelectItem value="persuasive">Persuasive</SelectItem>
                    <SelectItem value="informative">Informative</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>

            <div className="flex items-center justify-between p-4 bg-secondary rounded-lg">
              <div className="space-y-0.5">
                <Label htmlFor="premium" className="text-base font-medium">Premium AI</Label>
                <p className="text-sm text-muted-foreground">Use multi-model synthesis for higher quality</p>
              </div>
              <Switch
                id="premium"
                checked={usePremium}
                onCheckedChange={setUsePremium}
                disabled={isGenerating}
              />
            </div>

            <Button 
              onClick={handleGenerate}
              disabled={isGenerating}
              className="w-full h-12 text-base"
              size="lg"
            >
              <Sparkle className="mr-2" weight="fill" />
              {isGenerating ? 'Generating...' : 'Generate Content'}
            </Button>
          </div>
        </Card>

        <Card className="p-6">
          {!generatedContent && !isGenerating && (
            <div className="h-full flex flex-col items-center justify-center text-center p-8 text-muted-foreground">
              <Sparkle size={48} className="mb-4 opacity-50" />
              <p className="text-lg font-medium mb-2">Your content will appear here</p>
              <p className="text-sm">Fill out the form and click Generate to create AI-powered content</p>
            </div>
          )}

          {isGenerating && (
            <div className="h-full flex flex-col items-center justify-center text-center p-8">
              <div className="animate-spin mb-4">
                <Sparkle size={48} className="text-primary" weight="fill" />
              </div>
              <p className="text-lg font-medium mb-2">Generating your content...</p>
              <p className="text-sm text-muted-foreground">This may take a few moments</p>
            </div>
          )}

          {generatedContent && !isGenerating && (
            <div className="space-y-4">
              <div className="flex items-start justify-between gap-4">
                <div className="space-y-1">
                  <h3 className="text-lg font-semibold">Generated Content</h3>
                  <p className="text-sm text-muted-foreground">{generatedContent.topic}</p>
                </div>
                <Button onClick={handleCopy} variant="outline" size="sm">
                  <Copy className="mr-2" />
                  Copy
                </Button>
              </div>

              <div className="flex gap-2">
                <Badge variant="secondary" className="gap-1">
                  <TrendUp size={14} />
                  Quality: {generatedContent.quality_score}
                </Badge>
                <Badge variant="secondary" className="gap-1">
                  <TrendUp size={14} />
                  SEO: {generatedContent.seo_score}
                </Badge>
                <Badge className={`${getQualityColor(generatedContent.quality_score)} text-white`}>
                  {getQualityLabel(generatedContent.quality_score)}
                </Badge>
              </div>

              <div className="bg-muted p-4 rounded-lg max-h-[400px] overflow-y-auto">
                <p className="whitespace-pre-wrap text-sm leading-relaxed">{generatedContent.content}</p>
              </div>

              {generatedContent.quality_score < 60 && (
                <div className="flex gap-2 p-3 bg-amber-50 border border-amber-200 rounded-lg">
                  <WarningCircle className="text-amber-600 flex-shrink-0 mt-0.5" size={20} />
                  <div className="text-sm">
                    <p className="font-medium text-amber-900">Quality could be improved</p>
                    <p className="text-amber-700">Try enabling Premium AI or refining your keywords</p>
                  </div>
                </div>
              )}

              <div className="pt-2 border-t text-sm text-muted-foreground flex justify-between">
                <span>Cost: ${generatedContent.cost.toFixed(4)}</span>
                <span>Generated {new Date(generatedContent.created_at).toLocaleTimeString()}</span>
              </div>
            </div>
          )}
        </Card>
      </div>
    </div>
  )
}
