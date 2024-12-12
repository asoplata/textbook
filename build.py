# %%
import os
import pypandoc
from create_page_index import update_page_index
from create_navbar import generate_navbar_html
from bs4 import BeautifulSoup

# %%
test_path = os.getcwd()+'/content'
test_file = '/00_preface.md'

# %%
test_out = '/test_preface.html'

converted = pypandoc.convert_file(test_path+test_file, 'html')
converted = BeautifulSoup(converted, 'html.parser').prettify()

# %%
with open(test_path+test_out, 'w') as f:
    for line in converted:
        f.write(line)


# %% ######################################################################
def compile_page_components():
    """Compile base html components for building webpage"""

    templates_folder = os.path.join(os.getcwd(), 'templates')
    templates = ['header', 'topbar', 'script']
    html_parts = {}

    for template in templates:
        templates_path = os.path.join(templates_folder, f'{template}.html')
        with open(templates_path, 'r') as f:
            html_parts[template] = f.read()

    update_page_index()
    html_parts['navbar'] = generate_navbar_html()

    return html_parts


html_parts = compile_page_components()
html_parts.keys()


# %%
def get_page_paths(path=None):
    """Get paths to all .md pages to be converted to html"""

    md_pages = {}
    if path is None:
        path = os.path.join(os.getcwd(), "content")
    directories = os.listdir(path)
    for item in directories:
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            # add items from new dict into md_pages
            md_pages.update(get_page_paths(item_path))
        else:
            if not item == "README.md" and item.endswith(".md"):
                md_pages[item] = item_path

    return md_pages


get_page_paths()


# %%
def generate_page_html(page_paths):
    html_parts = compile_page_components()
    order = [
        'header',
        'navbar',
        'topbar',
        'body',
        'script',
    ]

    for page, path in page_paths.items():
        page_components = html_parts.copy()
        out_path = path.split(".md")[0] + ".html"

        converted = pypandoc.convert_file(path, 'html')
        converted = BeautifulSoup(converted, 'html.parser').prettify()
        page_components['body'] = converted

        file_contents = ""
        for section in order:
            file_contents += page_components[section]
        file_contents += '\n</body>\n</html>'

        with open(out_path, 'w') as out:
            out.write(file_contents)

    return


page_paths = get_page_paths()
generate_page_html(page_paths)

# %%
