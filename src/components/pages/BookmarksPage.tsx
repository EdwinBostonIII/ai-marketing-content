import { BookmarkSimple, ArrowRight, Book } from '@phosphor-icons/react'
import { Card } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { documents } from '@/lib/documents'
import { useKV } from '@github/spark/hooks'

interface BookmarksPageProps {
  onSelectDocument: (docId: string) => void
}

export default function BookmarksPage({ onSelectDocument }: BookmarksPageProps) {
  const [bookmarked] = useKV<string[]>('doc-bookmarks', [])

  const bookmarkedDocs = (bookmarked || []).map(id => documents[id]).filter(Boolean)

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      <div className="text-center">
        <h1 className="text-3xl font-semibold tracking-tight mb-4">Bookmarked Documentation</h1>
        <p className="text-muted-foreground">
          Quick access to your saved documentation pages
        </p>
      </div>

      {bookmarkedDocs.length === 0 ? (
        <Card className="p-12 text-center">
          <BookmarkSimple size={48} className="mx-auto mb-4 text-muted-foreground opacity-50" />
          <p className="text-lg font-medium mb-2">No bookmarks yet</p>
          <p className="text-sm text-muted-foreground mb-6">
            Bookmark documentation pages to access them quickly from here
          </p>
        </Card>
      ) : (
        <div className="space-y-3">
          {bookmarkedDocs.map((doc) => (
            <Card key={doc.id} className="p-6 hover:shadow-md transition-shadow">
              <div className="flex items-start justify-between gap-4">
                <div className="flex-1">
                  <h3 className="text-lg font-semibold mb-2">{doc.title}</h3>
                  <p className="text-sm text-muted-foreground mb-4">{doc.description}</p>
                  <div className="flex flex-wrap gap-2">
                    <Badge variant="secondary">{doc.readingTime}</Badge>
                    <Badge variant="secondary">{doc.lines} lines</Badge>
                    <Badge variant="outline">{doc.category}</Badge>
                  </div>
                </div>
                <Button
                  onClick={() => onSelectDocument(doc.id)}
                  variant="outline"
                >
                  <ArrowRight size={16} />
                </Button>
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  )
}
