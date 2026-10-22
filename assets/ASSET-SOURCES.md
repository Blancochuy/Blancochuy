# README visual sources

- `brands/saleshow.png`: the favicon served by https://saleshow.app/favicon.ico
- `brands/queueup.png`: the favicon served by https://www.queueup.quest/favicon.ico
- `brands/queueup-original.svg`: the scalable logo declared in QueueUp's public web app manifest, from https://www.queueup.quest/images/logo.svg
- `brands/portfolio.png`: the favicon served by https://blancochuy.dev/favicon.ico
- `brands/jarvis.png`: an original geometric mark representing the owner's personal AI agent.
- Technology paths: https://github.com/simple-icons/simple-icons, with individual source URLs recorded in `technology-icons.json`.

Favicons were retrieved on October 22, 2026. They identify the owner's linked projects;
their colors are preserved. Badges describe roles and technologies, not live metrics.
All displayed resources are checked into this repository and need no badge service.

Regenerate project headers and badges with Python and Pillow:

```sh
python -m pip install -r scripts/requirements.txt
python scripts/build-readme-assets.py
```

The script uses locally installed Segoe UI on Windows or DejaVu Sans on Linux.
The existing banner and technology strip are preserved.
Compact project headers and a two-row toolkit are selected below 800 px to keep
the logos and names readable on narrow displays.
