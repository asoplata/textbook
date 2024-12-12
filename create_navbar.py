# %% ######################################################################
import os
import json

# %% ######################################################################


def generate_navbar_html():
    """Function to generate the navbar from the structure specified
       in the index.json file"""

    indent = '\t\t'

    html = '\t<div id="mySidebar" class="sidebar">' + \
           f'\n{indent}<p style="color:#e5a734">' + \
           f'\n\t{indent}Human Neocortical Neurosolver' + \
           f'\n{indent}</p>\n{indent}<br>'

    # load page index .json file
    index_path = os.getcwd() + "/index.json"

    with open(index_path, 'r') as f:
        json_page_index = json.load(f)

    def get_relative_paths(path=None):
        """Get paths to all .md pages to be converted to html"""
        md_pages = {}
        if path is None:
            path = os.path.join(os.getcwd(), "content")

        directories = os.listdir(path)
        for item in directories:
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                # add items from new dict into md_pages
                md_pages.update(get_relative_paths(item_path))
            else:
                if not item == "README.md" and item.endswith(".md"):
                    location = item_path.split(os.getcwd())[1]
                    location = 'content' + location.split('content')[1]
                    location = location.split('.md')[0] + '.html'
                    md_pages[item] = location

        return md_pages

    def create_page_link(file, label, page_paths, indent):
        file_path = page_paths[file]
        return f'\n{indent}<a href="{file_path}">{label}</a>'

    def create_toggle_section(toggle_label):
        section = f'\n{indent}<div class="sidebar-list">' + \
                  f'\n{indent}\t<a id="sidebar-header"' + \
                    ' onclick="toggleSubmenu(event)">' + \
                  f'\n{indent}{indent}{toggle_label}' + \
                  f'\n{indent}\t</a>' + \
                  f'\n{indent}\t<div class="submenu">'
        return section

    def build_navbar(json_page_index):
        navbar_html = ''
        page_paths = get_relative_paths()
        for section, contents in json_page_index.items():
            # For pages that are not nested in a toggle
            if isinstance(contents, str):
                navbar_html += create_page_link(
                    section,
                    contents,
                    page_paths,
                    indent,
                )
            # For pages that are nested in a toggle
            elif isinstance(contents, list):
                toggle_label = contents[0]
                toggle_contents = contents[1]
                # Add toggle <div> sections and link
                navbar_html += create_toggle_section(toggle_label)
                # Add pages under toggle
                for sub_page, sub_name in toggle_contents.items():
                    navbar_html += create_page_link(
                        sub_page,
                        sub_name,
                        page_paths,
                        indent+indent,
                    )
                # Close toggle <div> sections
                navbar_html += f'\n{indent}\t</div>'
                navbar_html += f'\n{indent}</div>'
        return navbar_html

    html += build_navbar(json_page_index)
    html += '\n\t</div>'
    return html


# print(generate_navbar_html())
