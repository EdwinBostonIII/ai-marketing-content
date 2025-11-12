import { Book, Rocket, Lightning, Question, Wrench, Code, Cloud, List, ArrowRight, Clock, FileText } from '@phosphor-icons/react'
import { Card } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { documents } from '@/lib/documents'

const iconMap = {
  'Book': Book,
  'Rocket': Rocket,
  'Lightning': Lightning,
  'Question': Question,
  'Wrench': Wrench,
  'Code': Code,
  'Cloud': Cloud,
  'List': List
}

interface DocumentIndexPageProps {
  onSelectDocument: (docId: string) => void
}

export default function DocumentIndexPage({ onSelectDocument }: DocumentIndexPageProps) {
  const categories = {
    'getting-started': {
      title: 'Getting Started',
      description: 'Installation guides and quickstart tutorials',
      color: 'bg-blue-50 text-blue-700 border-blue-200'
    },
    'reference': {
      title: 'Reference',
      description: 'API documentation and FAQ',
      color: 'bg-purple-50 text-purple-700 border-purple-200'
    },
    'guides': {
      title: 'Guides',
      description: 'In-depth tutorials and best practices',
      color: 'bg-green-50 text-green-700 border-green-200'
    },
    'troubleshooting': {
      title: 'Troubleshooting',
      description: 'Solutions to common problems',
      color: 'bg-amber-50 text-amber-700 border-amber-200'
    }
  }

  const documentsByCategory = Object.values(documents).reduce((acc, doc) => {
    if (!acc[doc.category]) acc[doc.category] = []
    acc[doc.category].push(doc)
    return acc
  }, {} as Record<string, typeof documents[string][]>)

  return (
    <div className="space-y-12">
      <div className="text-center max-w-3xl mx-auto">
        <h1 className="text-4xl font-semibold tracking-tight mb-4">SPLANTS Documentation</h1>
        <p className="text-lg text-muted-foreground leading-relaxed">
          Comprehensive guides and references for the SPLANTS Marketing Engine. 
          7,000+ lines across 8 detailed documents covering installation, usage, and troubleshooting.
        </p>
        <div className="flex flex-wrap gap-3 justify-center mt-6">
          <Badge variant="outline" className="text-sm px-3 py-1">
            <FileText className="mr-1" size={14} />
            8 Documents
          </Badge>
          <Badge variant="outline" className="text-sm px-3 py-1">
            <Clock className="mr-1" size={14} />
            3-4 hours total reading
          </Badge>
          <Badge variant="outline" className="text-sm px-3 py-1">
            130KB+ content
          </Badge>
        </div>
      </div>

      {Object.entries(categories).map(([categoryId, category]) => {
        const docs = documentsByCategory[categoryId] || []
        if (docs.length === 0) return null

        return (
          <div key={categoryId} className="space-y-6">
            <div>
              <div className={`inline-flex items-center gap-2 px-3 py-1 rounded-full border ${category.color} text-sm font-medium mb-2`}>
                {category.title}
              </div>
              <p className="text-muted-foreground">{category.description}</p>
            </div>

            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {docs.map((doc) => {
                const Icon = iconMap[doc.icon as keyof typeof iconMap] || Book

                return (
                  <Card
                    key={doc.id}
                    className="p-6 hover:shadow-lg transition-all cursor-pointer group"
                    onClick={() => onSelectDocument(doc.id)}
                  >
                    <div className="flex items-start gap-4 mb-4">
                      <div className="p-3 bg-primary/10 text-primary rounded-lg group-hover:bg-primary group-hover:text-primary-foreground transition-colors">
                        <Icon size={24} weight="duotone" />
                      </div>
                      <div className="flex-1 min-w-0">
                        <h3 className="text-lg font-semibold mb-1 group-hover:text-primary transition-colors">
                          {doc.title}
                        </h3>
                        <p className="text-sm text-muted-foreground line-clamp-2">
                          {doc.description}
                        </p>
                      </div>
                    </div>

                    <div className="flex flex-wrap gap-2 mb-4">
                      <Badge variant="secondary" className="text-xs">
                        <Clock className="mr-1" size={12} />
                        {doc.readingTime}
                      </Badge>
                      <Badge variant="secondary" className="text-xs">
                        {doc.lines} lines
                      </Badge>
                      <Badge variant="secondary" className="text-xs">
                        {doc.size}
                      </Badge>
                    </div>

                    <Button
                      variant="ghost"
                      className="w-full justify-between group-hover:bg-primary/10"
                      onClick={(e) => {
                        e.stopPropagation()
                        onSelectDocument(doc.id)
                      }}
                    >
                      <span>Read documentation</span>
                      <ArrowRight className="group-hover:translate-x-1 transition-transform" size={16} />
                    </Button>
                  </Card>
                )
              })}
            </div>
          </div>
        )
      })}

      <Card className="p-8 bg-secondary/50 border-dashed">
        <div className="text-center max-w-2xl mx-auto">
          <Book size={48} className="mx-auto mb-4 text-muted-foreground" />
          <h2 className="text-xl font-semibold mb-2">Need Help Finding Something?</h2>
          <p className="text-muted-foreground mb-4">
            Use the search function to quickly find specific topics across all documentation, 
            or start with the Documentation Index for a guided tour.
          </p>
          <Button onClick={() => onSelectDocument('doc-index')} variant="outline">
            <List className="mr-2" size={16} />
            View Documentation Index
          </Button>
        </div>
      </Card>
    </div>
  )
}
