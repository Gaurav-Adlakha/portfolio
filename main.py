import numpy as np, pickle, yaml
from pathlib import Path
from typing import Union, List, Dict, Tuple, Optional, Callable
import os
from dataclasses import dataclass
from fastcore.utils import *
from execnb.nbio import read_nb
from execnb.shell import CaptureShell
from fasthtml.common import *
from monsterui.all import *
print("test")

# Font links - Inter (modern, used by Vercel, Linear, etc.) + IBM Plex Mono for code
font_links = (
    Link(rel="preconnect", href="https://fonts.googleapis.com"),
    Link(rel="preconnect", href="https://fonts.gstatic.com", crossorigin=""),
    Link(rel="stylesheet", href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap"),
)

# Inline styles to ensure clean look
clean_styles = Style("""
    body { font-family: 'IBM Plex Sans', sans-serif; background: #fff; }
    code, pre { font-family: 'IBM Plex Mono', monospace; }
    .hero-section, section, main { background: #fff !important; }
""")

app, rt = fast_app(
    hdrs=(
        Theme.slate.headers(mode='light', highlightjs=True, katex=True),
        *font_links,
        clean_styles,
        Link(rel="stylesheet", href="/static/styles.css"),
    ),
    live=True
)

def create_navbar():
    # Brand: small profile pic + name (like reference website)
    brand = A(
        Img(src="/static/image/profile.jpg", alt="Gaurav", cls="w-6 h-6 rounded-full object-cover"),
        Span("Gaurav Adlakha", cls="ml-2"),
        href="/", cls="flex items-center text-base font-semibold"
    )
    # Navigation links
    nav_links = Div(
        A("About", href="/about", cls="hover:text-primary transition-colors"),
        A("Blog", href="/blogs", cls="hover:text-primary transition-colors"),
        cls="flex items-center space-x-4"
    )
    return Nav(
        Div(brand, nav_links, cls="flex items-center justify-between p-4"),
        cls="border rounded-lg shadow-sm bg-white max-w-2xl mx-auto mt-4"
    )

def create_improved_hero():
    """Clean, professional hero section inspired by reference website"""
    # Social links (like reference website's footer but in hero)
    socials = [
        ("github", "https://github.com/Gaurav-Adlakha"),
        ("linkedin", "https://www.linkedin.com/in/gaurav-adlakha-406b1648/"),
        ("file-text", "/Resume_gaurav_adlakha.pdf"),
    ]
    social_links = Div(
        *[A(UkIcon(icon, width=18, height=18), href=url, 
            cls="hover:text-primary transition-colors", 
            target="_blank" if not url.startswith("/") else None)
          for icon, url in socials],
        cls="flex gap-4 text-muted-foreground mt-4"
    )
    
    return Main(
        Article(
            H3("Welcome", cls="text-2xl font-semibold mb-4"),
            Div(
                P("Hi, I'm Gaurav — an AI research scientist and builder."),
                P("I'm passionate about developing intelligent, scalable solutions that address real-world challenges. I thrive at the intersection of technology and problem-solving, transforming complex ideas into impactful applications."),
                P("Check out my ", A("Blog", href="/blogs", cls="text-primary underline"), " for my latest posts, or learn more ", A("About", href="/about", cls="text-primary underline"), " me."),
                cls="text-base text-muted-foreground leading-relaxed space-y-4"
            ),
            social_links,
        ),
        cls="w-full max-w-2xl mx-auto px-6 py-8"
    )

def create_about():
    """Clean, simple About section like reference website"""
    return Article(
        H2("About", cls="text-2xl font-semibold mb-4"),
        Div(
            P("I'm Gaurav Adlakha — an AI research scientist and builder based in Bangalore."),
            P("I'm passionate about developing intelligent, scalable solutions that address real-world challenges. I thrive at the intersection of technology and problem-solving, transforming complex ideas into impactful applications."),
            P("My work focuses on:"),
            Ul(
                Li("Building AI-powered applications and tools"),
                Li("Machine learning research and implementation"),
                Li("Data science and analytics"),
                cls="list-disc ml-6 space-y-2"
            ),
            P("Feel free to reach out via ", 
              A("LinkedIn", href="https://www.linkedin.com/in/gaurav-adlakha-406b1648/", cls="text-primary underline", target="_blank"),
              " or check out my work on ",
              A("GitHub", href="https://github.com/Gaurav-Adlakha", cls="text-primary underline", target="_blank"),
              "."),
            cls="text-base text-muted-foreground leading-relaxed space-y-4"
        )
    )

def create_footer():
    """Simple, clean footer like reference website"""
    socials = [
        ("github", "https://github.com/Gaurav-Adlakha"),
        ("linkedin", "https://www.linkedin.com/in/gaurav-adlakha-406b1648/"),
        ("mail", "mailto:contact@example.com"),
    ]
    social_links = Div(
        *[A(UkIcon(icon, width=20, height=20), href=url,
            cls="hover:text-primary transition-colors",
            target="_blank" if not url.startswith("mailto") else None)
          for icon, url in socials],
        cls="flex justify-center gap-6 text-muted-foreground"
    )
    return Footer(
        Divider(),
        social_links,
        cls="w-full max-w-2xl mx-auto px-6 mt-auto mb-6"
    )

def page_layout(title, *content):
    """Page layout with constrained width (max-w-2xl = 672px) like reference"""
    return Div(
        Div(create_navbar(), cls="w-full max-w-2xl mx-auto px-4 sticky top-0 z-50"),
        Main(*content, cls="w-full max-w-2xl mx-auto px-6 py-8 space-y-8"),
        create_footer(),
        cls="flex flex-col min-h-screen bg-white"
    )

def home():
    """Home page with clean hero section"""
    return Div(
        Div(create_navbar(), cls="w-full max-w-2xl mx-auto px-4 sticky top-0 z-50"),
        create_improved_hero(),
        create_footer(),
        cls="flex flex-col min-h-screen bg-white"
    )

def nb_to_markdown(nb_path):
    "Convert notebook to markdown format with executed outputs"
    shell = CaptureShell()
    nb = read_nb(nb_path)
    
    md_lines = []
    skipped_metadata = False  # Track if we've skipped the first metadata cell
    
    for cell in nb.cells:
        if cell.source.startswith('#| hide'):
            continue
        # Only skip the FIRST markdown cell that starts with '---' (YAML metadata)
        if cell.cell_type == 'markdown' and cell.source.startswith('---') and not skipped_metadata:
            skipped_metadata = True
            continue
        if cell.cell_type == 'markdown': #ignore the metadata cell
            # Fix double-escaped backslashes from some notebook editors (for LaTeX)
            source = cell.source.replace('\\\\', '\\')
            # Convert \[...\] to $$...$$ for KaTeX display math
            source = source.replace('\\[', '$$').replace('\\]', '$$')
            # Convert \(...\) to $...$ for KaTeX inline math
            source = source.replace('\\(', '$').replace('\\)', '$')
            md_lines.append(source)
            md_lines.append('')
        elif cell.cell_type == 'code':
            md_lines.append(f'```python\n{cell.source}\n```')
            
            if cell.outputs:
                md_lines.append('')
                for out in cell.outputs:
                    if 'text' in out:
                        md_lines.append('```\n' + ''.join(out['text']) + '\n```')
                    elif 'data' in out:
                        # Check for SVG first (graphviz outputs SVG)
                        if 'image/svg+xml' in out['data']:
                            svg_data = ''.join(out['data']['image/svg+xml'])
                            md_lines.append(f'<div class="graphviz-output">{svg_data}</div>')
                        elif 'image/png' in out['data']:
                            img_data = out['data']['image/png']
                            md_lines.append(f'![](data:image/png;base64,{img_data})')
                        elif 'image/jpeg' in out['data']:
                            img_data = out['data']['image/jpeg']
                            md_lines.append(f'![](data:image/jpeg;base64,{img_data})')
                        elif 'text/plain' in out['data']:
                            txt = ''.join(out['data']['text/plain'])
                            # Skip graphviz repr strings like <graphviz.graphs.Digraph at 0x...>
                            if not txt.strip().startswith('<graphviz.'):
                                md_lines.append('```\n' + txt + '\n```')
                        elif 'text/markdown' in out['data']:
                            md_markdown = ''.join(out['data']['text/markdown'])
                            md_lines.append(md_markdown)
                        elif 'text/html' in out['data']:
                            html_content = ''.join(out['data']['text/html'])
                            md_lines.append(f'<div class="notebook-html-output">{Safe(html_content)}</div>')
            md_lines.append('')
    
    return '\n'.join(md_lines)

def parse_notebook_file(file_path):
    nb = read_nb(file_path)
    meta_dict = {}
    
    if nb.cells and nb.cells[0].source.startswith('---'):
        parts = nb.cells[0].source.split("---", 2)
        if len(parts) >= 3:
            meta_str = parts[1].strip()
            meta_dict = yaml.safe_load(meta_str)
    
    meta_dict['file_name'] = file_path.name
    return meta_dict, nb

def get_notebook_content(file_path):
    shell = CaptureShell()
    nb = read_nb(file_path)
    # shell.run_all(nb)  # Uncomment to execute notebook (not recommended for production)
    
    md_content = nb_to_markdown(file_path)
    return nb, md_content

def create_toc(content):
    "Create a table of contents from markdown content with proper nesting"
    headings = []
    in_fence = False
    
    for line in content.split('\n'):
        # Toggle fence state when we see ```
        if line.startswith('```'):
            in_fence = not in_fence
            continue
        
        # Only look for headings when NOT inside a fence
        if not in_fence and line.startswith('#'):
            level = line.count('#', 0, line.find(' '))
            title = line[level+1:].strip()
            id = title.lower().replace(' ', '-').replace('?', '').replace('!', '').replace('.', '').replace('"', '').replace(':', '').replace('(', '').replace(')', '')
            headings.append((level, title, id))
    
    # Create nested structure based on heading levels
    toc_html = []
    current_level = 0
    
    for i, (level, title, id) in enumerate(headings):
        # Add closing tags for previous levels if needed
        if i > 0 and level < current_level:
            # Close the appropriate number of nested lists
            for _ in range(current_level - level):
                toc_html.append('</ul>')
        
        # Open a new list if level increases
        if i == 0 or level > current_level:
            toc_html.append('<ul class="toc-list">')
        
        # Add the list item with appropriate class
        toc_html.append(f'<li class="toc-item toc-level-{level}">')
        toc_html.append(f'<a href="#{id}" class="toc-link" data-level="{level}">{title}</a>')
        toc_html.append('</li>')
        
        current_level = level
    
    # Close any remaining open lists
    for _ in range(current_level):
        toc_html.append('</ul>')
    
    toc_html = '\n'.join(toc_html)
    
    # Add anchor IDs to headings in content
    for level, title, id in headings:
        old_heading = f"{'#' * level} {title}"
        new_heading = f"{'#' * level} <a id=\"{id}\"></a>{title}"
        content = content.replace(old_heading, new_heading, 1)
    
    # Return just the TOC links (no container - that's handled by the layout)
    toc_with_header = f'''
    <h4 class="toc-header">Contents</h4>
    {toc_html}
    '''
    
    return Safe(toc_with_header), content


def get_all_metadata():
    post_filenames = Path('static').ls(file_exts=['.ipynb'])
    if not post_filenames: return []
    files = post_filenames.map(parse_notebook_file)
    return [f[0] for f in files]



def create_blog_card_from_metadata(meta_dict, blog_id):
    """Simple, clean blog card like reference website"""
    title = meta_dict.get('title', 'No Title')
    desc = meta_dict.get('description', '')
    date = meta_dict.get('date', '')
    tags = meta_dict.get('categories', [])
    file_name = meta_dict.get('file_name', '')
    
    # Tag pills
    tag_pills = Div(
        *[Span(tag, cls="text-xs px-2 py-1 rounded border bg-muted") for tag in tags],
        cls="flex gap-2 flex-wrap"
    ) if tags else None
    
    # Date and tags row
    meta_row = Div(
        Span(date, cls="text-sm text-muted-foreground"),
        tag_pills,
        cls="flex justify-between items-center"
    )
    
    return Div(
        A(H3(title, cls="font-medium hover:underline"), href=posts.to(filename=file_name)),
        P(desc, cls="text-muted-foreground text-sm leading-relaxed mt-1") if desc else None,
        meta_row,
        cls="space-y-2 border-b pb-4 mb-4"
    )

def get_all_blog_cards():
    metadata_list = get_all_metadata()
    blog_ids = [f"post-{i}" for i in range(len(metadata_list))]
    return L(zip(metadata_list, blog_ids)).starmap(create_blog_card_from_metadata)

def create_blog_list():
    """Blog list with clean, simple card layout"""
    return page_layout(
        "Blog",
        H2("Blog", cls="text-2xl font-semibold mb-4"),
        Div(
            *get_all_blog_cards(),
            cls="space-y-6"
        )
    )

def display_post(filename):
    if not filename.endswith('.ipynb'): filename = f"{filename}.ipynb"
    
    file_path = Path('static')/filename
    if not file_path.exists(): 
        return Titled("Post Not Found", P(f"The post {filename} was not found"))
    
    # Get metadata and notebook content
    meta_dict, nb = parse_notebook_file(file_path)
    
    # Get markdown content from notebook
    _, md_content = get_notebook_content(file_path)
    
    # Get both TOC and updated content with IDs
    toc, content_with_ids = create_toc(md_content)
    
    # Tags
    tags = meta_dict.get('categories', [])
    tag_pills = Div(
        *[Span(tag, cls="text-xs px-2 py-1 rounded border bg-muted") for tag in tags],
        cls="flex gap-2 flex-wrap"
    ) if tags else None
    
    # Blog post - two column layout with TOC on right
    return Div(
        Div(create_navbar(), cls="w-full max-w-5xl mx-auto px-4"),
        Div(
            # Left column: Main content
            Article(
                H1(meta_dict.get('title', 'Untitled Post')),
                Div(
                    Span(meta_dict.get('date', ''), style="color:#6b7280; font-size:14px"),
                    tag_pills,
                    cls="flex items-center gap-3 mb-6 flex-wrap"
                ),
                Div(Safe(render_md(content_with_ids)), cls="prose"),
            ),
            # Right column: TOC sidebar (sticky)
            Aside(toc, style="position:sticky; top:2rem; max-height:calc(100vh - 4rem); overflow-y:auto;"),
            cls="blog-layout",
            style="display:grid; grid-template-columns: 1fr 200px; gap: 3rem; max-width: 100%; margin: 0 auto; padding: 2rem 4rem; align-items: start;"
        ),
        create_footer(),
        cls="flex flex-col min-h-screen bg-white"
    )

@rt
def posts(filename: str = None):
    "Display a blog post from a QMD file"
    if not filename:
        return Titled("No Post Selected", 
                     P("Please select a blog post to view"),
                     Button("Back to Blog List", href="/blogs", cls=ButtonT.primary))
    
    return display_post(filename)

@rt
def index():
    return Title("Gaurav's Portfolio - Home"), home()

@rt
def about():
    return Title("About Me - Gaurav's Portfolio"), page_layout("About", create_about())

@rt
def blogs():
    return Title(
        "Blog - Gaurav's Portfolio"), create_blog_list()

serve()
