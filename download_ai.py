#!/usr/bin/env python3
"""Download all generated FLUX images to assets/ai/ with stable names.
Maps: hero_*.png(5) + gal_*.png(10) + test already saved.
"""
import os, urllib.request, ssl

os.makedirs("assets/ai", exist_ok=True)
ctx = ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE

URLS = {
 "assets/ai/hero_midyaf.png":"https://v3b.fal.media/files/b/0aa5ab88/U-aAKDxwc4Bj8XyEIXXqT_3EPuoqXv.png",
 "assets/ai/hero_looknoor.png":"https://v3b.fal.media/files/b/0aa5ab88/Wo-0OrqdlILlsr6013nTz_Xyb6HVkF.png",
 "assets/ai/hero_monya.png":"https://v3b.fal.media/files/b/0aa5ab99/dZc-tat7V1nihmxNYHT_B_TkIRIkei.png",
 "assets/ai/hero_royaljasmine.png":"https://v3b.fal.media/files/b/0aa5ab88/f9oSzV8iCK-yIIaYRtr_0_NtSutr5K.png",
 "assets/ai/hero_larene.png":"https://v3b.fal.media/files/b/0aa5ab88/NZgBnRatIaLKi_PdnPL_t_wLp3pc1q.png",
 "assets/ai/gal_manicure.png":"https://v3b.fal.media/files/b/0aa5ab8a/FgAGWbEoH8PCHgw3NoLWl_RyEXUnCq.png",
 "assets/ai/gal_hair.png":"https://v3b.fal.media/files/b/0aa5ab9b/BcuvgorJeLEIcVEjUsVrG_ZafqgQmm.png",
 "assets/ai/gal_facial.png":"https://v3b.fal.media/files/b/0aa5ab8a/Eu2jVXvoqFs0hVdcO9hMp_I0KQM7oL.png",
 "assets/ai/gal_bridal.png":"https://v3b.fal.media/files/b/0aa5ab8a/u8_oRg9OIUTrq2-UphkIM_9g7zJPOY.png",
 "assets/ai/gal_pedicure.png":"https://v3b.fal.media/files/b/0aa5ab8a/olDBYKnFIVitDWZ28MBlo_nl9ANrkd.png",
}
for path,url in URLS.items():
    if os.path.exists(path) and os.path.getsize(path)>100000:
        print("skip",path); continue
    try:
        urllib.request.urlretrieve(url, path)  # nosec
        print("saved",path, os.path.getsize(path))
    except Exception as e:
        print("FAIL",path,e)
print("done")
