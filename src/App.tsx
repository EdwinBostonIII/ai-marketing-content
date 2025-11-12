import { useState } from 'react'
import { Sparkle, Database, ChartBar, Gear } from '@phosphor-icons/react'
import { Toaster } from '@/components/ui/sonner'
import GeneratePage from '@/components/pages/GeneratePage'
import LibraryPage from '@/components/pages/LibraryPage'
import DashboardPage from '@/components/pages/DashboardPage'
import SettingsPage from '@/components/pages/SettingsPage'
import { cn } from '@/lib/utils'

type Page = 'generate' | 'library' | 'dashboard' | 'settings'

function App() {
  const [currentPage, setCurrentPage] = useState<Page>('generate')

  const navigation = [
    { id: 'generate' as Page, label: 'Generate', icon: Sparkle },
    { id: 'library' as Page, label: 'Library', icon: Database },
    { id: 'dashboard' as Page, label: 'Dashboard', icon: ChartBar },
    { id: 'settings' as Page, label: 'Settings', icon: Gear }
  ]

  const renderPage = () => {
    switch (currentPage) {
      case 'generate':
        return <GeneratePage />
      case 'library':
        return <LibraryPage />
      case 'dashboard':
        return <DashboardPage />
      case 'settings':
        return <SettingsPage />
    }
  }

  return (
    <div className="min-h-screen bg-background">
      <header className="border-b bg-card sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-primary rounded-lg">
                <Sparkle size={24} weight="fill" className="text-primary-foreground" />
              </div>
              <div>
                <h1 className="text-xl font-semibold">AI Content Studio</h1>
                <p className="text-xs text-muted-foreground hidden sm:block">
                  Smart marketing content with built-in intelligence
                </p>
              </div>
            </div>

            <nav className="hidden md:flex gap-1">
              {navigation.map((item) => {
                const Icon = item.icon
                return (
                  <button
                    key={item.id}
                    onClick={() => setCurrentPage(item.id)}
                    className={cn(
                      'flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-colors',
                      currentPage === item.id
                        ? 'bg-primary text-primary-foreground'
                        : 'text-muted-foreground hover:text-foreground hover:bg-secondary'
                    )}
                  >
                    <Icon size={18} weight={currentPage === item.id ? 'fill' : 'regular'} />
                    {item.label}
                  </button>
                )
              })}
            </nav>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {renderPage()}
      </main>

      <nav className="md:hidden fixed bottom-0 left-0 right-0 bg-card border-t">
        <div className="grid grid-cols-4 gap-1 p-2">
          {navigation.map((item) => {
            const Icon = item.icon
            return (
              <button
                key={item.id}
                onClick={() => setCurrentPage(item.id)}
                className={cn(
                  'flex flex-col items-center gap-1 px-3 py-2 rounded-lg text-xs font-medium transition-colors',
                  currentPage === item.id
                    ? 'bg-primary text-primary-foreground'
                    : 'text-muted-foreground'
                )}
              >
                <Icon size={20} weight={currentPage === item.id ? 'fill' : 'regular'} />
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
