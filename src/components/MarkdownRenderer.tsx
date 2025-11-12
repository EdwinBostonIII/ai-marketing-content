import { useEffect, useRef } from 'react'
import { marked } from 'marked'

interface MarkdownRendererProps {
  content: string
  className?: string
}

export default function MarkdownRenderer({ content, className = '' }: MarkdownRendererProps) {
  const contentRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (contentRef.current && content) {
      const html = marked.parse(content, {
        breaks: true,
        gfm: true,
      })
      contentRef.current.innerHTML = html as string
    }
  }, [content])

  return (
    <div
      ref={contentRef}
      className={`prose prose-slate max-w-none ${className}`}
      style={{
        fontSize: '16px',
        lineHeight: '1.65',
      }}
    />
  )
}
