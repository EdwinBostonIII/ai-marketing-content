import { useState } from 'react'
import { Book, MagnifyingGlass, BookmarkSimple, BookOpen } from '@phosphor-icons/react'
import { Toaster } from '@/components/ui/sonner'
import DocumentIndexPage from '@/components/pages/GeneratePage'
import DocumentViewerPage from '@/components/pages/LibraryPage'
import SearchPage from '@/components/pages/DashboardPage'
import BookmarksPage from '@/components/pages/BookmarksPage'
import { cn } from '@/lib/utils'

type Page = 'index' | 'viewer' | 'search' | 'bookmarks'

function App() {
  const [currentPage, setCurrentPage] = useState<Page>('index')
  const [selectedDocId, setSelectedDocId] = useState<string | null>(null)

  const navigation = [
    { id: 'index' as Page, label: 'Documentation', icon: Book },
    { id: 'search' as Page, label: 'Search', icon: MagnifyingGlass },
    { id: 'bookmarks' as Page, label: 'Bookmarks', icon: BookmarkSimple },
  ]

  const handleSelectDocument = (docId: string) => {
    setSelectedDocId(docId)
    setCurrentPage('viewer')
  }

  const handleBackToIndex = () => {
    setCurrentPage('index')
    setSelectedDocId(null)
  }

  const renderPage = () => {
    switch (currentPage) {
      case 'index':
        return <DocumentIndexPage onSelectDocument={handleSelectDocument} />
      case 'viewer':
        return selectedDocId ? (
          <DocumentViewerPage documentId={selectedDocId} onBack={handleBackToIndex} />
        ) : null
      case 'search':
        return <SearchPage onNavigateToDocument={handleSelectDocument} />
      case 'bookmarks':
        return <BookmarksPage onSelectDocument={handleSelectDocument} />
    }
  }

  return (
    <div className="min-h-screen bg-background">
      <header className="border-b bg-card sticky top-0 z-10 backdrop-blur-sm bg-card/95">
        <div className="max-w-7xl mx-auto px-6">
          <div className="flex items-center justify-between h-16">
            <button 
              onClick={() => setCurrentPage('index')}
              className="flex items-center gap-3 hover:opacity-80 transition-opacity"
            >
              <div className="p-2 bg-primary rounded-lg">
                <BookOpen size={24} weight="fill" className="text-primary-foreground" />
              </div>
              <div>
                <h1 className="text-xl font-semibold">SPLANTS Docs</h1>
                <p className="text-xs text-muted-foreground hidden sm:block">
                  Marketing Engine Documentation
                </p>
              </div>
            </button>

            <nav className="hidden md:flex gap-1">
              {navigation.map((item) => {
                const Icon = item.icon
                const isActive = currentPage === item.id || (currentPage === 'viewer' && item.id === 'index')
                return (
                  <button
                    key={item.id}
                    onClick={() => {
                      setCurrentPage(item.id)
                      if (item.id !== 'viewer') setSelectedDocId(null)
                    }}
                    className={cn(
                      'flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-colors',
                      isActive
                        ? 'bg-primary text-primary-foreground'
                        : 'text-muted-foreground hover:text-foreground hover:bg-secondary'
                    )}
                  >
                    <Icon size={18} weight={isActive ? 'fill' : 'regular'} />
                    {item.label}
                  </button>
                )
              })}
            </nav>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-6 py-12">
        {renderPage()}
      </main>

      <nav className="md:hidden fixed bottom-0 left-0 right-0 bg-card border-t backdrop-blur-sm bg-card/95">
        <div className="grid grid-cols-3 gap-1 p-2">
          {navigation.map((item) => {
            const Icon = item.icon
            const isActive = currentPage === item.id || (currentPage === 'viewer' && item.id === 'index')
            return (
              <button
                key={item.id}
                onClick={() => {
                  setCurrentPage(item.id)
                  if (item.id !== 'viewer') setSelectedDocId(null)
                }}
                className={cn(
                  'flex flex-col items-center gap-1 px-3 py-2 rounded-lg text-xs font-medium transition-colors',
                  isActive
                    ? 'bg-primary text-primary-foreground'
                    : 'text-muted-foreground'
                )}
              >
                <Icon size={20} weight={isActive ? 'fill' : 'regular'} />
                {item.label}
              </button>
            )
          })}
        </div>
      </nav>

      <div className="h-20 md:hidden" />

      <Toaster />
    </div>
  )
}

export default App
