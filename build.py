#!/usr/bin/env python3
"""Build the Utrujj static site pages from shared partials and data."""

from __future__ import annotations

import html
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = Path("/tmp/utrujj-pages")

# ---------------------------------------------------------------------------
# Shared chrome
# ---------------------------------------------------------------------------

HEADER = """
  <a class="skip-link" href="#main">Skip to content</a>

  <header class="site-header" data-header>
    <div class="container header-inner">
      <a class="brand" href="index.html" aria-label="Utrujj home">
        <img src="assets/img/Utrujj-Logo-Web-AK-1.webp" alt="Utrujj — Knowledge &amp; Creativity" width="1007" height="383">
      </a>

      <nav class="primary-nav" aria-label="Primary navigation">
        <ul>
          <li class="nav-item has-sub" data-nav="about">
            <button class="nav-link" type="button" aria-expanded="false">About <svg class="icon icon--sm"><use href="#i-chevron"/></svg></button>
            <ul class="submenu">
              <li><a href="about.html">About Us</a></li>
              <li><a href="shaykh-haytham-tamim.html">Our Founder</a></li>
              <li><a href="our-team.html">The Team</a></li>
              <li><a href="contact.html">Contact Us</a></li>
            </ul>
          </li>
          <li class="nav-item has-sub" data-nav="learn">
            <button class="nav-link" type="button" aria-expanded="false">Learn <svg class="icon icon--sm"><use href="#i-chevron"/></svg></button>
            <ul class="submenu">
              <li><a href="tafseer-classes.html">Tafseer Classes</a></li>
              <li><a href="hadith-classes.html">Hadith Classes</a></li>
              <li><a href="on-demand.html">On Demand</a></li>
            </ul>
          </li>
          <li class="nav-item has-sub" data-nav="read">
            <button class="nav-link" type="button" aria-expanded="false">Read <svg class="icon icon--sm"><use href="#i-chevron"/></svg></button>
            <ul class="submenu">
              <li><a href="blog.html">Latest Articles</a></li>
              <li><a href="qa.html">Q &amp; A</a></li>
              <li><a href="booklets.html">Booklets</a></li>
            </ul>
          </li>
          <li class="nav-item has-sub" data-nav="attend">
            <button class="nav-link" type="button" aria-expanded="false">Attend <svg class="icon icon--sm"><use href="#i-chevron"/></svg></button>
            <ul class="submenu">
              <li><a href="events.html">Events</a></li>
              <li><a href="retreats.html">Retreats</a></li>
            </ul>
          </li>
          <li class="nav-item has-sub" data-nav="watch">
            <button class="nav-link" type="button" aria-expanded="false">Watch <svg class="icon icon--sm"><use href="#i-chevron"/></svg></button>
            <ul class="submenu">
              <li><a href="on-demand.html">On Demand</a></li>
              <li><a href="https://www.youtube.com/c/ShaykhHaythamTamim" target="_blank" rel="noopener">YouTube Courses</a></li>
            </ul>
          </li>
        </ul>
      </nav>

      <div class="header-actions">
        <button class="icon-btn" type="button" aria-label="Open search" data-search-open>
          <svg class="icon"><use href="#i-search"/></svg>
        </button>
        <a class="btn btn--primary btn--small header-donate" href="donate.html" data-nav="donate">Donate</a>
        <button class="icon-btn menu-btn" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="mobile-menu" data-menu-toggle>
          <svg class="icon"><use href="#i-menu"/></svg>
        </button>
      </div>
    </div>

    <div class="mobile-menu" id="mobile-menu" data-mobile-menu hidden>
      <nav aria-label="Mobile navigation">
        <div class="mobile-menu-group">
          <p class="mobile-menu-label">About</p>
          <a href="about.html">About Us</a>
          <a href="shaykh-haytham-tamim.html">Our Founder</a>
          <a href="our-team.html">The Team</a>
          <a href="contact.html">Contact Us</a>
        </div>
        <div class="mobile-menu-group">
          <p class="mobile-menu-label">Learn</p>
          <a href="tafseer-classes.html">Tafseer Classes</a>
          <a href="hadith-classes.html">Hadith Classes</a>
          <a href="on-demand.html">On Demand</a>
        </div>
        <div class="mobile-menu-group">
          <p class="mobile-menu-label">Read</p>
          <a href="blog.html">Latest Articles</a>
          <a href="qa.html">Q &amp; A</a>
          <a href="booklets.html">Booklets</a>
        </div>
        <div class="mobile-menu-group">
          <p class="mobile-menu-label">Attend</p>
          <a href="events.html">Events</a>
          <a href="retreats.html">Retreats</a>
          <a href="https://www.youtube.com/c/ShaykhHaythamTamim" target="_blank" rel="noopener">YouTube Courses</a>
        </div>
      </nav>
      <div class="mobile-menu-footer">
        <a class="btn btn--primary" href="donate.html">Donate</a>
        <a class="link-arrow" href="mailto:info@utrujj.org">info@utrujj.org <svg class="icon icon--sm"><use href="#i-arrow"/></svg></a>
      </div>
    </div>
  </header>

  <div class="search-panel" data-search-panel hidden>
    <div class="search-panel-inner">
      <button class="icon-btn search-close" type="button" aria-label="Close search" data-search-close>
        <svg class="icon"><use href="#i-close"/></svg>
      </button>
      <p class="eyebrow">Search Utrujj</p>
      <form action="https://www.utrujj.org/" method="get" role="search">
        <label class="sr-only" for="site-search">Search the site</label>
        <input id="site-search" name="s" type="search" placeholder="What would you like to learn about?" autocomplete="off">
        <button class="btn btn--primary" type="submit">Search <svg class="icon icon--sm"><use href="#i-arrow"/></svg></button>
      </form>
    </div>
  </div>
"""

FOOTER = """
  <footer class="site-footer">
    <div class="footer-pattern" aria-hidden="true"></div>
    <div class="container footer-main">
      <div class="footer-brand">
        <a class="footer-logo" href="index.html" aria-label="Utrujj home">
          <img src="assets/img/Utrujj-Logo-Web-AK-1.webp" alt="Utrujj — Knowledge &amp; Creativity" width="1007" height="383">
        </a>
        <p>Spreading the positive message of peace, love and justice for over two decades.</p>
        <div class="social-links">
          <a href="https://www.facebook.com/UtrujjFoundation" target="_blank" rel="noopener" aria-label="Utrujj on Facebook"><svg class="icon"><use href="#i-facebook"/></svg></a>
          <a href="https://www.instagram.com/utrujj/" target="_blank" rel="noopener" aria-label="Utrujj on Instagram"><svg class="icon"><use href="#i-instagram"/></svg></a>
          <a href="https://www.youtube.com/c/ShaykhHaythamTamim" target="_blank" rel="noopener" aria-label="Shaykh Haytham Tamim on YouTube"><svg class="icon"><use href="#i-youtube"/></svg></a>
          <a href="mailto:info@utrujj.org" aria-label="Email Utrujj"><svg class="icon"><use href="#i-mail"/></svg></a>
        </div>
      </div>

      <nav class="footer-nav" aria-label="About">
        <h3>About</h3>
        <a href="about.html">About Utrujj</a>
        <a href="shaykh-haytham-tamim.html">Our Founder</a>
        <a href="our-team.html">The Team</a>
        <a href="contact.html">Contact Us</a>
        <a href="volunteer.html">Volunteer</a>
      </nav>

      <nav class="footer-nav" aria-label="Learn">
        <h3>Learn</h3>
        <a href="tafseer-classes.html">Tafseer Classes</a>
        <a href="hadith-classes.html">Hadith Classes</a>
        <a href="on-demand.html">On Demand</a>
        <a href="events.html">Events</a>
        <a href="retreats.html">Retreats</a>
      </nav>

      <nav class="footer-nav" aria-label="Read">
        <h3>Read</h3>
        <a href="blog.html">Latest Articles</a>
        <a href="qa.html">Q &amp; A</a>
        <a href="booklets.html">Booklets</a>
        <a href="donate.html">Donate</a>
        <a href="privacy-policy.html">Privacy Policy</a>
      </nav>
    </div>

    <div class="container footer-bottom">
      <p>© 2026 Utrujj Foundation · Registered charity 1196901</p>
      <p><a href="mailto:info@utrujj.org">info@utrujj.org</a></p>
      <p class="footer-credit">Site design: Fahad Khan</p>
    </div>
  </footer>
"""

SPRITE = """
  <svg class="svg-sprite" aria-hidden="true">
    <symbol id="i-arrow" viewBox="0 0 24 24"><path d="M4 12h15M13 5l7 7-7 7"/></symbol>
    <symbol id="i-chevron" viewBox="0 0 24 24"><path d="m6 9 6 6 6-6"/></symbol>
    <symbol id="i-search" viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="m16.5 16.5 4 4"/></symbol>
    <symbol id="i-menu" viewBox="0 0 24 24"><path d="M4 7h16M4 12h16M4 17h16"/></symbol>
    <symbol id="i-close" viewBox="0 0 24 24"><path d="m6 6 12 12M18 6 6 18"/></symbol>
    <symbol id="i-play" viewBox="0 0 24 24"><path d="M8 5.5v13l11-6.5z" fill="currentColor" stroke="none"/></symbol>
    <symbol id="i-instagram" viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.2" cy="6.8" r="1" fill="currentColor" stroke="none"/></symbol>
    <symbol id="i-facebook" viewBox="0 0 24 24"><path d="M14.5 21v-7h2.4l.4-3h-2.8V9.2c0-.9.3-1.5 1.6-1.5h1.3V5.1c-.6-.1-1.5-.2-2.5-.2-2.5 0-4.1 1.5-4.1 4.2V11H8v3h2.8v7z" fill="currentColor" stroke="none"/></symbol>
    <symbol id="i-youtube" viewBox="0 0 24 24"><rect x="3" y="6" width="18" height="12" rx="4"/><path d="m10.5 9.5 5 2.5-5 2.5z" fill="currentColor" stroke="none"/></symbol>
    <symbol id="i-mail" viewBox="0 0 24 24"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m4 7 8 6 8-6"/></symbol>
    <symbol id="i-book" viewBox="0 0 24 24"><path d="M5 4.5A2.5 2.5 0 0 1 7.5 2H19v17H7.5A2.5 2.5 0 0 0 5 21.5z"/><path d="M5 19.5A2.5 2.5 0 0 1 7.5 17H19"/></symbol>
    <symbol id="i-question" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M9.5 9a2.6 2.6 0 0 1 5.1.7c0 1.8-2.6 2.1-2.6 3.8"/><circle cx="12" cy="17" r=".8" fill="currentColor" stroke="none"/></symbol>
    <symbol id="i-star" viewBox="0 0 24 24"><path d="m12 2 2.4 6.3L21 10l-5 4.1 1.7 6.4-5.7-3.7L6.3 20.5 8 14.1 3 10l6.6-1.7z"/></symbol>
    <symbol id="i-check" viewBox="0 0 24 24"><path d="m4 12.5 5 5L20 6.5"/></symbol>
    <symbol id="i-heart" viewBox="0 0 24 24"><path d="M12 20.5S3.5 15 3.5 9.1A4.6 4.6 0 0 1 12 6.4a4.6 4.6 0 0 1 8.5 2.7c0 5.9-8.5 11.4-8.5 11.4Z"/></symbol>
    <symbol id="i-users" viewBox="0 0 24 24"><circle cx="9" cy="8" r="3.2"/><path d="M3.5 20c0-3.2 2.5-5.5 5.5-5.5s5.5 2.3 5.5 5.5"/><circle cx="17" cy="9" r="2.5"/><path d="M16 14.6c2.6 0 4.5 2 4.5 4.4"/></symbol>
    <symbol id="i-globe" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.4 3.8 5.5 3.8 9s-1.3 6.6-3.8 9c-2.5-2.4-3.8-5.5-3.8-9S9.5 5.4 12 3Z"/></symbol>
  </svg>
"""


def clean_cats(value: str) -> str:
    text = value.split(">")[-1] if ">" in value else value
    text = re.sub(r"\s+", " ", text).replace("category-links", "").replace("term-links", "").replace("category-style-normal", "")
    text = text.strip(" \"'>")
    return text.strip()


def short_date(value: str) -> str:
    value = value.strip()
    for fmt in ("%B %d, %Y", "%d %B %Y"):
        try:
            return datetime.strptime(value, fmt).strftime("%d %b %Y")
        except ValueError:
            pass
    return value


def trim(text: str, limit: int = 165) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= limit:
        return text
    cut = text[:limit].rsplit(" ", 1)[0].rstrip(" ,;:.-")
    return cut + "…"


def esc(text: str) -> str:
    return html.escape(text, quote=False)


def eyebrow(text: str, light: bool = False) -> str:
    cls = "eyebrow eyebrow--light" if light else "eyebrow"
    return f'<p class="{cls}"><span class="eyebrow-line"></span>{text}</p>'


def cta_band(title, text, primary_label, primary_href, secondary_label=None,
             secondary_href=None, navy=False, eyebrow_text=None):
    extra = " cta-band--navy" if navy else ""
    eyebrow_html = eyebrow(eyebrow_text, light=navy) if eyebrow_text else ""
    secondary = (
        f'<a class="link-arrow" href="{secondary_href}">{secondary_label} '
        '<svg class="icon icon--sm"><use href="#i-arrow"/></svg></a>'
        if secondary_label and secondary_href else ""
    )
    return f"""
    <section class="cta-band{extra}">
      <div class="container cta-band__inner">
        <div>
          {eyebrow_html}
          <h2>{title}</h2>
          <p>{text}</p>
        </div>
        <div class="cta-band__actions">
          <a class="btn btn--{'cream' if navy else 'primary'}" href="{primary_href}">{primary_label} <svg class="icon icon--sm"><use href="#i-arrow"/></svg></a>
          {secondary}
        </div>
      </div>
    </section>
"""


def page(filename, title, description, active, body, page_key=None):
    header = HEADER
    if active:
        header = header.replace(
            f'<li class="nav-item has-sub" data-nav="{active}">',
            f'<li class="nav-item has-sub is-active" data-nav="{active}">',
        )
        header = header.replace(
            f'data-nav="{active}">\n            <button class="nav-link"',
            f'data-nav="{active}" aria-current="page">\n            <button class="nav-link"',
        )
    if active == "donate":
        header = header.replace('class="btn btn--primary btn--small header-donate"', 'class="btn btn--primary btn--small header-donate is-active"')
        header = header.replace('href="donate.html" data-nav="donate"', 'href="donate.html" data-nav="donate" aria-current="page"')
    page_key = page_key or active or "home"
    doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} | Utrujj</title>
  <meta name="description" content="{description}">
  <link rel="icon" href="assets/img/cropped-IMG_2768-180x180.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&family=Fraunces:ital,opsz,wght@0,9..144,300..700;1,9..144,300..700&family=Manrope:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="css/styles.css">
  <link rel="stylesheet" href="css/pages.css">
  <script>document.documentElement.classList.add("js");</script>
</head>
<body data-page="{page_key}">
{SPRITE}
{header}
  <main id="main">
{body}
  </main>
{FOOTER}
  <script src="js/main.js"></script>
</body>
</html>
"""
    (ROOT / filename).write_text(doc, encoding="utf-8")
    print("wrote", filename)


# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------

blog = json.loads((DATA / "blog-local.json").read_text())
qa = json.loads((DATA / "qa-local.json").read_text())
booklets = json.loads((DATA / "booklets-local.json").read_text())
courses = json.loads((DATA / "on-demand-local.json").read_text())
events = json.loads((DATA / "events-local.json").read_text())

for item in blog + qa:
    item["cats_clean"] = clean_cats(item.get("cats", ""))

for item in booklets + courses:
    item["title_clean"] = re.sub(r"\s+by Shaykh Haytham Tamim$", "", item["title"], flags=re.I)
    price = item.get("price", "")
    item["is_free"] = "0.00" in price or not price
    item["price_clean"] = "Free" if item["is_free"] else price.replace("£ ", "£").strip()

team = [
    ("Ayesha Khan", "Head of Operations", "Ayesha oversees the operations at Utrujj while supporting Shaykh Haytham. Her passion lies in preserving and sharing sacred knowledge. She has been a student of Shaykh Haytham since 2012 and has an Ijazah from him."),
    ("Samia Ahmed", "Advisor to the Board & Events Manager", "Samia joined Utrujj in 2003 and has held various leadership and managerial positions. She has overseen operations, volunteers, retreats and educational resources. She holds an Ijazah and a Master’s in Islamic Studies."),
    ("Hana Khan", "Technical Support, Transcriber & Volunteer", "Hana has volunteered since 2017, providing IT support, video management and event assistance. She also transcribes Taraweeh reminders and contributes to graphic design. She graduated from the University of Cambridge in Engineering."),
    ("Sabeen Sheikh", "Transcriber and Copyeditor", "Sabeen transcribes Shaykh Haytham's weekly Tafseer classes and helps with Arbaeen Nawawiya lectures. She has been awarded an Ijazah and holds degrees in Psychology, Public Health and an Alimiyya degree."),
    ("Rose Roslan", "Transcriber", "Rose has supported Utrujj by transcribing Shaykh Haytham’s lessons since 2017. She has been a student of Shaykh Haytham for over 20 years and holds an Ijazah."),
    ("Nimni Sultan", "Graphic Designer", "Nimni has been the creative force behind the Daily Gems since 2017, using design to connect knowledge with action. Her background is in dentistry and she also enjoys travelling, cooking and dawah."),
    ("Ayesha Malik", "Senior Volunteer", "Ayesha has been involved with Utrujj since 2001. She coordinated the Tajweed Centre and helped organise courses and family events. She holds an Ijazah and is a qualified Time to Think Coach, Facilitator and Consultant."),
    ("Yaqoob Johnson", "Proofreader and Arabic Language Editor", "Yaqoob helps proofread publications and translate Qur’anic verses and hadith into clear English. He has a strong grasp of Arabic and experience in teaching English and computer programming."),
    ("Abu Shama", "Advisor", "Abu Ibrahim Shama has been a close student of Shaykh Haytham since 2003. He advises Utrujj on writing, graphic design, history and Islamic studies. He holds an Ijazah, a Masters in IT and a degree in Mechanical Engineering."),
    ("Jasmine Ansari", "Content Curator", "Jasmine helped sort and categorise a thousand blogs for the website, including khutbahs, articles and lectures on Al-Ghazali. She came to London from Pakistan in the 1960s and was introduced to Islam through FOSIS."),
    ("Saania Bhatti", "Medical Advisor", "Saania is a GP and Utrujj’s main medical advisor. She has been a student and volunteer since 2001 and has an Ijazah. She has a special interest in mental health, neurodiversity and wellbeing."),
    ("Jamila Sherif", "Senior Volunteer", "Jamila has been a student of Shaykh Haytham since 2001 and holds an Ijazah. She supports Utrujj retreats and initiatives and helped establish a Hadith class in Watford. She is also an NHS GP, trainer and appraiser."),
    ("Siaf & Sazeda Alam", "Senior Volunteers", "Siaf and Sazeda volunteer with their children at Utrujj events. They run reflection-based sporting activities and organise family events. Siaf is a lawyer and co-founded Fitzrovia United."),
    ("Zayna Sheikh", "Volunteer", "Zayna is currently Utrujj’s youngest volunteer. She enjoys transcribing talks and helping at events, as well as sports, learning languages and travelling."),
    ("Mona Naem", "Photographer", "Mona takes photographs for Utrujj and provides images for the website and blogs. She is a family and wedding photographer based in North London and also teaches children, teenagers and adults."),
]

retreat_timeline = [
    ("2025", "Re-Imagining Prophetic Vision", "Burleigh Court Hotel, Loughborough", "Reflecting on the prophetic model of building a just, ethical and successful civilisation."),
    ("2023", "The Farewell Sermon", "De Vere Woking, Surrey", "Reflecting on the Prophet’s final sermon (peace be upon him) and its timeless legacy."),
    ("2019", "Maqasid by Imam Nawawi", "De Vere Woking, Surrey", "Al-Maqāṣid by Imam al-Nawawi presents the fundamentals and pillars of Islam in a concise and clear manner."),
    ("2018", "The 7 Dimensions of Ramadan", "Gilwell Park, Chingford, London", "A multi-faceted approach to preparing for Ramadan through reflection, worship, and knowledge."),
    ("2018", "The Seventy-Seven Branches of Faith (Part 2)", "Markfield Conference Centre, Leicestershire", "Examined the characteristics of a strong believer and practical applications."),
    ("2017", "The Seventy-Seven Branches of Faith (Part 1)", "Markfield Conference Centre, Leicestershire", "Unpacked the essential traits of faith and how to cultivate them in daily life."),
    ("2016", "Journey of the Soul (Part 2)", "Markfield Conference Centre, Leicestershire", "Continuing the exploration of spiritual wisdom, focusing on the soul’s journey through life."),
    ("2015", "Journey of the Soul (Part 1)", "Markfield Conference Centre, Leicestershire", "A reflection on Kitab Al-Hikam, guiding seekers through self-purification and closeness to Allah."),
    ("2012", "The Prophet’s Counsel (peace be upon him)", "Markfield Conference Centre, Leicestershire", "An in-depth investigation of the wisdom-filled hadith, Forty Wasiyyah from Rasulullah (peace be upon him) to his Ummah, collected by Imam Abdullah Sirajuddin."),
    ("2012", "In the Company of Muhammad (peace be upon him)", "Buckland Hall, Brecon Beacons, Wales", "Utrujj’s first five-day retreat immersed attendees in the life and teachings of the Prophet (peace be upon him) through the Shama’il by Tirmidhi, which was read in Arabic and English and attendees received Ijazahs."),
    ("2011", "Time for a Change", "The Link Hotel, Loughborough", "Defined personal transformation through faith, discipline, and productivity."),
    ("2010", "The Secrets of Success", "Park Inn Hotel, Birmingham", "Unpacked the divine guidance in the Quran and Sunnah that leads to success in all areas of life."),
]

# ---------------------------------------------------------------------------
# Builders for repetitive cards
# ---------------------------------------------------------------------------


def article_card(item, featured=False):
    cats = item.get("cats_clean", "")
    cat_html = " · ".join([c.strip() for c in cats.split(",")][:2])
    cls = "listing-card listing-card--featured" if featured else "listing-card"
    return f"""
          <article class="{cls}">
            <a class="listing-card__image" href="{item['url']}" aria-hidden="true" tabindex="-1">
              <img src="{item['local']}" alt="" width="800" height="500" loading="lazy">
            </a>
            <div class="listing-card__body">
              <p class="listing-card__cats">{esc(cat_html)}</p>
              <h3><a href="{item['url']}">{esc(item['title'])}</a></h3>
              <p>{esc(trim(item['excerpt'], 185 if not featured else 260))}</p>
              <div class="listing-card__foot">
                <span class="listing-card__date">{short_date(item['date'])}</span>
                <a class="link-arrow" href="{item['url']}">Read article <svg class="icon icon--sm"><use href="#i-arrow"/></svg></a>
              </div>
            </div>
          </article>"""


def qa_card(item):
    cats = item.get("cats_clean", "")
    cat_html = " · ".join([c.strip() for c in cats.split(",")][:2])
    return f"""
          <article class="qa-card">
            <p class="qa-card__cat">{esc(cat_html)}</p>
            <h3><a href="{item['url']}">{esc(item['title'])}</a></h3>
            <p>{esc(trim(item['excerpt'], 190))}</p>
            <a class="link-arrow" href="{item['url']}">Read the answer <svg class="icon icon--sm"><use href="#i-arrow"/></svg></a>
          </article>"""


def product_card(item, kind="booklet"):
    cover = item.get("local", "")
    title = esc(item["title_clean"])
    price = esc(item["price_clean"])
    excerpt = esc(trim(item.get("excerpt", ""), 125))
    meta = "e-booklet" if kind == "booklet" else "on-demand course"
    return f"""
          <article class="product-card">
            <a class="product-card__cover" href="{item['url']}" aria-hidden="true" tabindex="-1">
              <img src="{cover}" alt="" width="600" height="800" loading="lazy">
            </a>
            <div class="product-card__body">
              <h3><a href="{item['url']}">{title}</a></h3>
              <p class="product-card__price">{price}</p>
              <p>{excerpt}</p>
              <div class="product-card__foot">
                <span class="product-card__meta">{meta}</span>
                <a class="link-arrow" href="{item['url']}">View <svg class="icon icon--sm"><use href="#i-arrow"/></svg></a>
              </div>
            </div>
          </article>"""


def team_card(name, role, bio):
    initials = "".join([part[0] for part in name.replace("&", "").split() if part][:2]).upper()
    return f"""
          <article class="team-card">
            <div class="team-monogram" aria-hidden="true">{initials}</div>
            <h3>{esc(name)}</h3>
            <p class="team-role">{esc(role)}</p>
            <p>{esc(bio)}</p>
          </article>"""


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------

about_body = f"""
    <section class="page-hero">
      <div class="container page-hero__inner">
        <div>
          <nav class="breadcrumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><span aria-hidden="true">/</span><span>About</span></nav>
          {eyebrow("About Utrujj")}
          <h1>To empower individuals to <em>learn, love, and live</em> Islam.</h1>
          <p class="page-hero__lead">Utrujj, founded by Shaykh Haytham Tamim, is an Islamic educational institute that has been serving the UK Muslim community since 2001. Our work is founded on authentic scholarship, showing how traditional Islamic wisdom can help us deal with the realities of modern life.</p>
          <div class="page-hero__actions">
            <a class="btn btn--primary" href="shaykh-haytham-tamim.html">Meet our founder <svg class="icon icon--sm"><use href="#i-arrow"/></svg></a>
            <a class="link-arrow" href="tafseer-classes.html">Explore our classes <svg class="icon icon--sm"><use href="#i-arrow"/></svg></a>
          </div>
        </div>
        <figure class="hero-figure hero-figure--arch">
          <div class="hero-figure__media">
            <img src="assets/img/Shaykh-Tamim-About.webp" alt="Shaykh Haytham Tamim holding an open book in front of a library of Islamic texts" width="800" height="1000">
          </div>
          <figcaption class="hero-figure__caption">Shaykh Haytham Tamim<span>Founder &amp; teacher</span></figcaption>
        </figure>
      </div>
    </section>

    <section class="section section--paper">
      <div class="container">
        <div class="split split--top">
          <div class="split__copy">
            {eyebrow("Who we are")}
            <h2>Knowledge that <em>changes lives.</em></h2>
            <p>We change lives by teaching Islam through online classes, courses and retreats, equipping individuals with authentic Islamic knowledge and spiritual tools to deepen their faith, refine their character, and ‘live Islam’ with confidence.</p>
            <p>We believe that learning Islam is more than gaining knowledge — it is about becoming the best version of ourselves. Our mission is to inspire goodness, foster tolerance, and promote harmony within individuals, families, and communities.</p>
            <p>Through the Quran and sunnah, we empower individuals to become catalysts for goodness, spreading kindness, integrity, and positive change in their communities.</p>
          </div>
          <div class="split__media">
            <img src="assets/img/pages/founder-library.webp" alt="Shaykh Haytham Tamim selecting a book from a library shelf" width="1000" height="667" loading="lazy">
          </div>
        </div>

        <div class="stat-row">
          <div class="stat"><strong>2001</strong><span>Serving the UK community</span></div>
          <div class="stat"><strong>25+</strong><span>Years of teaching</span></div>
          <div class="stat"><strong>29</strong><span>Links in the chain of scholarship</span></div>
          <div class="stat"><strong>1196901</strong><span>Registered charity number</span></div>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="section-head">
          <div>
            {eyebrow("What guides us")}
            <h2>Our <em>values.</em></h2>
          </div>
          <div class="section-intro">
            <p>Three commitments shape every class, retreat and resource we produce.</p>
          </div>
        </div>
        <div class="value-grid">
          <article class="value-card">
            <span class="value-card__num">01</span>
            <h3>Authenticity</h3>
            <p>In a world of misinformation, we preserve and deliver Islam with clarity and integrity.</p>
          </article>
          <article class="value-card">
            <span class="value-card__num">02</span>
            <h3>Accessibility</h3>
            <p>In an age of confusion, we make Islamic knowledge practical and relevant.</p>
          </article>
          <article class="value-card">
            <span class="value-card__num">03</span>
            <h3>Empowerment</h3>
            <p>In times of doubt, we equip you to have confidence in your identity and faith.</p>
          </article>
        </div>
      </div>
    </section>

    <section class="section section--blue">
      <div class="container split">
        <div class="split__copy">
          {eyebrow("Our founder")}
          <h2>A lifelong seeker of <em>knowledge.</em></h2>
          <p>Shaykh Haytham Tamim is a scholar who has dedicated his life to making sacred, authentic Islamic knowledge accessible and practical. By the grace of Allah, he has been disseminating traditional Islamic learning in the UK for over two decades.</p>
          <p>With more than 30 years of expertise across major schools of thought and Islamic disciplines, his unbroken chain of scholarship traces directly back to the Prophet ﷺ.</p>
          <a class="btn btn--primary" href="shaykh-haytham-tamim.html">Read his story <svg class="icon icon--sm"><use href="#i-arrow"/></svg></a>
        </div>
        <figure class="split__media split__media--arch">
          <img src="assets/img/pages/founder-portrait.webp" alt="Portrait of Shaykh Haytham Tamim in a mosque" width="1000" height="750" loading="lazy">
        </figure>
      </div>
    </section>

    <section class="section section--tight">
      <div class="container">
        <div class="quote-panel">
          <figure>
            <blockquote><p>“Islam isn’t just about seeking knowledge from the right source. It is about understanding how it applies to your life.”</p></blockquote>
            <figcaption>Shaykh Haytham Tamim</figcaption>
          </figure>
        </div>
      </div>
    </section>

    {cta_band("Ready to <em>begin?</em>", "Join a class, explore our articles, or support the work that makes it all possible.", "Explore classes", "tafseer-classes.html", "Support our work", "donate.html", eyebrow_text="Take the next step")}
"""

page("about.html", "About", "Utrujj is an Islamic educational institute serving the UK Muslim community since 2001, founded by Shaykh Haytham Tamim.", "about", about_body)


founder_body = f"""
    <section class="page-hero">
      <div class="container page-hero__inner">
        <div>
          <nav class="breadcrumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><span aria-hidden="true">/</span><a href="about.html">About</a><span aria-hidden="true">/</span><span>Our Founder</span></nav>
          {eyebrow("Our founder")}
          <h1>Shaykh Haytham <em>Tamim.</em></h1>
          <p class="page-hero__lead">A scholar who has dedicated his life to making sacred, authentic Islamic knowledge accessible and practical — and to helping ordinary people develop a deep love for the Quran.</p>
          <div class="page-hero__actions">
            <a class="btn btn--primary" href="tafseer-classes.html">Study with the Shaykh <svg class="icon icon--sm"><use href="#i-arrow"/></svg></a>
            <a class="link-arrow" href="about.html">About Utrujj <svg class="icon icon--sm"><use href="#i-arrow"/></svg></a>
          </div>
          <p class="page-hero__meta"><span>Unbroken sanad</span><span>30+ years of scholarship</span><span>Founder since 2001</span></p>
        </div>
        <figure class="hero-figure hero-figure--portrait">
          <div class="hero-figure__media">
            <img src="assets/img/pages/founder-portrait.webp" alt="Shaykh Haytham Tamim standing in a mosque" width="1000" height="750">
          </div>
          <figcaption class="hero-figure__caption">Shaykh Haytham Tamim<span>Founder, Utrujj Foundation</span></figcaption>
        </figure>
      </div>
    </section>

    <section class="section section--paper">
      <div class="container split split--top">
        <div class="split__copy">
          {eyebrow("Founding Utrujj")}
          <h2>Knowledge that <em>transforms lives.</em></h2>
          <p>In 2000, Shaykh Haytham established the Utrujj Foundation with a clear mission: to spread Islamic knowledge with clarity, authenticity, and practicality. Utrujj is not about passive learning, but actively applying Islamic principles to real life.</p>
          <p>Spiritual growth combined with wisdom and common sense enables us to tap into the powerful potential we have — to transcend the mundane and live a life that is filled with hope, success and contentment.</p>
        </div>
        <div class="split__media">
          <img src="assets/img/pages/quran-open.webp" alt="A hand resting on an open Quran" width="1000" height="667" loading="lazy">
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container split">
        <div class="split__copy">
          {eyebrow("A legacy of scholarship")}
          <h2>An unbroken <em>chain.</em></h2>
          <p>Shaykh Haytham has an unbroken chain of transmission (sanad) that goes back to the Prophet ﷺ. He has learned from some of the most respected scholars of our time, including:</p>
          <ul class="prose-list">
            <li>The late Professor Wahba Al-Zuhayli</li>
            <li>The late Shaykh Muhammad Sukkar</li>
            <li>The late Shaykh Khalil Al-Mays</li>
            <li>Professor Ahmad Al-Haji Kurdi</li>
            <li>The late Shaykh Abdul Razzaq Al-Halabi</li>
            <li>The late Shaykh Adeeb Al-Kallas</li>
            <li>The late Mulla Abdul ‘Aleem Al-Zanki</li>
            <li>Professor Mustafa Azami</li>
            <li>Mufti Taqi Usmani</li>
            <li>Shaykh Nizam Yaqoubi</li>
          </ul>
          <p>With some of the highest Ijazahs in Quran, Hadith, and Fiqh, he ensures that Islamic knowledge is passed on with precision and integrity.</p>
        </div>
        <div class="split__media">
          <img src="assets/img/pages/founder-library.webp" alt="Shaykh Haytham Tamim choosing a classical Islamic text" width="1000" height="667" loading="lazy">
        </div>
      </div>
    </section>

    <section class="section section--blue">
      <div class="container">
        <div class="section-head">
          <div>
            {eyebrow("Teaching & leadership")}
            <h2>A life given to <em>service.</em></h2>
          </div>
          <div class="section-intro">
            <p>From the minbar to the manuscript, from the classroom to the Shariah boardroom.</p>
          </div>
        </div>
        <div class="value-grid">
          <article class="value-card">
            <span class="value-card__num">17</span>
            <h3>First sermon</h3>
            <p>Shaykh Haytham delivered his first sermon to a large congregation at just 17, beginning a lifetime of teaching and service.</p>
          </article>
          <article class="value-card">
            <span class="value-card__num">20+</span>
            <h3>Classical works</h3>
            <p>He has completed the critical verification (tahqeeq) of over 20 classical books and manuscripts in hadith, fiqh and the science of hadith.</p>
          </article>
          <article class="value-card">
            <span class="value-card__num">UK</span>
            <h3>Shariah expertise</h3>
            <p>An authority in Islamic finance and Shariah advisory, he consults for international firms, investment institutions and legal professionals.</p>
          </article>
        </div>
      </div>
    </section>

    <section class="section section--paper">
      <div class="container split">
        <figure class="split__media">
          <img src="assets/img/pages/founder-community.webp" alt="Shaykh Haytham Tamim speaking with members of the community" width="1000" height="667" loading="lazy">
        </figure>
        <div class="split__copy">
          {eyebrow("A voice of wisdom")}
          <h2>Compassion, clarity <em>and balance.</em></h2>
          <p>As the leader of the Lebanese Sunni community in the UK under Dar Al-Fatwa, Shaykh Haytham is a mentor, a guide, and a voice of reason in today’s fast-changing world.</p>
          <p>His students value his wisdom, clarity, and balanced perspective, often turning to him for advice on faith, personal growth, and navigating modern challenges.</p>
          <p>Whether through his teaching, advisory work, or leadership, his mission remains the same: to connect people to the Quran and Sunnah with confidence, purpose and conviction.</p>
          <a class="btn btn--primary" href="contact.html">Get in touch <svg class="icon icon--sm"><use href="#i-arrow"/></svg></a>
        </div>
      </div>
    </section>

    <section class="section section--tight">
      <div class="container">
        <div class="media-strip">
          <figure><img src="assets/img/pages/founder-library.webp" alt="Shaykh Haytham Tamim in his library" loading="lazy"></figure>
          <figure><img src="assets/img/pages/quran-open.webp" alt="An open Quran" loading="lazy"></figure>
          <figure><img src="assets/img/pages/founder-community.webp" alt="Shaykh Haytham Tamim with the community" loading="lazy"></figure>
        </div>
      </div>
    </section>

    {cta_band("Learn from a <em>living chain.</em>", "Study Tafseer or Hadith with Shaykh Haytham Tamim, online or in person.", "Explore Tafseer", "tafseer-classes.html", "Explore Hadith", "hadith-classes.html", eyebrow_text="Study with the Shaykh")}
"""

page("shaykh-haytham-tamim.html", "Shaykh Haytham Tamim", "Meet Shaykh Haytham Tamim, founder of Utrujj Foundation: a scholar with an unbroken chain of scholarship tracing back to the Prophet ﷺ.", "about", founder_body)


team_cards = "".join(team_card(*member) for member in team)
team_body = f"""
    <section class="page-hero page-hero--center">
      <div class="container page-hero__inner">
        <div>
          <nav class="breadcrumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><span aria-hidden="true">/</span><a href="about.html">About</a><span aria-hidden="true">/</span><span>The Team</span></nav>
          {eyebrow("Our team")}
          <h1>The people behind <em>Utrujj.</em></h1>
          <p class="page-hero__lead">At Utrujj, we deeply value the dedication and contributions of our volunteers, without whom our work would not be possible. Every effort, large or small, plays a vital role in our mission — and is greatly appreciated.</p>
          <div class="page-hero__actions">
            <a class="btn btn--primary" href="volunteer.html">Join our volunteers <svg class="icon icon--sm"><use href="#i-arrow"/></svg></a>
            <a class="link-arrow" href="contact.html">Contact the team <svg class="icon icon--sm"><use href="#i-arrow"/></svg></a>
          </div>
        </div>
      </div>
    </section>

    <section class="section section--paper">
      <div class="container">
        <div class="team-grid">
          {team_cards}
        </div>
        <div class="bundle-note">
          <p><strong>In addition, we have many other volunteers</strong> who give their time and skills behind the scenes. Every contribution helps keep authentic knowledge accessible.</p>
          <a class="btn btn--primary btn--small" href="volunteer.html">Volunteer with us <svg class="icon icon--sm"><use href="#i-arrow"/></svg></a>
        </div>
      </div>
    </section>

    {cta_band("Be part of the <em>work.</em>", "Whether you can offer an hour a week or a specialist skill, there is a place for you at Utrujj.", "Volunteer with us", "volunteer.html", "Support our work", "donate.html", eyebrow_text="Serve the Deen")}
"""

page("our-team.html", "Our Team", "Meet the volunteers and team behind Utrujj Foundation — the people who make our classes, events and resources possible.", "about", team_body)


contact_body = f"""
    <section class="page-hero">
      <div class="container page-hero__inner">
        <div>
          <nav class="breadcrumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><span aria-hidden="true">/</span><span>Contact</span></nav>
          {eyebrow("Contact us")}
          <h1>We’d love to <em>hear from you.</em></h1>
          <p class="page-hero__lead">Assalamalaykum. Do you have any questions or comments? You can contact Utrujj by emailing us directly at <a href="mailto:info@utrujj.org"><strong>info@utrujj.org</strong></a> or by using the form.</p>
          <p class="page-hero__meta"><span>Email replies</span><span>Course enquiries</span><span>Volunteering</span></p>
        </div>
        <div class="form-card">
          <h2>Send a message</h2>
          <p>Please note that while we strive to respond as soon as possible, there may be times when we are unable to reply to all queries. We appreciate your understanding and patience.</p>
          <form data-contact>
            <div class="form-grid">
              <div class="field"><label for="contact-name">Name</label><input id="contact-name" name="name" type="text" autocomplete="name" required></div>
              <div class="field"><label for="contact-email">Email</label><input id="contact-email" name="email" type="email" autocomplete="email" required></div>
              <div class="field field--full"><label for="contact-subject">Subject</label><input id="contact-subject" name="subject" type="text" required></div>
              <div class="field field--full"><label for="contact-message">Message</label><textarea id="contact-message" name="message" required></textarea></div>
            </div>
            <button class="btn btn--primary" type="submit">Send message <svg class="icon icon--sm"><use href="#i-arrow"/></svg></button>
            <p class="form-note" data-form-note>We will only use your details to respond to your enquiry.</p>
          </form>
        </div>
      </div>
    </section>

    <section class="section section--paper section--tight">
      <div class="container contact-grid">
        <div class="contact-details">
          {eyebrow("Other ways to reach us")}
          <h2>Direct <em>contact.</em></h2>
          <p>For course questions, volunteering, donations or general enquiries, email is the best way to reach the team.</p>
          <div class="contact-item">
            <span class="icon-tile"><svg class="icon"><use href="#i-mail"/></svg></span>
            <div><h3>Email</h3><a href="mailto:info@utrujj.org">info@utrujj.org</a></div>
          </div>
          <div class="contact-item">
            <span class="icon-tile icon-tile--blue"><svg class="icon"><use href="#i-users"/></svg></span>
            <div><h3>Volunteering</h3><a href="volunteer.html">Offer your time and skills</a></div>
          </div>
          <div class="contact-item">
            <span class="icon-tile"><svg class="icon"><use href="#i-heart"/></svg></span>
            <div><h3>Donations</h3><a href="donate.html">Support authentic knowledge</a></div>
          </div>
          <div class="contact-item">
            <span class="icon-tile icon-tile--blue"><svg class="icon"><use href="#i-book"/></svg></span>
            <div><h3>Registered charity</h3><p>Utrujj Foundation · 1196901</p></div>
          </div>
        </div>
        <div>
          <div class="quote-panel quote-panel--light">
            <figure>
              <blockquote><p>“If you have any questions or comments, please contact us. We appreciate your understanding and patience.”</p></blockquote>
              <figcaption>The Utrujj team</figcaption>
            </figure>
          </div>
          <div class="bundle-note">
            <p><strong>Looking for a class?</strong> Tafseer and Hadith run throughout the year, online and in person.</p>
            <a class="link-arrow" href="tafseer-classes.html">View classes <svg class="icon icon--sm"><use href="#i-arrow"/></svg></a>
          </div>
        </div>
      </div>
    </section>
"""

page("contact.html", "Contact", "Contact Utrujj Foundation by email at info@utrujj.org or send us a message using the contact form.", "about", contact_body)


def class_page(filename, title_label, h1, lead, image, image_alt, price, price_suffix, chips,
               quote_text, quote_cite, why_title, why_text, benefits, teacher_title,
               teacher_text, faq_items, nav_active="learn"):
    chips_html = "".join(f'<span class="detail-chip">{chip}</span>' for chip in chips)
    benefit_html = "".join(
        f"""
            <div class="check-item">
              <svg class="icon"><use href="#i-check"/></svg>
              <div><h3>{b_title}</h3><p>{b_text}</p></div>
            </div>"""
        for b_title, b_text in benefits
    )
    faq_html = "".join(
        f"""
          <details>
            <summary>{question}</summary>
            <p>{answer}</p>
          </details>"""
        for question, answer in faq_items
    )
    body = f"""
    <section class="page-hero">
      <div class="container page-hero__inner">
        <div>
          <nav class="breadcrumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><span aria-hidden="true">/</span><a href="on-demand.html">Learn</a><span aria-hidden="true">/</span><span>{title_label}</span></nav>
          {eyebrow("Learn with us")}
          <h1>{h1}</h1>
          <p class="page-hero__lead">{lead}</p>
          <div class="price-block"><strong>{price}</strong><span>{price_suffix}</span></div>
          <div class="detail-chips">{chips_html}</div>
          <div class="page-hero__actions">
            <a class="btn btn--primary" href="https://www.utrujj.org/{filename.replace('.html', '/')}">Enrol now <svg class="icon icon--sm"><use href="#i-arrow"/></svg></a>
            <a class="link-arrow" href="contact.html">Ask a question <svg class="icon icon--sm"><use href="#i-arrow"/></svg></a>
          </div>
        </div>
        <figure class="hero-figure hero-figure--portrait">
          <div class="hero-figure__media">
            <img src="{image}" alt="{image_alt}" width="800" height="1000">
          </div>
          <figcaption class="hero-figure__caption">Shaykh Haytham Tamim<span>Your teacher</span></figcaption>
        </figure>
      </div>
    </section>

    <section class="section section--paper">
      <div class="container split split--top">
        <div class="split__copy">
          {eyebrow("The class")}
          <h2>{why_title}</h2>
          {why_text}
          <a class="btn btn--primary" href="https://www.utrujj.org/{filename.replace('.html', '/')}">Join the class <svg class="icon icon--sm"><use href="#i-arrow"/></svg></a>
        </div>
        <div class="split__media">
          <img src="assets/img/pages/quran-open.webp" alt="An open Quran with a hand resting on the page" width="1000" height="667" loading="lazy">
        </div>
      </div>
    </section>

    <section class="section section--blue">
      <div class="container">
        <div class="section-head">
          <div>
            {eyebrow("What you will gain")}
            <h2>A deeper <em>understanding.</em></h2>
          </div>
          <div class="section-intro">
            <p>These are the marks of a class that stays with you long after the lesson ends.</p>
          </div>
        </div>
        <div class="check-grid">{benefit_html}</div>
      </div>
    </section>

    <section class="section section--tight">
      <div class="container">
        <div class="quote-panel">
          <figure>
            <blockquote><p>{quote_text}</p></blockquote>
            <figcaption>{quote_cite}</figcaption>
          </figure>
        </div>
      </div>
    </section>

    <section class="section section--paper">
      <div class="container split">
        <figure class="split__media split__media--arch">
          <img src="{image}" alt="{image_alt}" width="800" height="1000" loading="lazy">
        </figure>
        <div class="split__copy">
          {eyebrow("Your teacher")}
          <h2>{teacher_title}</h2>
          {teacher_text}
          <a class="link-arrow" href="shaykh-haytham-tamim.html">About the Shaykh <svg class="icon icon--sm"><use href="#i-arrow"/></svg></a>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="section-head">
          <div>
            {eyebrow("Questions")}
            <h2>Good to <em>know.</em></h2>
          </div>
          <div class="section-intro">
            <p>Still unsure? Email <a href="mailto:info@utrujj.org">info@utrujj.org</a> and the team will help.</p>
          </div>
        </div>
        <div class="faq">{faq_html}</div>
      </div>
    </section>

    {cta_band("Start your <em>journey.</em>", "Join a community of learners studying the Quran and Sunnah with clarity, depth and purpose.", "Enrol now", "https://www.utrujj.org/" + filename.replace('.html', '/'), "Explore On Demand", "on-demand.html", eyebrow_text="Learn with Utrujj")}
"""
    page(filename, title_label, f"{title_label} with Shaykh Haytham Tamim — authentic, practical and taught live by Utrujj.", nav_active, body)


class_page(
    "tafseer-classes.html",
    "Tafseer Classes",
    "Study the Quran with <em>clarity and purpose.</em>",
    "You need someone with deep knowledge to unlock its meanings, explain the background of revelations, and show how its rulings fit together as a complete way of life.",
    "assets/img/Shaykh-Haytham-Tamim-Tafseer-1.webp",
    "Shaykh Haytham Tamim reading from an open book",
    "£50",
    "/ month",
    ["58 lessons", "1.5 hours, twice weekly", "Online & in person", "Recordings available"],
    "“This is a blessed Book which We have revealed to you, that they might reflect upon its verses and that those of understanding would be reminded.”",
    "Quran (38:29)",
    "Why study <em>tafseer?</em>",
    "<p>The Quran is your divine guide to a successful life — but how much are you benefiting from it? Reciting it beautifully is one thing, but understanding its deeper meanings is another. Translations may help, yet without context, the coherence can be lost.</p><p>The Quran isn’t a simple narrative. It requires guidance. You need someone with deep knowledge to unlock its meanings, explain the background of revelations, and show how its rulings fit together as a complete way of life.</p><p>Studying Tafseer with a reputable and reliable source allows you to understand each verse clearly — how it connects to the life of the Prophet ﷺ, how it shaped mindsets, and how it transformed a society in need of guidance.</p>",
    [
        ("See the bigger picture", "Learn how rulings fit together in a divine system, rather than as isolated verses."),
        ("Understand the context", "Know the background of each revelation and the circumstances that shaped it."),
        ("Gain psychological insight", "Develop deeper self-awareness and emotional resilience through the Quran."),
        ("Strengthen your faith", "Find comfort, clarity and a stronger connection with Allah."),
    ],
    "A scholar of <em>the Quran.</em>",
    "<p>Shaykh Haytham Tamim has dedicated his life to studying the Quran, drawing from major classical texts and the teachings of renowned scholars. His knowledge has not just been acquired from books, but from being in the company of respected scholars from whom the knowledge has been passed down over generations, from chest to chest, going back to Prophet Muhammad ﷺ.</p><p>As a community leader, he understands that sacred knowledge is meant to shape lives, not sit on shelves. His explanations break down verses to reveal their psychological, emotional, historical and legal implications.</p>",
    [
        ("How long is each class?", "Classes run for 1.5 hours, twice weekly. Recordings are available if you cannot attend live."),
        ("Can I join online?", "Yes. The class is available online and in person, so you can learn from wherever you are."),
        ("What if I miss a lesson?", "Recordings are provided so you can catch up at a time that suits you."),
        ("Do I need to speak Arabic?", "No. The Shaykh teaches in clear English and explains the Arabic where it matters."),
        ("How do I enrol?", "Use the enrol button on this page, or email info@utrujj.org and the team will guide you."),
    ],
)

class_page(
    "hadith-classes.html",
    "Hadith Classes",
    "Unlock the <em>science of Hadith.</em>",
    "By studying Hadith properly, you begin to see how these narrations fit together — like pieces of a puzzle — alongside the Quran, forming a complete picture of divine guidance.",
    "assets/img/Shaykh-Haytahm-Tamim-Hadith-Classes.webp",
    "Shaykh Haytham Tamim outside a mosque",
    "£20",
    "/ month",
    ["Monthly subscription", "Online & in person", "Recordings available", "Taught by a muhaddith"],
    "“And whatever the Messenger has given you — take.”",
    "Quran (59:7)",
    "More than <em>a saying.</em>",
    "<p>Do you wonder how the different rulings in Islam come about? How scholars evaluate different narrations and establish their authenticity? How they reconcile seemingly contradictory narrations?</p><p>This Hadith class is unique. It is not just retelling a Hadith with an explanation of its meaning, but a glimpse into the mind of the scholars and the science of Hadith. It shows you how scholars critique narrations, evaluate and reconcile differing narrations through ta‘ārud wa tarjīḥ, derive rulings, and why their interpretations vary.</p><p>Through these classes you will see how the sciences of Hadith, Usul and Fiqh intertwine — and how the narrations connect us directly to the guidance of the Prophet ﷺ.</p>",
    [
        ("Context matters", "When the Prophet ﷺ spoke, he was addressing real people in specific situations. Context unlocks meaning."),
        ("A broad perspective", "Study with a qualified muhaddith and develop a well-rounded understanding of Islam."),
        ("A personal connection", "Step into the world of the companions and witness the Prophet’s kindness, justice and patience."),
        ("Quran and Sunnah together", "See how the Prophet ﷺ was the living embodiment of the Quran and how to apply its teachings."),
    ],
    "A scholar of <em>Hadith.</em>",
    "<p>Shaykh Haytham Tamim is a scholar of hadith with a great deal of expertise in this science. He has worked with highly respected shuyukh and has conducted tahqeeq (critical verification) of 20 books in the field. He was also part of the team that published the first-ever single-volume compilation of hadith.</p><p>With 29 links in his chain of transmission, his unbroken chain of scholarship traces directly back to the Prophet ﷺ. His knowledge spans all major Islamic schools of thought, with an in-depth understanding of hadith as a discipline, including its nuances, contexts and methodologies.</p>",
    [
        ("How long is each class?", "Classes are monthly and include recordings, so you can revisit the material whenever you need."),
        ("Can I join online?", "Yes. The class is available online and in person."),
        ("Is this suitable for beginners?", "Yes. The Shaykh builds understanding step by step, making complex material accessible."),
        ("What makes this class different?", "It goes beyond the meaning of a narration into the science of how scholars verify, interpret and apply it."),
        ("How do I enrol?", "Use the enrol button on this page, or email info@utrujj.org for help."),
    ],
)


blog_featured = article_card(blog[0], featured=True)
blog_cards = "".join(article_card(item) for item in blog[1:9])
blog_body = f"""
    <section class="page-hero">
      <div class="container page-hero__inner">
        <div>
          <nav class="breadcrumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><span aria-hidden="true">/</span><span>Articles</span></nav>
          {eyebrow("Read & reflect")}
          <h1>Articles from <em>Utrujj.</em></h1>
          <p class="page-hero__lead">Explore our latest articles for insights, reflections and inspiration — covering khutbahs delivered by the Shaykh, contemporary issues, Islamic principles, spirituality and more.</p>
          <div class="page-hero__actions">
            <a class="btn btn--primary" href="https://www.utrujj.org/Blog/">Browse the full archive <svg class="icon icon--sm"><use href="#i-arrow"/></svg></a>
            <a class="link-arrow" href="qa.html">Browse Q&amp;A <svg class="icon icon--sm"><use href="#i-arrow"/></svg></a>
          </div>
        </div>
        <figure class="hero-figure hero-figure--wide">
          <div class="hero-figure__media">
            <img src="assets/img/market.jpg" alt="Fresh produce on display at a market" width="1400" height="1050">
          </div>
          <figcaption class="hero-figure__caption">Latest article<span>Facing financial difficulties as a Muslim</span></figcaption>
        </figure>
      </div>
    </section>

    <section class="section section--paper">
      <div class="container">
        <div class="filter-row" aria-label="Article categories">
          <span class="chip is-active">All</span>
          <span class="chip">Khutbah</span>
          <span class="chip">Islamic rulings</span>
          <span class="chip">Q&amp;A</span>
          <span class="chip">Family &amp; community</span>
          <span class="chip">Get close to Allah</span>
        </div>
        <div class="listing-grid">
          {blog_featured}
          {blog_cards}
        </div>
        <p class="pagination-note">Showing 9 of our latest articles. <a class="link-arrow" href="https://www.utrujj.org/Blog/">View the full archive <svg class="icon icon--sm"><use href="#i-arrow"/></svg></a></p>
      </div>
    </section>

    {cta_band("Never miss a <em>reflection.</em>", "Monthly reflections, class updates and new articles — straight to your inbox.", "Subscribe", "index.html#newsletter", "Browse booklets", "booklets.html", eyebrow_text="Stay connected")}
"""

page("blog.html", "Articles", "Read the latest articles, khutbahs and reflections from Shaykh Haytham Tamim and the Utrujj team.", "read", blog_body)


qa_cards = "".join(qa_card(item) for item in qa[:8])
qa_body = f"""
    <section class="page-hero">
      <div class="container page-hero__inner">
        <div>
          <nav class="breadcrumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><span aria-hidden="true">/</span><span>Q &amp; A</span></nav>
          {eyebrow("Questions & answers")}
          <h1>Clear answers, <em>grounded in scholarship.</em></h1>
          <p class="page-hero__lead">Browse our Q&amp;A section to dispel confusion with clear answers to the questions on your mind. Find the scholarly rulings for common issues across different schools of thought.</p>
          <div class="page-hero__actions">
            <a class="btn btn--primary" href="contact.html">Ask a question <svg class="icon icon--sm"><use href="#i-arrow"/></svg></a>
            <a class="link-arrow" href="blog.html">Read the articles <svg class="icon icon--sm"><use href="#i-arrow"/></svg></a>
          </div>
        </div>
        <figure class="hero-figure hero-figure--wide">
          <div class="hero-figure__media">
            <img src="assets/img/rumman-amin-4NPXh6uGdaw-unsplash.jpg" alt="The interior of a mosque with carved wooden arches" width="640" height="960">
          </div>
          <figcaption class="hero-figure__caption">Q &amp; A<span>Answers for everyday life</span></figcaption>
        </figure>
      </div>
    </section>

    <section class="section section--paper">
      <div class="container">
        <div class="filter-row" aria-label="Question categories">
          <span class="chip is-active">All</span>
          <span class="chip">Islamic rulings</span>
          <span class="chip">Five Pillars</span>
          <span class="chip">Family &amp; community</span>
          <span class="chip">Du‘a</span>
          <span class="chip">Muslim matters</span>
        </div>
        <div class="qa-grid">
          {qa_cards}
        </div>
        <p class="pagination-note">Showing 8 recent questions. <a class="link-arrow" href="https://www.utrujj.org/category/q-and-a/">Browse the full Q&amp;A archive <svg class="icon icon--sm"><use href="#i-arrow"/></svg></a></p>
      </div>
    </section>

    {cta_band("Still have a <em>question?</em>", "Send it to the team and we will point you to the right answer, or ask the Shaykh directly in class.", "Contact us", "contact.html", "Join a class", "tafseer-classes.html", eyebrow_text="Ask Utrujj")}
"""

page("qa.html", "Q & A", "Clear, scholarly answers to common questions about Islamic rulings, worship, family life and contemporary issues.", "read", qa_body)


booklet_cards = "".join(product_card(item, "booklet") for item in booklets)
booklets_body = f"""
    <section class="page-hero">
      <div class="container page-hero__inner">
        <div>
          <nav class="breadcrumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><span aria-hidden="true">/</span><span>Booklets</span></nav>
          {eyebrow("Read & reflect")}
          <h1>Small books, <em>deep knowledge.</em></h1>
          <p class="page-hero__lead">Deepen your knowledge with our more detailed explorations of varied topics in our e-booklets — including our very popular look at ‘Culture vs Islam’.</p>
          <div class="page-hero__actions">
            <a class="btn btn--primary" href="https://www.utrujj.org/product-category/booklets/">Browse all booklets <svg class="icon icon--sm"><use href="#i-arrow"/></svg></a>
            <a class="link-arrow" href="blog.html">Read the articles <svg class="icon icon--sm"><use href="#i-arrow"/></svg></a>
          </div>
        </div>
        <figure class="hero-figure hero-figure--wide">
          <div class="hero-figure__media">
            <img src="assets/img/pages/booklet-3.webp" alt="Cover of the Culture vs Islam booklet" width="600" height="800">
          </div>
          <figcaption class="hero-figure__caption">Featured booklet<span>Culture vs Islam</span></figcaption>
        </figure>
      </div>
    </section>

    <section class="section section--paper">
      <div class="container">
        <div class="filter-row" aria-label="Booklet topics">
          <span class="chip is-active">All booklets</span>
          <span class="chip">Free</span>
          <span class="chip">Ramadan</span>
          <span class="chip">Death &amp; the Hereafter</span>
          <span class="chip">Spirituality</span>
        </div>
        <div class="product-grid">
          {booklet_cards}
        </div>
        <div class="bundle-note">
          <p><strong>Most booklets are free.</strong> They are made possible by the generosity of our supporters and the time of our volunteers.</p>
          <a class="btn btn--primary btn--small" href="donate.html">Support the work <svg class="icon icon--sm"><use href="#i-arrow"/></svg></a>
        </div>
      </div>
    </section>

    {cta_band("Read, reflect, <em>return.</em>", "Pair a booklet with a class or a retreat, and give the knowledge time to settle.", "Explore classes", "tafseer-classes.html", "Browse Q&A", "qa.html", eyebrow_text="Go deeper")}
"""

page("booklets.html", "Booklets", "Free and low-cost e-booklets from Utrujj on culture, Ramadan, death, spirituality and Islamic living.", "read", booklets_body)


course_cards = "".join(product_card(item, "course") for item in courses[:12])
courses_body = f"""
    <section class="page-hero">
      <div class="container page-hero__inner">
        <div>
          <nav class="breadcrumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><span aria-hidden="true">/</span><span>On Demand</span></nav>
          {eyebrow("Watch & learn")}
          <h1>Learn at <em>your own pace.</em></h1>
          <p class="page-hero__lead">Benefit from Shaykh Haytham’s balanced and down-to-earth teaching style, wherever you are. Choose from a selection of recorded courses and revisit them whenever you need.</p>
          <div class="page-hero__actions">
            <a class="btn btn--primary" href="https://www.utrujj.org/product-category/on-demand/">Browse all courses <svg class="icon icon--sm"><use href="#i-arrow"/></svg></a>
            <a class="link-arrow" href="https://www.youtube.com/c/ShaykhHaythamTamim" target="_blank" rel="noopener">Free on YouTube <svg class="icon icon--sm"><use href="#i-arrow"/></svg></a>
          </div>
          <p class="page-hero__meta"><span>Recorded courses</span><span>Study anytime</span><span>Access on any device</span></p>
        </div>
        <figure class="hero-figure hero-figure--wide">
          <div class="hero-figure__media">
            <img src="assets/img/pages/course-1.webp" alt="Cover of the 5 Fiqh Maxims course" width="600" height="800">
          </div>
          <figcaption class="hero-figure__caption">On demand<span>Learn when it suits you</span></figcaption>
        </figure>
      </div>
    </section>

    <section class="section section--paper">
      <div class="container">
        <div class="filter-row" aria-label="Course topics">
          <span class="chip is-active">All courses</span>
          <span class="chip">Quran</span>
          <span class="chip">Hadith</span>
          <span class="chip">Fiqh</span>
          <span class="chip">Spirituality</span>
          <span class="chip">Free</span>
        </div>
        <div class="product-grid">
          {course_cards}
        </div>
        <div class="bundle-note">
          <p><strong>Prefer to watch for free?</strong> A variety of Shaykh Haytham’s courses are available on YouTube.</p>
          <a class="btn btn--primary btn--small" href="https://www.youtube.com/c/ShaykhHaythamTamim" target="_blank" rel="noopener">Watch on YouTube <svg class="icon icon--sm"><use href="#i-arrow"/></svg></a>
        </div>
      </div>
    </section>

    {cta_band("Study with <em>structure.</em>", "Prefer a live class with recordings and a community? Join Tafseer or Hadith.", "Explore Tafseer", "tafseer-classes.html", "Explore Hadith", "hadith-classes.html", eyebrow_text="Go further")}
"""

page("on-demand.html", "On Demand", "Learn at your own pace with recorded courses from Shaykh Haytham Tamim on Quran, Hadith, Fiqh and spirituality.", "learn", courses_body)


event_cards = ""
event_meta = [
    ("Hadith Class", "Monthly subscription", "£20 / month", "event-2.webp", "event-2.webp"),
    ("Tafseer Classes", "Twice weekly", "£50 / month", "event-3.webp", "event-3.webp"),
    ("Arabic Tafsir Circle", "Free gathering", "Free", "event-4.webp", "event-4.webp"),
]
for title, meta, price, image, _ in event_meta:
    event_cards += f"""
          <article class="event-card">
            <div class="event-card__media">
              <img src="assets/img/pages/{image}" alt="{title} at Utrujj" width="750" height="1000" loading="lazy">
              <span class="event-card__tag">Utrujj</span>
            </div>
            <div class="event-card__body">
              <p class="event-card__meta">{meta}</p>
              <h3>{title}</h3>
              <p>Join Shaykh Haytham Tamim for a class built on authentic scholarship, clear explanation and practical application.</p>
              <div class="event-card__foot">
                <span class="event-card__price">{price}</span>
                <a class="link-arrow" href="https://www.utrujj.org/events/">Details <svg class="icon icon--sm"><use href="#i-arrow"/></svg></a>
              </div>
            </div>
          </article>"""
event_cards += """
          <article class="event-card">
            <div class="event-card__media">
              <img src="assets/img/De-Vere-Reading-3.webp" alt="De Vere estate, the setting for an Utrujj retreat" width="800" height="533" loading="lazy">
              <span class="event-card__tag">Retreat</span>
            </div>
            <div class="event-card__body">
              <p class="event-card__meta">A weekend away</p>
              <h3>Retreats</h3>
              <p>Take a break from the intensity of life with a relaxing and spiritually uplifting retreat, perfect for families.</p>
              <div class="event-card__foot">
                <span class="event-card__price">Family friendly</span>
                <a class="link-arrow" href="retreats.html">Explore retreats <svg class="icon icon--sm"><use href="#i-arrow"/></svg></a>
              </div>
            </div>
          </article>"""

events_body = f"""
    <section class="page-hero">
      <div class="container page-hero__inner">
        <div>
          <nav class="breadcrumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><span aria-hidden="true">/</span><span>Events</span></nav>
          {eyebrow("Gather & grow")}
          <h1>Learning, connection <em>and growth.</em></h1>
          <p class="page-hero__lead">We organise a select number of events, including one-off online courses and talks, as well as in-person courses and family gatherings. Whether virtual or face-to-face, our events provide opportunities for learning, reflection and community connection.</p>
          <div class="page-hero__actions">
            <a class="btn btn--primary" href="https://www.utrujj.org/events/">See what’s on <svg class="icon icon--sm"><use href="#i-arrow"/></svg></a>
            <a class="link-arrow" href="index.html#newsletter">Get event updates <svg class="icon icon--sm"><use href="#i-arrow"/></svg></a>
          </div>
        </div>
        <figure class="hero-figure hero-figure--wide">
          <div class="hero-figure__media">
            <img src="assets/img/home-events-1.webp" alt="Shaykh Haytham Tamim speaking at an Utrujj event" width="800" height="533">
          </div>
          <figcaption class="hero-figure__caption">Come together<span>Learning, reflection &amp; community</span></figcaption>
        </figure>
      </div>
    </section>

    <section class="section section--paper">
      <div class="container">
        <div class="section-head">
          <div>
            {eyebrow("What’s on")}
            <h2>Ways to <em>gather.</em></h2>
          </div>
          <div class="section-intro">
            <p>Regular classes, one-off talks, family gatherings and retreats — there is a place for every season of life.</p>
          </div>
        </div>
        <div class="event-grid">{event_cards}</div>
      </div>
    </section>

    <section class="section section--blue">
      <div class="container">
        <div class="section-head">
          <div>
            {eyebrow("What to expect")}
            <h2>More than <em>a class.</em></h2>
          </div>
          <div class="section-intro">
            <p>Every gathering is designed to leave you with something to carry home.</p>
          </div>
        </div>
        <div class="value-grid">
          <article class="value-card">
            <span class="icon-tile"><svg class="icon"><use href="#i-book"/></svg></span>
            <h3>Authentic teaching</h3>
            <p>Clear, balanced scholarship that connects classical knowledge to the realities of modern life.</p>
          </article>
          <article class="value-card">
            <span class="icon-tile icon-tile--blue"><svg class="icon"><use href="#i-users"/></svg></span>
            <h3>Real community</h3>
            <p>Meet like-minded people, share a meal, and build friendships that last beyond the event.</p>
          </article>
          <article class="value-card">
            <span class="icon-tile"><svg class="icon"><use href="#i-heart"/></svg></span>
            <h3>Space to reflect</h3>
            <p>Step away from the noise and give yourself time to reflect, renew and reconnect.</p>
          </article>
        </div>
      </div>
    </section>

    {cta_band("Come <em>together.</em>", "Join us at the next class, talk or retreat. Everyone is welcome.", "See upcoming events", "https://www.utrujj.org/events/", "Explore retreats", "retreats.html", eyebrow_text="Gather with us")}
"""

page("events.html", "Events", "Upcoming Utrujj classes, talks, family gatherings and retreats — learning, connection and growth.", "attend", events_body)


timeline_html = "".join(
    f"""
          <div class="timeline-item">
            <div class="timeline-year">{year}</div>
            <div class="timeline-body">
              <h3>{esc(title)}</h3>
              <span class="timeline-place">{esc(place)}</span>
              <p>{esc(desc)}</p>
            </div>
          </div>"""
    for year, title, place, desc in retreat_timeline
)

retreats_body = f"""
    <section class="page-hero">
      <div class="container page-hero__inner">
        <div>
          <nav class="breadcrumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><span aria-hidden="true">/</span><span>Retreats</span></nav>
          {eyebrow("Retreats")}
          <h1>A journey of connection <em>and renewal.</em></h1>
          <p class="page-hero__lead">For over two decades, we have been organising spiritually enriching retreats — a unique opportunity to deepen faith, strengthen family bonds, and find inspiration in a tranquil, halal environment.</p>
          <div class="page-hero__actions">
            <a class="btn btn--primary" href="contact.html">Register your interest <svg class="icon icon--sm"><use href="#i-arrow"/></svg></a>
            <a class="link-arrow" href="https://www.utrujj.org/retreats/">See the latest retreat <svg class="icon icon--sm"><use href="#i-arrow"/></svg></a>
          </div>
          <p class="page-hero__meta"><span>Family friendly</span><span>Halal environment</span><span>Taught by the Shaykh</span></p>
        </div>
        <figure class="hero-figure hero-figure--wide">
          <div class="hero-figure__media">
            <img src="assets/img/De-Vere-Reading-3.webp" alt="De Vere estate, the setting for an Utrujj retreat" width="800" height="533">
          </div>
          <figcaption class="hero-figure__caption">Retreat 2025<span>Burleigh Court, Loughborough</span></figcaption>
        </figure>
      </div>
    </section>

    <section class="section section--paper">
      <div class="container split split--top">
        <div class="split__copy">
          {eyebrow("Retreat 2025")}
          <h2>Re-imagining <em>Prophetic vision.</em></h2>
          <p>We recently held our 25th Anniversary Retreat, marking a special milestone. With Allah’s grace, the weekend was inspiring, deeply motivational and very topical and relevant.</p>
          <p>Attendees commented on the soothing atmosphere, as well as the buzz of meeting like-minded souls seeking to deepen their connection with Allah. There were moments of seriousness and depth, as well as lighthearted fun at the lively quiz night. There was something for all ages, as adults and children benefited from the thought-provoking talks and engaging workshops.</p>
          <p>The central theme was well-researched and delivered with clarity, leaving participants feeling blessed with plenty to reflect on.</p>
        </div>
        <div class="split__media">
          <img src="assets/img/hadith-study-circle.jpg" alt="A study circle seated on the floor of a sunlit mosque" width="1200" height="675" loading="lazy">
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="section-head">
          <div>
            {eyebrow("A rich history")}
            <h2>Places we have <em>gathered.</em></h2>
          </div>
          <div class="section-intro">
            <p>From Leeds to Wales, London to De Vere Woking, our gatherings have provided a sanctuary for spiritual reflection, growth and learning, guided by distinguished scholars.</p>
          </div>
        </div>
        <div class="timeline">{timeline_html}</div>
      </div>
    </section>

    <section class="section section--blue section--tight">
      <div class="container">
        <div class="media-strip">
          <figure><img src="assets/img/De-Vere-Reading-3.webp" alt="The De Vere estate" loading="lazy"></figure>
          <figure><img src="assets/img/pages/founder-community.webp" alt="Shaykh Haytham Tamim with the community" loading="lazy"></figure>
          <figure><img src="assets/img/pages/quran-open.webp" alt="An open Quran" loading="lazy"></figure>
        </div>
      </div>
    </section>

    {cta_band("Join us on the <em>next retreat.</em>", "Register your interest and be the first to hear when bookings open.", "Register interest", "contact.html", "Explore classes", "tafseer-classes.html", eyebrow_text="Rest & renew")}
"""

page("retreats.html", "Retreats", "Spiritually enriching Utrujj retreats for families — a halal environment to relax, reflect and reconnect with Allah.", "attend", retreats_body)


donate_body = f"""
    <section class="page-hero">
      <div class="container page-hero__inner">
        <div>
          <nav class="breadcrumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><span aria-hidden="true">/</span><span>Donate</span></nav>
          {eyebrow("Support Utrujj")}
          <h1>Help spread <em>authentic knowledge.</em></h1>
          <p class="page-hero__lead">Donate to Utrujj and help us raise £15,000 this year to spread knowledge you can trust. As a foundation dedicated to disseminating authentic Islamic knowledge, much of our resources are free and the course fees we charge do not fully cover our costs.</p>
          <p class="page-hero__meta"><span>One-off or monthly</span><span>Sadaqah jariyah</span><span>Registered charity 1196901</span></p>
        </div>
        <div class="donate-card">
          <h2>Make a donation</h2>
          <p>Choose an amount to give today.</p>
          <div class="amount-grid" data-amounts>
            <button class="amount" type="button" data-amount="10">£10</button>
            <button class="amount" type="button" data-amount="25">£25</button>
            <button class="amount is-selected" type="button" data-amount="50">£50</button>
            <button class="amount" type="button" data-amount="100">£100</button>
            <button class="amount" type="button" data-amount="250">£250</button>
            <button class="amount" type="button" data-amount="500">£500</button>
            <button class="amount amount--wide" type="button" data-amount="custom">Other amount</button>
          </div>
          <a class="btn btn--primary" href="https://www.utrujj.org/donate/">Donate securely <svg class="icon icon--sm"><use href="#i-arrow"/></svg></a>
          <p class="form-note">You will be taken to our secure donation page. Every donation, no matter the size, plays a vital role.</p>
        </div>
      </div>
    </section>

    <section class="section section--paper">
      <div class="container">
        <div class="section-head">
          <div>
            {eyebrow("Your impact")}
            <h2>Knowledge you can <em>trust.</em></h2>
          </div>
          <div class="section-intro">
            <p>Your contribution is not only a personal act of sadaqah, but also a source of ongoing reward (sadaqah jariyah) if given on behalf of your loved ones.</p>
          </div>
        </div>
        <div class="impact-grid">
          <article class="impact-card">
            <strong>Free</strong>
            <h3>Resources for all</h3>
            <p>Many of our articles, Q&amp;As and booklets are free to read, download and share.</p>
          </article>
          <article class="impact-card">
            <strong>Affordable</strong>
            <h3>Classes that reach people</h3>
            <p>Course fees do not fully cover our costs. Donations keep classes accessible and prices affordable.</p>
          </article>
          <article class="impact-card">
            <strong>Ongoing</strong>
            <h3>Sadaqah jariyah</h3>
            <p>Support the transmission of knowledge and share the reward on behalf of yourself or a loved one.</p>
          </article>
        </div>
      </div>
    </section>

    <section class="section section--tight">
      <div class="container">
        <div class="quote-panel">
          <figure>
            <blockquote><p>“The believer’s shade on the Day of Resurrection will be his charity.”</p></blockquote>
            <figcaption>The blessed Prophet ﷺ · Al-Tirmidhi</figcaption>
          </figure>
        </div>
      </div>
    </section>

    <section class="section section--blue">
      <div class="container split">
        <div class="split__copy">
          {eyebrow("Other ways to give")}
          <h2>Give in the way that <em>suits you.</em></h2>
          <p><strong>One-off donation</strong> — support the work today with a single gift.</p>
          <p><strong>Monthly donation</strong> — provide steady support that helps us plan ahead.</p>
          <p><strong>Sadaqah jariyah</strong> — give on behalf of a loved one and share in the ongoing reward.</p>
          <p><strong>Leave a legacy</strong> — include Utrujj in your will and support future generations.</p>
          <a class="btn btn--primary" href="contact.html">Talk to us about giving <svg class="icon icon--sm"><use href="#i-arrow"/></svg></a>
        </div>
        <figure class="split__media split__media--arch">
          <img src="assets/img/pages/quran-open.webp" alt="A hand resting on an open Quran" width="1000" height="667" loading="lazy">
        </figure>
      </div>
    </section>

    <section class="section section--tight">
      <div class="container">
        <div class="quote-panel quote-panel--light">
          <figure>
            <blockquote><p>“Those who spend their wealth for God’s cause may be compared to a grain which sprouts into seven ears, with a hundred grains in each ear: for God grants manifold increase to whom He wills.”</p></blockquote>
            <figcaption>Quran (2:261)</figcaption>
          </figure>
        </div>
      </div>
    </section>

    {cta_band("Give knowledge. <em>Give light.</em>", "Your support helps us preserve and share authentic Islamic knowledge for generations to come.", "Donate now", "https://www.utrujj.org/donate/", "Other ways to help", "volunteer.html", navy=True, eyebrow_text="Support Utrujj")}
"""

page("donate.html", "Donate", "Donate to Utrujj Foundation and help spread authentic Islamic knowledge. One-off and monthly donations, sadaqah jariyah.", "donate", donate_body)


volunteer_body = f"""
    <section class="page-hero">
      <div class="container page-hero__inner">
        <div>
          <nav class="breadcrumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><span aria-hidden="true">/</span><a href="about.html">About</a><span aria-hidden="true">/</span><span>Volunteer</span></nav>
          {eyebrow("Volunteer with us")}
          <h1>Use your skills <em>for the Deen.</em></h1>
          <p class="page-hero__lead">Do you have skills you’d like to use in the service of Allah and His Book? Are you reliable and have some time to dedicate? If you would like to earn the reward and blessings of serving the Deen, and become part of Utrujj Foundation volunteers, please get in touch.</p>
          <div class="page-hero__actions">
            <a class="btn btn--primary" href="#volunteer-form">Apply to volunteer <svg class="icon icon--sm"><use href="#i-arrow"/></svg></a>
            <a class="link-arrow" href="our-team.html">Meet the team <svg class="icon icon--sm"><use href="#i-arrow"/></svg></a>
          </div>
        </div>
        <figure class="hero-figure hero-figure--wide">
          <div class="hero-figure__media">
            <img src="assets/img/pages/founder-community.webp" alt="Shaykh Haytham Tamim speaking with members of the community" width="1000" height="667">
          </div>
          <figcaption class="hero-figure__caption">Our community<span>Every effort counts</span></figcaption>
        </figure>
      </div>
    </section>

    <section class="section section--paper">
      <div class="container">
        <div class="section-head">
          <div>
            {eyebrow("Why volunteer")}
            <h2>Every effort <em>matters.</em></h2>
          </div>
          <div class="section-intro">
            <p>At Utrujj, we deeply value the dedication and contributions of our volunteers, without whom our work would not be possible.</p>
          </div>
        </div>
        <div class="value-grid">
          <article class="value-card">
            <span class="icon-tile"><svg class="icon"><use href="#i-heart"/></svg></span>
            <h3>Serve the Deen</h3>
            <p>Use your time and skills in the service of Allah and His Book, and share in the reward of knowledge shared.</p>
          </article>
          <article class="value-card">
            <span class="icon-tile icon-tile--blue"><svg class="icon"><use href="#i-users"/></svg></span>
            <h3>Join a community</h3>
            <p>Work alongside a warm, dedicated team of volunteers who care about authentic knowledge and people.</p>
          </article>
          <article class="value-card">
            <span class="icon-tile"><svg class="icon"><use href="#i-star"/></svg></span>
            <h3>Use your gifts</h3>
            <p>From transcription and design to events and IT, there are many ways to contribute what you already do well.</p>
          </article>
        </div>
      </div>
    </section>

    <section class="section" id="volunteer-form">
      <div class="container contact-grid">
        <div class="contact-details">
          {eyebrow("Get involved")}
          <h2>Tell us a little <em>about you.</em></h2>
          <p>We would love to hear what time you have, what skills you can offer, and what you are currently doing. There is no commitment at this stage — just a conversation.</p>
          <div class="contact-item">
            <span class="icon-tile"><svg class="icon"><use href="#i-mail"/></svg></span>
            <div><h3>Prefer email?</h3><a href="mailto:info@utrujj.org">info@utrujj.org</a></div>
          </div>
          <div class="contact-item">
            <span class="icon-tile icon-tile--blue"><svg class="icon"><use href="#i-globe"/></svg></span>
            <div><h3>Where we work</h3><p>Online, in London and across the UK.</p></div>
          </div>
        </div>
        <div class="form-card">
          <h2>Volunteer application</h2>
          <p>All fields help us find the right way for you to contribute.</p>
          <form data-contact>
            <div class="form-grid">
              <div class="field"><label for="vol-name">Name</label><input id="vol-name" name="name" type="text" autocomplete="name" required></div>
              <div class="field"><label for="vol-email">Email</label><input id="vol-email" name="email" type="email" autocomplete="email" required></div>
              <div class="field field--full"><label for="vol-time">How much time do you have?</label><input id="vol-time" name="time" type="text" placeholder="e.g. a few hours a week" required></div>
              <div class="field field--full"><label for="vol-skills">What skills do you have?</label><textarea id="vol-skills" name="skills" required></textarea></div>
              <div class="field field--full"><label for="vol-role">What is your current role?</label><input id="vol-role" name="role" type="text"></div>
            </div>
            <button class="btn btn--primary" type="submit">Send application <svg class="icon icon--sm"><use href="#i-arrow"/></svg></button>
            <p class="form-note" data-form-note>We will only use these details to discuss volunteering with you.</p>
          </form>
        </div>
      </div>
    </section>

    {cta_band("Ready to <em>serve?</em>", "If you have time, skills and a desire to help, we would love to hear from you.", "Apply to volunteer", "#volunteer-form", "Support our work", "donate.html", eyebrow_text="Join the team")}
"""

page("volunteer.html", "Volunteer", "Volunteer with Utrujj Foundation — use your skills in the service of authentic Islamic knowledge and join a dedicated team.", "about", volunteer_body)


privacy_text = (DATA / "privacy.txt").read_text() if (DATA / "privacy.txt").exists() else ""
# Build privacy sections from the live text.
privacy_sections = [
    ("who-we-are", "Who we are", "<p>Utrujj Foundation is a UK registered charity #1196901. Our website address is <a href=\"https://www.utrujj.org/\">https://www.utrujj.org/</a>.</p>"),
    ("what-we-collect", "What personal data we collect and why we collect it", """
      <ul>
        <li>We will collect your name and email address if you subscribe to our mailing list or register for a course. This information is collected so we can communicate information about the course or about courses or events we may run or be involved with or where any of our teachers may be involved with.</li>
        <li>Where you have provided your mobile number in relation to any courses we will only use this to contact you in relation to the course.</li>
        <li>Where you have provided any details in relation to donations you may have made to us, we will only use this information for our administrative purposes in dealing with the donations and related matters such as claiming tax back from the tax authorities etc.</li>
        <li>Where you may provide details to us for any other purposes, such as wishing to volunteer or requesting for a course or booking a teacher, we will only retain that information for the purpose it was provided and to deal with it in relation to the relevant request.</li>
      </ul>"""),
    ("cookies", "Cookies", """
      <ul>
        <li>If you leave a comment on our site you may opt-in to saving your name, email address and website in cookies. These are for your convenience so that you do not have to fill in your details again when you leave another comment. These cookies will last for one year.</li>
        <li>If you have an account and you log in to this site, we will set a temporary cookie to determine if your browser accepts cookies. This cookie contains no personal data and is discarded when you close your browser.</li>
        <li>When you log in, we will also set up several cookies to save your login information and your screen display choices. Login cookies last for two days, and screen options cookies last for a year. If you select “Remember Me”, your login will persist for two weeks. If you log out of your account, the login cookies will be removed.</li>
        <li>If you edit or publish an article, an additional cookie will be saved in your browser. This cookie includes no personal data and simply indicates the post ID of the article you just edited. It expires after 1 day.</li>
      </ul>"""),
    ("embedded", "Embedded content from other websites", """
      <ul>
        <li>Articles on this site may include embedded content (e.g. videos, images, articles, etc.). Embedded content from other websites behaves in the exact same way as if the visitor has visited the other website.</li>
        <li>These websites may collect data about you, use cookies, embed additional third-party tracking, and monitor your interaction with that embedded content, including tracing your interaction with the embedded content if you have an account and are logged in to that website.</li>
      </ul>"""),
    ("sharing", "Who we share your data with", """
      <ul>
        <li>We use the email platform Brevo to send transactional emails and newsletters. We store your name and email address in Brevo's distribution list.</li>
        <li>We will never sell or share your personal data or other information you may provide with any third party other than where we may be required to by law or any regulations that may require us to do so.</li>
      </ul>"""),
    ("retention", "How long we retain your data", """
      <ul>
        <li>If you leave a comment, the comment and its metadata are retained indefinitely. This is so we can recognise and approve any follow-up comments automatically instead of holding them in a moderation queue.</li>
        <li>For users that register on our website, we also store the personal information they provide in their user profile. All users can see, edit, or delete their personal information at any time (except they cannot change their username). Website administrators can also see and edit that information.</li>
      </ul>"""),
    ("rights", "What rights you have over your data", """
      <ul>
        <li>If you have an account on this site, or have left comments, you can request to receive an exported file of the personal data we hold about you, including any data you have provided to us.</li>
        <li>You can also request that we erase any personal data we hold about you. This does not include any data we are obliged to keep for administrative, legal, or security purposes.</li>
      </ul>"""),
    ("where", "Where we send your data", "<p>Visitor comments may be checked through an automated spam detection service.</p>"),
]

privacy_toc = "".join(f'<a href="#{slug}">{label}</a>' for slug, label, _ in privacy_sections)
privacy_sections_html = "".join(f'<section id="{slug}"><h2>{label}</h2>{content}</section>' for slug, label, content in privacy_sections)
privacy_body = f"""
    <section class="page-hero page-hero--center">
      <div class="container page-hero__inner">
        <div>
          <nav class="breadcrumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><span aria-hidden="true">/</span><span>Privacy Policy</span></nav>
          {eyebrow("Legal")}
          <h1>Privacy <em>policy.</em></h1>
          <p class="page-hero__lead">How Utrujj Foundation collects, uses and protects your personal data.</p>
        </div>
      </div>
    </section>

    <section class="section section--paper">
      <div class="container legal-layout">
        <aside class="legal-toc" aria-label="On this page">
          <p>On this page</p>
          {privacy_toc}
        </aside>
        <div class="prose">
          {privacy_sections_html}
          <section id="contact">
            <h2>Contact</h2>
            <p>If you have any questions about this privacy policy or your personal data, please email <a href="mailto:info@utrujj.org">info@utrujj.org</a>.</p>
          </section>
        </div>
      </div>
    </section>

    {cta_band("Questions about your <em>data?</em>", "Email the team and we will help with any privacy request.", "Contact us", "contact.html", eyebrow_text="We are here to help")}
"""

page("privacy-policy.html", "Privacy Policy", "How Utrujj Foundation collects, uses, stores and protects your personal data.", "about", privacy_body)


error_body = f"""
    <section class="error-page">
      <div class="container">
        <p class="error-page__arabic" lang="ar" dir="rtl">الأُتْرُجَّة</p>
        {eyebrow("Page not found")}
        <h1>404</h1>
        <p>The page you are looking for has moved or no longer exists. Let’s guide you back to something beneficial.</p>
        <div class="page-hero__actions" style="justify-content:center">
          <a class="btn btn--primary" href="index.html">Back to home <svg class="icon icon--sm"><use href="#i-arrow"/></svg></a>
          <a class="link-arrow" href="blog.html">Read an article <svg class="icon icon--sm"><use href="#i-arrow"/></svg></a>
        </div>
      </div>
    </section>
"""
page("404.html", "Page not found", "The page you are looking for could not be found.", None, error_body, page_key="404")

print("Build complete.")
