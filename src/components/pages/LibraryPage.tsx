import { useState, useEffect } from 'react'
import { Database, Copy, Trash, MagnifyingGlass, Article, ChatCircle, EnvelopeSimple, Megaphone } from '@phosphor-icons/react'
import { Button } from '@/components/ui/button'
import { Card } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Badge } from '@/components/ui/badge'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { toast } from 'sonner'
import { GeneratedContent, ContentType } from '@/lib/types'
import { useSettings, createApiRequest } from '@/lib/api'
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from '@/components/ui/alert-dialog'

export default function LibraryPage() {
  const { settings } = useSettings()
  const [contents, setContents] = useState<GeneratedContent[]>([])
  const [filteredContents, setFilteredContents] = useState<GeneratedContent[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [filterType, setFilterType] = useState<ContentType | 'all'>('all')
  const [deleteId, setDeleteId] = useState<string | null>(null)
  const [expandedId, setExpandedId] = useState<string | null>(null)

  useEffect(() => {
    loadContent()
  }, [])

  useEffect(() => {
    filterContent()
  }, [contents, searchTerm, filterType])

  const loadContent = async () => {
    if (!settings?.apiKey) {
      setIsLoading(false)
      return
    }

    try {
      const apiRequest = await createApiRequest(settings)
      const result = await apiRequest<GeneratedContent[]>('/v1/content', {
        method: 'GET'
      })
      setContents(result)
    } catch (error) {
      toast.error('Failed to load content library')
    } finally {
      setIsLoading(false)
    }
  }

  const filterContent = () => {
    let filtered = contents

    if (filterType !== 'all') {
      filtered = filtered.filter(c => c.content_type === filterType)
    }

    if (searchTerm) {
      const term = searchTerm.toLowerCase()
      filtered = filtered.filter(c =>
        c.topic.toLowerCase().includes(term) ||
        c.content.toLowerCase().includes(term)
      )
    }

    setFilteredContents(filtered)
  }

  const handleCopy = (content: string) => {
    navigator.clipboard.writeText(content)
    toast.success('Content copied to clipboard!')
  }

  const handleDelete = async () => {
    if (!deleteId || !settings) return

    try {
      const apiRequest = await createApiRequest(settings)
      await apiRequest(`/v1/content/${deleteId}`, {
        method: 'DELETE'
      })
      setContents(contents.filter(c => c.id !== deleteId))
      toast.success('Content deleted successfully')
    } catch (error) {
      toast.error('Failed to delete content')
    } finally {
      setDeleteId(null)
    }
  }

  const getContentIcon = (type: ContentType) => {
    switch (type) {
      case 'blog_post':
        return <Article size={20} />
      case 'social_post':
        return <ChatCircle size={20} />
      case 'email':
        return <EnvelopeSimple size={20} />
      case 'ad_copy':
        return <Megaphone size={20} />
    }
  }

  const getTypeLabel = (type: ContentType) => {
    return type.split('_').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ')
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-center">
          <Database size={48} className="mx-auto mb-4 opacity-50 animate-pulse" />
          <p className="text-muted-foreground">Loading content library...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-semibold tracking-tight">Content Library</h1>
        <p className="text-muted-foreground mt-2">
          Browse and manage all your generated content
        </p>
      </div>

      <Card className="p-6">
        <div className="flex flex-col sm:flex-row gap-4 mb-6">
          <div className="relative flex-1">
            <MagnifyingGlass className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground" size={20} />
            <Input
              placeholder="Search content..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10"
            />
          </div>
          <Select value={filterType} onValueChange={(value) => setFilterType(value as ContentType | 'all')}>
            <SelectTrigger className="w-full sm:w-[200px]">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Types</SelectItem>
              <SelectItem value="blog_post">Blog Posts</SelectItem>
              <SelectItem value="social_post">Social Posts</SelectItem>
              <SelectItem value="email">Emails</SelectItem>
              <SelectItem value="ad_copy">Ad Copy</SelectItem>
            </SelectContent>
          </Select>
        </div>

        {!settings?.apiKey ? (
          <div className="text-center py-12">
            <Database size={48} className="mx-auto mb-4 opacity-50" />
            <p className="text-lg font-medium mb-2">Configure API Key</p>
            <p className="text-sm text-muted-foreground">
              Set up your API key in Settings to view your content library
            </p>
          </div>
        ) : filteredContents.length === 0 ? (
          <div className="text-center py-12">
            <Database size={48} className="mx-auto mb-4 opacity-50" />
            <p className="text-lg font-medium mb-2">
              {contents.length === 0 ? 'No content yet' : 'No matching content'}
            </p>
            <p className="text-sm text-muted-foreground">
              {contents.length === 0
                ? 'Generate your first piece of content to get started'
                : 'Try adjusting your search or filters'}
            </p>
          </div>
        ) : (
          <div className="space-y-3">
            {filteredContents.map((item) => (
              <Card key={item.id} className="p-4 hover:shadow-md transition-shadow">
                <div className="space-y-3">
                  <div className="flex items-start justify-between gap-4">
                    <div className="flex items-start gap-3 flex-1 min-w-0">
                      <div className="text-primary mt-1">
                        {getContentIcon(item.content_type)}
                      </div>
                      <div className="flex-1 min-w-0">
                        <h3 className="font-medium text-base mb-1 truncate">{item.topic}</h3>
                        <div className="flex flex-wrap gap-2 text-sm text-muted-foreground">
                          <Badge variant="outline">{getTypeLabel(item.content_type)}</Badge>
                          <Badge variant="outline">Quality: {item.quality_score}</Badge>
                          <Badge variant="outline">SEO: {item.seo_score}</Badge>
                          <span className="text-xs">
                            {new Date(item.created_at).toLocaleDateString()}
                          </span>
                        </div>
                      </div>
                    </div>
                    <div className="flex gap-2">
                      <Button
                        size="sm"
                        variant="outline"
                        onClick={() => handleCopy(item.content)}
                      >
                        <Copy size={16} />
                      </Button>
                      <Button
                        size="sm"
                        variant="outline"
                        onClick={() => setDeleteId(item.id)}
                      >
                        <Trash size={16} />
                      </Button>
                    </div>
                  </div>

                  {expandedId === item.id && (
                    <div className="bg-muted p-3 rounded-lg text-sm">
                      <p className="whitespace-pre-wrap">{item.content}</p>
                    </div>
                  )}

                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => setExpandedId(expandedId === item.id ? null : item.id)}
                    className="w-full text-xs"
                  >
                    {expandedId === item.id ? 'Show less' : 'Show full content'}
                  </Button>
                </div>
              </Card>
            ))}
          </div>
        )}
      </Card>

      <AlertDialog open={!!deleteId} onOpenChange={(open) => !open && setDeleteId(null)}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Delete content?</AlertDialogTitle>
            <AlertDialogDescription>
              This action cannot be undone. This will permanently delete this content from your library.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Cancel</AlertDialogCancel>
            <AlertDialogAction onClick={handleDelete} className="bg-destructive text-destructive-foreground">
              Delete
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </div>
  )
}
