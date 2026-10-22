"""Generate local README visuals. Requires Pillow; run from any directory."""
from pathlib import Path
from html import escape
import json
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
SCALE = 2
FONT_DIRS = [Path('C:/Windows/Fonts'), Path('/usr/share/fonts/truetype/dejavu')]

def font(size, bold=False, mono=False):
    names = (['consola.ttf', 'DejaVuSansMono.ttf'] if mono else
             ['segoeuib.ttf', 'DejaVuSans-Bold.ttf'] if bold else
             ['segoeui.ttf', 'DejaVuSans.ttf'])
    for directory in FONT_DIRS:
        for name in names:
            if (directory / name).exists():
                return ImageFont.truetype(str(directory / name), size * SCALE)
    raise RuntimeError('Install Segoe UI or DejaVu Sans to generate the visuals.')

def rect(draw, coords, fill, radius=0, outline=None):
    coords = tuple(round(v * SCALE) for v in coords)
    if radius:
        draw.rounded_rectangle(coords, radius * SCALE, fill, outline)
    else:
        draw.rectangle(coords, fill, outline)

def text(draw, xy, value, size, fill, bold=False, mono=False):
    draw.text(tuple(round(v * SCALE) for v in xy), value, font=font(size, bold, mono), fill=fill)

def jarvis_mark():
    im = Image.new('RGBA', (192, 192))
    d = ImageDraw.Draw(im)
    d.ellipse((39, 39, 153, 153), fill='#456b57', outline='#c5e5d1', width=3)
    for box in [(42, 70, 150, 122), (45, 87, 147, 105), (70, 42, 122, 150)]:
        d.ellipse(box, outline='#a5d8b8', width=2)
    for angle in [-27, 33]:
        ring = Image.new('RGBA', im.size)
        ImageDraw.Draw(ring).ellipse((14, 65, 178, 127), outline='#bde0c9', width=2)
        im.alpha_composite(ring.rotate(angle, resample=Image.Resampling.BICUBIC))
    im.save(ASSETS / 'brands/jarvis.png')

def project_header(name, title, subtitle, category, light=False, width=1120):
    bg = '#eae4d8' if light else '#20262b'
    ink = '#262c29' if light else '#f2eee5'
    secondary = '#576259' if light else '#b3c3b9'
    im = Image.new('RGB', (width * SCALE, 128 * SCALE), bg)
    d = ImageDraw.Draw(im)
    rect(d, (0, 0, 5, 128), '#a3d4ac')
    rect(d, (25, 25, 103, 103), '#faf7ef' if light else '#151b1e', radius=13)
    icon = Image.open(ASSETS / f'brands/{name}.png').convert('RGBA')
    bounds = icon.getbbox()
    if bounds:
        icon = icon.crop(bounds)
    ratio = 58 * SCALE / max(icon.size)
    icon = icon.resize(tuple(round(v * ratio) for v in icon.size), Image.Resampling.LANCZOS)
    im.paste(icon, (64 * SCALE - icon.width // 2, 64 * SCALE - icon.height // 2), icon)
    text(d, (126, 23), title, 32, ink, bold=True)
    text(d, (128, 75), subtitle, 17, secondary)
    # Descriptive category, not an unverified uptime or activity status.
    if width > 800:
        f = font(12, mono=True)
        badge_width = d.textbbox((0, 0), category, font=f)[2] / SCALE + 28
        x = width - 30 - badge_width
        rect(d, (x, 29, width - 30, 58), '#d8e2d4' if light else '#31463a', radius=5)
        text(d, (x + 14, 34), category, 12, '#3c5c44' if light else '#c1e2ca', mono=True)
    suffix = '-compact' if width < 800 else ''
    im.save(ASSETS / f'projects/{name}{suffix}.png', optimize=True)

def compact_toolkit():
    rows = [
        [('typescript', 'TypeScript'), ('react', 'React'), ('nextdotjs', 'Next.js'), ('python', 'Python')],
        [('docker', 'Docker'), ('supabase', 'Supabase'), ('modelcontextprotocol', 'MCP')],
    ]
    marks = []
    for row, items in enumerate(rows):
        for i, (name, label) in enumerate(items):
            x = (i + 1) * 640 / (len(items) + 1)
            y = 22 + row * 112
            icon = ICONS[name]
            paths = ''.join(f'<path d="{escape(p)}"/>' for p in icon['paths'])
            marks.append(f'<svg x="{x-22}" y="{y}" width="44" height="44" viewBox="{icon["viewBox"]}" fill="#bed2c2">{paths}</svg><text x="{x}" y="{y+73}" text-anchor="middle" font-family="Consolas,monospace" font-size="16" fill="#e4e9e5">{label}</text>')
    (ASSETS / 'technology-stack-compact.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" width="640" height="240" viewBox="0 0 640 240"><title>TypeScript, React, Next.js, Python, Docker, Supabase and MCP</title><rect width="640" height="240" rx="6" fill="#1b2025"/>' + ''.join(marks) + '</svg>', encoding='utf-8')

UI_MARKS = {
    'architecture': '<path d="M3 7 12 3l9 4-9 4-9-4Zm0 5 9 4 9-4M3 17l9 4 9-4"/>',
    'backend': '<rect x="3" y="3" width="18" height="7" rx="2"/><rect x="3" y="14" width="18" height="7" rx="2"/><path d="M7 6.5h.01M7 17.5h.01M12 6.5h5M12 17.5h5"/>',
    'deployment': '<path d="M6 17a4 4 0 0 1-1-7.87 7 7 0 0 1 13.4-1.4A4.5 4.5 0 0 1 19 17M12 21V11m-4 4 4-4 4 4"/>',
    'email': '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
    'graph': '<circle cx="5" cy="6" r="2"/><circle cx="19" cy="5" r="2"/><circle cx="12" cy="12" r="2"/><circle cx="5" cy="19" r="2"/><circle cx="20" cy="19" r="2"/><path d="m7 7 3.5 3.5M14 11l3.5-4.5M10.5 13.5 6.5 17M13.5 13.5l5 4"/>',
    'vr': '<path d="M5 7h14a3 3 0 0 1 3 3v6a2 2 0 0 1-2 2h-4l-4-3-4 3H4a2 2 0 0 1-2-2v-6a3 3 0 0 1 3-3Z"/><circle cx="7" cy="12" r="1.5"/><circle cx="17" cy="12" r="1.5"/>',
    'voice': '<rect x="9" y="2" width="6" height="12" rx="3"/><path d="M5 10v2a7 7 0 0 0 14 0v-2M12 19v3m-4 0h8"/>',
}

def badge(filename, label, mark):
    offset = 35
    if mark in UI_MARKS:
        icon = '<svg x="11" y="7" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#b9ddc3" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">' + UI_MARKS[mark] + '</svg>'
    else:
        data = ICONS[mark]
        icon = f'<svg x="11" y="7" width="16" height="16" viewBox="{data["viewBox"]}" fill="#b9ddc3">' + ''.join(f'<path d="{escape(p)}"/>' for p in data['paths']) + '</svg>'
    width = round(len(label) * 7.25 + offset + 13)
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="30" viewBox="0 0 {width} 30" role="img" aria-label="{escape(label)}"><title>{escape(label)}</title><rect x=".5" y=".5" width="{width-1}" height="29" rx="5" fill="#202a25" stroke="#405449"/>{icon}<text x="{offset}" y="20" font-family="DejaVu Sans, Arial, sans-serif" font-size="12" fill="#e2ece5">{escape(label)}</text></svg>'
    (ASSETS / f'badges/{filename}.svg').write_text(svg, encoding='utf-8')

def image_badge(filename, label, source):
    width = max(100, round(len(label) * 7.25 + 48))
    im = Image.new('RGB', (width * SCALE, 30 * SCALE), '#202a25')
    d = ImageDraw.Draw(im)
    rect(d, (.5, .5, width - .5, 29.5), '#202a25', radius=5, outline='#405449')
    icon = Image.open(ASSETS / source).convert('RGBA')
    icon = icon.resize((20 * SCALE, 20 * SCALE), Image.Resampling.LANCZOS)
    im.paste(icon, (9 * SCALE, 5 * SCALE), icon)
    text(d, (37, 6), label, 12, '#e2ece5')
    im.save(ASSETS / f'badges/{filename}.png', optimize=True)

for directory in ['projects', 'badges', 'brands']:
    (ASSETS / directory).mkdir(parents=True, exist_ok=True)
ICONS = json.loads((ASSETS / 'technology-icons.json').read_text(encoding='utf-8'))
jarvis_mark()
for width in [1120, 600]:
    project_header('saleshow', 'Saleshow.app', 'Architecture, APIs and product delivery', 'B2B SAAS / LATAM', light=True, width=width)
    project_header('queueup', 'QueueUp.quest', 'Payments, players and community integrations', 'GAMING PLATFORM', width=width)
    project_header('jarvis', 'JARVIS / Hermes', 'Graph memory, custom tools and voice access', 'SELF-HOSTED AI', width=width)
compact_toolkit()
for filename, label, mark in [
    ('typescript', 'TypeScript', 'typescript'), ('nextjs', 'Next.js', 'nextdotjs'),
    ('supabase', 'Supabase', 'supabase'), ('docker', 'Docker', 'docker'),
    ('coolify', 'Coolify', 'coolify'), ('mcp', 'MCP', 'modelcontextprotocol'),
    ('stripe', 'Stripe', 'stripe'), ('wise', 'Wise', 'wise'),
    ('architecture', 'Architecture', 'architecture'),
    ('apis', 'Backend APIs', 'backend'), ('delivery', 'Deployment', 'deployment'),
    ('linkedin', 'LinkedIn', 'linkedin'),
    ('email', 'Get in touch', 'email'),
    ('github', 'GitHub', 'github'), ('vercel', 'Vercel', 'vercel'),
    ('cloudflare', 'Cloudflare', 'cloudflare'),
    ('qwen', 'Qwen 3.8 Flash Next', 'qwen'),
    ('llama', 'Llama / fallback', 'llama'), ('minimax', 'MiniMax / fallback', 'minimax'),
    ('notion', 'Notion', 'notion'), ('graph-memory', 'Graph memory', 'graph'),
    ('vr-dashboard', 'VR dashboard', 'vr'), ('siri-shortcuts', 'Siri Shortcuts', 'voice'),
    ('zero-trust', 'Cloudflare Zero Trust', 'cloudflare'),
]:
    badge(filename, label, mark)
image_badge('portfolio', 'Portfolio', 'brands/portfolio.png')
image_badge('hermes', 'Hermes Agent', 'brands/hermes.png')
image_badge('infisical', 'Infisical', 'brands/infisical.png')
print('Generated project headers, responsive toolkit and badges with explicit icons.')
