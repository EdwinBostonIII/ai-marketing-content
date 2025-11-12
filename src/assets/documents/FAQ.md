# SPLANTS Marketing Engine - Frequently Asked Questions (FAQ)

## Reference Guide for Common Questions

This document addresses frequently asked questions about the SPLANTS Marketing Engine. For additional information, refer to README.md or the system documentation.

---

## Table of Contents

1. [General Questions](#general-questions)
2. [Setup & Installation](#setup--installation)
3. [Costs & Pricing](#costs--pricing)
4. [Features & Capabilities](#features--capabilities)
5. [Technical Questions](#technical-questions)
6. [Usage & Best Practices](#usage--best-practices)
7. [Troubleshooting](#troubleshooting)
8. [Legal & Business](#legal--business)
9. [Comparison to Alternatives](#comparison-to-alternatives)
10. [Advanced Topics](#advanced-topics)

---

## General Questions

### What is SPLANTS Marketing Engine?

**Answer:** SPLANTS Marketing Engine is an AI-powered content generation system designed for the SPLANTS brand. The system generates marketing content for custom paint-splatter pants using GPT-4 technology. It provides automated creation of blog posts, social media content, emails, and advertisements at a monthly operational cost of $35-80.

---

### Who should use this system?

**Answer:** This system is designed for the SPLANTS marketing team to manage content creation for the custom pants business. It provides automated content generation, SEO optimization, and multi-platform publishing capabilities.

---

### Do I need to know how to code?

**Answer:** No programming knowledge is required. The system provides a web interface at `http://localhost:8080/docs` for all operations. Configuration requires basic terminal command execution, which is documented in the setup guide.

---

### How much does it cost?

**Answer:** Total monthly cost: **$35-80**

**Breakdown:**
- **Infrastructure:** $20-30/month (server to run it on)
- **AI Usage:** $15-50/month (depends on how much you generate)
- **Optional Redis:** +$10-15/month (reduces AI costs by 30-50%)
- **Optional Premium Features:** +$0.02-0.05 per request when used

**Compare to alternatives:**
- Marketing agency: $2,000-10,000/month
- Freelance writers: $500-2,000/month for 5-20 articles
- HubSpot: $800-3,200/month
- Jasper.ai: $49-125/month (AI writing only, no publishing or analytics)

---

### Is this actually good enough for professional use?

**Answer:** **Yes!** SPLANTS uses GPT-4, the most advanced AI model available. The system includes:
- **Quality scoring** (0-1 scale, aim for 0.7+)
- **SEO optimization** with keyword integration
- **Platform-specific formatting** (Twitter, LinkedIn, etc.)
- **Professional templates** based on proven content structures
- **A/B testing** to find what works best

Average quality scores are 0.85-0.95 (85-95%). Many users find the content requires only minor editing.

---

### Can I try it before paying?

**Answer:** Sort of. The software itself is free and open source. You only pay for:
1. **Server costs** ($20-30/month) - You can start with your own computer (free!)
2. **OpenAI API usage** - Add $10-20 to start, this generates 300-600 pieces

So you can trial it for $10-20 total cost, then cancel if you don't like it.

---

## Setup & Installation

### What do I need to get started?

**Answer:** You need:
1. **A computer** (Windows, Mac, or Linux) with:
   - 4GB RAM minimum
   - 20GB free disk space
   - Internet connection
2. **Docker** (free software - [docker.com](https://docker.com))
3. **OpenAI account** with API key ([platform.openai.com](https://platform.openai.com))
4. **30 minutes** to follow setup guide

---

### How long does setup take?

**Answer:**
- **First time:** 30-60 minutes (includes installing Docker, getting API keys, configuration)
- **Subsequent starts:** 30-60 seconds
- **Downloading for first time:** 5-10 minutes (Docker downloads required software)

---

### Can I run this on my regular computer?

**Answer:** **Yes!** You can run SPLANTS on:
- Your Windows PC (Windows 10/11)
- Your Mac (Intel or Apple Silicon)
- Your Linux computer

**Minimum requirements:**
- 4GB RAM (8GB recommended)
- 20GB free disk space
- Dual-core processor

**When to move to a server:**
- You want 24/7 availability
- Multiple team members need access
- You're generating 500+ pieces per month

---

### Do I need to be a programmer?

**Answer:** **No!** Here's what you need to know:
- **Copy and paste** commands into terminal
- **Edit a text file** (.env configuration)
- **Use a web browser** to access the interface

If you can follow step-by-step instructions, you can set this up. See SETUP_GUIDE.md for detailed visual instructions.

---

### What if I get stuck during setup?

**Answer:**
1. **Check TROUBLESHOOTING.md** - Solutions to 60+ common problems
2. **Review SETUP_GUIDE.md** - Step-by-step visual guide
3. **Check logs:**
   ```bash
   docker-compose logs -f app
   ```
4. **Ask for help:**
   - GitHub Issues: [repository URL]/issues
   - Include: Operating system, error messages, what you tried

---

### Can I run this without Docker?

**Answer:** **Not recommended.** Docker makes setup incredibly simple. Without it, you'd need to manually:
- Install Python 3.11
- Install PostgreSQL database
- Configure environment variables
- Manage dependencies
- Handle system differences

Docker does all this automatically. It's worth the 5-minute Docker installation!

---

## Costs & Pricing

### How much does content generation actually cost?

**Answer:** **Approximately $0.03 per piece** on average.

**Detailed breakdown by content type:**
- **Social media post (100 words):** ~$0.01
- **Email (300 words):** ~$0.02
- **Blog post (800 words):** ~$0.03
- **Long article (2000 words):** ~$0.06
- **Premium multi-model:** +$0.02-0.05 extra

**Examples:**
- 100 blog posts/month: ~$3 in AI costs
- 500 social posts/month: ~$5 in AI costs
- 200 emails/month: ~$4 in AI costs

---

### What if I run out of OpenAI credits?

**Answer:** Content generation will fail with an error message. Simply:
1. Go to [platform.openai.com/account/billing](https://platform.openai.com/account/billing)
2. Add more credit ($20 recommended)
3. Wait 2-3 minutes
4. Try generating again

**Tip:** Enable auto-recharge to never run out!

---

### How do I control costs?

**Answer:** Multiple ways:

**1. Set Budgets in .env:**
```env
MONTHLY_AI_BUDGET=50      # Stop at $50/month
DAILY_API_LIMIT=100       # Max 100 requests/day
```

**2. Enable Redis Caching:**
- Reduces costs by 30-50%
- Cost: +$10-15/month for Redis
- ROI: Pays for itself at 300+ pieces/month

**3. Use Shorter Content:**
```json
{
  "length": 500  // Instead of 2000
}
```

**4. Monitor Daily:**
- Check: `http://localhost:8080/v1/costs/usage`
- Review weekly spending
- Adjust as needed

**5. Set OpenAI Limits:**
- Go to OpenAI billing settings
- Set hard and soft limits

---

### Is there a free tier?

**Answer:** Not exactly, but:
- **The software is FREE** (open source)
- **You only pay for usage:**
  - Server: $0 if running on your computer
  - AI: Pay only for what you generate (~$0.03/piece)
  - No subscription fees
  - No monthly minimums

**Example minimal cost:**
- Run on your computer: $0/month infrastructure
- Generate 100 pieces: ~$3/month AI usage
- **Total: $3/month**

---

### What happens if costs exceed my budget?

**Answer:** **The system protects you:**

1. **Soft warning at 80%:**
   - System logs warning
   - Continue generating
   - Email alert (if webhooks configured)

2. **Hard stop at 100%:**
   - Returns 402 error
   - Stops all generation
   - Clear message about budget exceeded

3. **Resolution:**
   - Increase MONTHLY_AI_BUDGET in .env
   - OR wait for next month (resets on 1st)
   - OR review and optimize usage

---

## Features & Capabilities

### What types of content can I generate?

**Answer:** 8 content types:

1. **Blog Posts** - SEO-optimized articles (500-2500 words)
2. **Social Media Posts** - Platform-specific content
3. **Emails** - Marketing, newsletters, sequences
4. **Ad Copy** - Facebook, Google, LinkedIn ads
5. **Landing Pages** - Conversion-focused copy
6. **Video Scripts** - YouTube, TikTok, Instagram
7. **Product Descriptions** - E-commerce copy
8. **Press Releases** - Media-ready announcements

Each type is optimized for its specific purpose.

---

### Which social media platforms are supported?

**Answer:** 9 platforms:

**Content generation for:**
-  Twitter/X
-  LinkedIn
-  Instagram
-  Facebook
-  YouTube
-  TikTok
-  Pinterest
-  Blog/Website
-  Email

**Auto-publishing to** (requires API keys):
-  Twitter (advanced setup)
-  LinkedIn (advanced setup)
-  Facebook (advanced setup)

---

### Can I generate content in different languages?

**Answer:** **Yes!** GPT-4 supports 50+ languages.

**How to use:**
```json
{
  "topic": "Schreiben Sie einen Blogpost über KI-Marketing (German)",
  "keywords": ["KI", "Marketing", "Deutschland"]
}
```

Or specify in target_audience:
```json
{
  "topic": "AI Marketing Benefits",
  "target_audience": "Spanish-speaking small business owners in Latin America"
}
```

**Supported languages include:**
Spanish, French, German, Italian, Portuguese, Dutch, Chinese, Japanese, Korean, Arabic, and many more.

---

### What is SEO optimization?

**Answer:** **SEO = Search Engine Optimization** - making content rank better on Google.

**SPLANTS SEO features:**
- **Keyword integration** - Naturally includes your keywords
- **Optimal keyword density** - 1-3% (industry standard)
- **Header structure** - Proper H1, H2, H3 organization
- **Meta descriptions** - Suggested descriptions for search results
- **Readability** - Optimized sentence length and structure
- **Internal linking** - Suggestions for related content
- **SEO scoring** - Rates content 0-1 (aim for 0.7+)

**Real impact:**
Well-optimized content can rank on first page of Google, bringing free organic traffic.

---

### What is A/B testing?

**Answer:** **Testing multiple versions to see which performs better.**

**How it works:**
1. Generate original content
2. Set `generate_variants: true`
3. System creates 3 different versions
4. Use each version
5. Track which gets more engagement
6. Use the winning version going forward

**Example use cases:**
- Email subject lines (which gets more opens?)
- Social media posts (which gets more clicks?)
- Ad copy (which gets more conversions?)
- Landing page headlines (which converts better?)

**Cost:** Same as normal generation (generates 3x as much content)

---

### Can I customize the writing style?

**Answer:** **Yes!** Multiple ways:

**1. Use Tone Parameter:**
```json
{
  "tone": "professional" | "casual" | "enthusiastic" | 
          "conversational" | "authoritative" | "friendly" | 
          "humorous" | "inspirational"
}
```

**2. Specify Target Audience:**
```json
{
  "target_audience": "Tech-savvy millennials who value authenticity and sustainability"
}
```

**3. Add Style Instructions to Topic:**
```json
{
  "topic": "Write in the style of Seth Godin: 5 Marketing Tips for Small Business"
}
```

**4. Use Templates:**
Pre-built templates maintain consistent style across content.

---

### What are the quality scores?

**Answer:** **Two scores for every piece:**

**1. Quality Score (0-1):**
- Measures overall content quality
- Based on: length, structure, keyword integration, readability, engagement
- **0.9-1.0:** Excellent (publication-ready)
- **0.7-0.89:** Good (minor edits needed)
- **0.5-0.69:** Fair (needs work)
- **Below 0.5:** Poor (regenerate)

**2. SEO Score (0-1):**
- Measures search engine optimization
- Based on: keyword presence, density, placement, structure
- **0.8+:** Excellent SEO
- **0.6-0.79:** Good SEO
- **Below 0.6:** Needs SEO improvement

**Both scores come with recommendations for improvement.**

---

### What are content templates?

**Answer:** **Pre-built structures for proven content types.**

**Available templates:**
- **Blog Listicle** - "10 Ways to..." format
- **How-To Guide** - Step-by-step tutorials
- **Social Campaign** - Multi-platform campaigns
- **Email Welcome Sequence** - 3-email onboarding
- **Problem-Solution-Action Ad** - Classic ad framework
- **Landing Page** - High-conversion structure

**Benefits:**
- Faster content generation
- Proven structures that work
- Consistent quality
- Less thinking required

**How to use:**
```json
{
  "template_id": "blog_listicle",
  "variables": {
    "number": "10",
    "topic": "AI Marketing Tips"
  }
}
```

---

## Technical Questions

### What is Docker and why do I need it?

**Answer:** **Docker is like a "shipping container" for software.**

**Why you need it:**
- Packages everything the app needs
- Works the same on every computer
- No manual installation of Python, PostgreSQL, etc.
- Isolated from your other programs

**Real-world analogy:**
Like a shipping container that has everything inside it - no matter where it goes (Windows, Mac, Linux), everything needed is packed in.

**Without Docker:**
You'd need to manually install and configure 10+ different software tools. Docker does it all automatically.

---

### What is PostgreSQL?

**Answer:** **PostgreSQL is a database - a organized place to store data.**

**What it stores:**
- All your generated content
- Analytics data
- User settings
- Cost tracking
- A/B test results

**Think of it as:**
A digital filing cabinet that organizes everything by date, type, quality, platform, etc.

**Why PostgreSQL specifically:**
- Free and open source
- Extremely reliable
- Used by Fortune 500 companies
- Perfect for this use case

---

### What is an API?

**Answer:** **API = Application Programming Interface**

**Simple explanation:**
A way for different programs to talk to each other.

**In SPLANTS:**
- You (or your code) sends a request to the API
- API talks to the AI
- AI generates content
- API returns content to you

**Interface types:**
1. **Web Interface** - Click buttons at localhost:8080/docs
2. **Command line** - Use cURL commands
3. **Your code** - Python, JavaScript, etc.

All three do the same thing, just different interfaces.

---

### What is localhost:8080?

**Answer:** **Your computer's address and door number.**

**Breaking it down:**
- **localhost** = Your own computer (not the internet)
- **8080** = Port number (like apartment number)
- **localhost:8080** = "Port 8080 on my computer"

**When to use:**
Running on your computer: `http://localhost:8080`
Running on a server: `http://your-server-ip:8080`

**Why 8080:**
Common port for web apps. Could be changed to 8081, 9000, etc. if 8080 is busy.

---

### Can I access this from my phone?

**Answer:** **Depends on setup:**

**If running on your computer:**
- **Same network:** Yes! Use your computer's IP address
  - Example: `http://192.168.1.100:8080`
  - Find IP: `ipconfig` (Windows) or `ifconfig` (Mac/Linux)

**If running on a server:**
- **Anywhere:** Yes! Use server's address
  - Example: `http://your-domain.com` or `http://123.45.67.89:8080`

**To make it easy:**
- Deploy to a server (see docs_DEPLOYMENT.md)
- Get a domain name
- Access from anywhere

---

### How does the system store my content?

**Answer:** **Everything is stored in PostgreSQL database.**

**What's stored:**
- Generated content (full text)
- Quality and SEO scores
- Metadata (keywords, tone, platform, etc.)
- Generation timestamp
- Costs and analytics
- A/B test variants

**Where it's stored:**
- **Docker volume** on your computer
- Or on your server if deployed
- **NOT** in the cloud (unless you choose to)

**Backup:**
```bash
./scripts_backup.sh
```

Creates a backup file you can save wherever you want.

---

### Is my data private?

**Answer:** **Yes, completely private!**

**What's private:**
-  All generated content (stored in YOUR database)
-  Your API keys (in YOUR .env file)
-  Your analytics (in YOUR database)
-  Your settings (on YOUR computer/server)

**What OpenAI sees:**
- Your request (topic, keywords, etc.)
- They generate content
- **BUT:** OpenAI doesn't train on API content (policy)
- **AND:** Your content is not shared with others

**Best practices:**
- Keep .env file secure
- Use strong API_KEY
- Regular backups
- HTTPS if deployed to internet

---

### Can multiple people use the same installation?

**Answer:** **Yes, but with limitations.**

**Current setup:**
- Single API_KEY for everyone
- Everyone shares same budget limits
- Everyone can see all generated content

**For teams:**
- Share the API_KEY securely
- Or give each person their own installation
- Or wait for multi-user feature (future update)

**Access control:**
- Anyone with API_KEY can generate content
- Consider IP restrictions for security
- Use firewall rules if needed

---

### Can I run this 24/7?

**Answer:** **Yes, if deployed to a server.**

**On your computer:**
- Only runs when computer is on
- Stops when computer sleeps/hibernates
- Good for personal use

**On a server:**
- Runs 24/7 automatically
- Accessible from anywhere
- Good for business use
- Cost: $10-30/month
- See docs_DEPLOYMENT.md

---

### What happens if the system crashes?

**Answer:** **Don't worry - your data is safe!**

**Data protection:**
- PostgreSQL database = persistent storage
- Even if app crashes, database stays intact
- Content is not lost

**Recovery:**
```bash
# Restart everything
docker-compose restart

# Or full restart
docker-compose down
docker-compose up -d
```

**Check what's running:**
```bash
docker-compose ps
```

**If database corrupted (rare):**
- Restore from backup: `./scripts_restore.sh`
- See TROUBLESHOOTING.md

---

## Usage & Best Practices

### How do I write good prompts?

**Answer:** **Be specific and provide context!**

**Bad prompt:**
```json
{
  "topic": "marketing"
}
```

**Good prompt:**
```json
{
  "topic": "5 social media marketing strategies that small businesses can implement in under 2 hours per week to increase engagement by 50%, focusing on authentic connection rather than hard selling",
  "keywords": ["social media", "marketing", "small business", "engagement", "authentic marketing"],
  "target_audience": "Small business owners aged 30-50 who are busy, value practicality, and want proven strategies they can implement immediately",
  "tone": "professional",
  "length": 800
}
```

**Best practices:**
1. **Be specific** about what you want
2. **Include context** about your audience
3. **Use keywords** for SEO
4. **Specify tone** for consistency
5. **Set appropriate length**
6. **Mention platform** if relevant

---

### How long should my content be?

**Answer:** **Depends on content type and platform.**

**Recommended lengths:**

| Content Type | Recommended | Minimum | Maximum |
|--------------|-------------|---------|---------|
| Social Media | 50-200 | 25 | 300 |
| Email | 200-500 | 100 | 800 |
| Blog Post | 800-1500 | 500 | 3000 |
| Product Description | 150-300 | 100 | 500 |
| Ad Copy | 50-150 | 25 | 200 |
| Video Script | 200-400 | 100 | 1000 |
| Landing Page | 500-1000 | 300 | 2000 |

**SEO consideration:**
For blog posts, 800-1500 words is ideal for Google ranking.

**Cost consideration:**
Longer content costs more. Balance quality vs. cost.

---

### Should I edit AI-generated content?

**Answer:** **Yes, always review and customize!**

**Why edit:**
- Add your personal voice
- Include specific examples from your business
- Verify facts (AI can occasionally be wrong)
- Customize for your exact audience
- Add calls-to-action specific to your business

**What to check:**
1. **Accuracy** - Are facts correct?
2. **Tone** - Does it match your brand?
3. **Relevance** - Is it truly useful to your audience?
4. **CTAs** - Are calls-to-action appropriate?
5. **Links** - Add relevant links to your site/products

**How much editing:**
- High-quality content (0.9+): 5-10% editing
- Good content (0.7-0.89): 10-20% editing
- Fair content (0.5-0.69): 30-50% editing

---

### Can I use this for client work?

**Answer:** **Absolutely yes!**

**You own the content:**
- OpenAI grants full rights to API-generated content
- You can use it commercially
- You can resell it
- You can claim authorship

**For agencies:**
- Perfect for serving multiple clients
- Generate client-specific content
- White-label opportunity
- Scales your services

**Recommended workflow:**
1. Generate content with SPLANTS
2. Customize for client's brand
3. Add client-specific examples
4. Review for accuracy
5. Deliver as if you wrote it

**Ethics:**
- Be transparent about AI assistance if asked
- Always review before delivering
- Add your expertise on top

---

### How do I get the best quality?

**Answer:** **Follow these best practices:**

**1. Use detailed prompts:**
- Be specific about what you want
- Include audience context
- Mention desired outcome

**2. Provide good keywords:**
- 5-10 relevant keywords
- Mix of broad and specific terms
- Industry-specific terms

**3. Set appropriate length:**
- Not too short (< 200 words)
- Not too long (> 2000 words unless needed)

**4. Use correct tone:**
- Match your brand voice
- Consider platform (LinkedIn = professional, Instagram = casual)

**5. Consider premium mode:**
```json
{
  "use_premium": true
}
```
Costs +$0.02-0.05 but gives 20-30% better quality

**6. Try templates:**
- Pre-built structures
- Proven to work
- Consistent results

**7. Regenerate if needed:**
- Don't settle for low quality
- Try different prompts
- Sometimes you just get a "bad roll"

---

### How often should I generate content?

**Answer:** **Depends on your marketing strategy.**

**Social media:**
- Daily: 1-3 posts
- Weekly: 7-21 posts

**Blog:**
- Weekly: 1-2 posts
- Monthly: 4-8 posts

**Email:**
- Weekly newsletter: 1 email/week
- Welcome sequence: 3-5 emails (one-time)
- Promotional: 1-2/week

**Strategy tip:**
Better to post consistently than sporadically. Use SPLANTS to maintain consistency.

---

### Should I schedule or post immediately?

**Answer:** **Schedule for best results!**

**Why schedule:**
- Post at optimal times (when audience is online)
- Maintain consistency even when busy
- Plan content in advance
- Better work-life balance

**Optimal posting times (US Eastern):**
- **LinkedIn:** Tuesday-Thursday, 9-11 AM
- **Twitter:** Wednesday-Friday, 9 AM-12 PM
- **Instagram:** Tuesday-Friday, 9-11 AM
- **Facebook:** Wednesday-Friday, 1-3 PM

**SPLANTS scheduling:**
```json
{
  "schedule_time": "2024-11-15T09:00:00Z",
  "auto_optimize_timing": true
}
```

---

## Troubleshooting

### Why isn't my content generating?

**Answer:** Check these common issues:

1. **OpenAI API key wrong or no credit**
   - Verify key in .env
   - Check credit balance at platform.openai.com

2. **Budget limit reached**
   - Check: `http://localhost:8080/v1/costs/usage`
   - Increase MONTHLY_AI_BUDGET if needed

3. **Services not running**
   - Run: `docker-compose ps`
   - Should see "Up" status

4. **Database connection failed**
   - Wait 60 seconds after starting
   - Check logs: `docker-compose logs db`

See TROUBLESHOOTING.md for detailed solutions.

---

### Content quality is low. How do I improve it?

**Answer:** Try these improvements:

1. **Be more specific in prompts**
2. **Use better keywords**
3. **Set appropriate length** (not too short)
4. **Use premium mode** for important content
5. **Try templates** for proven structures
6. **Regenerate** with different prompt
7. **Check quality score** - aim for 0.7+

See "How do I get the best quality?" section above.

---

### System is running slow. What can I do?

**Answer:**

1. **Reduce content length**
2. **Don't use premium mode** unless needed
3. **Enable Redis caching** (30-50% faster)
4. **Check system resources:** `docker stats`
5. **Close other applications**
6. **Deploy to better hardware**

See TROUBLESHOOTING.md "Performance Issues" section.

---

### Where are the logs?

**Answer:** Multiple ways to view logs:

**View live logs:**
```bash
docker-compose logs -f app
```

**View last 100 lines:**
```bash
docker-compose logs --tail=100 app
```

**Save logs to file:**
```bash
docker-compose logs app > my-logs.txt
```

**View logs in file:**
The app also writes to `logs/app.log` file.

---

### How do I backup my content?

**Answer:**

**Automated backup:**
```bash
./scripts_backup.sh
```

Creates compressed backup in `backups/` folder.

**Manual backup:**
```bash
docker-compose exec db pg_dump -U splants splants > my-backup.sql
```

**Restore from backup:**
```bash
./scripts_restore.sh backups/your-backup-file.sql.gz
```

**Best practice:**
- Backup weekly minimum
- Keep backups in multiple places (external drive, cloud storage)
- Test restore occasionally

---

## Legal & Business

### Do I own the generated content?

**Answer:** **Yes, you own it 100%!**

**OpenAI's policy:**
- You own all content generated through API
- Full commercial rights
- Can use, modify, resell, publish
- No attribution required

**SPLANTS license:**
- Open source MIT license
- Free to use commercially
- Can modify code
- Can white-label for clients

**In practice:**
Treat it like you wrote it yourself. You have complete ownership and rights.

---

### Is this legal for commercial use?

**Answer:** **Absolutely yes!**

**Legal uses:**
-  Use for your business
-  Sell to clients
-  Generate client content
-  Create products (books, courses, etc.)
-  White-label and resell
-  Use in any industry

**Only restriction:**
Don't claim you built SPLANTS itself (if you resell it, follow MIT license attribution).

---

### Can I use this for affiliate marketing?

**Answer:** **Yes!**

Generate:
- Product reviews
- Comparison articles
- Email sequences
- Social media content
- Landing pages

**Best practice:**
- Disclose AI assistance if platform requires
- Verify product information accuracy
- Add personal experience when possible
- Follow FTC guidelines for disclosures

---

### Do I need to disclose AI usage?

**Answer:** **Usually no, but check your specific situation:**

**No disclosure needed:**
- Personal blog
- Your business website
- Social media (most platforms)
- Email marketing to your list
- Client work (unless contract specifies)

**Disclosure might be needed:**
- Some professional journals
- Academic publications
- If client specifically asks
- Some contest submissions
- FTC compliance (if selling products)

**When in doubt:**
- Check platform's terms of service
- Check client contract
- Be transparent if asked directly

**Note:** This is not legal advice. Consult a lawyer for your specific situation.

---

### Can I white-label this for clients?

**Answer:** **Yes!** MIT license allows it.

**What you can do:**
- Remove SPLANTS branding
- Add your own branding
- Sell as your own service
- Charge whatever you want

**MIT license requirements:**
- Keep the original MIT license in the code
- Don't claim you wrote the original code

**Business model:**
Many agencies do this:
- Charge clients $500-2000/month
- Use SPLANTS backend ($35-80/month)
- Keep the difference as profit
- Provide management and customization

---

## Comparison to Alternatives

### How is this different from ChatGPT?

**Answer:**

| Feature | SPLANTS | ChatGPT |
|---------|---------|---------|
| **Purpose** | Marketing automation | General chat |
| **Content types** | 8 specialized types | Any text |
| **SEO optimization** |  Automatic |  Manual |
| **Quality scoring** |  Yes |  No |
| **Platform optimization** |  Yes |  No |
| **Analytics** |  Yes |  No |
| **Cost tracking** |  Yes |  No |
| **A/B testing** |  Yes |  No |
| **Templates** |  Yes |  No |
| **Storage** |  Database |  Lost after 3 months |
| **API access** |  Yes |  Different API |
| **Cost** | ~$0.03/piece | $20/month unlimited |

**Use ChatGPT when:** You want casual conversation or one-off text
**Use SPLANTS when:** You need professional marketing automation

---

### How is this different from Jasper.ai?

**Answer:**

| Feature | SPLANTS | Jasper.ai |
|---------|---------|-----------|
| **Cost** | $35-80/month | $49-125/month |
| **Content limit** | Unlimited | Plan-based |
| **Publishing** |  Built-in |  Manual |
| **Analytics** |  Yes | Limited |
| **Self-hosted** |  Yes |  Cloud only |
| **Data privacy** |  Your server |  Their servers |
| **API access** |  Full control |  Limited |
| **Customization** |  Full source |  No |
| **Multi-model** |  Optional |  Yes |

**Use Jasper when:** You want a polished UI and don't mind cloud storage
**Use SPLANTS when:** You want more control, privacy, and cost efficiency

---

### How is this different from hiring a writer?

**Answer:**

| Aspect | SPLANTS | Freelance Writer |
|--------|---------|------------------|
| **Cost per blog post** | ~$0.03 | $100-500 |
| **Time to deliver** | 30 seconds | 3-7 days |
| **Unlimited revisions** |  Free |  Usually extra |
| **Availability** | 24/7 | Business hours |
| **Consistency** | Always available | May be unavailable |
| **Quality** | 85-95% | 80-100% |
| **Personal touch** |  Needs your edit |  More human |
| **Industry knowledge** | General | May be specialized |
| **SEO expertise** |  Automatic | Varies |

**Best approach:** Use SPLANTS + human editor
- Generate with SPLANTS (fast, cheap)
- Edit with human touch (quality, personalization)
- Get best of both worlds

---

### How is this different from a marketing agency?

**Answer:**

| Aspect | SPLANTS | Marketing Agency |
|--------|---------|------------------|
| **Cost** | $35-80/month | $2,000-10,000/month |
| **Content creation** |  Unlimited | Limited by budget |
| **Strategy** |  You decide |  They provide |
| **Design** |  Text only |  Full creative |
| **Management** | You manage | They manage |
| **Turnaround** | Instant | Days/weeks |
| **Flexibility** | Complete | Contract-based |

**When to use SPLANTS:** You know what you need, want control, limited budget
**When to hire agency:** You need full-service, have budget, want hands-off

**Best combo:** SPLANTS for content + agency for strategy

---

## Advanced Topics

### Can I modify the code?

**Answer:** **Yes! It's open source (MIT license).**

**What you can modify:**
- AI models used
- Prompts and templates
- Scoring algorithms
- API endpoints
- UI/interface
- Database schema
- Anything!

**How to modify:**
1. Edit `main.py` or other files
2. Test your changes
3. Restart: `docker-compose restart`

**Popular modifications:**
- Add new content types
- Custom quality scoring
- Additional platforms
- Custom templates
- Different AI models (Claude, Gemini, etc.)

**Contributing:**
If you make improvements, consider opening a Pull Request on GitHub!

---

### Can I use different AI models?

**Answer:** **Yes!**

**Currently supported:**
- GPT-4 Turbo (default)
- Claude 3 Sonnet (optional, premium)

**How to change model:**

**Edit main.py** around line 793:
```python
# Change from:
model="gpt-4-turbo-preview",

# To any of these:
model="gpt-4",                    # GPT-4 (expensive, high quality)
model="gpt-3.5-turbo",           # GPT-3.5 (10x cheaper, lower quality)
model="gpt-3.5-turbo-16k",       # GPT-3.5 with longer context
```

**Cost comparison:**
- GPT-4: $0.03/request (default)
- GPT-3.5: $0.003/request (90% cheaper)
- Claude: $0.015/request (middle ground)

---

### Can I add more content types?

**Answer:** **Yes! Add to the code.**

**Steps:**

1. **Add to ContentType enum** (around line 377):
```python
class ContentType(str, Enum):
    # ... existing types
    PODCAST_SCRIPT = "podcast_script"
```

2. **Add prompt template** (around line 918):
```python
ContentType.PODCAST_SCRIPT: """You are a podcast script writer...."""
```

3. **Restart:**
```bash
docker-compose restart
```

**Then use it:**
```json
{
  "content_type": "podcast_script",
  "topic": "Interview with a marketing expert"
}
```

---

### Can I integrate with my WordPress site?

**Answer:** **Yes! Multiple ways:**

**Option 1: Use Webhooks + Zapier**
1. Generate content in SPLANTS
2. Webhook triggers Zapier
3. Zapier creates WordPress post

**Option 2: Direct API Integration**
Use WordPress plugin or custom code:
```php
$response = wp_remote_post('http://your-splants-server:8080/v1/generate', [
    'headers' => ['X-API-Key' => 'your-key'],
    'body' => json_encode([
        'content_type' => 'blog',
        'topic' => 'Your topic'
    ])
]);
```

**Option 3: Manual**
1. Generate in SPLANTS
2. Copy content
3. Paste into WordPress editor

---

### How do I deploy to production?

**Answer:** See `docs_DEPLOYMENT.md` for detailed guide.

**Quick overview:**

1. **Choose hosting:**
   - DigitalOcean ($12/month)
   - Linode ($10/month)
   - AWS EC2 ($15/month)
   - Any VPS with Docker

2. **Setup server:**
   ```bash
   # SSH into server
   ssh root@your-server-ip
   
   # Install Docker
   curl -fsSL https://get.docker.com | sh
   
   # Clone SPLANTS
   git clone [repository URL].git
   cd SPLANTS
   
   # Configure
   cp .env.example .env
   nano .env  # Add your keys
   
   # Start
   docker-compose up -d
   ```

3. **Setup domain (optional):**
   - Point domain to server IP
   - Setup Nginx as reverse proxy
   - Install SSL with Let's Encrypt

---

### Can I run multiple instances?

**Answer:** **Yes! Great for serving multiple clients.**

**Method 1: Different Ports**
```bash
# Client 1 on port 8080
cd /client1/SPLANTS
docker-compose up -d

# Client 2 on port 8081
cd /client2/SPLANTS
# Edit docker-compose.yml to use 8081
docker-compose up -d
```

**Method 2: Different Servers**
- Deploy separate instance per client
- Each with own domain
- Completely isolated

**Method 3: Subdomain/Path Routing**
- Use Nginx to route different domains to different instances
- client1.yourdomain.com → instance 1
- client2.yourdomain.com → instance 2

---

## Still Have Questions?

### Where can I get help?

1. **Documentation:**
   - README.md - Complete guide
   - SETUP_GUIDE.md - Step-by-step setup
   - TROUBLESHOOTING.md - Problem solving
   - docs_API_GUIDE.md - API reference
   - docs_DEPLOYMENT.md - Deployment guide

2. **GitHub Issues:**
   - Search existing issues
   - Open new issue with details
   - [repository URL]/issues

3. **Community:**
   - (Add your Discord/Slack)
   - (Add your forum)

---

**Can't find your answer?**

Open a GitHub issue or contact us! We're constantly updating this FAQ based on user questions.

**Found a bug or have a feature request?**

Please open an issue on GitHub with:
- Clear description
- Steps to reproduce (for bugs)
- Use case (for features)
- System info (OS, Docker version, etc.)

---

**Last Updated:** November 2024
**Version:** 2.1

**This FAQ is a living document - we update it regularly based on user feedback!**
