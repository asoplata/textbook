from copy import deepcopy
import json
from pathlib import Path


# AES TODO: "Index" and "ordered_page_links" should probably be greatly expanded to
# prevent frequent re-searching of Markdown and other files in
# generate_page_html.py. For example, "Index" could have titles removed and consist only
# of the hierarchical mapping, while "ordered_page_links" could be changed to something
# like "page_metadata", where each Section (dir containing md files) and markdown
# filenames each contain child data like "title", "relative root path" (to textbook
# root), "output path" (where their output html goes, if necessary), etc.


def _get_title(file_path):
    with open(file_path, "r") as file:
        title = "NA"
        for line in file:
            if "# Title: " in line:
                title = line[9:]
                if title.endswith("\n"):
                    title = title[0:-1]
    return title


def create_hier_index(content_path, save_indices=False, hier_index_path=None):
    def _recur_create_hier_index(input_path):
        """
        TODO
        This is done independently of the "flat index", due to recursion and because we DO
        care about the directory-defining "README.md" files, unlike in the flat case.
        """
        page_index = {}
        directory_contents = sorted(Path(input_path).glob("*"))
        for item_path in directory_contents:
            readme_path = item_path / "README.md"
            if item_path.is_dir() and readme_path.exists():
                # Check for README inside any directories, which indicate a directory to be
                # indexed
                section_title = _get_title(readme_path)
                # Recursively search directories for files to index
                page_index[item_path.name] = [
                    section_title,
                    _recur_create_hier_index(item_path),
                ]
            elif (item_path.suffix == ".md") and (item_path.name != "README.md"):
                # Check for non-README markdown files
                page_index[item_path.name] = _get_title(item_path)
        return page_index

    hier_index = _recur_create_hier_index(content_path)

    if save_indices and hier_index_path:
        with open(hier_index_path, "w", encoding="utf-8") as f:
            json.dump(hier_index, f, ensure_ascii=False, indent=4)

    return hier_index


def create_flat_index(content_path, save_indices=False, flat_index_path=None, dev_build=False):
    def _create_flat_index(content_path: Path):
        """TODO"""
        # This glob is recursive, see
        # https://docs.python.org/3/library/pathlib.html#pathlib-pattern-language
        paths_all = sorted(content_path.glob("**/*.md"))
        paths_excluding_readme = [p for p in paths_all if ("README" not in str(p))]
        # md_paths = {
        #     p.relative_to(content_path): p.absolute()
        #     for p in paths_excluding_readme
        # }

        # AES TODO hopefully we don't need relative input
        # "relative input" is relative to "textbook_root / content"
        flat_index = [
            {
                "absolute_input_path": input_path,
                # "relative_input_path" : input_path.relative_to(content_path), AES TODO
                "title": _get_title(input_path),
            }
            for input_path in paths_excluding_readme
        ]
        return flat_index

    def _generate_output_html_paths(content_path, flat_index, dev_build=False):
        """TODO

        Side-effects: This also creates any needed parent directories needed for each output file.
        """
        for page in flat_index:
            abs_inp_md_path = page["absolute_input_path"]
            # --------------------------------------------------------------------------
            # First, let's make the new filename, independent of any parent directories
            new_filename = abs_inp_md_path.stem.split("_", 1)[1] + ".html"

            # --------------------------------------------------------------------------
            # Let's make the new absolute output path, and create any necessary parent dirs
            # along the way. This is needed to create the actual output files.
            abs_out_dir_path = abs_inp_md_path.parents[0]
            if dev_build:
                # Replace "content" with "dev" among all the parents. We do NOT know how
                # many levels above it will be.
                abs_out_dir_path = Path(str(abs_out_dir_path).replace("content", "dev"))
                # This needs to be done separately in both the notebook-execution code
                # and here in the page-generation code, since there is not necessarily a
                # 1-to-1 correspondence between every markdown file and every notebook.
                abs_out_dir_path.mkdir(parents=True, exist_ok=True)
            abs_out_html_path = abs_out_dir_path / new_filename

            # --------------------------------------------------------------------------
            # Let's make the new "relative" output path, which will be used to insert the
            # proper links in the website HTML for pages relative to the website root.
            #
            # Since "content" is always a child of the textbook root, parents[1] can be used to
            # give us the textbook root.
            rel_out_html_path = abs_out_html_path.relative_to(content_path.parents[1])
            # Finally, change our path to treat the website root as root.
            rel_out_html_path = "/" + str(rel_out_html_path)

            page.update(
                {
                    "absolute_output_html_path": abs_out_html_path,
                    "relative_output_html_path": rel_out_html_path,
                }
            )
        return flat_index

    flat_index_no_output = _create_flat_index(content_path)
    flat_index = _generate_output_html_paths(
        content_path,
        flat_index_no_output,
        dev_build,
    )

    if save_indices and flat_index_path:
        flat_index_serializable = deepcopy(flat_index)
        for idx, page in enumerate(flat_index):
            for key, val in page.items():
                flat_index_serializable[idx][key] = str(val)
        with open(flat_index_path, "w", encoding="utf-8") as f:
            json.dump(flat_index_serializable, f, ensure_ascii=False, indent=4)

    return flat_index
