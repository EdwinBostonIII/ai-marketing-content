# SPLANTS Quick Start - Windows Users

## Windows 10/11 Setup Guide

This guide provides setup instructions for Windows 10/11 systems. Follow the documented steps in sequence.

---

## Prerequisites

Required components:
- [ ] Windows 10 or Windows 11 (64-bit)
- [ ] Internet connection
- [ ] Approximately 15 minutes for setup
- [ ] OpenAI account with credit ($20 recommended initial amount)

---

## Step 1: Install Docker Desktop (5 minutes)

### Docker Overview
Docker is a containerization platform that provides the runtime environment for SPLANTS. This is a one-time installation.

### Download Docker

1. Access web browser (Edge, Chrome, or Firefox)
2. Navigate to: https://www.docker.com/products/docker-desktop
3. Select "Download for Windows"
4. File size: approximately 500MB (download time varies by connection speed)

### Install Docker

1. Locate downloaded file in `Downloads` folder
   - File name: `Docker Desktop Installer.exe`
2. Execute the installer file
3. Grant administrator permission when prompted
4. Follow installation wizard:
   - Select "OK" to begin installation
   - Wait 5-10 minutes for installation completion
   - Select "Close and restart" when prompted
5. Restart computer

### Start Docker

1. After system restart, Docker Desktop should launch automatically
2. Verify Docker status by checking system tray (bottom-right corner)
3. Docker whale icon indicates active status
4. If icon is not visible:
   - Open Start menu
   - Search for "Docker Desktop"
   - Click to open it

### Troubleshooting

**If Docker won't start:**
- Enable WSL 2: Download from https://aka.ms/wsl2kernel
- Enable Virtualization: See BIOS instructions in TROUBLESHOOTING.md

**Test Docker:**
1. Press `Windows + R` keys
2. Type `cmd` and press Enter
3. Type: `docker --version`
4. Should show: `Docker version 24.0.6...`

---

## Step 2: Get OpenAI API Key (5 minutes)

### What is this?
A "key" that lets SPLANTS use OpenAI's AI (the same AI that powers ChatGPT).

### Create Account

1. **Go to:** https://platform.openai.com/signup
2. **Sign up** with email or Google account
3. **Verify email** (check inbox, click link)
4. **Add phone number** (required for API access)
5. **Verify phone** with SMS code

### Add Payment

1. **Go to:** https://platform.openai.com/account/billing/overview
2. **Click:** "Add payment method"
3. **Enter:** Credit card details
4. **Click:** "Add payment method"

### Add Credits

1. **Click:** "Add to credit balance"
2. **Enter:** $20 (this generates 600-700 pieces of content)
3. **Click:** "Continue" → "Confirm"

### Create API Key

1. **Go to:** https://platform.openai.com/api-keys
2. **Click:** "Create new secret key"
3. **Name it:** "SPLANTS Marketing Engine"
4. **Click:** "Create secret key"
5. **IMPORTANT:** Copy the key (starts with `sk-`)
   - This is the ONLY time you'll see it!
   - Save in Notepad or somewhere safe
   - Example: `sk-proj-AbC123xyz...`

---

## Step 3: Download SPLANTS (2 minutes)

### Download

1. **Go to:** [repository URL]
2. **Click:** Green "Code" button
3. **Click:** "Download ZIP"
4. **Wait:** File downloads (~1MB)

### Extract

1. **Open File Explorer** (Windows + E)
2. **Go to:** Downloads folder
3. **Find:** `SPLANTS-main.zip`
4. **Right-click** on it
5. **Choose:** "Extract All..."
6. **Click:** "Extract"

### Move to Better Location

1. **In File Explorer,** go to: `C:\Users\YourName\`
2. **Create new folder:** `Projects`
3. **Move** the extracted `SPLANTS-main` folder into `Projects`
4. **Rename** `SPLANTS-main` to just `SPLANTS`

**Final location:** `C:\Users\YourName\Projects\SPLANTS`

---

## Step 4: Configure Settings (3 minutes)

### Create Configuration File

1. **Open File Explorer**
2. **Navigate to:** `C:\Users\YourName\Projects\SPLANTS`
3. **Find file:** `.env.example`
4. **Right-click** it → **Copy**
5. **Right-click** in empty space → **Paste**
6. **Rename** the copy to just `.env`
   - Remove the `.example` part
   - Final name: `.env` (exactly)

**Tip:** Can't see file extensions?
- Click "View" tab in File Explorer
- Check "File name extensions"

### Edit Configuration

1. **Right-click** `.env` file
2. **Choose:** "Open with" → **Notepad**
3. **Find line:** `OPENAI_API_KEY=sk-your-api-key-here`
4. **Replace** `sk-your-api-key-here` with your actual OpenAI key
   - Paste the key you saved earlier
   - Should look like: `OPENAI_API_KEY=sk-proj-AbC123...`
5. **Find line:** `API_KEY=change-this-to-a-secure-password-123`
6. **Change** to a strong password
   - Example: `API_KEY=MyBusiness!Marketing2024`
   - At least 12 characters, mix letters/numbers/symbols
7. **Save file:** File → Save (or Ctrl+S)
8. **Close** Notepad

---

## Step 5: Start SPLANTS (5 minutes)

### Open Command Prompt

1. **Open File Explorer**
2. **Navigate to:** `C:\Users\YourName\Projects\SPLANTS`
3. **Click** in the address bar (top, where it shows the path)
4. **Type:** `cmd` and press Enter
5. **Command Prompt opens** in the SPLANTS folder

### Start the System

**In Command Prompt, type:**

```
docker-compose up -d
```

**Press Enter**

### What You'll See

**First time (5-10 minutes):**
```
Pulling db (postgres:15-alpine)...
Creating splants_db_1 ... done
Creating splants_app_1 ... done
```

This is downloading software (normal, only happens once!)

**Wait for:** Both lines say "done"

### Wait for Startup

**After "done" appears:**
- **Wait 60 seconds**
- Services are initializing
- Be patient!

---

## Step 6: Test It Works!

### Open Web Browser

1. **Open** Chrome, Edge, or Firefox
2. **Go to:** `http://localhost:8080`

### You Should See

A page with system information like:
```json
{
  "name": "SPLANTS Marketing Engine",
  "version": "2.1-SB",
  "status": "operational"
}
```

**If you see this: SUCCESS! **

### Open API Documentation

**Go to:** `http://localhost:8080/docs`

You'll see a beautiful interface with:
- List of features
- "Try it out" buttons
- Examples

**Bookmark this page!** This is your main interface.

---

## Step 7: Generate First Content!

### Authorize

1. **On the API docs page,** find "Authorize" button (🔓 icon, top-right)
2. **Click it**
3. **Enter** your API_KEY (from .env file)
4. **Click** "Authorize"
5. **Click** "Close"

### Generate Content

1. **Scroll down** to: **"POST /v1/generate"**
2. **Click** on it to expand
3. **Click** "Try it out"
4. **You'll see example JSON** - leave it as is for now
5. **Click** "Execute" (blue button at bottom)
6. **Wait** 10-30 seconds
7. **Scroll down** to see your generated content!

** Complete. You just generated AI content!**

---

## Daily Usage

### Starting SPLANTS

**When you want to use SPLANTS:**

1. **Make sure Docker is running** (whale icon in tray)
2. **Open Command Prompt** in SPLANTS folder
3. **Type:** `docker-compose up -d`
4. **Wait** 30-60 seconds
5. **Open browser:** `http://localhost:8080/docs`

### Stopping SPLANTS

**When you're done:**

1. **Open Command Prompt** in SPLANTS folder
2. **Type:** `docker-compose down`
3. **Frees up** computer memory

### Check Status

**Anytime, type:**
```
docker-compose ps
```

Should show "Up" for both services.

### View Logs

**If something goes wrong:**
```
docker-compose logs -f app
```

Press Ctrl+C to exit logs.

---

## Quick Reference

### Important URLs

```
Main API:      http://localhost:8080
API Docs:      http://localhost:8080/docs  👈 Use this!
Health Check:  http://localhost:8080/health
System Status: http://localhost:8080/v1/system/status
```

### Important Commands

```
Start:    docker-compose up -d
Stop:     docker-compose down
Restart:  docker-compose restart
Status:   docker-compose ps
Logs:     docker-compose logs -f app
```

### Important Files

```
.env                  - Your configuration (keep safe!)
docker-compose.yml    - Service definitions
main.py               - Application code
README.md             - Complete documentation
```

---

## Common Problems

### "Can't reach localhost:8080"

**Solution:**
1. Wait 60 seconds after starting
2. Check Docker is running (whale icon)
3. Run: `docker-compose ps` (should say "Up")
4. Try refreshing browser

### "Invalid API Key"

**Solution:**
1. Check .env file has correct API_KEY
2. Make sure you clicked "Authorize" in docs
3. Restart: `docker-compose restart app`

### "Port 8080 is already in use"

**Solution:**
```
netstat -ano | findstr :8080
taskkill /PID [number] /F
docker-compose up -d
```

### "Out of OpenAI credits"

**Solution:**
1. Go to: platform.openai.com/account/billing
2. Add more credit ($20 recommended)
3. Try again in 2-3 minutes

**More problems?** See TROUBLESHOOTING.md

---

## Next Steps

Now that it's working:

1.  **Generate different content types**
   - Blog posts
   - Social media posts
   - Emails
   - Ad copy

2.  **Explore features**
   - Analytics dashboard
   - Content templates
   - Cost tracking
   - A/B testing

3.  **Set up automation**
   - Webhooks for Zapier
   - Scheduled content
   - Backup routine

4.  **Read documentation**
   - README.md - Complete guide
   - FAQ.md - 100+ questions answered
   - TROUBLESHOOTING.md - Problem solving

---

## Getting Help

**Documentation:**
- README.md - Complete guide
- SETUP_GUIDE.md - Detailed setup
- TROUBLESHOOTING.md - Solutions
- FAQ.md - Common questions

**Need More Help?**
- GitHub Issues: [repository URL]/issues
- Include: Windows version, error messages, screenshots

---

** Configuration complete. Welcome to AI-powered marketing automation!**

**Remember:** You now have a tool worth thousands of dollars that costs only $35-80/month. Use it well!

**Pro Tip:** Bookmark `http://localhost:8080/docs` - you'll use it daily!
