# 📋 KB Rewaq Digital — Daily Operations Plan

**Owner:** Faizan (co-founder) + AI Co-Founder (automation engine)  
**Location:** Kuwait  
**Brand:** KB Rewaq Digital (WA +965 50703252)  
**Pricing:** Starter 35 KWD | Growth 95 KWD | Monthly 55 KWD  
**Market:** Kuwait salons/beauty + bilingual EN/العربية  
**No cloud APIs.** All local/offline automation.

---

## 🗓️ Daily Workflow (Mon–Sat)

### 🌅 Morning (8:00–9:00 AM)
| Step | Action | Who |
|------|--------|-----|
| 1 | Open `crm.json` → check yesterday's leads status | AI |
| 2 | Web-research 3–5 new Kuwait salon leads (name, phone, area, language) | AI |
| 3 | Add new leads to `leads.js` + `crm.json` | AI |
| 4 | Generate `outreach_report.html` via `node outreach.js` | AI |
| 5 | Print first 3 pending leads + wa.me links for manual sending | Console |

### 📱 Mid-Morning (9:00–10:00 AM)
| Step | Action | Who |
|------|--------|-----|
| 6 | Open Chrome → outreach_report.html → click "Send →" for lead 1 | Faizan |
| 7 | Wait 45s → click Send for lead 2 | Faizan |
| 8 | Wait 45s → click Send for lead 3 | Faizan |
| 9 | AI updates `sent.json` + `crm.json` with "contacted" status | Auto |

### 📊 Late Morning (10:00–11:00 AM)
| Step | Action | Who |
|------|--------|-----|
| 10 | Check `crm.json` for any replies from yesterday | AI |
| 11 | If reply found → generate human-style response via REPLIES | AI draft |
| 12 | Draft goes to console → Faizan reviews & sends | Faizan |
| 13 | Update lead status in CRM (replied → negotiating → won) | Manual flag |

### 📸 Social Media (11:00 AM)
| Step | Action | Who |
|------|--------|-----|
| 14 | Generate Instagram caption + hashtag set for today's post | AI |
| 15 | Generate Twitter/X post (short version) | AI |
| 16 | Draft saved to `social_drafts/` → Faizan posts from real accounts | Faizan |
| 17 | Post 3x/week (Mon/Wed/Fri) — rest days: stories only | Schedule |

### 🕐 Afternoon (2:00–4:00 PM)
| Step | Action | Who |
|------|--------|-----|
| 18 | Second outreach batch (3 more leads) | Same as morning |
| 19 | Follow up on leads who got replies but no deal yet | AI draft → Faizan |
| 20 | Check email drafts for pending cold outreach | AI |

### 📧 Email (3:00–3:30 PM)
| Step | Action | Who |
|------|--------|-----|
| 21 | Generate 2 cold outreach email drafts (salon owners) | AI |
| 22 | Save to `email_drafts/` with subject + body | Auto |
| 23 | Faizan copies from drafts → sends via his Gmail | Faizan |

### 📋 Evening (5:00–6:00 PM)
| Step | Action | Who |
|------|--------|-----|
| 24 | Generate daily report (`daily_report.md`) | AI |
| 25 | Print to console: leads contacted, replies received, deals progress | Console |
| 26 | Update `crm.json` with any status changes | AI |
| 27 | Prepare tomorrow's first 3 leads | AI |

---

## 🤖 Automation Tools (All Local)

### WhatsApp Outreach
- **`outreach.js`** → generates `outreach_report.html` with wa.me links
- **`wa-control.js`** → command processor for status tracking
- **`command.txt`** → edit here to log replies/status updates
- **No browser launch needed** — your logged-in Chrome handles WhatsApp

### CRM System
- **`crm.json`** → all lead data, status, history, notes
- **`sent.json`** → tracks which phones got messages
- **Auto-update** on every command.txt entry

### Social Media
- **`social_drafts/`** → Instagram + Twitter captions auto-generated
- **Content calendar** → 3 posts/week per platform
- **Hashtag bank** → Kuwait/beauty/salon Arabic + English hashtags

### Email
- **`email_drafts/`** → cold outreach drafts (2/day)
- **Template bank** → Starter pitch, Growth pitch, Follow-up, Welcome

### Reports
- **`daily_report.md`** → auto-generated every evening at 5PM
- **Weekly summary** → every Sunday: leads contacted, replies, deals closed, revenue

---

## 📊 Weekly Automation Schedule

| Day | Special Task |
|-----|-------------|
| **Monday** | Week planner: assign 15 outreach targets for the week |
| **Wednesday** | Mid-week report: halfway check + adjust targets |
| **Friday** | Week close: deals summary + revenue tracking |
| **Saturday** | Social media week review + content planning for next week |
| **Sunday** | Lead research batch: find 10+ new salon contacts |

---

## 💰 Revenue Tracking (in CRM)

```
CRM Status Flow:
lead → contacted → replied → negotiating → quoted → won → paid

Each stage:
- lead = new, no outreach yet
- contacted = message sent
- replied = they responded
- negotiating = discussing scope/price
- quoted = proposal sent (35 or 95 KWD)
- won = they said yes
- paid = 50% advance received
```

---

## 🔧 Daily Commands (Edit command.txt)

```
# Track a reply:
STATUS 96566339766 replied

# Move to negotiation:
STATUS 96566339766 negotiating

# Deal won:
STATUS 96566339766 won

# Payment received:
STATUS 96566339766 paid

# Manual send (if needed):
SEND 96566339766 Custom message here

# Reply tracking:
REPLY 96566339766 Thank you for your interest!

# Read recent messages from a lead:
READ 96566339766
```

---

## 📈 Monthly Targets

| Metric | Monthly Target |
|--------|---------------|
| Leads contacted | 50+ |
| Replies received | 15-20 |
| Proposals sent | 8-10 |
| Deals closed | 3-5 |
| Revenue (Starter) | 105-175 KWD |
| Revenue (Growth) | 285-475 KWD |
| Social posts | 12 (3/week) |
| Emails sent | 40+ (2/day × 20 working days) |

---

## 🚀 Next Steps (Immediate)

1. **Today:** Open `outreach_report.html` in Chrome → send first 3 leads
2. **This week:** Set up `command.txt` tracking for any replies
3. **This week:** Generate first `daily_report.md` evening report
4. **This month:** Reach 50 leads contacted → 15+ replies → 3-5 deals

---

## ⚡ Quick Start (You Do This)

```
# 1. Open Chrome (already logged into WhatsApp)
# 2. Run this every morning:
cd /d D:\digitalfirst-agency\wa-bot && node outreach.js

# 3. Open outreach_report.html in Chrome
# 4. Click "Send →" for first 3 pending leads (45s gap)
# 5. When replies come, update command.txt with STATUS commands
# 6. Run `node wa-control.js` again to regenerate report
# 7. I print your daily report at 5PM
```

---

*Auto-generated by KB Rewaq Digital AI Co-Founder*  
*All tools local. No cloud APIs. No paid services.*
