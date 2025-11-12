import { FolderOpen, MagnifyingGlass, Calendar, FileText } from '@phosphor-icons/react'
import { Card } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { useState } from 'react'

interface ContentItem {
  id: number
  title: string
  type: string
  date: string
  quality: number
  seo: number
  words: number
}

const mockLibrary: ContentItem[] = [
  { id: 1, title: '10 Reasons to Love Custom Paint-Splatter Pants', type: 'blog', date: '2025-01-15', quality: 92, seo: 88, words: 850 },
  { id: 2, title: 'Spring Fashion Trends with SPLANTS', type: 'blog', date: '2025-01-14', quality: 89, seo: 85, words: 720 },
  { id: 3, title: 'New Arrivals - Bold and Colorful', type: 'social', date: '2025-01-13', quality: 94, seo: 90, words: 120 },
  { id: 4, title: 'Express Your Creativity Through Fashion', type: 'email', date: '2025-01-12', quality: 87, seo: 82, words: 450 },
  { id: 5, title: 'Limited Edition: Pollock-Inspired Collection', type: 'ad', date: '2025-01-11', quality: 95, seo: 92, words: 200 },
  { id: 6, title: 'Customer Spotlight: Style Stories', type: 'blog', date: '2025-01-10', quality: 91, seo: 87, words: 680 },
]

export default function LibraryPage() {
  const [search, setSearch] = useState('')

  const filteredLibrary = mockLibrary.filter(item =>
    item.title.toLowerCase().includes(search.toLowerCase())
  )

  const getTypeColor = (type: string) => {
    switch (type) {
      case 'blog': return 'bg-blue-100 text-blue-700 border-blue-200'
      case 'social': return 'bg-purple-100 text-purple-700 border-purple-200'
      case 'email': return 'bg-green-100 text-green-700 border-green-200'
      case 'ad': return 'bg-amber-100 text-amber-700 border-amber-200'
      default: return 'bg-gray-100 text-gray-700 border-gray-200'
    }
  }

  return (
    <div className="space-y-8">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-4xl font-bold mb-2">Content Library</h1>
          <p className="text-muted-foreground">Browse and manage your generated content</p>
        </div>
        <div className="relative w-full sm:w-80">
          <MagnifyingGlass
            size={20}
            className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground"
          />
          <Input
            placeholder="Search content..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="pl-10"
          />
        </div>
      </div>

      <div className="grid gap-4">
        {filteredLibrary.map((item) => (
          <Card key={item.id} className="p-6 shadow-md hover:shadow-lg transition-shadow">
            <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
              <div className="flex-1 space-y-3">
                <div className="flex items-start gap-3">
                  <FileText size={24} weight="fill" style={{ color: 'oklch(0.75 0.15 85)' }} className="mt-1" />
                  <div className="flex-1">
                    <h3 className="text-lg font-semibold mb-1">{item.title}</h3>
                    <div className="flex flex-wrap items-center gap-3 text-sm text-muted-foreground">
                      <div className="flex items-center gap-1">
                        <Calendar size={16} />
                        {new Date(item.date).toLocaleDateString()}
                      </div>
                      <span>•</span>
                      <span>{item.words} words</span>
                      <span>•</span>
                      <span>Quality: {item.quality}%</span>
                      <span>•</span>
                      <span>SEO: {item.seo}%</span>
                    </div>
                  </div>
                </div>
              </div>
              
              <div className="flex items-center gap-3 lg:ml-4">
                <Badge className={`${getTypeColor(item.type)} border`}>
                  {item.type}
                </Badge>
                <div className="flex gap-2">
                  <Button variant="outline" size="sm">
                    View
                  </Button>
                  <Button variant="outline" size="sm">
                    Edit
                  </Button>
                </div>
              </div>
            </div>
          </Card>
        ))}
      </div>

      {filteredLibrary.length === 0 && (
        <Card className="p-12 shadow-md flex items-center justify-center border-dashed">
          <div className="text-center space-y-4">
            <FolderOpen size={64} className="mx-auto text-muted-foreground" weight="thin" />
            <div>
              <h3 className="text-lg font-semibold mb-1">No Content Found</h3>
              <p className="text-sm text-muted-foreground">
                Try adjusting your search or generate new content
              </p>
            </div>
          </div>
        </Card>
      )}
    </div>
  )
}
