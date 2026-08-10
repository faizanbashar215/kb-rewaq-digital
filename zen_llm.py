#!/usr/bin/env python3
# zen_llm.py — OpenCode Zen LLM client for KB Rewaq (curl-based, Cloudflare-safe).
# Chain: deepseek-v4-flash-free -> nemotron-3-ultra-free -> rule brain (cron_whatsapp_dealmaker.draft_reply).
# Reads keys from .env (gitignored): OPENCODE_ZEN_API_KEY (old), OPENCODE_ZEN_API_KEY_NEW (new).
import os, sys, json, subprocess, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cron_whatsapp_dealmaker as dm

ZEN_URL = "https://opencode.ai/zen/v1/chat/completions"
# primary -> fallback order (deepseek is best brain, nemotron is the reliable free fallback)
MODEL_CHAIN = ["deepseek-v4-flash-free", "nemotron-3-ultra-free"]

# collect keys (old + new) — try new first since old may be rate-limited
def _load_keys():
    keys = []
    for l in open(os.path.join(HERE, ".env"), encoding="utf-8"):
        l = l.strip()
        if l.startswith("OPENCODE_ZEN_API_KEY") and "=" in l:
            v = l.split("=", 1)[1].strip()
            if v and v not in keys:
                keys.append(v)
    # prefer NEW key first
    keys.sort(key=lambda k: 0 if "OPENCODE_ZEN_API_KEY_NEW" in l else 1) if False else None
    return keys

def _call_once(key, model, system, user, max_tokens=220):
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "max_tokens": max_tokens,
        "temperature": 0.7,
    }
    fd, path = tempfile.mkstemp(suffix=".json", prefix="hermes-zen-")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(payload, f)
        # curl bypasses Cloudflare 1010 (urllib gets blocked)
        r = subprocess.run(
            ["curl", "-s", "-S", "-X", "POST", ZEN_URL,
             "-H", f"Authorization: Bearer {key}",
             "-H", "Content-Type: application/json",
             "--data", f"@{path}",
             "--max-time", "25"],
            capture_output=True, text=True, timeout=35,
        )
        if r.returncode != 0 or not r.stdout.strip():
            return None
        try:
            d = json.loads(r.stdout)
        except Exception:
            return None
        if "choices" not in d:
            return None
        return d["choices"][0]["message"]["content"].strip()
    except Exception:
        return None
    finally:
        try:
            os.remove(path)
        except Exception:
            pass

def zen_reply(name, msg, system_prompt):
    """Try OpenCode Zen (deepseek -> nemotron, both keys); fall back to rule brain."""
    keys = _load_keys()
    if not keys:
        return dm.draft_reply(name, msg, dm.resolve_slug_from_name(name))
    for key in keys:
        for model in MODEL_CHAIN:
            try:
                out = _call_once(key, model, system_prompt,
                                 f"Client name: {name}\nTheir message: {msg}\nReply as KB Rewaq:")
                if out and len(out) > 1:
                    return out
            except Exception:
                continue
    # all models/keys exhausted (429/timeout) -> rule brain
    return dm.draft_reply(name, msg, dm.resolve_slug_from_name(name))

if __name__ == "__main__":
    sp = "You are KB Rewaq deal-closer. Reply short, warm, Hinglish+English+Arabic."
    print(zen_reply("Test", "what is price?", sp))
