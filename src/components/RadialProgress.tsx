import { motion } from 'framer-motion'

interface RadialProgressProps {
  value: number
  size?: number
  strokeWidth?: number
  label: string
  className?: string
}

export default function RadialProgress({
  value,
  size = 120,
  strokeWidth = 8,
  label,
  className = ''
}: RadialProgressProps) {
  const radius = (size - strokeWidth) / 2
  const circumference = 2 * Math.PI * radius
  const offset = circumference - (value / 100) * circumference
  const center = size / 2

  const getColor = () => {
    if (value >= 90) return 'oklch(0.75 0.15 85)'
    if (value >= 70) return 'oklch(0.65 0.15 85)'
    return 'oklch(0.60 0.15 85)'
  }

  return (
    <div className={`flex flex-col items-center gap-2 ${className}`}>
      <svg width={size} height={size} className="transform -rotate-90">
        <circle
          cx={center}
          cy={center}
          r={radius}
          fill="none"
          stroke="oklch(0.92 0.005 85)"
          strokeWidth={strokeWidth}
        />
        <motion.circle
          cx={center}
          cy={center}
          r={radius}
          fill="none"
          stroke={getColor()}
          strokeWidth={strokeWidth}
          strokeDasharray={circumference}
          strokeDashoffset={circumference}
          strokeLinecap="round"
          animate={{ strokeDashoffset: offset }}
          transition={{ duration: 1, ease: 'easeOut' }}
        />
        <text
          x={center}
          y={center}
          textAnchor="middle"
          dominantBaseline="middle"
          className="transform rotate-90 origin-center text-2xl font-semibold"
          fill="oklch(0.20 0 0)"
        >
          {Math.round(value)}
        </text>
      </svg>
      <span className="text-sm font-medium text-muted-foreground">{label}</span>
    </div>
  )
}
