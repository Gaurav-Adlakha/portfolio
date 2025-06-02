import numpy as np, pickle, yaml
from pathlib import Path
from typing import Union, List, Dict, Tuple, Optional, Callable 
from dataclasses import dataclass
from fastcore.utils import *
from execnb.nbio import read_nb
from execnb.shell import CaptureShell
from fasthtml.common import *
from monsterui.all import *
print("test")

app, rt = fast_app(
    hdrs=(
        Theme.violet.headers(mode='light', daisy=True, highlightjs=True),
        Link(rel="stylesheet", href="/static/styles.css"),
    ),
    live=True
)

def create_navbar():
    return NavBar(
        A("Home", href="/", cls="text-lg font-medium hover:text-primary-color transition-colors"),
        A("About", href="/about", cls="text-lg font-medium hover:text-primary-color transition-colors"),
        A("Blogs", href="/blogs", cls="text-lg font-medium hover:text-primary-color transition-colors"),
        brand=H3("Gaurav Adlakha", cls="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-primary-color to-secondary-color"),
        cls="uk-navbar-container backdrop-blur-md border-b border-gray-200 dark:border-gray-800"
    )

def create_improved_hero():
    return Section(
        Container(
            Grid(
                Div(
                    H1("Hi, I'm Gaurav", cls="text-6xl font-bold mb-4 bg-clip-text text-transparent bg-gradient-to-r from-primary-color to-secondary-color"),
                    P("AI Innovator, Data Scientist & Builder", 
                      cls="text-xl font-semibold text-accent-color mb-4"),
                    P("I am passionate about developing intelligent, scalable solutions that address real-world challenges. I thrive at the intersection of technology and problem-solving, transforming complex ideas into impactful applications—one model at a time.", 
                      cls="mb-8 max-w-lg text-text-secondary"),
                    Div(
                        A(DivHStacked(UkIcon("github", height=35), 
                                    P("GitHub", cls="font-medium hover:text-primary-color transition-colors")), 
                          cls="text-text-secondary hover:text-primary-color", 
                          href="https://github.com/Gaurav-Adlakha"),
                        A(DivHStacked(UkIcon("linkedin", height=35), 
                                    P("LinkedIn", cls="font-medium hover:text-primary-color transition-colors")), 
                          cls="text-text-secondary hover:text-primary-color", 
                          href="https://www.linkedin.com/in/gaurav-adlakha-406b1648/"),
                        A(DivHStacked(UkIcon("file-text", height=35), 
                                    P("Resume", cls="font-medium hover:text-primary-color transition-colors")), 
                          cls="text-text-secondary hover:text-primary-color", 
                          href="/Resume_gaurav_adlakha.pdf", 
                          download=True),
                        cls="flex space-x-10 mt-6"
                    ),
                    cls="flex flex-col justify-center"
                ),
                Div(
                    Div(
                        Img(src="/static/image/profile.jpg", 
                            cls="rounded-full w-[250px] h-[250px] object-cover shadow-xl border-4 border-primary-color"),
                        cls="relative"
                    ),
                    cls="flex justify-center items-center"
                ),
                cols_lg=2,
                cls="py-20 items-center"
            )
        ),
        cls="hero-section"
    )

def create_about():
    return Section(
        Container(
            DivCentered(
                H2("About Me", 
                   cls="text-4xl font-bold mb-6 bg-clip-text text-transparent bg-gradient-to-r from-primary-color to-secondary-color", 
                   id="about"),
                P("I'm a passionate developer with expertise in AI and machine learning. I love building tools that make a difference.", 
                  cls="max-w-2xl mb-12 text-lg text-text-secondary"),
                Grid(
                    Card(
                        UkIcon("code", cls="mb-4 text-primary-color w-12 h-12"),
                        H4("Development", cls="text-xl font-semibold mb-2"),
                        P("Building web applications with modern frameworks and AI integration",
                          cls="text-text-secondary"),
                        cls="p-6 hover:border-primary-color transition-colors"
                    ),
                    Card(
                        UkIcon("brain", cls="mb-4 text-secondary-color w-12 h-12"),
                        H4("AI Research", cls="text-xl font-semibold mb-2"),
                        P("Exploring the frontiers of artificial intelligence and machine learning",
                          cls="text-text-secondary"),
                        cls="p-6 hover:border-secondary-color transition-colors"
                    ),
                    Card(
                        UkIcon("lightbulb", cls="mb-4 text-accent-color w-12 h-12"),
                        H4("Problem Solving", cls="text-xl font-semibold mb-2"),
                        P("Finding elegant solutions to complex problems through innovative approaches",
                          cls="text-text-secondary"),
                        cls="p-6 hover:border-accent-color transition-colors"
                    ),
                    cols_lg=3,
                    cls="gap-6"
                )
            ),
            cls="py-16"
        ),
        cls="section-muted"
    )

def create_footer():
    return Div(
        Container(
            DivFullySpaced(
                P("© 2024 Gaurav. All rights reserved.", cls="text-text-secondary"),
                DivHStacked(
                    A(UkIcon("github", height=20), 
                      href="https://github.com/Gaurav-Adlakha",
                      cls="text-text-secondary hover:text-primary-color transition-colors"),
                    A(UkIcon("linkedin", height=20),
                      href="https://www.linkedin.com/in/gaurav-adlakha-406b1648/",
                      cls="text-text-secondary hover:text-primary-color transition-colors"),
                    A(UkIcon("twitter", height=20),
                      href="#",
                      cls="text-text-secondary hover:text-primary-color transition-colors"),
                    cls="space-x-6"
                )
            ),
            cls="py-8"
        ),
        cls="section-muted border-t border-gray-200 dark:border-gray-800"
    )

def page_layout(title, *content):
    return Div(
        create_navbar(),
        Div(*content, cls="flex-grow"),
        # *content,
        create_footer()
    )

def home():
    return page_layout(
        "Home",
        create_improved_hero()
    )

def nb_to_markdown(nb_path):
    "Convert notebook to markdown format with executed outputs"
    shell = CaptureShell()
    nb = read_nb(nb_path)
    
    md_lines = []
    
    if nb.cells and nb.cells[0].source.startswith('---'):
        # md_lines.append(nb.cells[0].source)
        pass
    
    for cell in nb.cells:
        if cell.cell_type == 'markdown' and not cell.source.startswith('---'): #ignore the metadata cell
            md_lines.append(cell.source)
            md_lines.append('')
        elif cell.cell_type == 'code':
            md_lines.append(f'```python\n{cell.source}\n```')
            
            if cell.outputs:
                md_lines.append('')
                for out in cell.outputs:
                    if 'text' in out:
                        md_lines.append('```\n' + ''.join(out['text']) + '\n```')
                    elif 'data' in out:
                        if 'image/png' in out['data']:
                            img_data = out['data']['image/png']
                            md_lines.append(f'![](data:image/png;base64,{img_data})')
                        elif 'image/jpeg' in out['data']:
                            img_data = out['data']['image/jpeg']
                            md_lines.append(f'![](data:image/jpeg;base64,{img_data})')
                        elif 'text/plain' in out['data']:
                            txt = ''.join(out['data']['text/plain'])
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
    # shell.run_all(nb)  # Uncomment to execute notebook
    
    md_content = nb_to_markdown(file_path)
    return nb, md_content

def create_toc(content):
    "Create a table of contents from markdown content with proper nesting"
    headings = []
    for line in content.split('\n'):
        if line.startswith('#'):
            level = line.count('#', 0, line.find(' '))
            title = line[level+1:].strip()
            id = title.lower().replace(' ', '-').replace('?', '').replace('!', '').replace('.', '')
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
    
    # Create the TOC container with mobile and desktop versions
    desktop_toc = f'''
    <div class="toc-container sticky-toc desktop-toc">
        <h4>Contents</h4>
        {toc_html}
    </div>
    '''
    
    mobile_toc = f'''
    <div class="toc-container mobile-toc">
        <details>
            <summary><h4>Contents</h4></summary>
            {toc_html}
        </details>
    </div>
    '''
    
    return Safe(desktop_toc + mobile_toc), content


def get_all_metadata():
    post_filenames = Path('static').ls(file_exts=['.ipynb'])
    if not post_filenames: return []
    files = post_filenames.map(parse_notebook_file)
    return [f[0] for f in files]

def create_navbar():
    return NavBar(
        A("Home", href="/", cls="text-lg font-medium hover:text-primary-color transition-colors"),
        A("About", href="/about", cls="text-lg font-medium hover:text-primary-color transition-colors"),
        A("Blogs", href="/blogs", cls="text-lg font-medium hover:text-primary-color transition-colors"),
        brand=H3("Gaurav Adlakha", cls="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-primary-color to-secondary-color"),
        cls="uk-navbar-container backdrop-blur-md border-b border-gray-200 dark:border-gray-800"
    )

def create_footer():
    return Div(
        Container(
            DivFullySpaced(
                P("© 2024 Gaurav. All rights reserved.", cls="text-text-secondary"),
                DivHStacked(
                    A(UkIcon("github", height=20), 
                      href="https://github.com/Gaurav-Adlakha",
                      cls="text-text-secondary hover:text-primary-color transition-colors"),
                    A(UkIcon("linkedin", height=20),
                      href="https://www.linkedin.com/in/gaurav-adlakha-406b1648/",
                      cls="text-text-secondary hover:text-primary-color transition-colors"),
                    A(UkIcon("twitter", height=20),
                      href="#",
                      cls="text-text-secondary hover:text-primary-color transition-colors"),
                    cls="space-x-6"
                )
            ),
            cls="py-8"
        ),
        cls="section-muted border-t border-gray-200 dark:border-gray-800"
    )

def page_layout(title, *content):
    return Div(
        create_navbar(),
        Div(*content, cls="flex-grow"),
        create_footer()
    )

def create_blog_card_from_metadata(meta_dict, blog_id):
    title = meta_dict.get('title', 'No Title')
    desc = meta_dict.get('description', 'No Description')
    author = meta_dict.get('author', 'Unknown Author')
    date = meta_dict.get('date', 'Unknown Date')
    tags = meta_dict.get('categories', [])
    file_name = meta_dict.get('file_name', 'Unknown File Name')
    img_id = np.random.randint(1, 20)

    return Card(
        DivLAligned(
            A(
                Img(src=f"https://picsum.photos/800/400?random={img_id}", 
                    cls="w-full h-64 object-cover rounded-t-lg"),
                href=posts.to(filename=file_name),
                cls="block overflow-hidden"
            ),
            Div(
                A(
                    H3(title, 
                       cls="text-2xl font-bold mb-3 hover:text-primary-color transition-colors tracking-tight"), 
                    href=posts.to(filename=file_name)
                ),
                P(desc, cls="text-text-secondary text-lg mb-6 leading-relaxed"),
                Div(
                    DivHStacked(
                        UkIcon("user", cls="h-4 w-4 opacity-75"),
                        Small(author),
                        cls="text-text-secondary"
                    ),
                    Small("·", cls="text-text-secondary mx-3 opacity-50"),
                    DivHStacked(
                        UkIcon("calendar", cls="h-4 w-4 opacity-75"),
                        Small(date),
                        cls="text-text-secondary"
                    ),
                    cls="flex items-center mb-6"
                ),
                Div(
                    *[Label(tag, 
                           cls="bg-background-light hover:bg-background-card text-text-secondary px-3 py-1 rounded-full text-sm font-medium transition-colors") 
                      for tag in tags],
                    cls="flex gap-2 flex-wrap"
                ),
                cls="p-8"
            ),
            cls="flex flex-col"
        ),
        cls="overflow-hidden hover:shadow-lg transition-shadow duration-300 bg-background-card border border-border-color rounded-lg"
    )

def get_all_blog_cards():
    metadata_list = get_all_metadata()
    blog_ids = [f"post-{i}" for i in range(len(metadata_list))]
    return L(zip(metadata_list, blog_ids)).starmap(create_blog_card_from_metadata)

def create_blog_list():
    return page_layout(
        "Blog",
        Section(
            Container(
                H1("Blog", 
                   cls="text-4xl sm:text-5xl font-bold mb-4 tracking-tight text-center"),
                P("Thoughts, tutorials, and insights on technology and more", 
                  cls="text-xl text-text-secondary text-center mb-16 max-w-2xl mx-auto"),
                Grid(
                    *get_all_blog_cards(),
                    cols=1, 
                    cls="gap-12 max-w-5xl mx-auto"
                ),
                cls="py-20 px-4 sm:px-6 lg:px-8"
            ),
            cls="bg-background-main"
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
    
    return page_layout(
        "Blog Post",
        Section(
            Container(
                Div(
                    Div(
                        H1(meta_dict.get('title', 'Untitled Post'), 
                           cls="text-4xl sm:text-5xl font-bold mb-4 tracking-tight w-full"),
                        P(meta_dict.get('description', ''), 
                          cls="text-xl text-text-secondary leading-relaxed mb-6 w-full"),
                        
                        Div(
                            DivHStacked(
                                UkIcon("user", cls="h-4 w-4 opacity-75"),
                                Small(meta_dict.get('author', 'Unknown Author')), 
                                cls="text-text-secondary"
                            ),
                            Small("·", cls="text-text-secondary mx-3 opacity-50"),
                            DivHStacked(
                                UkIcon("calendar", cls="h-4 w-4 opacity-75"),
                                Small(meta_dict.get('date', '')),
                                cls="text-text-secondary"
                            ),
                            cls="flex items-center mb-6"
                        ),
                        
                        Div(
                            *[Label(tag, 
                                   cls="bg-background-light hover:bg-background-card text-text-secondary px-3 py-1 rounded-full text-sm font-medium transition-colors") 
                              for tag in meta_dict.get('categories', [])],
                            cls="flex gap-2 flex-wrap mb-12"
                        ),
                        
                        Div(
                            Safe(render_md(content_with_ids))
                        ),
                        
                        Div(
                            A(
                                DivHStacked(
                                    UkIcon("arrow-left", cls="h-5 w-5"),
                                    "Back to Blog"
                                ),
                                href="/blogs",
                                cls="inline-flex items-center px-5 py-2.5 rounded-lg bg-background-light text-text-primary hover:text-primary-color transition-all hover:-translate-x-1 font-medium"
                            ),
                            cls="mt-16 pt-6 border-t border-border-color"
                        ),
                        cls="w-full"
                    ),
                    
                    toc,
                    cls="blog-content-wrapper"
                ),
            ),
            cls='ml-40'
        )
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
