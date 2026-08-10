import json, urllib.request, os

keys = {}
for l in open(".env", encoding="utf-8"):
    l = l.strip()
    if l.startswith("OPENCODE_ZEN_API_KEY"):
        k, v = l.split("=", 1)
        keys[k] = v.strip()

print("keys:", list(keys.keys()))

# correct names from Hermes config: deepseek-v4-flash-free, plus your requested deepseek + nemotron-ultra-3
models = [
    "deepseek-v4-flash-free",
    "deepseek",
    "deepseek-v3",
    "deepseek-chat",
    "nemotron-ultra-3",
    "nvidia/nemotron-ultra-3",
    "nemotron-ultra-3-253-tpt",
]

for kn, key in keys.items():
    print("===", kn, "===")
    for m in models:
        payload = json.dumps({
            "model": m,
            "messages": [{"role": "user", "content": "say hi in 2 words"}],
        }).encode()
        req = urllib.request.Request(
            "https://opencode.ai/zen/v1/chat/completions",
            data=payload,
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {key}"},
        )
        try:
            r = urllib.request.urlopen(req, timeout=15)
            d = json.loads(r.read())
            print("OK  ", m, "->", d["choices"][0]["message"]["content"][:30])
        except urllib.error.HTTPError as e:
            body = e.read().decode()[:80]
            print("FAIL", m, "->", e.code, body)
        except Exception as e:
            print("FAIL", m, "->", str(e)[:45])
