import { useState, useEffect } from 'react'
import { ChartBar, TrendUp, CurrencyDollar, Article } from '@phosphor-icons/react'
import { Card } from '@/components/ui/card'
import { toast } from 'sonner'
import { AnalyticsData } from '@/lib/types'
import { useSettings, createApiRequest } from '@/lib/api'

export default function DashboardPage() {
  const { settings } = useSettings()
  const [analytics, setAnalytics] = useState<AnalyticsData | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [monthlyCost, setMonthlyCost] = useState(0)

  useEffect(() => {
    loadAnalytics()
    loadCosts()
  }, [])

  const loadAnalytics = async () => {
    if (!settings?.apiKey) {
      setIsLoading(false)
      return
    }

    try {
      const apiRequest = await createApiRequest(settings)
      const result = await apiRequest<AnalyticsData>('/v1/analytics/dashboard', {
        method: 'GET'
      })
      setAnalytics(result)
    } catch (error) {
      toast.error('Failed to load analytics data')
    } finally {
      setIsLoading(false)
    }
  }

  const loadCosts = async () => {
    if (!settings?.apiKey) return

    try {
      const apiRequest = await createApiRequest(settings)
      const result = await apiRequest<{ monthly_cost: number }>('/v1/costs/usage', {
        method: 'GET'
      })
      setMonthlyCost(result.monthly_cost)
    } catch (error) {
      console.error('Failed to load cost data')
    }
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-center">
          <ChartBar size={48} className="mx-auto mb-4 opacity-50 animate-pulse" />
          <p className="text-muted-foreground">Loading analytics...</p>
        </div>
      </div>
    )
  }

  if (!settings?.apiKey) {
    return (
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-semibold tracking-tight">Analytics Dashboard</h1>
          <p className="text-muted-foreground mt-2">
            Track your content performance and ROI
          </p>
        </div>
        <Card className="p-12 text-center">
          <ChartBar size={48} className="mx-auto mb-4 opacity-50" />
          <p className="text-lg font-medium mb-2">Configure API Key</p>
          <p className="text-sm text-muted-foreground">
            Set up your API key in Settings to view your analytics dashboard
          </p>
        </Card>
      </div>
    )
  }

  if (!analytics) {
    return null
  }

  const budgetUsagePercent = settings.monthlyBudget > 0
    ? Math.min((monthlyCost / settings.monthlyBudget) * 100, 100)
    : 0

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-semibold tracking-tight">Analytics Dashboard</h1>
        <p className="text-muted-foreground mt-2">
          Track your content performance and ROI
        </p>
      </div>

      <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card className="p-6">
          <div className="flex items-center gap-3 mb-2">
            <div className="p-2 bg-primary/10 text-primary rounded-lg">
              <Article size={24} />
            </div>
            <p className="text-sm font-medium text-muted-foreground">Total Content</p>
          </div>
          <p className="text-3xl font-semibold">{analytics.total_content}</p>
        </Card>

        <Card className="p-6">
          <div className="flex items-center gap-3 mb-2">
            <div className="p-2 bg-accent/20 text-accent-foreground rounded-lg">
              <TrendUp size={24} />
            </div>
            <p className="text-sm font-medium text-muted-foreground">Avg Quality</p>
          </div>
          <p className="text-3xl font-semibold">{analytics.avg_quality_score.toFixed(1)}</p>
        </Card>

        <Card className="p-6">
          <div className="flex items-center gap-3 mb-2">
            <div className="p-2 bg-accent/20 text-accent-foreground rounded-lg">
              <TrendUp size={24} />
            </div>
            <p className="text-sm font-medium text-muted-foreground">Avg SEO Score</p>
          </div>
          <p className="text-3xl font-semibold">{analytics.avg_seo_score.toFixed(1)}</p>
        </Card>

        <Card className="p-6">
          <div className="flex items-center gap-3 mb-2">
            <div className="p-2 bg-green-100 text-green-700 rounded-lg">
              <CurrencyDollar size={24} weight="fill" />
            </div>
            <p className="text-sm font-medium text-muted-foreground">ROI</p>
          </div>
          <p className="text-3xl font-semibold">{analytics.roi.toFixed(1)}x</p>
        </Card>
      </div>

      <div className="grid lg:grid-cols-2 gap-6">
        <Card className="p-6">
          <h2 className="text-lg font-semibold mb-4">Monthly Budget</h2>
          <div className="space-y-4">
            <div>
              <div className="flex justify-between text-sm mb-2">
                <span className="text-muted-foreground">Usage</span>
                <span className="font-medium">
                  ${monthlyCost.toFixed(2)} / ${settings.monthlyBudget.toFixed(2)}
                </span>
              </div>
              <div className="w-full bg-secondary h-3 rounded-full overflow-hidden">
                <div
                  className={`h-full transition-all ${
                    budgetUsagePercent >= 90
                      ? 'bg-destructive'
                      : budgetUsagePercent >= 75
                      ? 'bg-accent'
                      : 'bg-primary'
                  }`}
                  style={{ width: `${budgetUsagePercent}%` }}
                />
              </div>
            </div>

            {budgetUsagePercent >= 90 && (
              <div className="p-3 bg-red-50 border border-red-200 rounded-lg text-sm">
                <p className="font-medium text-red-900">Budget Alert</p>
                <p className="text-red-700">You've used over 90% of your monthly budget</p>
              </div>
            )}

            <div className="pt-4 border-t space-y-2">
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">Total Spent</span>
                <span className="font-medium">${analytics.total_cost.toFixed(2)}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">This Month</span>
                <span className="font-medium">${analytics.monthly_cost.toFixed(2)}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">Avg per Content</span>
                <span className="font-medium">
                  ${analytics.total_content > 0
                    ? (analytics.total_cost / analytics.total_content).toFixed(4)
                    : '0.00'}
                </span>
              </div>
            </div>
          </div>
        </Card>

        <Card className="p-6">
          <h2 className="text-lg font-semibold mb-4">Content by Type</h2>
          <div className="space-y-3">
            {Object.entries(analytics.content_by_type).map(([type, count]) => {
              const total = analytics.total_content
              const percentage = total > 0 ? (count / total) * 100 : 0
              const label = type.split('_').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ')

              return (
                <div key={type}>
                  <div className="flex justify-between text-sm mb-1">
                    <span className="font-medium">{label}</span>
                    <span className="text-muted-foreground">{count} ({percentage.toFixed(0)}%)</span>
                  </div>
                  <div className="w-full bg-secondary h-2 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-primary transition-all"
                      style={{ width: `${percentage}%` }}
                    />
                  </div>
                </div>
              )
            })}
          </div>
        </Card>
      </div>

      {analytics.quality_trend.length > 0 && (
        <Card className="p-6">
          <h2 className="text-lg font-semibold mb-4">Quality Trend</h2>
          <div className="space-y-2">
            {analytics.quality_trend.slice(0, 10).map((item, index) => (
              <div key={index} className="flex items-center gap-4">
                <span className="text-sm text-muted-foreground w-24">
                  {new Date(item.date).toLocaleDateString()}
                </span>
                <div className="flex-1 bg-secondary h-8 rounded-lg overflow-hidden relative">
                  <div
                    className="h-full bg-primary transition-all"
                    style={{ width: `${item.score}%` }}
                  />
                  <span className="absolute inset-0 flex items-center justify-center text-sm font-medium">
                    {item.score}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </Card>
      )}
    </div>
  )
}
