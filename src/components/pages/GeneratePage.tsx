import { useState } from 'react'
import { PaintBrushBroad, Sparkle } from '@phosphor-icons/react'
import { Card } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import RadialProgress from '@/components/RadialProgress'
import { toast } from 'sonner'

interface GeneratedContent {
  content: string
  quality_score: number
  seo_score: number
  word_count: number
  reading_time: number
}

export default function GeneratePage() {
  const [loading, setLoading] = useState(false)
  const [generated, setGenerated] = useState<GeneratedContent | null>(null)
  
  const [contentType, setContentType] = useState('blog')
  const [topic, setTopic] = useState('')
  const [tone, setTone] = useState('professional')
  const [platform, setPlatform] = useState('blog')
  const [length, setLength] = useState('800')

  const handleGenerate = async () => {
    if (!topic.trim()) {
      toast.error('Please enter a topic')
      return
    }

    setLoading(true)
    
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    const mockContent = {
      content: `# ${topic}\n\nTransform your style with SPLANTS custom paint-splatter pants. Each pair features unique Jackson Pollock-inspired patterns that make a bold statement.\n\n## Why Choose SPLANTS?\n\nOur handcrafted pants combine artistic expression with everyday wearability. Every splash of paint is carefully applied to create one-of-a-kind pieces that reflect your personality.\n\n### Premium Quality\n- Durable fabric that withstands daily wear\n- Vibrant, long-lasting colors\n- Comfortable fit for all-day comfort\n\n### Unique Design\nNo two pairs are exactly alike. Your SPLANTS are as individual as you are.\n\n### Express Yourself\nMake a statement without saying a word. SPLANTS let your creativity shine through your wardrobe.`,
      quality_score: Math.random() * 20 + 80,
      seo_score: Math.random() * 20 + 75,
      word_count: parseInt(length) || 800,
      reading_time: Math.ceil((parseInt(length) || 800) / 200)
    }
    
    setGenerated(mockContent)
    setLoading(false)
    toast.success('Content generated successfully!')
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-4xl font-bold mb-2">Generate Content</h1>
        <p className="text-muted-foreground">Create AI-powered marketing content in seconds</p>
      </div>

      <div className="grid lg:grid-cols-2 gap-8">
        <Card className="p-8 shadow-md">
          <div className="space-y-6">
            <div className="space-y-2">
              <Label htmlFor="content-type">Content Type</Label>
              <Select value={contentType} onValueChange={setContentType}>
                <SelectTrigger id="content-type">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="blog">Blog Post</SelectItem>
                  <SelectItem value="social">Social Media</SelectItem>
                  <SelectItem value="email">Email</SelectItem>
                  <SelectItem value="ad">Advertisement</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label htmlFor="topic">Topic</Label>
              <Input
                id="topic"
                placeholder="e.g., 10 Reasons to Love Custom Pants"
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="tone">Tone</Label>
              <Select value={tone} onValueChange={setTone}>
                <SelectTrigger id="tone">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="professional">Professional</SelectItem>
                  <SelectItem value="casual">Casual</SelectItem>
                  <SelectItem value="playful">Playful</SelectItem>
                  <SelectItem value="inspirational">Inspirational</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label htmlFor="platform">Platform</Label>
              <Select value={platform} onValueChange={setPlatform}>
                <SelectTrigger id="platform">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="blog">Blog</SelectItem>
                  <SelectItem value="twitter">Twitter</SelectItem>
                  <SelectItem value="linkedin">LinkedIn</SelectItem>
                  <SelectItem value="instagram">Instagram</SelectItem>
                  <SelectItem value="facebook">Facebook</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label htmlFor="length">Word Count</Label>
              <Input
                id="length"
                type="number"
                placeholder="800"
                value={length}
                onChange={(e) => setLength(e.target.value)}
              />
            </div>

            <Button
              onClick={handleGenerate}
              disabled={loading}
              className="w-full wet-paint-sheen text-lg py-6 font-semibold"
            >
              {loading ? (
                <>
                  <Sparkle className="animate-spin" weight="fill" />
                  Generating...
                </>
              ) : (
                <>
                  <PaintBrushBroad weight="fill" />
                  Generate Content
                </>
              )}
            </Button>
          </div>
        </Card>

        <div className="space-y-6">
          {generated && (
            <>
              <Card className="p-6 shadow-md">
                <div className="flex items-center justify-around">
                  <RadialProgress value={generated.quality_score} label="Quality Score" />
                  <RadialProgress value={generated.seo_score} label="SEO Score" />
                </div>
              </Card>

              <Card className="p-6 shadow-md">
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <h3 className="text-xl font-semibold">Generated Content</h3>
                    <div className="flex gap-4 text-sm text-muted-foreground">
                      <span>{generated.word_count} words</span>
                      <span>{generated.reading_time} min read</span>
                    </div>
                  </div>
                  <div className="prose prose-sm max-w-none">
                    <Textarea
                      value={generated.content}
                      readOnly
                      className="min-h-[400px] font-mono text-sm"
                    />
                  </div>
                  <div className="flex gap-2">
                    <Button variant="outline" className="flex-1">
                      Copy
                    </Button>
                    <Button variant="outline" className="flex-1">
                      Save to Library
                    </Button>
                  </div>
                </div>
              </Card>
            </>
          )}

          {!generated && (
            <Card className="p-12 shadow-md flex items-center justify-center border-dashed">
              <div className="text-center space-y-4">
                <PaintBrushBroad size={64} className="mx-auto text-muted-foreground" weight="thin" />
                <div>
                  <h3 className="text-lg font-semibold mb-1">Ready to Create</h3>
                  <p className="text-sm text-muted-foreground">
                    Fill out the form and generate your first piece of content
                  </p>
                </div>
              </div>
            </Card>
          )}
        </div>
      </div>
    </div>
  )
}
