#!/usr/bin/env python3
# DIAGNOSTIC: why does multi-source find 0 WA-active? Test (a) wa_active() against a KNOWN-active
# number, (b) does source_opensooq actually return candidates for one lead?
import importlib.util, os
spec = importlib.util.spec_from_file_location("ms", r"D:\digitalfirst-agency\scrape_multisource.py")
ms = importlib.util.module_from_spec(spec); spec.loader.exec_module(ms)

print("=== (a) wa_active() sanity (known-active test numbers) ===")
for t in ["96524831136", "96550000000", "15551234567"]:
    print(f"  {t}: wa_active={ms.wa_active(t)}")

print("\n=== (b) source_opensooq candidates for 'Akrram' ===")
c = ms.source_opensooq("Akrram")
print("  candidates:", c[:10])

print("\n=== (c) source_yellowpages candidates for 'Akrram' ===")
c2 = ms.source_yellowpages("Akrram")
print("  candidates:", c2[:10])

print("\n=== (d) source_instagram candidates for 'Akrram' ===")
c3 = ms.source_instagram("Akrram")
print("  candidates:", c3[:10])

print("\n=== (e) raw DDG fetch test ===")
h = ms.fetch("https://html.duckduckgo.com/html/?q=Akrram%20Kuwait%20phone")
print("  DDG html length:", len(h), "| sample phones:", ms.KW.findall(h)[:5])
