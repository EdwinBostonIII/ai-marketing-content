export interface Document {
  id: string
  title: string
  description: string
  filename: string
  size: string
  lines: number
  readingTime: string
  category: 'getting-started' | 'reference' | 'guides' | 'troubleshooting'
  icon: string
}

export interface TOCItem {
  id: string
  title: string
  level: number
  children?: TOCItem[]
}

export interface SearchResult {
  documentId: string
  documentTitle: string
  snippet: string
  lineNumber: number
  relevance: number
}

export interface ReadingProgress {
  documentId: string
  scrollPosition: number
  lastRead: string
  completed: boolean
}
