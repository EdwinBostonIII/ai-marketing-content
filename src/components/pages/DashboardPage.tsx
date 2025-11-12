import { ChartBar, TrendUp, FileText, Clock } from '@phosphor-icons/react'
import { Card } from '@/components/ui/card'
import { BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

const contentData = [
  { month: 'Jan', posts: 12, quality: 85 },
  { month: 'Feb', posts: 18, quality: 88 },
  { month: 'Mar', posts: 15, quality: 92 },
  { month: 'Apr', posts: 22, quality: 90 },
  { month: 'May', posts: 28, quality: 94 },
  { month: 'Jun', posts: 32, quality: 91 },
]

const platformData = [
  { name: 'Blog', count: 45 },
  { name: 'Twitter', count: 78 },
  { name: 'LinkedIn', count: 32 },
  { name: 'Instagram', count: 56 },
  { name: 'Facebook', count: 41 },
]

export default function DashboardPage() {
  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-4xl font-bold mb-2">Analytics Dashboard</h1>
        <p className="text-muted-foreground">Track your content performance and engagement</p>
      </div>

      <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card className="p-6 shadow-md">
          <div className="flex items-center justify-between mb-2">
            <FileText size={24} weight="fill" style={{ color: 'oklch(0.75 0.15 85)' }} />
            <TrendUp size={20} weight="bold" className="text-green-600" />
          </div>
          <div className="text-3xl font-bold mb-1">127</div>
          <div className="text-sm text-muted-foreground">Total Content</div>
        </Card>

        <Card className="p-6 shadow-md">
          <div className="flex items-center justify-between mb-2">
            <ChartBar size={24} weight="fill" style={{ color: 'oklch(0.60 0.15 85)' }} />
            <TrendUp size={20} weight="bold" className="text-green-600" />
          </div>
          <div className="text-3xl font-bold mb-1">89%</div>
          <div className="text-sm text-muted-foreground">Avg Quality</div>
        </Card>

        <Card className="p-6 shadow-md">
          <div className="flex items-center justify-between mb-2">
            <Clock size={24} weight="fill" style={{ color: 'oklch(0.75 0.15 85)' }} />
            <TrendUp size={20} weight="bold" className="text-green-600" />
          </div>
          <div className="text-3xl font-bold mb-1">32</div>
          <div className="text-sm text-muted-foreground">This Month</div>
        </Card>

        <Card className="p-6 shadow-md">
          <div className="flex items-center justify-between mb-2">
            <TrendUp size={24} weight="fill" style={{ color: 'oklch(0.60 0.15 85)' }} />
            <TrendUp size={20} weight="bold" className="text-green-600" />
          </div>
          <div className="text-3xl font-bold mb-1">86%</div>
          <div className="text-sm text-muted-foreground">Avg SEO</div>
        </Card>
      </div>

      <div className="grid lg:grid-cols-2 gap-8">
        <Card className="p-6 shadow-md">
          <h3 className="text-xl font-semibold mb-6">Content Generation Trend</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={contentData}>
              <CartesianGrid strokeDasharray="3 3" stroke="oklch(0.92 0.005 85)" />
              <XAxis dataKey="month" stroke="oklch(0.50 0 0)" />
              <YAxis stroke="oklch(0.50 0 0)" />
              <Tooltip />
              <Line
                type="monotone"
                dataKey="posts"
                stroke="oklch(0.75 0.15 85)"
                strokeWidth={3}
                dot={{ fill: 'oklch(0.75 0.15 85)', r: 5 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </Card>

        <Card className="p-6 shadow-md">
          <h3 className="text-xl font-semibold mb-6">Content by Platform</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={platformData}>
              <CartesianGrid strokeDasharray="3 3" stroke="oklch(0.92 0.005 85)" />
              <XAxis dataKey="name" stroke="oklch(0.50 0 0)" />
              <YAxis stroke="oklch(0.50 0 0)" />
              <Tooltip />
              <Bar dataKey="count" fill="oklch(0.75 0.15 85)" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </Card>
      </div>

      <Card className="p-6 shadow-md">
        <h3 className="text-xl font-semibold mb-6">Quality Score Over Time</h3>
        <ResponsiveContainer width="100%" height={250}>
          <LineChart data={contentData}>
            <CartesianGrid strokeDasharray="3 3" stroke="oklch(0.92 0.005 85)" />
            <XAxis dataKey="month" stroke="oklch(0.50 0 0)" />
            <YAxis stroke="oklch(0.50 0 0)" domain={[70, 100]} />
            <Tooltip />
            <Line
              type="monotone"
              dataKey="quality"
              stroke="oklch(0.60 0.15 85)"
              strokeWidth={3}
              dot={{ fill: 'oklch(0.60 0.15 85)', r: 5 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </Card>
    </div>
  )
}
