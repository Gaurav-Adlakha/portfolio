from fasthtml.common import *
from monsterui.all import *
import yaml
from fastcore.utils import *
import numpy as np

app, rt = fast_app(hdrs=Theme.blue.headers(mode='light'),live=True)

def create_navbar():
    return NavBar(
        A("Home", href="/", cls=AT.primary),
        A("About", href="/about"),
        A("Blogs", href="/blogs"),
        brand=H3("Gaurav Adlakha", cls=TextT.bold)
    )

def create_improved_hero():
    return Section(
        Container(
            Grid(
                Div(
                    H1("Hi, I'm Gaurav", cls="text-5xl font-bold mb-4"),
                    P("AI Innovator, Data Scientist & Builder", cls=TextT.lead),
                    P(" I am passionate about developing intelligent, scalable solutions that address real-world challenges. I thrive at the intersection of technology and problem-solving, transforming complex ideas into impactful applications—one model at a time..", 
                      cls="mb-8 max-w-lg"),
                    Div(
                        A(DivHStacked(UkIcon("github", height=35), P("GitHub", cls=TextT.medium)), 
                          cls="text-gray-700 hover:text-gray-900", href="https://github.com/Gaurav-Adlakha"),
                        A(DivHStacked(UkIcon("linkedin", height=35), P("LinkedIn", cls=TextT.medium)), 
                          cls="text-gray-700 hover:text-gray-900", href="https://www.linkedin.com/in/gaurav-adlakha-406b1648/"),
                        A(DivHStacked(UkIcon("file-text", height=35), P("Resume", cls=TextT.medium)), 
                          cls="text-gray-700 hover:text-gray-900", href="/Resume_gaurav_adlakha.pdf", download=True),
                        cls="flex space-x-10 mt-2"
                    ),
                    cls="flex flex-col justify-center"
                ),
                Div(
                    Img(src="/static/image/profile.jpg", cls="rounded-full w-[200px] h-[200px] object-cover"), # for deploy
                    # Img(src="/static/gaurav_img.jpg", cls="rounded-full w-[200px] h-[200px] object-cover"), # for solveit
                    cls="flex justify-center items-center"
                ),
                cols_lg=2,
                cls="py-20"
            )
        ),
        cls="bg-gray-50 dark:bg-gray-900"
    )

def create_about():
    return Section(
        Container(
            DivCentered(
                H2("About Me", cls="text-3xl mb-6", id="about"),
                P("I'm a passionate developer with expertise in AI, machine learning. I love building tools that make a difference.", 
                  cls="max-w-2xl mb-6"),
                Grid(
                    Card(UkIcon("code", cls="mb-4"), H4("Development"), P("Building web applications with modern frameworks")),
                    Card(UkIcon("brain", cls="mb-4"), H4("AI Research"), P("Exploring the frontiers of artificial intelligence")),
                    Card(UkIcon("lightbulb", cls="mb-4"), H4("Problem Solving"), P("Finding elegant solutions to complex problems")),
                    cols_lg=3
                )
            ),
            cls="py-16"
        ),
        cls=SectionT.muted
    )


def create_footer():
    return Div(
        Container(
            DivFullySpaced(
                P("© 2024 Gaurav. All rights reserved."),
                DivHStacked(
                    UkIconLink("github", height=20),
                    UkIconLink("linkedin", height=20),
                    UkIconLink("twitter", height=20),
                    cls="space-x-3"
                )
            ),
            cls="py-6"
        ),
        cls="bg-gray-800 text-white"
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
            A(Img(src=f"https://picsum.photos/200/200?random={img_id}", style="width:200px"), href=f"/blog/{blog_id}"),
            Div(cls='space-y-3 uk-width-expand')(
                A(H4(title), href=posts.to(filename=file_name)),
                P(desc),
                DivFullySpaced(map(Small, [author, date]), cls=TextT.muted),
                Div(
                    DivLAligned(map(Label, tags)),
                    # P(blog_id)
                    DivFullySpaced(
                        P(""),
                        A("Read More", href=posts.to(filename=file_name), cls=("uk-button rounded-md px-2 px-2 " , ButtonT.primary))
                    ),
                    cls='flex items-center w-full mt-6'))),
        cls=CardT.hover)

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
                H1("Blogs", cls="text-4xl text-center mb-10"),
                P("Thoughts, tutorials, and insights on technology and more", 
                  cls="text-center mb-12 max-w-2xl mx-auto"),
                Grid(*get_all_blog_cards(),cols=1, cls="gap-6"),
                cls="py-16"
            )
        )
    )

def create_toc(content):
    "Create a table of contents from markdown content"
    headings = []
    for line in content.split('\n'):
        if line.startswith('#'):
            level = len(line.split()[0])  # Count the number of # symbols
            title = ' '.join(line.split()[1:])
            # Create an ID from the title (simplified version)
            id = title.lower().replace(' ', '-')
            headings.append((level, title, id))
    return headings

def display_post_with_nav(filename):
    "Display a blog post with navigation panel"
    if not filename.endswith('.qmd'): filename = f"{filename}.qmd"
    
    file_path = Path('static') / filename
    if not file_path.exists(): return Titled("Post Not Found", P(f"The post {filename} was not found"))
    
    meta_dict, content = parse_qmd_file(file_path)
    toc = create_toc(content)
    
    # Create the navigation panel
    nav_items = [Li(A(title, href=f"#{id}", cls=f"pl-{(level-1)*4}")) for level, title, id in toc]
    nav_panel = Div(
        H4("Table of Contents", cls="mb-4"),
        Ul(*nav_items, cls="space-y-2"),
        cls="bg-gray-100 p-4 rounded-lg sticky top-4"
    )
    
    # Main content
    main_content = Div(
        H1(meta_dict.get('title', 'Untitled Post'), cls="text-4xl mb-4"),
        DivFullySpaced(
            Small(meta_dict.get('author', 'Unknown Author')), 
            Small(meta_dict.get('date', '')),
            cls=TextT.muted + " mb-4"
        ),
        DivLAligned(*[Label(tag) for tag in meta_dict.get('categories', [])], cls="mb-6"),
        Safe(render_md(content)),
        Button("← Back to Blog", hx_get="/blogs", cls=ButtonT.secondary + " mt-8"),
        cls="prose"
    )
    
    # Combine navigation and content in a grid
    return Container(
        Grid(
            Div(nav_panel, cls="col-span-1"),
            Div(main_content, cls="col-span-3"),
            cols=4, gap=6
        ),
        cls="py-8"
    )

def display_post(filename):
    if not filename.endswith('.qmd'): filename = f"{filename}.qmd"
    
    file_path = Path('static')/filename
    if not file_path.exists(): return Titled("Post Not Found", P(f"The post {filename} was not found"))
    
    meta_dict, content = parse_qmd_file(file_path)
    
    return Container(
        H1(meta_dict.get('title', 'Untitled Post'), cls="text-4xl mb-4"),
        Div(
            DivFullySpaced(
                Small(meta_dict.get('author', 'Unknown Author')), 
                Small(meta_dict.get('date', '')),
                cls=TextT.muted + " mb-4"
            ),
            DivFullySpaced(*[Label(tag) for tag in meta_dict.get('categories', [])], cls="mb-2"),
            Safe(render_md(content)),
            Button("← Back to Blog", hx_get="/blogs", cls=ButtonT.secondary + " mt-8"),
            cls="prose max-w-4xl mx-auto"
        ),
        cls="py-8"
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
    return display_post_with_nav(filename)

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
