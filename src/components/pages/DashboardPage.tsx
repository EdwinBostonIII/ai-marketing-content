import { useState, useMemo } from 'react'
import { MagnifyingGlass, ArrowRight, Book } from '@phosphor-icons/react'
import { Input } from '@/components/ui/input'
import { Card } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { searchDocuments, documents } from '@/lib/documents'

interface SearchPageProps {
  onNavigateToDocument: (docId: string) => void
}

export default function SearchPage({ onNavigateToDocument }: SearchPageProps) {
  const [query, setQuery] = useState('')

  const results = useMemo(() => {
    if (query.trim().length < 3) return []
    return searchDocuments(query)
  }, [query])

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      <div className="text-center">
        <h1 className="text-3xl font-semibold tracking-tight mb-4">Search Documentation</h1>
        <p className="text-muted-foreground mb-8">
          Search across all 7,000+ lines of SPLANTS documentation
        </p>
      </div>

      <Card className="p-6">
        <div className="relative">
          <MagnifyingGlass className="absolute left-4 top-1/2 -translate-y-1/2 text-muted-foreground" size={24} />
          <Input
            placeholder="Search for topics, keywords, or specific questions..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="pl-12 h-14 text-lg"
            autoFocus
          />
        </div>
      </Card>

      {query.trim().length > 0 && query.trim().length < 3 && (
        <Card className="p-8 text-center">
          <p className="text-muted-foreground">Type at least 3 characters to search</p>
        </Card>
      )}

      {query.trim().length >= 3 && results.length === 0 && (
        <Card className="p-12 text-center">
          <Book size={48} className="mx-auto mb-4 text-muted-foreground opacity-50" />
          <p className="text-lg font-medium mb-2">No results found</p>
          <p className="text-sm text-muted-foreground">Try different keywords or browse the documentation index</p>
        </Card>
      )}

      {results.length > 0 && (
        <div className="space-y-3">
          <p className="text-sm text-muted-foreground">
            Found {results.length} result{results.length !== 1 ? 's' : ''} for &quot;{query}&quot;
          </p>
          
          {results.map((result, index) => (
            <Card key={index} className="p-4 hover:shadow-md transition-shadow">
              <div className="space-y-3">
                <div className="flex items-start justify-between gap-4">
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-2">
                      <h3 className="font-medium">{result.documentTitle}</h3>
                      <Badge variant="outline" className="text-xs">
                        Line {result.lineNumber}
                      </Badge>
                      <Badge variant="secondary" className="text-xs">
                        {documents[result.documentId]?.category}
                      </Badge>
                    </div>
                    <p className="text-sm text-muted-foreground whitespace-pre-wrap line-clamp-3">
                      {result.snippet}
                    </p>
                  </div>
                  <Button
                    size="sm"
                    variant="ghost"
                    onClick={() => onNavigateToDocument(result.documentId)}
                  >
                    <ArrowRight size={16} />
                  </Button>
                </div>
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  )
}
