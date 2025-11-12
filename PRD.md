# Planning Guide

A simple, family-friendly web interface that transforms a powerful marketing AI backend into an accessible tool for non-technical users to generate, manage, and analyze AI-powered content.

**Experience Qualities**: 
1. **Approachable** - The interface should feel welcoming and easy to understand, removing all technical jargon and presenting complex AI capabilities through simple forms and clear labels.
2. **Confident** - Users should feel assured by visible quality scores, cost tracking, and clear feedback that the AI is working intelligently on their behalf.
3. **Professional** - While simple, the design should convey capability and trustworthiness, positioning this as a superior alternative to generic subscription services.

**Complexity Level**: Light Application (multiple features with basic state)
  - The app provides four distinct feature areas (Generate, Library, Analytics, Settings) with form inputs, data display, and API integration, but without requiring user accounts or complex state management beyond API communication and local settings.

## Essential Features

### Content Generation
- **Functionality**: Form-based interface to create AI-generated marketing content with configurable parameters
- **Purpose**: Democratizes access to sophisticated multi-model AI synthesis that would otherwise require technical expertise
- **Trigger**: User navigates to Generate page and fills out content form
- **Progression**: Select content type → Enter topic and keywords → Choose tone → Toggle premium AI → Click Generate → View generated content with quality/SEO scores → Copy or regenerate
- **Success criteria**: Users can generate content in under 60 seconds with visible quality metrics; error messages are clear and actionable

### Content Library Management
- **Functionality**: Browsable history of all generated content with search, filter, and management capabilities
- **Purpose**: Provides organization and reusability, preventing loss of previous work and enabling content strategy overview
- **Trigger**: User navigates to Library page
- **Progression**: View table of past content → Filter by type/date → Click to expand full content → Copy to clipboard → Delete if needed
- **Success criteria**: Users can find any previous content within 10 seconds; table loads smoothly even with 100+ items

### Analytics Dashboard
- **Functionality**: Visual charts and metrics displaying content performance, quality trends, and ROI calculations
- **Purpose**: Demonstrates the superior value proposition over "dumb" subscription services by surfacing built-in intelligence
- **Trigger**: User navigates to Dashboard page
- **Progression**: View dashboard → See total costs → Review quality score trends → Check monthly content volume → Understand ROI metrics
- **Success criteria**: Non-technical users can understand their usage patterns and cost-benefit without explanation

### Settings Configuration
- **Functionality**: Simple form to configure API keys, budget limits, and integration webhooks
- **Purpose**: Gives users control over costs and connections while maintaining simplicity
- **Trigger**: User navigates to Settings page
- **Progression**: Enter API key → Set monthly budget → Add webhook URLs → Save settings → See confirmation
- **Success criteria**: Settings persist between sessions; users understand the impact of each setting

## Edge Case Handling
- **API Connection Failures**: Show friendly error messages with retry buttons rather than technical error codes
- **Empty States**: Display helpful onboarding messages when no content exists yet ("Generate your first piece of content to get started!")
- **Budget Limits**: Warn users when approaching monthly budget limit; prevent generation when exceeded with clear upgrade path
- **Invalid API Keys**: Detect and surface API key issues immediately on the Settings page with links to documentation
- **Long Generation Times**: Show animated loading states with progress indicators; allow cancellation if supported by backend
- **Mobile Responsiveness**: Gracefully collapse complex tables and charts into mobile-friendly views

## Design Direction
The design should feel professional yet approachable—like a premium SaaS tool that happens to be simple to use. Think of the clarity of Stripe's dashboard combined with the friendliness of Notion. The interface should use a minimal approach where the content itself is the hero, with controls and metrics providing subtle but confident support.

## Color Selection
Complementary (opposite colors) - A sophisticated blue-purple primary color evokes trust and intelligence (AI/tech) while a warm amber accent creates approachable energy and highlights important actions.

- **Primary Color**: Deep Blue-Purple (oklch(0.45 0.15 270)) - Communicates intelligence, trustworthiness, and premium AI capabilities
- **Secondary Colors**: Soft neutral grays (oklch(0.96 0 0)) for backgrounds and cards, creating breathing room without competing with content
- **Accent Color**: Warm Amber (oklch(0.70 0.15 70)) - Draws attention to primary actions and success states with approachable energy
- **Foreground/Background Pairings**:
  - Background (White oklch(1 0 0)): Dark text (oklch(0.2 0 0)) - Ratio 16.1:1 ✓
  - Card (Light Gray oklch(0.98 0 0)): Dark text (oklch(0.2 0 0)) - Ratio 15.3:1 ✓
  - Primary (Blue-Purple oklch(0.45 0.15 270)): White text (oklch(1 0 0)) - Ratio 6.8:1 ✓
  - Secondary (Light Gray oklch(0.96 0 0)): Dark text (oklch(0.25 0 0)) - Ratio 11.2:1 ✓
  - Accent (Amber oklch(0.70 0.15 70)): Dark text (oklch(0.2 0 0)) - Ratio 7.3:1 ✓
  - Muted (Mid Gray oklch(0.94 0 0)): Muted text (oklch(0.50 0 0)) - Ratio 6.1:1 ✓

## Font Selection
Clean, highly legible sans-serif typography that balances professionalism with approachability—Inter provides excellent readability at all sizes while maintaining a modern, tech-forward personality.

- **Typographic Hierarchy**: 
  - H1 (Page Titles): Inter SemiBold/32px/tight tracking (-0.02em) - Used for main page headers
  - H2 (Section Headers): Inter SemiBold/24px/tight tracking (-0.01em) - Used for card titles and major sections
  - H3 (Subsections): Inter Medium/18px/normal tracking - Used for form labels and list headers
  - Body (Content): Inter Regular/16px/relaxed leading (1.6) - Used for paragraphs and descriptions
  - Small (Metadata): Inter Regular/14px/normal leading - Used for timestamps, helper text, metrics
  - Label (Form Labels): Inter Medium/14px/normal tracking - Used for input labels with slightly heavier weight
  - Button Text: Inter Medium/16px/tight tracking - Used for all button labels

## Animations
Animations should be purposeful and subtle—reinforcing actions rather than decorating the interface. The motion language should feel intelligent and responsive, like the AI itself is reacting to user input.

- **Purposeful Meaning**: Smooth transitions between pages suggest seamless navigation through a cohesive system; loading states with subtle pulse animations convey active AI processing
- **Hierarchy of Movement**: Primary actions (Generate button) get satisfying press animations; quality scores count up when revealed; dashboard charts animate in with staggered delays to guide attention

## Component Selection
- **Components**: 
  - `Card` for content containers (Generate form, Library items, Dashboard widgets, Settings panels)
  - `Button` with variants (default for Generate, outline for secondary actions, destructive for delete)
  - `Input`, `Textarea` for text entry with clear labels
  - `Select` for Content Type and Tone dropdowns
  - `Switch` for Premium AI toggle
  - `Table` for Content Library with sortable columns
  - `Badge` for content type tags and status indicators
  - `Tabs` for potential multi-section views
  - `Dialog` for delete confirmations
  - `Separator` for visual section breaks
  - `Progress` for budget usage visualization
  - `Skeleton` for loading states
  - `Toast` (sonner) for success/error notifications
  
- **Customizations**: 
  - Custom stat cards for dashboard metrics with large numbers and trend indicators
  - Custom quality score badges with color coding (red <60, amber 60-79, green 80+)
  - Custom empty state illustrations using simple SVG graphics
  
- **States**: 
  - Buttons: Hover shows slight scale (1.02) and color shift; Active shows press down; Disabled shows reduced opacity with not-allowed cursor
  - Inputs: Focus shows accent color ring; Error shows destructive color ring with shake animation
  - Cards: Hover on interactive cards shows subtle shadow lift
  
- **Icon Selection**: 
  - `Sparkles` for AI/generation features
  - `Article`, `ChatCircle`, `EnvelopeSimple` for content types
  - `TrendUp` for analytics/quality
  - `Database` for library
  - `Gear` for settings
  - `Copy`, `Trash` for actions
  - `ChartBar`, `ChartLine` for dashboard
  - `Warning` for budget alerts
  
- **Spacing**: 
  - Page padding: `p-6 md:p-8`
  - Card padding: `p-6`
  - Section gaps: `gap-6`
  - Form field gaps: `gap-4`
  - Inline element gaps: `gap-2`
  
- **Mobile**: 
  - Navigation collapses to bottom tab bar on mobile
  - Tables transform to stacked cards on mobile
  - Dashboard charts stack vertically on mobile
  - Form fields use full width on mobile
  - Large buttons for easy touch targets (min-h-11)
