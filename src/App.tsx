import { useState } from 'react'
import { PaintBrushBroad, ChartBar, FolderOpen, Gear } from '@phosphor-icons/react'
import { Toaster } from '@/components/ui/sonner'
import GeneratePage from '@/components/pages/GeneratePage'
import DashboardPage from '@/components/pages/DashboardPage'
import LibraryPage from '@/components/pages/LibraryPage'
import SettingsPage from '@/components/pages/SettingsPage'
import { cn } from '@/lib/utils'

type Page = 'generate' | 'analytics' | 'library' | 'settings'

function App() {
  const [currentPage, setCurrentPage] = useState<Page>('generate')

  const navigation = [
    { id: 'generate' as Page, label: 'Generate', icon: PaintBrushBroad },
    { id: 'analytics' as Page, label: 'Analytics', icon: ChartBar },
    { id: 'library' as Page, label: 'Library', icon: FolderOpen },
    { id: 'settings' as Page, label: 'Budget', icon: Gear },
  ]

  const renderPage = () => {
    switch (currentPage) {
      case 'generate':
        return <GeneratePage />
      case 'analytics':
        return <DashboardPage />
      case 'library':
        return <LibraryPage />
      case 'settings':
        return <SettingsPage />
    }
  }

  return (
    <div className="min-h-screen bg-background">
      <header className="border-b bg-card sticky top-0 z-10 backdrop-blur-sm bg-card/95 shadow-sm splatter-texture">
        <div className="max-w-6xl mx-auto px-8">
          <div className="flex items-center justify-between h-20">
            <button 
              onClick={() => setCurrentPage('generate')}
              className="flex items-center gap-3 hover:opacity-80 transition-opacity group"
            >
              <div className="p-2.5 bg-primary rounded-lg group-hover:scale-105 transition-transform">
                <PaintBrushBroad size={28} weight="fill" className="text-primary-foreground" />
              </div>
              <div>
                <h1 className="text-2xl font-bold">SPLANTS</h1>
                <p className="text-xs text-muted-foreground hidden sm:block">
                  Marketing Engine
                </p>
              </div>
            </button>

            <nav className="hidden md:flex gap-2">
              {navigation.map((item) => {
                const Icon = item.icon
                const isActive = currentPage === item.id
                return (
                  <button
                    key={item.id}
                    onClick={() => setCurrentPage(item.id)}
                    className={cn(
                      'flex items-center gap-2 px-5 py-2.5 rounded-lg text-sm font-semibold transition-all',
                      isActive
                        ? 'bg-primary text-primary-foreground shadow-md'
                        : 'text-muted-foreground hover:text-foreground hover:bg-secondary'
                    )}
                  >
                    <Icon size={20} weight={isActive ? 'fill' : 'regular'} />
                    {item.label}
                  </button>
                )
              })}
            </nav>
          </div>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-8 py-12">
        {renderPage()}
      </main>

      <nav className="md:hidden fixed bottom-0 left-0 right-0 bg-card border-t backdrop-blur-sm bg-card/95 shadow-lg">
        <div className="grid grid-cols-4 gap-1 p-2">
          {navigation.map((item) => {
            const Icon = item.icon
            const isActive = currentPage === item.id
            return (
              <button
                key={item.id}
                onClick={() => setCurrentPage(item.id)}
                className={cn(
                  'flex flex-col items-center gap-1 px-3 py-2.5 rounded-lg text-xs font-semibold transition-all',
                  isActive
                    ? 'bg-primary text-primary-foreground'
                    : 'text-muted-foreground'
                )}
              >
                <Icon size={22} weight={isActive ? 'fill' : 'regular'} />
                {item.label}
              </button>
            )
          })}
        </div>
      </nav>

      <div className="h-24 md:hidden" />

      <Toaster />
    </div>
  )
}

export default App
