import { useState } from 'react'
import { Gear, Key, CurrencyDollar, Plugs, FloppyDisk, CheckCircle } from '@phosphor-icons/react'
import { Button } from '@/components/ui/button'
import { Card } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Separator } from '@/components/ui/separator'
import { toast } from 'sonner'
import { useSettings } from '@/lib/api'

export default function SettingsPage() {
  const { settings, setSettings } = useSettings()
  const [apiKey, setApiKey] = useState(settings?.apiKey || '')
  const [monthlyBudget, setMonthlyBudget] = useState(settings?.monthlyBudget || 100)
  const [apiEndpoint, setApiEndpoint] = useState(settings?.apiEndpoint || 'http://localhost:8000')
  const [webhookUrl, setWebhookUrl] = useState('')
  const [webhookUrls, setWebhookUrls] = useState<string[]>(settings?.webhookUrls || [])
  const [isSaved, setIsSaved] = useState(false)

  const handleSave = () => {
    setSettings((current) => ({
      ...current!,
      apiKey,
      monthlyBudget,
      apiEndpoint,
      webhookUrls
    }))

    setIsSaved(true)
    toast.success('Settings saved successfully!')

    setTimeout(() => setIsSaved(false), 3000)
  }

  const handleAddWebhook = () => {
    if (!webhookUrl.trim()) return

    try {
      new URL(webhookUrl)
      setWebhookUrls([...webhookUrls, webhookUrl.trim()])
      setWebhookUrl('')
      toast.success('Webhook URL added')
    } catch {
      toast.error('Please enter a valid URL')
    }
  }

  const handleRemoveWebhook = (index: number) => {
    setWebhookUrls(webhookUrls.filter((_, i) => i !== index))
    toast.success('Webhook URL removed')
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-semibold tracking-tight">Settings</h1>
        <p className="text-muted-foreground mt-2">
          Configure your API keys, budget limits, and integrations
        </p>
      </div>

      <Card className="p-6">
        <div className="space-y-6">
          <div>
            <div className="flex items-center gap-2 mb-4">
              <Key size={20} className="text-primary" />
              <h2 className="text-lg font-semibold">API Configuration</h2>
            </div>

            <div className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="api-key" className="text-base font-medium">OpenAI API Key</Label>
                <Input
                  id="api-key"
                  type="password"
                  placeholder="sk-..."
                  value={apiKey}
                  onChange={(e) => setApiKey(e.target.value)}
                />
                <p className="text-sm text-muted-foreground">
                  Your API key is stored locally and never sent to external servers
                </p>
              </div>

              <div className="space-y-2">
                <Label htmlFor="api-endpoint" className="text-base font-medium">API Endpoint</Label>
                <Input
                  id="api-endpoint"
                  type="url"
                  placeholder="http://localhost:8000"
                  value={apiEndpoint}
                  onChange={(e) => setApiEndpoint(e.target.value)}
                />
                <p className="text-sm text-muted-foreground">
                  The base URL of your backend API server
                </p>
              </div>
            </div>
          </div>

          <Separator />

          <div>
            <div className="flex items-center gap-2 mb-4">
              <CurrencyDollar size={20} className="text-primary" weight="fill" />
              <h2 className="text-lg font-semibold">Budget Control</h2>
            </div>

            <div className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="monthly-budget" className="text-base font-medium">Monthly Budget ($)</Label>
                <Input
                  id="monthly-budget"
                  type="number"
                  min="0"
                  step="10"
                  value={monthlyBudget}
                  onChange={(e) => setMonthlyBudget(parseFloat(e.target.value) || 0)}
                />
                <p className="text-sm text-muted-foreground">
                  Set a monthly spending limit to control AI generation costs
                </p>
              </div>

              <div className="p-4 bg-accent/10 border border-accent/20 rounded-lg">
                <p className="text-sm font-medium mb-1">Cost Savings Tip</p>
                <p className="text-sm text-muted-foreground">
                  The backend includes built-in caching that can save 30-50% on repeated requests
                </p>
              </div>
            </div>
          </div>

          <Separator />

          <div>
            <div className="flex items-center gap-2 mb-4">
              <Plugs size={20} className="text-primary" />
              <h2 className="text-lg font-semibold">Webhook Integrations</h2>
            </div>

            <div className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="webhook-url" className="text-base font-medium">Add Webhook URL</Label>
                <div className="flex gap-2">
                  <Input
                    id="webhook-url"
                    type="url"
                    placeholder="https://hooks.zapier.com/..."
                    value={webhookUrl}
                    onChange={(e) => setWebhookUrl(e.target.value)}
                    onKeyDown={(e) => e.key === 'Enter' && handleAddWebhook()}
                  />
                  <Button onClick={handleAddWebhook} variant="outline">Add</Button>
                </div>
                <p className="text-sm text-muted-foreground">
                  Connect to Zapier, Slack, or other webhook services
                </p>
              </div>

              {webhookUrls.length > 0 && (
                <div className="space-y-2">
                  <Label className="text-sm font-medium">Configured Webhooks</Label>
                  {webhookUrls.map((url, index) => (
                    <div key={index} className="flex items-center gap-2 p-3 bg-muted rounded-lg">
                      <span className="flex-1 text-sm truncate">{url}</span>
                      <Button
                        size="sm"
                        variant="ghost"
                        onClick={() => handleRemoveWebhook(index)}
                      >
                        Remove
                      </Button>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>

          <Separator />

          <Button onClick={handleSave} size="lg" className="w-full sm:w-auto">
            {isSaved ? (
              <>
                <CheckCircle className="mr-2" weight="fill" />
                Saved!
              </>
            ) : (
              <>
                <FloppyDisk className="mr-2" />
                Save Settings
              </>
            )}
          </Button>
        </div>
      </Card>

      <Card className="p-6 bg-primary/5 border-primary/20">
        <h3 className="font-semibold mb-2">Why This is Better Than a Subscription</h3>
        <ul className="space-y-2 text-sm text-muted-foreground">
          <li className="flex gap-2">
            <span className="text-primary">•</span>
            <span><strong>Smart AI:</strong> Multi-model synthesis instead of generic prompts</span>
          </li>
          <li className="flex gap-2">
            <span className="text-primary">•</span>
            <span><strong>Quality Control:</strong> Built-in quality and SEO scoring on every piece</span>
          </li>
          <li className="flex gap-2">
            <span className="text-primary">•</span>
            <span><strong>Cost Control:</strong> Budget limits and caching to save 30-50%</span>
          </li>
          <li className="flex gap-2">
            <span className="text-primary">•</span>
            <span><strong>Full Analytics:</strong> ROI tracking and performance metrics included</span>
          </li>
          <li className="flex gap-2">
            <span className="text-primary">•</span>
            <span><strong>Purpose-Built:</strong> Designed for marketing, not generic workflows</span>
          </li>
        </ul>
      </Card>
    </div>
  )
}
