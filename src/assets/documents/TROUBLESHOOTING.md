# SPLANTS Marketing Engine - Troubleshooting Guide

## Problem-Solving Reference

This guide provides solutions to common system issues. Locate the relevant problem category and follow the provided steps.

---

## Quick Diagnostic Checklist

Verify these basic requirements before proceeding to specific problem categories:

- [ ] Docker service is running
- [ ] Services status: Run `docker-compose ps`
- [ ] System initialization: Wait 60 seconds after starting
- [ ] Configuration file (`.env`) is properly configured
- [ ] Network connectivity is established

---

## Table of Contents

1. [Installation Problems](#installation-problems)
2. [Docker Issues](#docker-issues)
3. [API Connection Problems](#api-connection-problems)
4. [Authentication Errors](#authentication-errors)
5. [Content Generation Failures](#content-generation-failures)
6. [Database Problems](#database-problems)
7. [Performance Issues](#performance-issues)
8. [Cost/Billing Issues](#costbilling-issues)
9. [Configuration Problems](#configuration-problems)
10. [Advanced Troubleshooting](#advanced-troubleshooting)

---

## Installation Problems

### Problem: "Docker is not installed"

**Symptoms:**
```
docker: command not found
```
Or: "Docker Desktop is not running"

**Solutions:**

**Check if Docker is Actually Installed:**
```bash
# Windows (Command Prompt)
docker --version

# Mac/Linux (Terminal)
docker --version
```

**If you see a version number:**
- Docker IS installed
- It's just not running
- Start Docker Desktop application

**If you see "command not found":**
- Docker is NOT installed
- Follow installation guide in README.md
- Restart computer after installation

**Windows Specific:**
- Check for whale icon in system tray (bottom-right)
- Right-click tray, find Docker
- If not there, search Start Menu for "Docker Desktop"
- Click to start it

**Mac Specific:**
- Check menu bar (top-right) for whale icon
- If not there, open Applications → Docker
- Wait for whale icon to appear

**Linux Specific:**
```bash
# Check if Docker service is running
sudo systemctl status docker

# If not running, start it
sudo systemctl start docker
sudo systemctl enable docker

# Add yourself to docker group
sudo usermod -aG docker $USER

# Logout and login again (or reboot)
```

---

### Problem: "Permission denied" (Linux)

**Symptoms:**
```
Got permission denied while trying to connect to the Docker daemon socket
```

**Solution:**
```bash
# Add your user to docker group
sudo usermod -aG docker $USER

# Logout and login again (important!)
# Or reboot your computer

# Verify it worked
docker ps
```

**Why this happens:**
- Docker requires special permissions
- Adding to 'docker' group gives you those permissions
- Must logout/login for changes to take effect

---

### Problem: Docker Desktop won't start (Windows)

**Symptoms:**
- Docker Desktop crashes on startup
- Error: "WSL 2 installation is incomplete"
- Error: "Hyper-V is not enabled"

**Solution 1: Install WSL 2 Kernel**

1. Download WSL 2 kernel: https://aka.ms/wsl2kernel
2. Run the installer
3. Restart Docker Desktop

**Solution 2: Enable Hyper-V (Windows Pro/Enterprise/Education)**

1. Open Control Panel
2. Programs → Turn Windows features on or off
3. Check these boxes:
   -  Hyper-V
   -  Windows Subsystem for Linux
   -  Virtual Machine Platform
4. Click OK
5. Restart computer
6. Start Docker Desktop

**Solution 3: Enable Virtualization in BIOS**

1. Restart computer
2. Enter BIOS (usually F2, F10, F12, or Del key during startup)
3. Find "Virtualization" setting (might be called):
   - Intel VT-x
   - AMD-V
   - Virtualization Technology
4. Enable it
5. Save and exit BIOS
6. Start Docker Desktop

**Solution 4: Windows Home Users**

Windows Home doesn't support Hyper-V, but Docker can use WSL 2:

1. Install WSL 2: https://aka.ms/wsl2kernel
2. Docker Desktop will use WSL 2 backend automatically
3. If problems persist, upgrade to Windows Pro (or use Linux)

---

## Docker Issues

### Problem: "Cannot connect to Docker daemon"

**Symptoms:**
```
Error response from daemon: dial unix docker.raw.sock: connect: no such file or directory
```

**Solutions:**

**Solution 1: Start Docker**
- Open Docker Desktop application
- Wait for whale icon to appear
- Try your command again

**Solution 2: Restart Docker**
```bash
# Stop Docker Desktop completely
# Then start it again

# On Linux:
sudo systemctl restart docker
```

**Solution 3: Check Docker is Responding**
```bash
docker ps
```

If this works, Docker is fine!

---

### Problem: "Port is already allocated"

**Symptoms:**
```
Error: Bind for 0.0.0.0:8080 failed: port is already allocated
```

**Meaning:**
- Something else is using port 8080
- Could be another application or old SPLANTS instance

**Solution 1: Stop Old Instance**
```bash
docker-compose down
docker-compose up -d
```

**Solution 2: Find What's Using Port 8080**

**Windows:**
```bash
netstat -ano | findstr :8080
```
You'll see a number (PID) at the end. Then:
```bash
taskkill /PID [number] /F
```

**Mac/Linux:**
```bash
lsof -i :8080
```
You'll see a process. Then:
```bash
kill -9 [PID]
```

**Solution 3: Use Different Port**

Edit `docker-compose.yml`:
```yaml
ports:
  - "8081:8080"  # Changed from 8080:8080
```

Then access at: `http://localhost:8081`

---

### Problem: "docker-compose: command not found"

**Symptoms:**
```
docker-compose: command not found
```

**Solutions:**

**Solution 1: Use docker compose (no dash)**

Newer Docker versions use `docker compose` instead:
```bash
docker compose up -d
docker compose down
docker compose ps
```

**Solution 2: Install docker-compose**

**Mac with Homebrew:**
```bash
brew install docker-compose
```

**Linux:**
```bash
sudo apt install docker-compose
```

**Windows:**
- docker-compose should come with Docker Desktop
- If not, reinstall Docker Desktop

---

## API Connection Problems

### Problem: "This site can't be reached" (localhost:8080)

**Symptoms:**
- Browser shows "This site can't be reached"
- Or "ERR_CONNECTION_REFUSED"
- Cannot access http://localhost:8080

**Diagnostic Steps:**

**Step 1: Is SPLANTS Running?**
```bash
docker-compose ps
```

**Expected output:**
```
Name                State    Ports
splants_app_1       Up       0.0.0.0:8080->8080/tcp
splants_db_1        Up       5432/tcp
```

**If "State" column doesn't say "Up":**
```bash
docker-compose up -d
# Wait 60 seconds
docker-compose ps
```

**Step 2: Check Application Logs**
```bash
docker-compose logs -f app
```

**Look for:**
-  "SPLANTS Marketing Engine Ready!"
-  "Application startup complete"
-  Any error messages in red

**Step 3: Is Database Connected?**

In logs, look for:
```
 Database connected successfully
```

If you see:
```
 Database connection failed
```
See [Database Problems](#database-problems) section.

**Step 4: Wait Longer**
- Services need 30-90 seconds to fully start
- Especially first time (need to initialize database)
- Be patient!

**Step 5: Try Health Check**

Instead of main page, try:
```
http://localhost:8080/health
```

If this works but main page doesn't, it's a browser cache issue.

**Step 6: Clear Browser Cache**

- Press Ctrl+Shift+R (Windows/Linux)
- Or Cmd+Shift+R (Mac)
- Or try different browser

**Step 7: Check Firewall**

**Windows:**
- Open Windows Defender Firewall
- Click "Allow an app through firewall"
- Make sure Docker Desktop is allowed
- For both Private and Public networks

**Mac:**
- System Preferences → Security & Privacy → Firewall
- If firewall is on, click "Firewall Options"
- Make sure Docker is allowed

---

### Problem: "504 Gateway Timeout"

**Symptoms:**
- Request times out after 60 seconds
- Error: "504 Gateway Timeout"

**Causes:**
1. Content generation is taking too long
2. System is overloaded
3. Network problems

**Solutions:**

**Solution 1: Reduce Content Length**
```json
{
  "length": 300  // Instead of 2000
}
```

**Solution 2: Don't Use Premium Mode**
```json
{
  "use_premium": false
}
```

**Solution 3: Check OpenAI Status**
- Go to: https://status.openai.com
- Check if there are outages

**Solution 4: Restart Services**
```bash
docker-compose restart
```

**Solution 5: Check System Resources**
```bash
docker stats
```

If CPU or Memory is at 100%, you might need:
- More RAM
- Faster computer
- To deploy to a server

---

## Authentication Errors

### Problem: "Invalid API Key" (403 error)

**Symptoms:**
```json
{
  "error": "Invalid API Key. Please check your X-API-Key header.",
  "status_code": 403
}
```

**Solutions:**

**Solution 1: Check .env File**
```bash
cat .env | grep ^API_KEY=
```

**Should show:**
```
API_KEY=your-actual-password
```

**Common mistakes:**
-  Still using default: `change-this-to-a-secure-password-123`
-  Extra spaces: `API_KEY= mypassword` (space after =)
-  Quotes: `API_KEY="mypassword"` (shouldn't have quotes)
-  Comments: `# API_KEY=mypassword` (shouldn't be commented out)

**Solution 2: Restart After Changing**
```bash
docker-compose restart app
```

**Solution 3: Check Your Request**

**Using web interface (localhost:8080/docs):**
1. Click "Authorize" button (🔓 icon)
2. Enter your API_KEY value
3. Click "Authorize"
4. Try request again

**Using cURL or code:**

Make sure you're including the header:
```bash
-H "X-API-Key: your-actual-password"
```

**Full example:**
```bash
curl -X POST "http://localhost:8080/v1/generate" \
  -H "X-API-Key: MyBusinessMarketing2024" \
  -H "Content-Type: application/json" \
  -d '{"content_type":"blog","topic":"Test"}'
```

---

### Problem: "OpenAI API key not configured"

**Symptoms:**
```
CRITICAL: OPENAI_API_KEY not set!
Content generation will not function properly.
```

**Solutions:**

**Solution 1: Check .env File**
```bash
cat .env | grep ^OPENAI_API_KEY=
```

**Should show:**
```
OPENAI_API_KEY=sk-proj-abc123...
```

**Common mistakes:**
-  Still placeholder: `OPENAI_API_KEY=sk-your-api-key-here`
-  Missing entirely
-  Commented out: `# OPENAI_API_KEY=...`
-  Extra spaces or quotes

**Solution 2: Get New API Key**

1. Go to: https://platform.openai.com/api-keys
2. Create new secret key
3. Copy it completely (starts with `sk-`)
4. Add to `.env` file:
   ```env
   OPENAI_API_KEY=sk-proj-your-actual-key-here
   ```
5. Save file
6. Restart:
   ```bash
   docker-compose restart app
   ```

**Solution 3: Verify in System Status**

Go to: http://localhost:8080/v1/system/status

Look for:
```json
{
  "services": {
    "ai_models": {
      "gpt4": {
        "status": "available"  // Should be "available", not "not_configured"
      }
    }
  }
}
```

---

## Content Generation Failures

### Problem: "Content generation failed" (500 error)

**Symptoms:**
```json
{
  "error": "Content generation failed: [error message]"
}
```

**Diagnostic Steps:**

**Step 1: Check Error Message**

The error message usually tells you exactly what's wrong. Common ones:

**"insufficient_quota":**
- You're out of OpenAI credits
- Solution: Add credits at https://platform.openai.com/account/billing

**"invalid_api_key":**
- OpenAI API key is wrong
- Solution: Get new key, update .env, restart

**"rate_limit_exceeded":**
- Too many requests too fast
- Solution: Wait 60 seconds, try again

**"model_not_found":**
- Trying to use a model you don't have access to
- Solution: Stick with default (gpt-4-turbo-preview)

**Step 2: Check OpenAI Account**

1. Go to: https://platform.openai.com/account/billing/overview
2. Check:
   -  Do you have credits remaining?
   -  Is your payment method valid?
   -  Did you set usage limits that block all requests?

**Step 3: Test OpenAI API Directly**

```bash
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer YOUR_OPENAI_API_KEY"
```

If this fails, problem is with OpenAI account/key, not SPLANTS.

**Step 4: Check Application Logs**

```bash
docker-compose logs -f app | grep -i error
```

Look for detailed error messages.

**Step 5: Try Simple Request**

Use minimal request to isolate problem:

```json
{
  "content_type": "blog",
  "topic": "Test",
  "length": 100
}
```

If this works, problem might be with your specific request parameters.

---

### Problem: "Monthly budget exceeded" (402 error)

**Symptoms:**
```json
{
  "detail": "Monthly budget of $50 would be exceeded. Current usage: $49.87",
  "status_code": 402
}
```

**This is actually WORKING AS INTENDED!**

The system is protecting you from overspending.

**Solutions:**

**Solution 1: Increase Budget**

Edit `.env`:
```env
MONTHLY_AI_BUDGET=100  # Increased from 50
```

Restart:
```bash
docker-compose restart app
```

**Solution 2: Wait for Next Month**

The budget resets on the 1st of each month.

**Solution 3: Check Current Usage**

Go to: http://localhost:8080/v1/costs/usage

See how much you've actually spent and when it resets.

**Solution 4: Disable Budget (Not Recommended)**

```env
MONTHLY_AI_BUDGET=0  # 0 = unlimited
```

 **Warning:** You could accidentally spend a lot!

---

### Problem: Content quality is low

**Symptoms:**
- Quality score below 0.5
- Content doesn't make sense
- Wrong tone or style
- Missing keywords

**Solutions:**

**Solution 1: Be More Specific**

Bad request:
```json
{
  "topic": "marketing"
}
```

Good request:
```json
{
  "topic": "5 social media marketing strategies that small businesses can implement in under 2 hours per week to increase engagement by 50%",
  "keywords": ["social media", "marketing strategies", "small business", "engagement"],
  "target_audience": "Small business owners who are busy and need practical, actionable advice",
  "tone": "professional"
}
```

**Solution 2: Use Appropriate Length**

- Too short (< 100 words): Often low quality
- Too long (> 2000 words): Can become unfocused

**Recommended:**
- Blog posts: 500-1500 words
- Social media: 50-200 words
- Emails: 200-500 words

**Solution 3: Try Premium Mode**

```json
{
  "use_premium": true
}
```

This uses GPT-4 + Claude for 20-30% better quality.
Cost: +$0.02-0.05 per request

**Solution 4: Regenerate**

Sometimes you just get a "bad roll". Generate again!

**Solution 5: Use Templates**

Templates provide proven structures:

1. Get templates: http://localhost:8080/v1/templates
2. Choose one (e.g., "blog_listicle")
3. Generate using template

---

## Database Problems

### Problem: "Database connection failed"

**Symptoms:**
```
 Database connection failed: connection refused
```

**Solutions:**

**Solution 1: Check Database is Running**
```bash
docker-compose ps db
```

**Should see:**
```
Name             State    Ports
splants_db_1     Up       5432/tcp
```

**If not "Up":**
```bash
docker-compose up -d db
# Wait 30 seconds
docker-compose ps db
```

**Solution 2: Check Database Logs**
```bash
docker-compose logs db
```

Look for:
```
database system is ready to accept connections
```

**Solution 3: Wait Longer**

Database takes 20-30 seconds to start, especially first time.

**Solution 4: Restart Everything**
```bash
docker-compose down
docker-compose up -d
# Wait 60 seconds
docker-compose ps
```

**Solution 5: Check DATABASE_URL**

In `.env`:
```env
DATABASE_URL=postgresql://splants:password@db:5432/splants
```

This should be **exactly** as shown above if using Docker Compose.

---

### Problem: "Database initialization failed"

**Symptoms:**
```
Error creating tables
Failed to initialize database
```

**Solution: Reset Database**

 **Warning:** This deletes all content!

```bash
# Stop everything
docker-compose down

# Delete database volume
docker-compose down -v

# Start fresh
docker-compose up -d

# Wait 60 seconds
docker-compose logs -f app
```

Look for:
```
 Database tables initialized
```

---

### Problem: "Too many database connections"

**Symptoms:**
```
FATAL: sorry, too many clients already
```

**Causes:**
- Multiple SPLANTS instances running
- Old connections not closed
- System overload

**Solutions:**

**Solution 1: Restart Database**
```bash
docker-compose restart db
```

**Solution 2: Stop Old Instances**
```bash
docker-compose down
docker-compose up -d
```

**Solution 3: Check for Multiple Instances**
```bash
docker ps -a | grep splants
```

Stop any old ones:
```bash
docker stop [container_id]
docker rm [container_id]
```

---

## Performance Issues

### Problem: System is slow

**Symptoms:**
- Content generation takes > 60 seconds
- API responses are delayed
- System feels sluggish

**Diagnostic:**

**Check Resource Usage:**
```bash
docker stats
```

Look at:
- **CPU %**: Should be < 80%
- **MEM USAGE**: Should have headroom
- **NET I/O**: Shows network activity

**Solutions:**

**Solution 1: Reduce Content Length**
```json
{
  "length": 500  // Instead of 2000
}
```

**Solution 2: Don't Use Premium Mode**
```json
{
  "use_premium": false
}
```

**Solution 3: Enable Redis Caching**

Reduces repeat requests by 30-50%:

1. Edit `docker-compose.yml`
2. Uncomment Redis service
3. Add to `.env`:
   ```env
   REDIS_URL=redis://redis:6379
   ```
4. Restart:
   ```bash
   docker-compose down
   docker-compose up -d
   ```

**Solution 4: Check Internet Speed**

Run speed test: https://fast.com

OpenAI requires decent connection. Minimum 5 Mbps recommended.

**Solution 5: Deploy to Server**

If your computer is too slow, deploy to a VPS.
See `docs_DEPLOYMENT.md`

---

### Problem: High CPU usage

**Symptoms:**
```bash
docker stats
# Shows 90-100% CPU
```

**Solutions:**

**Solution 1: Close Other Applications**
- Free up CPU for SPLANTS
- Especially browsers with many tabs

**Solution 2: Restart Services**
```bash
docker-compose restart
```

**Solution 3: Limit Concurrent Requests**

Don't generate multiple pieces at once.
Wait for one to finish before starting next.

**Solution 4: Deploy to Better Hardware**

Minimum recommended:
- 2 CPU cores
- 4GB RAM
- 10GB disk space

---

### Problem: Running out of disk space

**Symptoms:**
```
no space left on device
```

**Check Space:**
```bash
# Windows
wmic logicaldisk get size,freespace,caption

# Mac/Linux
df -h
```

**Solutions:**

**Solution 1: Clean Docker**
```bash
# Remove unused containers, images, volumes
docker system prune -a

# When asked "Are you sure?", type: y
```

 This removes ALL unused Docker data (not just SPLANTS).

**Solution 2: Clean Old Backups**

If you have many backups:
```bash
# Delete backups older than 30 days
find backups/ -name "*.sql.gz" -mtime +30 -delete
```

**Solution 3: Move Database to External Drive**

Advanced - see Docker volume documentation.

---

## Cost/Billing Issues

### Problem: Costs higher than expected

**Symptoms:**
- OpenAI bill is $100 when you expected $20
- Cost tracking shows high usage

**Diagnostic:**

**Check Your Usage:**

Go to: http://localhost:8080/v1/costs/usage

See:
- Total monthly cost
- Cost per piece
- Which days had high usage

**Common Causes:**

1. **Generating very long content**
   - Solution: Reduce `length` parameter

2. **Using premium mode often**
   - Solution: Use only when quality is critical

3. **Regenerating content many times**
   - Solution: Get it right first time with good prompts

4. **Daily limit not set**
   - Solution: Set `DAILY_API_LIMIT` in .env

5. **No budget control**
   - Solution: Set `MONTHLY_AI_BUDGET` in .env

**Solutions:**

**Solution 1: Enable Cost Controls**

Edit `.env`:
```env
MONTHLY_AI_BUDGET=50      # Stop at $50/month
DAILY_API_LIMIT=100       # Max 100 requests/day
```

**Solution 2: Enable Redis Caching**

Saves 30-50% on costs:
- See Performance Issues section
- Uncomment Redis in docker-compose.yml

**Solution 3: Use GPT-3.5 Instead**

Edit `main.py` line ~793:
```python
model="gpt-3.5-turbo",  # Instead of gpt-4-turbo-preview
```

Cost drops 90%, but quality drops too.

**Solution 4: Monitor Daily**

Check costs daily:
```
http://localhost:8080/v1/costs/usage
```

**Solution 5: Set OpenAI Limits**

Go to: https://platform.openai.com/account/billing/limits

Set hard limits on OpenAI's side too.

---

### Problem: "Insufficient quota" error

**Symptoms:**
```
Error: You exceeded your current quota
```

**Meaning:**
You're out of OpenAI credits!

**Solution:**

1. Go to: https://platform.openai.com/account/billing/overview
2. Click "Add to credit balance"
3. Add $20-50 (or your budget)
4. Wait 2-3 minutes for it to register
5. Try generating content again

**Prevention:**

Set up auto-recharge:
- https://platform.openai.com/account/billing/payment-methods
- Enable "Automatic recharge"
- Set threshold and amount

---

## Configuration Problems

### Problem: ".env file not found"

**Symptoms:**
```
.env file not found
Using default configuration
```

**Solution:**

**Windows:**
1. Make sure file is named exactly `.env` (not `.env.txt`)
2. In File Explorer, click "View" tab
3. Check "File name extensions"
4. Rename if needed

**Mac:**
1. File must be named `.env` (starts with dot)
2. Press `Cmd + Shift + .` in Finder to show hidden files
3. Make sure file is there

**Linux:**
```bash
ls -la .env
```

If missing:
```bash
cp .env.example .env
nano .env  # Edit it
```

---

### Problem: Changes to .env not taking effect

**Symptoms:**
- You edit .env
- Save it
- But system still uses old values

**Solution:**

**ALWAYS restart after changing .env:**
```bash
docker-compose restart app
```

Or full restart:
```bash
docker-compose down
docker-compose up -d
```

---

### Problem: "Invalid environment variable"

**Symptoms:**
```
Error: Invalid value for MONTHLY_AI_BUDGET
```

**Solutions:**

**Check Data Types:**

```env
#  CORRECT
MONTHLY_AI_BUDGET=50
DAILY_API_LIMIT=100

#  WRONG
MONTHLY_AI_BUDGET=$50
DAILY_API_LIMIT=100 requests
MONTHLY_AI_BUDGET=fifty dollars
```

**No quotes needed:**
```env
#  CORRECT
API_KEY=MyPassword123

#  WRONG
API_KEY="MyPassword123"
API_KEY='MyPassword123'
```

**No spaces around =:**
```env
#  CORRECT
API_KEY=value

#  WRONG
API_KEY = value
API_KEY= value
```

---

## Advanced Troubleshooting

### Viewing Detailed Logs

**See All Logs:**
```bash
docker-compose logs -f
```

**See Only Application Logs:**
```bash
docker-compose logs -f app
```

**See Only Database Logs:**
```bash
docker-compose logs -f db
```

**See Last 100 Lines:**
```bash
docker-compose logs --tail=100 app
```

**Save Logs to File:**
```bash
docker-compose logs app > logs.txt
```

---

### Getting Into Containers

**Access Application Container:**
```bash
docker-compose exec app /bin/sh
```

**Access Database Container:**
```bash
docker-compose exec db /bin/sh
```

**Run Database Queries:**
```bash
docker-compose exec db psql -U splants splants
```

Then you can run SQL:
```sql
SELECT COUNT(*) FROM content;
SELECT * FROM content LIMIT 5;
```

Type `\q` to exit.

---

### Complete Reset (Nuclear Option)

 **Warning:** This deletes EVERYTHING!

```bash
# Stop and remove everything
docker-compose down -v

# Remove all Docker images
docker system prune -a

# Start fresh
docker-compose up -d
```

Use this only as last resort!

---

### Checking System Health

**Quick Health Check:**
```
http://localhost:8080/health
```

**Detailed System Status:**
```
http://localhost:8080/v1/system/status
```

**Detailed Health:**
```
http://localhost:8080/v1/system/health/detailed
```

---

### Testing Individual Components

**Test Database:**
```bash
docker-compose exec db pg_isready -U splants
```

Should say: "accepting connections"

**Test OpenAI Connection:**
```bash
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer YOUR_OPENAI_API_KEY"
```

Should return list of models.

**Test Full API:**
```bash
python test_api.py
```

Should run 10 tests, all passing.

---

## Still Having Problems?

### Before Asking for Help

Gather this information:

1. **Your Setup:**
   - Operating system (Windows/Mac/Linux)
   - Docker version: `docker --version`
   - SPLANTS version (from README)

2. **What You're Trying to Do:**
   - Specific steps you're following
   - What you expect to happen

3. **What's Happening Instead:**
   - Exact error messages
   - Screenshots if possible

4. **What You've Tried:**
   - Which solutions from this guide
   - Any other troubleshooting steps

5. **Logs:**
   ```bash
   docker-compose logs app > logs.txt
   ```

### Where to Get Help

1. **Check Documentation:**
   - README.md - Full documentation
   - SETUP_GUIDE.md - Step-by-step setup
   - docs_API_GUIDE.md - API reference
   - docs_DEPLOYMENT.md - Deployment guide

2. **GitHub Issues:**
   - [repository URL]/issues
   - Search existing issues first
   - Create new issue with information above

3. **Community:**
   - (Add Discord/Slack links)
   - (Add forum links)

---

## Prevention Tips

### Avoid Problems Before They Happen

**1. Regular Backups:**
```bash
# Run weekly
./scripts_backup.sh
```

**2. Monitor Costs:**
```bash
# Check daily
curl http://localhost:8080/v1/costs/usage
```

**3. Keep Docker Updated:**
- Update Docker Desktop monthly
- Check for new SPLANTS versions

**4. Set Limits:**
```env
MONTHLY_AI_BUDGET=50
DAILY_API_LIMIT=100
```

**5. Use Version Control:**
```bash
# Save your .env file (securely!)
# Track your customizations
git commit -m "My custom setup"
```

**6. Document Your Setup:**
- Keep notes on what you changed
- Save your API keys securely
- Document any custom configurations

---

**Remember:** Most problems are simple configuration issues. Take a deep breath, read error messages carefully, and work through solutions systematically!

** Pro Tip:** When in doubt, restart:
```bash
docker-compose restart
```

This fixes 80% of issues! 😊
