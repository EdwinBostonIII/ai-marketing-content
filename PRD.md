# SPLANTS Documentation Hub - Product Requirements Document

## Mission Statement

A comprehensive, beautifully organized documentation browser that transforms 7,000+ lines of SPLANTS Marketing Engine documentation into an accessible, searchable, and delightful user experience.

**Experience Qualities**:
1. **Clarity** - Information is organized hierarchically and intuitively discoverable
2. **Accessibility** - Complex technical concepts presented in digestible, visual chunks
3. **Efficiency** - Users find what they need quickly through smart search and navigation

**Complexity Level**: Light Application (multiple features with basic state)
- Single-purpose documentation browsing
- Multiple documents with navigation
- Search and filter capabilities
- Bookmarking and progress tracking

## Essential Features

### 1. Document Browser
- **Functionality**: Display full documentation with proper markdown rendering
- **Purpose**: Make 7,000+ lines of docs readable and navigable
- **Trigger**: User selects document from sidebar or index
- **Progression**: Select document → Load content → Render markdown → Display with TOC → Navigate sections
- **Success criteria**: All markdown formats render correctly, navigation is smooth

### 2. Smart Search
- **Functionality**: Full-text search across all documentation with highlighted results
- **Purpose**: Help users find specific information instantly
- **Trigger**: User types in search bar
- **Progression**: Type query → Debounced search → Show results with context → Click result → Jump to location
- **Success criteria**: Sub-second search, relevant results, proper highlighting

### 3. Quick Navigation Index
- **Functionality**: Visual card-based index showing all documentation sections
- **Purpose**: Provide overview of what's available and quick access
- **Trigger**: User lands on home page or clicks "Documentation Index"
- **Progression**: View index → Browse categories → Click card → Navigate to document
- **Success criteria**: All 8 major documents accessible, clear categorization

### 4. Table of Contents Sidebar
- **Functionality**: Auto-generated TOC from document headings with scroll-spy
- **Purpose**: Show document structure and enable quick section jumping
- **Trigger**: Document loads
- **Progression**: Parse headings → Generate TOC → Track scroll position → Highlight current section
- **Success criteria**: TOC syncs with scroll, click jumps to section

### 5. Reading Progress Tracking
- **Functionality**: Save user's reading position and mark completed sections
- **Purpose**: Help users track their learning journey through extensive docs
- **Trigger**: User scrolls through document
- **Progression**: Track position → Save to KV → Show progress indicator → Restore on return
- **Success criteria**: Progress persists between sessions, visual feedback

## Edge Case Handling

- **Empty search results** - Show helpful suggestions and popular topics
- **Long documents** - Implement virtual scrolling and lazy loading
- **Broken markdown** - Graceful fallback rendering
- **Mobile viewing** - Responsive layout with collapsible sidebar
- **Deep linking** - Support direct URLs to specific sections

## Design Direction

The design should feel like a premium technical documentation site - clean, professional, focused on readability. Think Stripe Docs meets Notion. The interface should fade into the background, letting the content shine. Whitespace is generous, typography is impeccable, and navigation feels effortless.

## Color Selection

**Triadic color scheme** balanced for technical documentation with warm accents for approachability.

- **Primary Color (Deep Blue)**: `oklch(0.45 0.09 250)` - Professional, trustworthy, technical depth. Used for primary navigation and interactive elements.
- **Secondary Color (Soft Slate)**: `oklch(0.95 0.01 250)` - Neutral, recessive, content-focused. Used for backgrounds and subtle UI elements.
- **Accent Color (Warm Orange)**: `oklch(0.70 0.13 50)` - Attention, energy, helpful. Used for highlights, badges, and calls-to-action.

**Foreground/Background Pairings**:
- **Background (Pure White)** `oklch(1 0 0)`: Dark text `oklch(0.2 0 0)` - Ratio 16.4:1 ✓
- **Card (Light Gray)** `oklch(0.98 0 0)`: Dark text `oklch(0.2 0 0)` - Ratio 14.8:1 ✓
- **Primary (Deep Blue)** `oklch(0.45 0.09 250)`: White text `oklch(1 0 0)` - Ratio 7.2:1 ✓
- **Accent (Warm Orange)** `oklch(0.70 0.13 50)`: Dark text `oklch(0.2 0 0)` - Ratio 6.1:1 ✓
- **Muted (Subtle Gray)** `oklch(0.92 0 0)`: Medium text `oklch(0.45 0 0)` - Ratio 5.8:1 ✓

## Font Selection

Professional, highly readable typeface optimized for technical documentation with excellent number rendering.

- **Typographic Hierarchy**:
  - **H1 (Document Title)**: Inter SemiBold/32px/tight (-0.02em)/1.2 line height
  - **H2 (Major Section)**: Inter SemiBold/24px/tight (-0.01em)/1.3 line height
  - **H3 (Subsection)**: Inter Medium/20px/normal/1.4 line height
  - **H4 (Detail Header)**: Inter Medium/16px/normal/1.5 line height
  - **Body (Content)**: Inter Regular/16px/normal/1.65 line height
  - **Caption (Metadata)**: Inter Regular/14px/normal/1.5 line height
  - **Code**: SF Mono/14px/normal/1.5 line height

## Animations

**Subtle and functional** - animations serve navigation clarity and provide feedback, never decoration.

- **Purposeful Meaning**: Smooth transitions between documents establish spatial relationships. Search results fade in to indicate new content. TOC highlights slide to show position changes.
- **Hierarchy of Movement**: 
  1. **Primary** - Page transitions and document loads (300ms ease-out)
  2. **Secondary** - Search results and filter changes (200ms ease-in-out)
  3. **Tertiary** - Hover states and micro-interactions (150ms ease-in-out)

## Component Selection

- **Components**: 
  - `ScrollArea` for document content with custom scrollbar styling
  - `Card` for document index grid with hover elevation
  - `Input` with `MagnifyingGlass` icon for search
  - `Tabs` for switching between guides/references
  - `Badge` for document metadata (reading time, lines, size)
  - `Button` for navigation and actions
  - `Separator` for visual hierarchy
  - `Sidebar` for navigation structure
  
- **Customizations**:
  - Custom markdown renderer with syntax highlighting
  - Scroll-spy TOC with smooth scrolling
  - Search result highlighter component
  - Reading progress indicator
  
- **States**:
  - Search: Empty, Loading, Results, No Results
  - Documents: Loading skeleton, Loaded, Error
  - TOC: Collapsed (mobile), Expanded (desktop), Active section highlighted
  - Progress: Unread, In Progress, Completed
  
- **Icon Selection**:
  - `Book` - Documentation index
  - `MagnifyingGlass` - Search
  - `ListBullets` - Table of contents
  - `BookmarkSimple` - Saved/bookmarked
  - `CheckCircle` - Completed sections
  - `ArrowRight` - Navigation
  - `CaretRight` - Expandable sections
  
- **Spacing**: 
  - Container: `max-w-7xl mx-auto px-6`
  - Section gaps: `gap-12` (major), `gap-6` (subsections)
  - Content margins: `mb-8` (h2), `mb-4` (h3), `mb-3` (p)
  - Card padding: `p-6` (standard), `p-8` (featured)
  
- **Mobile**: 
  - Collapsible sidebar with overlay on mobile
  - Sticky search bar at top
  - Full-width content on small screens
  - TOC as bottom sheet on mobile
  - Reading progress as sticky top bar
