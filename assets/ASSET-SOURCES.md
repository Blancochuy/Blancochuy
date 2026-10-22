# README visual sources

- `brands/saleshow.png`: the favicon served by https://saleshow.app/favicon.ico
- `brands/queueup.png`: the favicon served by https://www.queueup.quest/favicon.ico
- `brands/queueup-original.svg`: the scalable logo declared in QueueUp's public web app manifest, from https://www.queueup.quest/images/logo.svg
- `brands/portfolio.png`: the favicon served by https://blancochuy.dev/favicon.ico
- `brands/jarvis.png`: an original geometric mark representing the owner's personal AI agent.
- Technology paths: https://github.com/simple-icons/simple-icons, with individual source URLs recorded in `technology-icons.json`.
- LinkedIn mark: Bootstrap Icons, https://github.com/twbs/icons/blob/main/icons/linkedin.svg (MIT).
- Architecture, backend, deployment, email, graph memory, VR and voice glyphs: locally authored SVG line icons with a consistent 1.7 px stroke.
- Qwen and MiniMax marks: https://github.com/lobehub/lobe-icons (MIT), with original source URLs recorded in `technology-icons.json`.
- Hermes badge: the official favicon declared by https://hermes-agent.nousresearch.com/ (exact asset URL recorded in `brands/sources.json`).
- Infisical badge: the official favicon from https://infisical.com/infisical.ico (also recorded in `brands/sources.json`).
- `brands/emoji-styles.svg`: the actual favicon declared by https://emoji-styles.space (asset URL recorded in `brands/sources.json`), also published in the owner's emoji-styles repository.
- `brands/git.svg`: the Git mark from Simple Icons, used to identify git-why's Git-history focus; it is not presented as a separate git-why brand logo.
- Professional-profile and live-demo glyphs: locally authored line icons matching the existing badges. X and Go marks come from Simple Icons.

The JARVIS section distinguishes Hermes Agent, Qwen 3.8 Flash Next as the primary
model, Llama and MiniMax fallbacks, custom capabilities, and protected remote
access. These details and QueueUp's Wise integration were supplied by the owner.
Infisical is included as the agent's secrets manager, as confirmed by the owner.

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
