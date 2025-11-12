import { useState, useEffect, useRef } from 'react'
import { ArrowLeft, ListBullets, BookmarkSimple } from '@phosphor-icons/react'
import { Button } from '@/components/ui/button'
import { Card } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { ScrollArea } from '@/components/ui/scroll-area'
import { documents, documentContent, parseMarkdownTOC } from '@/lib/documents'
import { TOCItem } from '@/lib/doc-types'
import { useKV } from '@github/spark/hooks'
import MarkdownRenderer from '@/components/MarkdownRenderer'
import { cn } from '@/lib/utils'

interface DocumentViewerPageProps {
  documentId: string
  onBack: () => void
}

export default function DocumentViewerPage({ documentId, onBack }: DocumentViewerPageProps) {
  const doc = documents[documentId]
  const content = documentContent[documentId]
  const [toc, setToc] = useState<TOCItem[]>([])
  const [activeSection, setActiveSection] = useState<string>('')
  const [showTOC, setShowTOC] = useState(true)
  const contentRef = useRef<HTMLDivElement>(null)
  const [bookmarked, setBookmarked] = useKV<string[]>('doc-bookmarks', [])
  const [scrollProgress, setScrollProgress] = useState(0)

  const isBookmarked = bookmarked?.includes(documentId) || false

  useEffect(() => {
    if (content) {
      const tocItems = parseMarkdownTOC(content)
      setToc(tocItems)
    }
  }, [content])

  useEffect(() => {
    const handleScroll = () => {
      if (!contentRef.current) return
      
      const scrollTop = contentRef.current.scrollTop
      const scrollHeight = contentRef.current.scrollHeight - contentRef.current.clientHeight
      const progress = (scrollTop / scrollHeight) * 100
      setScrollProgress(Math.min(100, Math.max(0, progress)))
    }

    const currentRef = contentRef.current
    if (currentRef) {
      currentRef.addEventListener('scroll', handleScroll)
      return () => currentRef.removeEventListener('scroll', handleScroll)
    }
  }, [])

  const toggleBookmark = () => {
    setBookmarked((current) => {
      const bookmarks = current || []
      if (bookmarks.includes(documentId)) {
        return bookmarks.filter(id => id !== documentId)
      } else {
        return [...bookmarks, documentId]
      }
    })
  }

  const scrollToSection = (id: string) => {
    const element = document.getElementById(id)
    if (element && contentRef.current) {
      const top = element.offsetTop - contentRef.current.offsetTop - 80
      contentRef.current.scrollTo({ top, behavior: 'smooth' })
      setActiveSection(id)
    }
  }

  const renderTOCItems = (items: TOCItem[], level = 0) => {
    return items.map((item) => (
      <div key={item.id}>
        <button
          onClick={() => scrollToSection(item.id)}
          className={cn(
            'w-full text-left text-sm py-1.5 px-3 rounded transition-colors',
            activeSection === item.id
              ? 'bg-primary/10 text-primary font-medium'
              : 'text-muted-foreground hover:text-foreground hover:bg-muted'
          )}
          style={{ paddingLeft: `${(level + 1) * 12}px` }}
        >
          {item.title}
        </button>
        {item.children && item.children.length > 0 && (
          <div className="mt-1">
            {renderTOCItems(item.children, level + 1)}
          </div>
        )}
      </div>
    ))
  }

  if (!doc || !content) {
    return (
      <div className="flex items-center justify-center h-96">
        <p className="text-muted-foreground">Document not found</p>
      </div>
    )
  }

  return (
    <div className="flex flex-col h-[calc(100vh-180px)]">
      <div className="flex items-center gap-4 mb-6">
        <Button onClick={onBack} variant="ghost" size="sm">
          <ArrowLeft className="mr-2" size={16} />
          Back to Index
        </Button>
        <div className="flex-1" />
        <Button
          onClick={() => setShowTOC(!showTOC)}
          variant="outline"
          size="sm"
          className="hidden md:flex"
        >
          <ListBullets className="mr-2" size={16} />
          {showTOC ? 'Hide' : 'Show'} Contents
        </Button>
        <Button
          onClick={toggleBookmark}
          variant={isBookmarked ? 'default' : 'outline'}
          size="sm"
        >
          <BookmarkSimple className="mr-2" size={16} weight={isBookmarked ? 'fill' : 'regular'} />
          {isBookmarked ? 'Bookmarked' : 'Bookmark'}
        </Button>
      </div>

      <div className="flex-1 grid md:grid-cols-[1fr_300px] gap-6 min-h-0">
        <Card className="flex flex-col overflow-hidden">
          <div className="p-6 border-b bg-card">
            <h1 className="text-3xl font-semibold tracking-tight mb-2">{doc.title}</h1>
            <p className="text-muted-foreground mb-4">{doc.description}</p>
            <div className="flex flex-wrap gap-2">
              <Badge variant="secondary">{doc.readingTime}</Badge>
              <Badge variant="secondary">{doc.lines} lines</Badge>
              <Badge variant="secondary">{doc.size}</Badge>
            </div>
          </div>

          <div className="relative flex-1">
            <div
              className="absolute top-0 left-0 right-0 h-1 bg-primary transition-all z-10"
              style={{ width: `${scrollProgress}%` }}
            />
            <ScrollArea className="h-full">
              <div ref={contentRef} className="p-8">
                <MarkdownRenderer content={content} />
              </div>
            </ScrollArea>
          </div>
        </Card>

        {showTOC && toc.length > 0 && (
          <Card className="p-6 hidden md:block overflow-hidden">
            <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
              <ListBullets size={20} />
              Table of Contents
            </h2>
            <ScrollArea className="h-[calc(100%-3rem)]">
              <div className="space-y-1">
                {renderTOCItems(toc)}
              </div>
            </ScrollArea>
          </Card>
        )}
      </div>
    </div>
  )
}
