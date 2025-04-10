from fasthtml.common import *
from monsterui.all import *
import yaml
from fastcore.utils import *
import numpy as np

# app, rt = fast_app(hdrs=Theme.blue.headers(mode='light'),live=True)


app, rt = fast_app(
    hdrs=(
        Theme.violet.headers(mode='light', daisy=True, highlightjs=True),
        Style("""
        /* Custom theme colors */
        :root {
            --primary-color: #7c3aed;
            --secondary-color: #4f46e5;
            --accent-color: #8b5cf6;
            --background-main: #f8fafc;  /* Softer white background */
            --background-light: #f1f5f9;  /* Muted light background */
            --background-card: #ffffff;
            --text-primary: #1f2937;
            --text-secondary: #4b5563;
            --border-color: #e2e8f0;
            --code-bg: #f5f7fa;
            --code-text: #374151;
            --code-border: #e5e7eb;
            --code-selection: rgba(124, 58, 237, 0.1);
            --inline-code-bg: rgba(124, 58, 237, 0.08);
            --inline-code-text: #6d28d9;
        }

        /* Dark mode colors */
        [data-theme="dark"] {
            --primary-color: #8b5cf6;
            --secondary-color: #6366f1;
            --accent-color: #a78bfa;
            --background-main: #111827;  /* Softer dark background */
            --background-light: #1e293b;  /* Muted dark background */
            --background-card: #1f2937;
            --text-primary: #f9fafb;
            --text-secondary: #e5e7eb;
            --border-color: #374151;
            --code-bg: #1e293b;
            --code-text: #e2e8f0;
            --code-border: #334155;
            --code-selection: rgba(124, 58, 237, 0.15);
            --inline-code-bg: rgba(139, 92, 246, 0.1);
            --inline-code-text: #a78bfa;
        }

        /* Global styles */
        body {
            font-family: 'Inter', sans-serif;
            line-height: 1.5;
            color: var(--text-primary);
            background-color: var(--background-main);
        }

        /* Enhanced card styling */
        .uk-card {
            transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
            border-radius: 0.75rem;
            background-color: var(--background-card);
            border: 1px solid var(--border-color);
        }

        .uk-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
        }

        /* Button enhancements */
        .uk-button {
            font-weight: 500;
            border-radius: 0.5rem;
            transition: all 0.2s ease-in-out;
        }

        .uk-button-primary {
            background: var(--primary-color);
            color: white;
        }

        .uk-button-primary:hover {
            background: var(--secondary-color);
            transform: translateY(-2px);
        }

        /* Navigation styling */
        .uk-navbar-container {
            background: rgba(248, 250, 252, 0.8) !important;  /* Matches --background-main */
            backdrop-filter: blur(10px);
            border-bottom: 1px solid var(--border-color);
        }

        [data-theme="dark"] .uk-navbar-container {
            background: rgba(17, 24, 39, 0.8) !important;  /* Matches dark mode --background-main */
        }

        /* Hero section enhancement */
        .hero-section {
            background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
            color: white;
            padding: 4rem 0;
        }

        /* Blog card enhancements */
        .blog-card {
            border: 1px solid #e5e7eb;
            border-radius: 1rem;
            overflow: hidden;
        }

        [data-theme="dark"] .blog-card {
            border-color: #374151;
        }

        /* Existing blog content wrapper styles */
        .blog-content-wrapper {
            display: flex;
            flex-direction: column;
        }
        
        .blog-main-content {
            width: 100%;
            order: 1;
        }
        
        .blog-toc {
            width: 100%;
            order: 2;
            margin-top: 2rem;
        }
        
        /* Desktop TOC styling */
        .desktop-toc {
            display: none; /* Hidden by default on mobile */
        }
        
        /* Mobile TOC styling */
        .mobile-toc {
            display: block; /* Visible by default on mobile */
            margin-bottom: 2rem;
        }
        
        /* Responsive adjustments */
        @media (min-width: 768px) {
            .blog-content-wrapper {
                flex-direction: row;
                gap: 2rem;
            }
            
            .blog-main-content {
                width: 70%;
                order: 1;
            }
            
            .blog-toc {
                width: 30%;
                order: 2;
                margin-top: 0;
            }
            
            .mobile-toc {
                display: none; /* Hide on larger screens */
            }
            
            .desktop-toc {
                display: block; /* Show on larger screens */
            }
        }
        
        /* TOC Container Styling */
        .toc-container {
            background-color: var(--background-card);
            border-radius: 1rem;
            padding: 1.25rem 0.5rem;
            border: 1px solid var(--border-color);
            position: sticky;
            top: 2rem;
            margin-left: 2rem;
            width: 100%;
            max-width: 320px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        }

        .toc-container h4 {
            font-size: 1.5rem;
            font-weight: 600;
            margin-bottom: 1rem;
            color: var(--text-primary);
            letter-spacing: -0.02em;
            padding-left: 0.25rem;
        }

        .toc-list {
            list-style: none;
            padding: 0;
            margin: 0;
        }

        .toc-item {
            margin-bottom: 0;
        }

        .toc-link {
            display: block;
            padding: 0.25rem;
            color: var(--text-secondary);
            text-decoration: none;
            transition: all 0.15s ease;
            font-size: 0.95rem;
            line-height: 1.4;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            border-radius: 0.25rem;
        }

        .toc-link:hover {
            background-color: var(--background-light);
            color: var(--primary-color);
        }

        .toc-link.active {
            background-color: var(--background-light);
            color: var(--primary-color);
            font-weight: 500;
        }

        /* TOC hierarchy levels */
        .toc-level-1 { 
            padding-left: 0.25rem;
            position: relative;
        }
        
        .toc-level-2 { 
            padding-left: 0.5rem;
            position: relative;
        }
        
        .toc-level-2::before {
            content: "";
            position: absolute;
            left: 0.25rem;
            top: 0;
            bottom: 0;
            width: 1px;
            background-color: var(--border-color);
            border-radius: 1px;
        }
        
        .toc-level-3 { 
            padding-left: 0.75rem;
            font-size: 0.9rem;
        }

        /* Code blocks in TOC */
        .toc-link code {
            font-family: ui-monospace, 'Cascadia Code', 'Source Code Pro', Menlo, Monaco, Consolas, monospace;
            font-size: 0.9em;
            padding: 0.125rem 0.25rem;
            background-color: var(--background-light);
            border-radius: 0.25rem;
        }

        /* Blog layout with right-aligned TOC */
        .blog-content-wrapper {
            display: grid;
            grid-template-columns: minmax(0, 1fr) 320px;
            gap: 3rem;
            align-items: start;
            width: 100%;
            max-width: 1800px;
            margin: 0 auto;
            padding: 0 2rem;
        }
        
        .blog-content {
            width: 100%;
            max-width: none;
            margin: 0 auto;
        }
        
        /* Ensure content has comfortable reading width */
        .prose {
            max-width: none !important;
            width: 100%;
            margin: 0 auto;
        }

        /* Adjust heading sizes for better readability */
        .prose h1 {
            font-size: 2.5rem !important;
            line-height: 1.2 !important;
            max-width: 95%;
        }

        .prose h2 {
            font-size: 2rem !important;
            line-height: 1.3 !important;
            max-width: 95%;
        }

        .prose h3 {
            font-size: 1.5rem !important;
            line-height: 1.4 !important;
            max-width: 95%;
        }

        /* Improve readability for content */
        .prose p, .prose li {
            font-size: 1.125rem !important;
            line-height: 1.75 !important;
            max-width: 95%;
        }

        /* Make code blocks slightly less wide than text */
        .prose pre {
            width: 100%;
            max-width: 95%;
            margin-left: auto;
            margin-right: auto;
        }

        @media (max-width: 1024px) {
            .blog-content-wrapper {
                grid-template-columns: 1fr;
                gap: 2rem;
                padding: 0 1rem;
            }
            
            .toc-container {
                display: none;
            }

            .prose {
                max-width: none !important;
            }

            .prose p, .prose li, .prose h1, .prose h2, .prose h3, .prose pre {
                max-width: 100%;
            }
        }
        
        /* Container modifications */
        .blog-container {
            width: 100%;
            max-width: none;
            padding: 0 2rem;
        }

        /* Social sharing buttons */
        .social-share-buttons {
            display: flex;
            gap: 10px;
        }

        .social-share-buttons a {
            transition: transform 0.2s;
        }

        .social-share-buttons a:hover {
            transform: translateY(-3px);
        }

        /* Comments styling */
        .comments-section {
            border-top: 1px solid #e0e0e0;
            padding-top: 2rem;
        }

        [data-theme="dark"] .comments-section {
            border-top-color: #4a5568;
        }

        /* Section backgrounds */
        .section-muted {
            background-color: var(--background-light);
        }

        /* Code block enhancements */
        .prose pre {
            background-color: var(--code-bg) !important;
            border: 1px solid var(--code-border) !important;
            border-radius: 0.75rem !important;
            padding: 1.5rem !important;
            margin: 1.5rem 0 !important;
            overflow-x: auto !important;
            color: var(--code-text) !important;
            font-size: 0.95rem !important;
            line-height: 1.75 !important;
            letter-spacing: -0.01em !important;
        }

        .prose pre code {
            background-color: transparent !important;
            border-radius: 0 !important;
            padding: 0 !important;
            color: inherit !important;
            font-size: inherit !important;
            font-family: ui-monospace, 'Cascadia Code', 'Source Code Pro', Menlo, Monaco, Consolas, monospace !important;
            line-height: inherit !important;
            white-space: pre;
        }

        .prose code {
            background-color: var(--inline-code-bg) !important;
            color: var(--inline-code-text) !important;
            padding: 0.2em 0.4em !important;
            border-radius: 0.375rem !important;
            font-size: 0.875em !important;
            font-weight: 450 !important;
            font-family: ui-monospace, 'Cascadia Code', 'Source Code Pro', Menlo, Monaco, Consolas, monospace !important;
        }

        /* Code syntax highlighting - lighter theme */
        .prose pre .keyword { color: #7c3aed; font-weight: 500; }  /* purple */
        .prose pre .function { color: #2563eb; }  /* blue */
        .prose pre .string { color: #059669; }    /* green */
        .prose pre .number { color: #db2777; }    /* pink */
        .prose pre .comment { color: #6b7280; font-style: italic; }  /* gray */
        .prose pre .operator { color: #4f46e5; }  /* indigo */
        .prose pre .punctuation { color: #6b7280; }  /* gray */
        .prose pre .class { color: #0891b2; }     /* cyan */
        .prose pre .builtin { color: #9333ea; }   /* purple */
        .prose pre .variable { color: #0284c7; }  /* blue */

        [data-theme="dark"] .prose pre .keyword { color: #a78bfa; }
        [data-theme="dark"] .prose pre .function { color: #60a5fa; }
        [data-theme="dark"] .prose pre .string { color: #34d399; }
        [data-theme="dark"] .prose pre .number { color: #f472b6; }
        [data-theme="dark"] .prose pre .comment { color: #9ca3af; }
        [data-theme="dark"] .prose pre .operator { color: #818cf8; }
        [data-theme="dark"] .prose pre .punctuation { color: #9ca3af; }
        [data-theme="dark"] .prose pre .class { color: #22d3ee; }
        [data-theme="dark"] .prose pre .builtin { color: #c084fc; }
        [data-theme="dark"] .prose pre .variable { color: #38bdf8; }

        /* Code block scrollbar styling */
        .prose pre::-webkit-scrollbar {
            height: 0.5rem;
            background-color: transparent;
        }

        .prose pre::-webkit-scrollbar-thumb {
            background-color: var(--code-border);
            border-radius: 0.25rem;
        }

        .prose pre::-webkit-scrollbar-thumb:hover {
            background-color: #9ca3af;
        }

        /* Code selection styling */
        .prose pre ::selection {
            background-color: var(--code-selection);
        }

        /* Ensure code blocks stretch full width */
        .prose pre {
            margin-left: calc(-1 * var(--prose-margin, 1rem));
            margin-right: calc(-1 * var(--prose-margin, 1rem));
            border-radius: 0.5rem;
        }

        @media (min-width: 640px) {
            .prose pre {
                margin-left: 0;
                margin-right: 0;
                border-radius: 0.75rem;
            }
        }

        """)
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

def parse_qmd_file(file_path):
    txt = Path(file_path).read_text()
    parts = txt.split("---", 2)
    if len(parts) < 3: return {}, txt
    
    meta_str, content = parts[1].strip(), parts[2].strip()
    meta_dict = yaml.safe_load(meta_str)
    meta_dict['file_name'] = file_path.name
    return meta_dict, content

def get_all_metadata():
    post_filename = Path('static').ls(file_exts=['.qmd'])
    if not post_filename: return []
    files = post_filename.map(parse_qmd_file)
    return [f[0] for f in files]

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

def create_blog_detail(metadata, content):
    title = metadata.get('title', 'No Title')
    author = metadata.get('author', 'Unknown Author')
    date = metadata.get('date', 'Unknown Date')
    tags = metadata.get('categories', [])
    
    def Tags(cats): return DivLAligned(map(Label, cats))
    
    return Section(
        Container(
            Card(
                DivCentered(
                    H1(title, cls="text-3xl mb-2"),
                    DivHStacked(Small(author), Small(date), cls=TextT.muted + " mb-4 space-x-4"),
                    Tags(tags),
                    cls="mb-8"
                ),
                Div(Safe(render_md(content)), cls="prose max-w-none"),
                footer=DivFullySpaced(
                    Button("← Back to Blogs", cls=ButtonT.secondary, hx_get="/blogs"),
                    Button(DivHStacked(UkIcon("share"), P("Share")), cls=ButtonT.ghost)
                ),
                cls="p-8"
            ),
            cls="max-w-4xl mx-auto py-8"
        )
    )

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

def create_toc(content):
    "Create a table of contents from markdown content"
    headings = []
    for line in content.split('\n'):
        if line.startswith('## '):  # Only match H2 headings (double #)
            title = line[3:].strip()  # Remove the ## and space
            # Create a URL-friendly ID from the title
            id = title.lower().replace(' ', '-').replace('?', '').replace('!', '').replace('.', '')
            headings.append((2, title, id))
    
    # Create TOC items with proper hierarchy and IDs
    toc_items = []
    for level, title, id in headings:
        toc_items.append(
            Li(
                A(title, href=f"#{id}", 
                  cls=f"toc-link"),
                cls=f"toc-item toc-level-{level}"
            )
        )
    
    # Also update the content headings with matching IDs
    new_content = content
    for _, title, id in headings:
        # Replace the heading with the same heading plus an ID
        old_heading = f"## {title}"
        new_heading = f'## <a id="{id}"></a>{title}'
        new_content = new_content.replace(old_heading, new_heading, 1)
    
    return Div(
        H4("Contents"),
        Ul(*toc_items, cls="toc-list"),
        cls="toc-container"
    ), new_content

def display_post(filename):
    if not filename.endswith('.qmd'): filename = f"{filename}.qmd"
    
    file_path = Path('static')/filename
    if not file_path.exists(): 
        return Titled("Post Not Found", P(f"The post {filename} was not found"))
    
    meta_dict, content = parse_qmd_file(file_path)
    
    # Get both TOC and updated content with IDs
    toc, content_with_ids = create_toc(content)
    
    return page_layout(
        "Blog Post",
        Section(
            Container(
                Div(
                    Div(
                        # Title and metadata section
                        H1(meta_dict.get('title', 'Untitled Post'), 
                           cls="text-4xl sm:text-5xl font-bold mb-4 tracking-tight w-full"),
                        P(meta_dict.get('description', ''), 
                          cls="text-xl text-text-secondary leading-relaxed mb-6 w-full"),
                        
                        # Author and date info
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
                        
                        # Tags
                        Div(
                            *[Label(tag, 
                                   cls="bg-background-light hover:bg-background-card text-text-secondary px-3 py-1 rounded-full text-sm font-medium transition-colors") 
                              for tag in meta_dict.get('categories', [])],
                            cls="flex gap-2 flex-wrap mb-12"
                        ),
                        
                        # Main content
                        Div(
                            Safe(render_md(content_with_ids)),
                            cls="""
                                prose w-full
                                prose-headings:font-bold prose-headings:tracking-tight
                                prose-h1:text-4xl prose-h1:mb-4
                                prose-h2:text-3xl prose-h2:mt-12 prose-h2:mb-4
                                prose-h3:text-2xl prose-h3:mt-8 prose-h3:mb-3
                                prose-p:text-text-secondary prose-p:leading-relaxed prose-p:mb-4
                                prose-a:text-primary-color prose-a:no-underline prose-a:font-medium hover:prose-a:underline
                                prose-ul:my-4 prose-li:text-text-secondary prose-li:my-1
                                prose-blockquote:border-l-4 prose-blockquote:border-primary-color prose-blockquote:pl-6 prose-blockquote:py-1 prose-blockquote:my-6 prose-blockquote:font-normal prose-blockquote:text-text-secondary prose-blockquote:italic
                                prose-img:rounded-lg prose-img:shadow-md
                                selection:bg-primary-color/10 selection:text-primary-color
                            """
                        ),
                        
                        # Footer with back button
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
                    
                    # Right-aligned TOC
                    toc,
                    
                    cls="blog-content-wrapper"
                ),
                cls="py-12 px-4 sm:px-6 lg:px-8 w-full max-w-none"
            ),
            cls="bg-background-main w-full"
        )
    )


@rt
def posts(filename: str = None):
    "Display a blog post from a QMD file"
    if not filename:
        # If no filename provided, redirect to blog list or show an error
        return Titled("No Post Selected", 
                     P("Please select a blog post to view"),
                     Button("Back to Blog List", href="/blogs", cls=ButtonT.primary))
    
    # Now use our display_post function
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
        "Blog - Gaurav's Portfolio"), create_blog_list(),A( UkIcon("home"), Div(id='search-results'),"Back to Home", href="/create_blog_list", cls="fixed bottom-4 right-4")

serve()
