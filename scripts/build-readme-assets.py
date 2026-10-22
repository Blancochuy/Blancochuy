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

def project_header(name, title, subtitle, category, light=False):
    bg = '#eae4d8' if light else '#20262b'
    ink = '#262c29' if light else '#f2eee5'
    secondary = '#576259' if light else '#b3c3b9'
    im = Image.new('RGB', (1120 * SCALE, 128 * SCALE), bg)
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
    f = font(12, mono=True)
    width = d.textbbox((0, 0), category, font=f)[2] / SCALE + 28
    x = 1090 - width
    rect(d, (x, 29, 1090, 58), '#d8e2d4' if light else '#31463a', radius=5)
    text(d, (x + 14, 34), category, 12, '#3c5c44' if light else '#c1e2ca', mono=True)
    im.save(ASSETS / f'projects/{name}.png', optimize=True)

def badge(filename, label, mark=None):
    icon = ''
    offset = 13
    if mark:
        data = ICONS[mark]
        icon = f'<svg x="11" y="7" width="16" height="16" viewBox="{data["viewBox"]}" fill="#b9ddc3">' + ''.join(f'<path d="{escape(p)}"/>' for p in data['paths']) + '</svg>'
        offset = 35
    width = round(len(label) * 7.25 + offset + 13)
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="30" viewBox="0 0 {width} 30" role="img" aria-label="{escape(label)}"><title>{escape(label)}</title><rect x=".5" y=".5" width="{width-1}" height="29" rx="5" fill="#202a25" stroke="#405449"/>{icon}<text x="{offset}" y="20" font-family="DejaVu Sans, Arial, sans-serif" font-size="12" fill="#e2ece5">{escape(label)}</text></svg>'
    (ASSETS / f'badges/{filename}.svg').write_text(svg, encoding='utf-8')

def portfolio_badge():
    im = Image.new('RGB', (112 * SCALE, 30 * SCALE), '#202a25')
    d = ImageDraw.Draw(im)
    rect(d, (.5, .5, 111.5, 29.5), '#202a25', radius=5, outline='#405449')
    icon = Image.open(ASSETS / 'brands/portfolio.png').convert('RGBA')
    icon = icon.resize((20 * SCALE, 20 * SCALE), Image.Resampling.LANCZOS)
    im.paste(icon, (9 * SCALE, 5 * SCALE), icon)
    text(d, (37, 6), 'Portfolio', 12, '#e2ece5')
    im.save(ASSETS / 'badges/portfolio.png', optimize=True)

for directory in ['projects', 'badges', 'brands']:
    (ASSETS / directory).mkdir(parents=True, exist_ok=True)
ICONS = json.loads((ASSETS / 'technology-icons.json').read_text(encoding='utf-8'))
jarvis_mark()
project_header('saleshow', 'Saleshow.app', 'Architecture, APIs and product delivery', 'B2B SAAS / LATAM', light=True)
project_header('queueup', 'QueueUp.quest', 'Payments, players and community integrations', 'GAMING PLATFORM')
project_header('jarvis', 'JARVIS', 'A personal AI agent, running on my own infrastructure', 'SELF-HOSTED AI')
for filename, label, mark in [
    ('typescript', 'TypeScript', 'typescript'), ('nextjs', 'Next.js', 'nextdotjs'),
    ('supabase', 'Supabase', 'supabase'), ('docker', 'Docker', 'docker'),
    ('coolify', 'Coolify', 'coolify'), ('mcp', 'MCP', 'modelcontextprotocol'),
    ('stripe', 'Stripe', None), ('architecture', 'Architecture', None),
    ('apis', 'Backend APIs', None), ('delivery', 'Deployment', None),
    ('linkedin', 'LinkedIn', None),
    ('email', 'Get in touch', None),
]:
    badge(filename, label, mark)
portfolio_badge()
print('Generated 3 project headers, 13 badges and JARVIS mark.')
