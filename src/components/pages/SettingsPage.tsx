import { CurrencyDollar, ChartBar, Warning } from '@phosphor-icons/react'
import { Card } from '@/components/ui/card'
import { Progress } from '@/components/ui/progress'

export default function SettingsPage() {
  const monthlyBudget = 80
  const currentUsage = 42
  const usagePercent = (currentUsage / monthlyBudget) * 100

  const getProgressStyle = () => {
    if (usagePercent >= 95) return { backgroundColor: 'oklch(0.55 0.22 25)' }
    if (usagePercent >= 80) return { backgroundColor: 'oklch(0.65 0.20 50)' }
    return {}
  }

  const costBreakdown = [
    { name: 'AI Usage (GPT-4)', cost: 28, percent: 67 },
    { name: 'Server & Hosting', cost: 10, percent: 24 },
    { name: 'Database Storage', cost: 4, percent: 9 },
  ]

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-4xl font-bold mb-2">Budget & Settings</h1>
        <p className="text-muted-foreground">Monitor costs and manage your usage</p>
      </div>

      <Card className="p-8 shadow-md">
        <div className="flex items-start justify-between mb-6">
          <div>
            <h3 className="text-2xl font-semibold mb-1">Monthly Budget</h3>
            <p className="text-muted-foreground">Track your spending against the $80/month budget</p>
          </div>
          <CurrencyDollar size={48} weight="fill" style={{ color: 'oklch(0.75 0.15 85)' }} />
        </div>

        <div className="space-y-4">
          <div className="flex items-baseline justify-between">
            <span className="text-4xl font-bold">${currentUsage}</span>
            <span className="text-xl text-muted-foreground">of ${monthlyBudget}</span>
          </div>

          <div className="space-y-2">
            <div className="relative h-4 w-full overflow-hidden rounded-full bg-muted">
              <div
                className="h-full transition-all duration-500 rounded-full"
                style={{
                  width: `${usagePercent}%`,
                  ...getProgressStyle()
                }}
              />
            </div>
            <div className="flex items-center justify-between text-sm">
              <span className="text-muted-foreground">{usagePercent.toFixed(1)}% used</span>
              <span className="text-muted-foreground">${(monthlyBudget - currentUsage).toFixed(2)} remaining</span>
            </div>
          </div>

          {usagePercent >= 80 && (
            <div className={`flex items-start gap-3 p-4 rounded-lg ${
              usagePercent >= 95 ? 'bg-red-50 border border-red-200' : 'bg-amber-50 border border-amber-200'
            }`}>
              <Warning
                size={24}
                weight="fill"
                className={usagePercent >= 95 ? 'text-red-600' : 'text-amber-600'}
              />
              <div>
                <h4 className={`font-semibold mb-1 ${
                  usagePercent >= 95 ? 'text-red-900' : 'text-amber-900'
                }`}>
                  {usagePercent >= 95 ? 'Budget Almost Depleted' : 'Approaching Budget Limit'}
                </h4>
                <p className={`text-sm ${
                  usagePercent >= 95 ? 'text-red-700' : 'text-amber-700'
                }`}>
                  {usagePercent >= 95
                    ? 'You\'ve used nearly all of your monthly budget. Consider upgrading or reducing usage.'
                    : 'You\'re using more than 80% of your monthly budget. Monitor your usage carefully.'}
                </p>
              </div>
            </div>
          )}
        </div>
      </Card>

      <Card className="p-8 shadow-md">
        <div className="flex items-start justify-between mb-6">
          <div>
            <h3 className="text-2xl font-semibold mb-1">Cost Breakdown</h3>
            <p className="text-muted-foreground">Where your budget is being spent</p>
          </div>
          <ChartBar size={48} weight="fill" style={{ color: 'oklch(0.60 0.15 85)' }} />
        </div>

        <div className="space-y-6">
          {costBreakdown.map((item) => (
            <div key={item.name} className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="font-medium">{item.name}</span>
                <span className="text-lg font-semibold">${item.cost}</span>
              </div>
              <Progress value={item.percent} className="h-2" />
              <div className="text-sm text-muted-foreground">{item.percent}% of total</div>
            </div>
          ))}
        </div>
      </Card>

      <Card className="p-8 shadow-md">
        <h3 className="text-2xl font-semibold mb-6">Usage Tips</h3>
        <div className="space-y-4 text-muted-foreground">
          <div className="flex gap-3">
            <div className="w-2 h-2 rounded-full bg-primary mt-2" />
            <p>Enable Redis caching to reduce AI costs by 30-50%</p>
          </div>
          <div className="flex gap-3">
            <div className="w-2 h-2 rounded-full bg-primary mt-2" />
            <p>Generate content in batches to optimize API usage</p>
          </div>
          <div className="flex gap-3">
            <div className="w-2 h-2 rounded-full bg-primary mt-2" />
            <p>Use shorter content lengths when appropriate to reduce costs</p>
          </div>
          <div className="flex gap-3">
            <div className="w-2 h-2 rounded-full bg-primary mt-2" />
            <p>Review and edit generated content before publishing to maintain quality</p>
          </div>
        </div>
      </Card>
    </div>
  )
}
