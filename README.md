# startup-launch-checker
🚀 Startup Launch Readiness Checker
A free CLI tool that audits your startup's website before launch day — so you don't go live with broken meta tags, missing sitemaps, or slow load times.
Run one command. Get a complete launch readiness score in seconds.

Why This Exists
Most startup founders focus on the product and forget the launch infrastructure. Then they launch on Product Hunt, get 500 visitors… and lose half of them because:

No Open Graph tags → links look broken on social media
No meta description → Google shows nothing in search results
No sitemap.xml → search engines can't index the site
Slow load time → users bounce before the page loads

This tool checks all of it automatically.

After fixing these issues, get your startup in front of real early adopters. List it on StartupLaunchDay.com — a curated directory where founders, investors, and early adopters discover new products.


What It Checks
CheckWhy It MattersSSL/HTTPSGoogle ranks HTTPS sites higher; users trust them morePage speed (<2s)Every second of delay reduces conversions by ~7%robots.txtTells search engines how to crawl your sitesitemap.xmlHelps Google discover and index all your pagesOpen Graph tagsControls how your link looks on Twitter, LinkedIn, SlackMeta descriptionYour 160-char pitch in Google search resultsMobile viewportRequired for Google's mobile-first indexingFaviconSmall but signals a polished, complete product

Installation
No dependencies. Python 3.7+ only.
bashgit clone https://github.com/yourusername/startup-launch-checker.git
cd startup-launch-checker
python launch_checker.py <your-domain.com>

Usage
bashpython launch_checker.py mystartup.com
Example output:
==========================================================
  🚀 Startup Launch Readiness Checker
  Target: mystartup.com
==========================================================

----------------------------------------------------------
  LAUNCH CHECKLIST (6/8 passed)
----------------------------------------------------------
  ✅ SSL/HTTPS
  ✅ Fast load (<2s)
  ✅ robots.txt
  ✅ sitemap.xml
  ✅ Mobile viewport
  ✅ Favicon
  ❌ Open Graph tags  ← fix before launch
  ❌ Meta description  ← fix before launch

----------------------------------------------------------
  LAUNCH READINESS SCORE: 75/100
  🟡 ALMOST READY — fix a few things first
----------------------------------------------------------

  📋 Priority fixes:
     → Open Graph tags
     → Meta description

==========================================================
  🚀 Ready to launch? Get listed in front of
  early adopters, founders & investors:
  👉  https://startuplaunchday.com
==========================================================

Score Interpretation
ScoreStatus80–100🟢 Launch ready55–79🟡 Almost ready — fix flagged issues first0–54🔴 Not ready — critical issues need fixing

Quick Fix Guide
Missing Open Graph tags? Add to your <head>:
html<meta property="og:title" content="Your Startup Name" />
<meta property="og:description" content="One sentence pitch" />
<meta property="og:image" content="https://yoursite.com/og-image.png" />
<meta property="og:url" content="https://yoursite.com" />
Missing meta description?
html<meta name="description" content="Your 150-160 character pitch here." />
Missing sitemap.xml? Most frameworks generate this automatically:

Next.js: add next-sitemap package
WordPress: install Yoast SEO
Other: use xml-sitemaps.com to generate one


The Launch Checklist Beyond Tech
This tool handles the technical side. For a successful launch you also need:

📣 A launch platform strategy (Product Hunt, HN, Reddit)
📋 A directory listing plan for SEO backlinks
👥 An early adopter community lined up

StartupLaunchDay.com covers the last two — it's a free directory where you can list your startup and reach people actively looking for new tools.

Roadmap

 Core Web Vitals check via PageSpeed API
 Twitter Card validation
 Structured data / JSON-LD detection
 Email/contact page presence check
 Privacy policy & terms of service detection
 PWA manifest check

PRs welcome.

Contributing

Fork the repo
Create a feature branch
Submit a PR with a description of what your check does and why it matters for launch


License
MIT — free to use for your own launches.

Related

StartupLaunchDay.com — List your startup, get early users
The Launch Checklist — Complete pre-launch guide for founders
Startup directories list — Where to submit your startup for backlinks


Built by founders, for founders. Because launch day only happens once.
