# teams-pirate-assets

Cartoon images for the TERRAHydro team's GitLab notifications in Microsoft Teams. Each GitLab webhook builds an Adaptive Card whose image URLs include the event's action, so the action picks the picture:

| Path | Shown |
|---|---|
| `icons/mr.png`, `icons/issue.png` | card header icon for merge requests and for issues |
| `banner/<mr or issue>/<action>.png` | the pirate line for that action, e.g. `banner/mr/approved.png` |
| `celebrate/merge.gif` | the celebration when a merge request is merged |
| `celebrate/<other action>.gif` | a transparent 1×1 image, so other actions show nothing |

`make_assets.py` draws them all (it needs Pillow): `python make_assets.py`.
