# SPLANTS Marketing Engine - Product Requirements Document

A clean, art gallery-inspired dashboard for small business owners to generate AI-powered marketing content with analytics and cost tracking.

**Experience Qualities**:
1. **Clarity** - Information architecture prioritizes usability; small business owners can generate content in seconds
2. **Minimalism** - 90% clean white canvas lets vibrant accent colors and content stand out like paint on canvas
3. **Efficiency** - Fast content generation, readable analytics, and clear cost tracking

**Complexity Level**: Light Application (multiple features with basic state)
- The interface is a tool for small business owners to generate marketing content and check analytics
- Must be fast, easy to read, and usable first
- Artistic touches come from deliberate splashes of color

## Essential Features

### 1. Content Generator
- **Functionality**: AI-powered content generation with customizable parameters
- **Purpose**: Create blog posts, social media content, emails, and ads instantly
- **Trigger**: User clicks "Generate" tab or primary CTA
- **Progression**: Select content type → Configure parameters (topic, tone, length) → Generate → View content with quality/SEO scores → Save or regenerate
- **Success criteria**: Form is intuitive, generation takes <5 seconds, quality scores visible

### 2. Analytics Dashboard
- **Functionality**: Visual charts showing content performance and usage metrics
- **Purpose**: Help business owners see what's working
- **Trigger**: User navigates to Analytics/Dashboard
- **Progression**: View dashboard → See bar/line charts in accent colors → Review quality/SEO scores as radial progress → Understand performance
- **Success criteria**: Data is energetic and visual, charts use vibrant colors

### 3. Content Library
- **Functionality**: Browse and manage previously generated content
- **Purpose**: Access and reuse past content
- **Trigger**: User navigates to Library
- **Progression**: View list → Filter by type/date/quality → Click to view details → Republish or edit
- **Success criteria**: Easy to scan, sorted by recency, searchable

### 4. Cost & Budget Tracking
- **Functionality**: Display current usage against monthly budget with progress bars
- **Purpose**: Keep business owners aware of spending
- **Trigger**: Visible in header or settings page
- **Progression**: View usage → See progress bar fill with accent color → Warning when approaching limit
- **Success criteria**: Always visible, turns red near 100%, clear numbers

### 5. Quality & SEO Scoring
- **Functionality**: Radial progress bars showing quality and SEO scores
- **Purpose**: Visual, artistic way to show content performance
- **Trigger**: After content generation
- **Progression**: Content generated → Scores calculated → Display as circular fills in accent colors
- **Success criteria**: Intuitive, colorful, instantly readable

## Edge Case Handling

- **Generation failures** - Clear error message with retry button
- **Budget exceeded** - Warning modal, prevent further generation
- **Empty library** - Helpful empty state with CTA to generate first content
- **Long generation times** - Loading state with progress indicator
- **Mobile usage** - Fully responsive, touch-friendly controls

## Design Direction

The interface should feel like a clean, white art gallery or minimalist artist's studio. The "canvas" (background) is pristine to make the "paint" (content and interactive elements) stand out. Usability comes first for small business owners who need speed and readability. The brand's artistic personality emerges through deliberate, high-impact splashes of color in buttons, charts, and scores.

## Color Selection

**Custom palette** - Black, Gold, White with artistic splatter aesthetic.

- **Primary Color (Charcoal Black)**: `oklch(0.20 0 0)` - Bold, professional, gallery walls. Used for headings and key text.
- **Secondary Color (Bright Gold)**: `oklch(0.75 0.15 85)` - Vibrant, energetic, the "paint splatter." Used for primary buttons, active tabs, chart accents.
- **Accent Color (Off-White)**: `oklch(0.98 0.005 85)` - Clean canvas, gallery white. Used for page background and card surfaces.
- **Supporting (Pure White)**: `oklch(1 0 0)` - Brightest highlights on cards and elements.

**Foreground/Background Pairings**:
- **Background (Off-White)** `oklch(0.98 0.005 85)`: Charcoal text `oklch(0.20 0 0)` - Ratio 13.2:1 ✓
- **Card (Pure White)** `oklch(1 0 0)`: Charcoal text `oklch(0.20 0 0)` - Ratio 15.8:1 ✓
- **Primary Button (Gold)** `oklch(0.75 0.15 85)`: Black text `oklch(0.20 0 0)` - Ratio 8.1:1 ✓
- **Charts**: Gold `oklch(0.75 0.15 85)`, Gold Dark `oklch(0.60 0.15 85)`, Charcoal `oklch(0.20 0 0)`
- **Warning (Red)**: `oklch(0.55 0.22 25)` for budget warnings approaching 100%

## Font Selection

Headings should feel classy and quirky like a modern art gallery - old English style or similar. Body text must be extremely readable for generated content.

- **Typographic Hierarchy**:
  - **H1 (App Title)**: Playfair Display Bold/32px/tight letter-spacing (-0.02em)/1.2 line height
  - **H2 (Section Headers)**: Playfair Display SemiBold/24px/tight (-0.01em)/1.3 line height
  - **H3 (Card Titles)**: Playfair Display Medium/20px/normal/1.4 line height
  - **Body (Generated Content)**: Inter Regular/16px/normal/1.65 line height
  - **UI Text (Buttons, Labels)**: Inter Medium/14px/normal/1.5 line height
  - **Caption (Metadata)**: Inter Regular/13px/normal/1.4 line height

## Animations

Subtle and purposeful. The "wet paint sheen" effect on buttons is the most prominent animation, plus smooth transitions that feel premium.

- **Purposeful Meaning**: Button hover creates a subtle shimmer/sheen like wet paint. Progress bars animate fills smoothly. Page transitions feel gallery-like.
- **Hierarchy of Movement**:
  1. **Primary** - Generate button with wet paint sheen (shimmer gradient animation)
  2. **Secondary** - Progress bar fills and chart animations (300ms ease-out)
  3. **Tertiary** - Hover states on cards and links (150ms ease-in-out)

## Component Selection

- **Components**:
  - `Card` with subtle shadows for content blocks
  - `Button` with gold accent and optional paint sheen animation
  - `Progress` bar for budget and radial for scores
  - `Tabs` for switching between Generate/Analytics/Library
  - `Input`, `Textarea`, `Select` for content generation form
  - `Badge` for content type labels
  - Custom radial progress for quality/SEO scores
  - `recharts` for analytics dashboard with gold accents
  
- **Customizations**:
  - Radial progress component for scores (circular fills)
  - Wet paint sheen animation for primary button
  - Subtle splatter texture for header/footer (low opacity, far from text)
  - Custom color scheme for charts (gold, dark gold, charcoal)
  
- **States**:
  - Generate button: Rest, Hover (sheen), Active, Loading
  - Content generation: Idle, Generating (loading), Success (show scores), Error
  - Budget progress: Normal (gold), Warning (>80%, orange), Critical (>95%, red)
  - Quality scores: Display as radial progress in gold
  
- **Icon Selection**:
  - `PaintBrushBroad` or `PaintBrush` - Primary generate icon
  - `ChartBar` - Analytics
  - `FolderOpen` - Library
  - `Gauge` or `CircleHalf` - Quality/SEO scores
  - `CurrencyDollar` - Cost tracking
  - `Sparkle` - AI generation indicator
  
- **Spacing**:
  - Container: `max-w-6xl mx-auto px-8`
  - Section gaps: `gap-8` (major sections)
  - Card padding: `p-6` (standard), `p-8` (featured)
  - Form spacing: `gap-4` between fields
  
- **Mobile**:
  - Stacked layout for forms
  - Full-width cards
  - Bottom tab navigation
  - Collapsible sections for analytics
  - Radial progress scales appropriately
