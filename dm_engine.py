#!/usr/bin/env python3
# dm_engine.py — shared per-lead human DM generator for KB Rewaq.
# English, no em-dash, Jarvis intro, automation story, NO price in first message.
# Varies opener/about/pitch/close so no two DMs read identical.
import os

GITHUB_BASE = "https://faizanbashar215.github.io/kb-rewaq-digital/fresh_sites"

openers = [
    "Hey {name}", "Hi {name}", "Hello {name}", "Good day {name}", "Hi there {name}",
]
about = [
    "I'm Jarvis, manager at KB Rewaq Digital. I build automation systems for Kuwait salons and spas.",
    "This is Jarvis from KB Rewaq Digital. I run automation for Kuwait beauty businesses.",
    "Jarvis here, I manage KB Rewaq Digital where we automate Kuwait salons end to end.",
    "I'm Jarvis, I look after KB Rewaq Digital and we set up automation for Kuwait salons.",
    "Hey, Jarvis from KB Rewaq Digital. We handle automation for salons across Kuwait.",
]
pitch = [
    "Your business gets a live website, a services page, Instagram content, and a WhatsApp booking bot that replies to clients 24/7 while you focus on the salon.",
    "We give your salon a live site, social posts, and a WhatsApp bot that books clients for you around the clock.",
    "You get a website, fresh Instagram content, and an auto-reply WhatsApp that takes bookings even when you are busy with clients.",
    "The setup is a website plus Instagram plus a WhatsApp assistant that handles client bookings on its own.",
    "We put your salon on a website, keep Instagram active, and let a WhatsApp bot answer booking requests day and night.",
]
close = [
    "I saw {name} and your setup would fit this really well. I can put together a free demo of your own site in a day. Want me to send it over?",
    "I came across {name} and thought your place would suit this perfectly. I will build a free demo site for you in a day if you want to see it.",
    "Your salon {name} caught my eye and this system would suit you. I can show you a free demo of your own site within a day.",
    "I noticed {name} and believe this would work great for you. A free demo of your site takes me about a day to make. Shall I send it?",
    "{name} stood out to me and I think automation would lift your bookings. I can draft a free demo site for you in a day. Interested?",
]


def compose_dm(name, area, site_slug, idx):
    """Compose a unique human DM for lead at index idx."""
    area_note = f" Based in {area}." if area else ""
    dm = (f"{openers[idx % 5]}. {about[(idx + 1) % 5]}{area_note} "
          f"{pitch[(idx + 2) % 5]} {close[(idx + 2) % 5]}")
    dm = dm.replace("{name}", name)
    if site_slug:
        dm += f"\n\nHere is your free demo site: {GITHUB_BASE}/{site_slug}/"
    return dm


def site_url_for(slug):
    return f"{GITHUB_BASE}/{slug}/"
