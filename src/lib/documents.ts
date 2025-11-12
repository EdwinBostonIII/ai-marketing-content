import readmeDoc from '@/assets/documents/README_(1).md?raw'
import setupGuideDoc from '@/assets/documents/SETUP_GUIDE.md?raw'
import faqDoc from '@/assets/documents/FAQ.md?raw'
import troubleshootingDoc from '@/assets/documents/TROUBLESHOOTING.md?raw'
import apiGuideDoc from '@/assets/documents/docs_API_GUIDE_(1).md?raw'
import deploymentDoc from '@/assets/documents/docs_DEPLOYMENT_(1).md?raw'
import quickstartDoc from '@/assets/documents/QUICKSTART_WINDOWS.md?raw'
import docIndexDoc from '@/assets/documents/DOCUMENTATION_INDEX.md?raw'
import { Document, TOCItem } from './doc-types'

export const documents: Record<string, Document> = {
  'readme': {
    id: 'readme',
    title: 'README',
    description: 'Complete system overview, features, installation, and getting started guide',
    filename: 'README_(1).md',
    size: '35KB',
    lines: 1425,
    readingTime: '30-45 min',
    category: 'getting-started',
    icon: 'Book'
  },
  'setup-guide': {
    id: 'setup-guide',
    title: 'Setup Guide',
    description: 'Step-by-step installation instructions with platform-specific guidance',
    filename: 'SETUP_GUIDE.md',
    size: '29KB',
    lines: 1308,
    readingTime: '20-30 min',
    category: 'getting-started',
    icon: 'Rocket'
  },
  'quickstart': {
    id: 'quickstart',
    title: 'Windows Quickstart',
    description: 'Fast 15-minute setup guide for Windows users',
    filename: 'QUICKSTART_WINDOWS.md',
    size: '10KB',
    lines: 423,
    readingTime: '10-15 min',
    category: 'getting-started',
    icon: 'Lightning'
  },
  'faq': {
    id: 'faq',
    title: 'FAQ',
    description: '100+ questions and answers across 10 categories',
    filename: 'FAQ.md',
    size: '35KB',
    lines: 1427,
    readingTime: '20-30 min',
    category: 'reference',
    icon: 'Question'
  },
  'troubleshooting': {
    id: 'troubleshooting',
    title: 'Troubleshooting',
    description: '60+ common problems with detailed solutions',
    filename: 'TROUBLESHOOTING.md',
    size: '25KB',
    lines: 1424,
    readingTime: '15-20 min',
    category: 'troubleshooting',
    icon: 'Wrench'
  },
  'api-guide': {
    id: 'api-guide',
    title: 'API Guide',
    description: 'Complete API reference with endpoints and examples',
    filename: 'docs_API_GUIDE_(1).md',
    size: '6KB',
    lines: 293,
    readingTime: '10-15 min',
    category: 'reference',
    icon: 'Code'
  },
  'deployment': {
    id: 'deployment',
    title: 'Deployment',
    description: 'Production deployment instructions for various platforms',
    filename: 'docs_DEPLOYMENT_(1).md',
    size: '7KB',
    lines: 350,
    readingTime: '15-20 min',
    category: 'guides',
    icon: 'Cloud'
  },
  'doc-index': {
    id: 'doc-index',
    title: 'Documentation Index',
    description: 'Master navigation guide to all documentation',
    filename: 'DOCUMENTATION_INDEX.md',
    size: '8KB',
    lines: 458,
    readingTime: '10 min',
    category: 'reference',
    icon: 'List'
  }
}

export const documentContent: Record<string, string> = {
  'readme': readmeDoc,
  'setup-guide': setupGuideDoc,
  'faq': faqDoc,
  'troubleshooting': troubleshootingDoc,
  'api-guide': apiGuideDoc,
  'deployment': deploymentDoc,
  'quickstart': quickstartDoc,
  'doc-index': docIndexDoc
}

export function parseMarkdownTOC(markdown: string): TOCItem[] {
  const lines = markdown.split('\n')
  const toc: TOCItem[] = []
  const stack: { level: number; item: TOCItem }[] = []

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i]
    const match = line.match(/^(#{1,6})\s+(.+)$/)
    
    if (match) {
      const level = match[1].length
      const title = match[2].replace(/[*_`]/g, '').trim()
      const id = title.toLowerCase().replace(/[^a-z0-9]+/g, '-')

      const item: TOCItem = {
        id,
        title,
        level,
        children: []
      }

      while (stack.length > 0 && stack[stack.length - 1].level >= level) {
        stack.pop()
      }

      if (stack.length === 0) {
        toc.push(item)
      } else {
        const parent = stack[stack.length - 1].item
        if (!parent.children) parent.children = []
        parent.children.push(item)
      }

      stack.push({ level, item })
    }
  }

  return toc
}

export function searchDocuments(query: string, maxResults = 20): Array<{
  documentId: string
  documentTitle: string
  snippet: string
  lineNumber: number
  relevance: number
}> {
  const results: Array<{
    documentId: string
    documentTitle: string
    snippet: string
    lineNumber: number
    relevance: number
  }> = []

  const lowerQuery = query.toLowerCase()
  const queryWords = lowerQuery.split(/\s+/).filter(w => w.length > 2)

  for (const [docId, content] of Object.entries(documentContent)) {
    const lines = content.split('\n')
    
    lines.forEach((line, index) => {
      const lowerLine = line.toLowerCase()
      let relevance = 0

      if (lowerLine.includes(lowerQuery)) {
        relevance = 10
      } else {
        relevance = queryWords.reduce((score, word) => {
          return score + (lowerLine.includes(word) ? 1 : 0)
        }, 0)
      }

      if (relevance > 0) {
        const snippetStart = Math.max(0, index - 1)
        const snippetEnd = Math.min(lines.length, index + 2)
        const snippet = lines.slice(snippetStart, snippetEnd).join('\n')

        results.push({
          documentId: docId,
          documentTitle: documents[docId].title,
          snippet,
          lineNumber: index + 1,
          relevance
        })
      }
    })
  }

  return results
    .sort((a, b) => b.relevance - a.relevance)
    .slice(0, maxResults)
}
