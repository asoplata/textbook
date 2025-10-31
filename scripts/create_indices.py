from copy import deepcopy
import json
from pathlib import Path


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

    # Save our hierarchical index, if desired:
    if save_indices and hier_index_path:
        with open(hier_index_path, "w", encoding="utf-8") as f:
            json.dump(hier_index, f, ensure_ascii=False, indent=4)

    return hier_index


def create_flat_index(
    content_path, is_dev_build, save_indices=False, flat_index_path=None
):
    # Get all markdown files, but excluding 'README.md' files. We don't care about the
    # sections.
    # ----------------------------------------------------------------------------------
    # This glob is recursive, see
    # https://docs.python.org/3/library/pathlib.html#pathlib-pattern-language
    paths_all = sorted(content_path.glob("**/*.md"))
    paths_excluding_readme = [p for p in paths_all if ("README" not in str(p))]

    # Create the initial flat index, containing only input files:
    # ----------------------------------------------------------------------------------
    flat_index = [
        {
            "absolute_input_md_path": input_path,
            "title": _get_title(input_path),
        }
        for input_path in paths_excluding_readme
    ]

    # Update the flat index to include output files, and create any output directories
    # we need:
    # ----------------------------------------------------------------------------------
    for page in flat_index:
        abs_inp_md_path = page["absolute_input_md_path"]
        # First, let's make the new filename, independent of any parent directories:
        new_filename = abs_inp_md_path.stem.split("_", 1)[1] + ".html"

        # Let's make the new absolute output directory path, which will contain the new
        # output file. If we're usind a "dev" version, let's also change it to be a
        # "dev" version of the directory path, and create the directories along that
        # path if necessary.
        abs_out_dir_path = abs_inp_md_path.parents[0]
        if is_dev_build:
            # This needs to be done separately in both the notebook-execution code
            # before and here in the page-generation code, since there is not
            # necessarily a 1-to-1 correspondence between every markdown file and every
            # notebook.
            #
            # In this page-generation case, we do NOT necessarily know how many levels
            # are between the `dev` directory and the `abs_out_dir_path`, since not all
            # markdown pages are inside sections.
            #
            # Replace "content" parent directory with "dev" one, and, importantly,
            # create parent directories if they don't exist.
            abs_out_dir_path = Path(str(abs_out_dir_path).replace("content", "dev"))
            abs_out_dir_path.mkdir(parents=True, exist_ok=True)
        abs_out_html_path = abs_out_dir_path / new_filename

        # Let's make the new "relative" output path, which will be used to insert the
        # proper links in the website HTML for pages relative to the website root:
        #
        # Since "content" is always a child of the textbook root, parents[1] can be used
        # to give us the textbook root.
        rel_out_html_path = abs_out_html_path.relative_to(content_path.parents[1])
        # Finally, change our path to treat the website root as root:
        rel_out_html_path = "/" + str(rel_out_html_path)

        # Add our new paths to the dictionary of the individual markdown page:
        page.update(
            {
                "absolute_output_html_path": abs_out_html_path,
                "relative_output_html_path": rel_out_html_path,
            }
        )

    # Save our flat index, if desired:
    if save_indices and flat_index_path:
        flat_index_serializable = deepcopy(flat_index)
        for idx, page in enumerate(flat_index):
            for key, val in page.items():
                flat_index_serializable[idx][key] = str(val)
        with open(flat_index_path, "w", encoding="utf-8") as f:
            json.dump(flat_index_serializable, f, ensure_ascii=False, indent=4)

    return flat_index
