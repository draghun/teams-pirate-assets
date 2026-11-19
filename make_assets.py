"""Pirate artwork for the TERRAHydro GitLab feed in Teams.

    python make_assets.py      (needs Pillow)

Writes:
    icons/mr.png, icons/issue.png    card header icons (Jolly Roger, treasure map)
    celebrate/merge.gif              the celebration, shown when an MR is merged
    celebrate/<action>.gif           a transparent 1x1 GIF for every other MR action, so the
                                     card's image URL (celebrate/{{object_attributes.action}}.gif)
                                     shows nothing for them
"""
import math
import os
import random

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = "/System/Library/Fonts/Supplemental/Impact.ttf"
GOLD, DARK, NAVY = (247, 196, 46), (24, 24, 32), (20, 40, 72)
OTHER_ACTIONS = ["open", "close", "reopen", "update", "approved", "unapproved", "approval", "unapproval"]
BANNER_FONT = "/System/Library/Fonts/Supplemental/Trattatello.ttf"
# banner/<kind>/<action>.png: the pirate line for each GitLab action (the card adds the plain meaning)
BANNERS = {
    "mr": {"open": "A new ship sets sail!", "update": "The crew be patchin' the hull!",
           "approval": "A shipmate gives the nod!", "approved": "Aye! The cap'n gives the nod!",
           "unapproval": "The nod be taken back!", "unapproved": "The nod be taken back!",
           "merge": "Treasure be ours!", "close": "Scuttled!", "reopen": "Raised from Davy Jones' locker!"},
    "issue": {"open": "A new quest be posted!", "update": "The map be redrawn!",
              "close": "Quest complete! X marks the spot!", "reopen": "The quest be back on!"},
}


def banner(text, h=40):
    """Gold pirate lettering with a dark outline on a transparent strip (reads on light and dark Teams)."""
    font = ImageFont.truetype(BANNER_FONT, 28)
    tw = int(ImageDraw.Draw(Image.new("RGBA", (1, 1))).textlength(text, font=font))
    img = Image.new("RGBA", (tw + 16, h), (0, 0, 0, 0))
    ImageDraw.Draw(img).text((8, 2), text, font=font, fill=GOLD, stroke_width=2, stroke_fill=DARK)
    return img


def skull_and_bones(d, cx, cy, s, fg=(245, 245, 240), bg=DARK):
    """A Jolly Roger at (cx, cy), roughly s pixels across."""
    w = max(2, int(s // 9))
    for a, b in (((-0.45, -0.05), (0.45, 0.55)), ((0.45, -0.05), (-0.45, 0.55))):   # crossbones
        x0, y0, x1, y1 = cx + a[0] * s, cy + a[1] * s, cx + b[0] * s, cy + b[1] * s
        d.line((x0, y0, x1, y1), fill=fg, width=w)
        for x, y in ((x0, y0), (x1, y1)):
            r = w * 0.9
            d.ellipse((x - r, y - r, x + r, y + r), fill=fg)
    r = s * 0.30                                                                        # skull
    d.ellipse((cx - r, cy - r * 1.25, cx + r, cy + r * 0.55), fill=fg)
    d.rounded_rectangle((cx - r * 0.55, cy + r * 0.2, cx + r * 0.55, cy + r * 0.85), radius=r * 0.15, fill=fg)
    for ex in (-0.42, 0.42):                                                            # eyes
        er = r * 0.24
        d.ellipse((cx + ex * r - er, cy - r * 0.45 - er, cx + ex * r + er, cy - r * 0.45 + er), fill=bg)
    d.polygon([(cx, cy - r * 0.05), (cx - r * 0.12, cy + r * 0.2), (cx + r * 0.12, cy + r * 0.2)], fill=bg)
    for tx in (-0.3, 0, 0.3):                                                           # teeth
        d.line((cx + tx * r, cy + r * 0.45, cx + tx * r, cy + r * 0.85), fill=bg, width=max(1, w // 2))


def icon_mr(size=96):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse((2, 2, size - 2, size - 2), fill=DARK, outline=GOLD, width=4)
    skull_and_bones(d, size / 2, size / 2 - 2, size * 0.54)
    return img


def icon_issue(size=96):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse((2, 2, size - 2, size - 2), fill=NAVY, outline=GOLD, width=4)
    m = size * 0.24                                                                     # parchment
    d.rounded_rectangle((m, m * 1.1, size - m, size - m * 1.1), radius=6, fill=(236, 214, 160), outline=(150, 110, 60), width=2)
    pts = [(m + 6, size - m * 1.1 - 8), (size * 0.42, size * 0.55), (size * 0.5, size * 0.62), (size * 0.62, size * 0.42)]
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):                                        # dashed trail
        for t in (0.15, 0.55):
            d.line((x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, x0 + (x1 - x0) * (t + 0.25), y0 + (y1 - y0) * (t + 0.25)),
                   fill=(110, 80, 40), width=2)
    x, y, k = size * 0.66, size * 0.38, size * 0.07                                     # the X
    d.line((x - k, y - k, x + k, y + k), fill=(200, 30, 30), width=4)
    d.line((x - k, y + k, x + k, y - k), fill=(200, 30, 30), width=4)
    return img


def ship(d, cx, base, s, tilt):
    """A small pirate ship whose waterline centre is at (cx, base)."""
    hull = [(cx - s, base - s * 0.25), (cx + s, base - s * 0.25 - tilt), (cx + s * 0.7, base + s * 0.2 - tilt / 2),
            (cx - s * 0.7, base + s * 0.2 + tilt / 2)]
    d.polygon(hull, fill=(110, 62, 30), outline=(60, 32, 14))
    d.line((cx - s * 0.8, base - s * 0.12, cx + s * 0.8, base - s * 0.12 - tilt * 0.8), fill=GOLD, width=2)
    mx = cx + tilt * 0.3
    d.line((mx, base - s * 0.25, mx, base - s * 1.55), fill=(70, 40, 18), width=4)       # mast
    d.polygon([(mx + 3, base - s * 1.4), (mx + s * 0.75, base - s * 0.95), (mx + 3, base - s * 0.45)], fill=(250, 248, 236))
    d.polygon([(mx - 3, base - s * 1.3), (mx - s * 0.6, base - s * 0.85), (mx - 3, base - s * 0.5)], fill=(236, 232, 214))
    d.rectangle((mx, base - s * 1.85, mx + s * 0.5, base - s * 1.55), fill=DARK)          # flag
    skull_and_bones(d, mx + s * 0.25, base - s * 1.71, s * 0.26)


def celebrate_gif(w=360, h=200, frames=30):
    rng = random.Random(7)
    coins = [(rng.uniform(10, w - 10), rng.uniform(0, h + 40), rng.uniform(4, 7), rng.uniform(0, math.tau))
             for _ in range(26)]
    font = ImageFont.truetype(FONT, 40)
    out = []
    for f in range(frames):
        t = f / frames
        img = Image.new("RGB", (w, h), (64, 140, 214))
        d = ImageDraw.Draw(img)
        d.rectangle((0, 0, w, h * 0.45), fill=(120, 190, 240))                          # sky
        d.ellipse((w - 70, 12, w - 30, 52), fill=(255, 230, 120))                       # sun
        bob = math.sin(t * math.tau) * 4
        waves = ((40, 110, 190, 0.66), (30, 90, 170, 0.81), (20, 70, 150, 0.91))       # far wave, then near ones
        for i, (shade, amp, y0, level) in enumerate(waves):
            if i == 1:                                                                  # ship rides between them
                ship(d, w * 0.5, h * 0.75 + bob, 40, tilt=math.sin(t * math.tau) * 6)
            yb = h * level
            pts = [(x, yb + math.sin(x / 22 + t * math.tau * (1 + i * 0.5) + i) * (4 + i * 2)) for x in range(0, w + 6, 6)]
            d.polygon(pts + [(w, h), (0, h)], fill=(shade + 20, amp, y0 + 30))
        for x, y0, r, ph in coins:                                                      # coins: one loop per GIF
            y = (y0 + t * (h + 40)) % (h + 40) - 20
            x2 = x + math.sin(ph + t * math.tau) * 6
            sq = abs(math.cos(ph + t * math.tau * 2))                                   # spinning
            d.ellipse((x2 - r * sq - 1, y - r, x2 + r * sq + 1, y + r), fill=GOLD, outline=(160, 110, 20))
        text = "ARRR! MERGED!"
        tw = d.textlength(text, font=font)
        ty = 8 + abs(math.sin(t * math.tau * 2)) * -4 + 4
        d.text(((w - tw) / 2, ty), text, font=font, fill=GOLD, stroke_width=3, stroke_fill=DARK)
        out.append(img.convert("P", palette=Image.ADAPTIVE, colors=64))
    return out


def main():
    os.makedirs(f"{HERE}/icons", exist_ok=True)
    os.makedirs(f"{HERE}/celebrate", exist_ok=True)
    icon_mr().save(f"{HERE}/icons/mr.png", optimize=True)
    icon_issue().save(f"{HERE}/icons/issue.png", optimize=True)
    frames = celebrate_gif()
    frames[0].save(f"{HERE}/celebrate/merge.gif", save_all=True, append_images=frames[1:], duration=70, loop=0,
                   optimize=True, disposal=2)
    blank = Image.new("P", (1, 1), 0)
    blank.info["transparency"] = 0
    for action in OTHER_ACTIONS:
        blank.save(f"{HERE}/celebrate/{action}.gif", transparency=0)
    for kind, lines in BANNERS.items():
        os.makedirs(f"{HERE}/banner/{kind}", exist_ok=True)
        for action, text in lines.items():
            banner(text).save(f"{HERE}/banner/{kind}/{action}.png", optimize=True)
    for root, _, files in os.walk(HERE):
        for name in sorted(files):
            if name.endswith((".png", ".gif")):
                p = os.path.join(root, name)
                print(f"{os.path.relpath(p, HERE):28} {os.path.getsize(p):>7} bytes")


if __name__ == "__main__":
    main()
