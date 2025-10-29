import argparse
from pathlib import Path
import textwrap

from scripts.execute_and_convert_nbs import execute_and_convert_nbs_to_json
from scripts.generate_page_html import generate_page_html
from scripts.get_commit_hash import get_commit_hash

textbook_root_path = Path(__file__).parents[0]


def main():
    """
    Main function to generate html pages for deployment

    AES TODO: describe required file structure
    """

    # ----------------------------------------------------------------------------------
    # Define command line arguments
    parser = argparse.ArgumentParser(
        description="Generate html pages for deployment",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "--code-version",
        action="store",
        default="stable",
        choices=[
            "stable",
            "master",
            "custom",
            "no-check",
        ],
        help=textwrap.dedent(
            """Specify which version of HNN-core you want to use for building the
textbook. The default is 'stable'. This ASSUMES you have the correct version installed
in your local environment. The three options are below:
- 'stable': This builds the textbook using the latest stable version of HNN-Core, as
    detected from a request to PyPI. This compiles the output HTML into the 'content'
    folder.
- 'master': This builds the textbook using the latest development version of HNN-Core
    from the 'master' branch, as detected from a request to Github. This compiles the
    output HTML into the 'dev' folder, creating one if it doesn't exist.
- 'custom': This builds the textbook using a custom commit and, optionally, a custom
    repository-owner's version of HNN-Core. If using this option, you must provide the
    repository-owner and/or commit you want using the '--custom-repo-commit' argument.
    This compiles the output HTML into the 'dev' folder, creating one if it doesn't
    exist.
- 'no-check': AES TODO
"""
        ),
    )
    parser.add_argument(
        "--execution-type",
        action="store",
        default="no-execution",
        choices=[
            "no-execution",
            "execute-updated-unskipped-notebooks",
            "execute-all-unskipped-notebooks",
            "execute-absolutely-all-notebooks",
        ],
        help=textwrap.dedent(
            """Specify different criteria for which notebooks you want to execute before
converting them to HTML. The default is 'no-execution'. The four options are below, in
order of more execution:
- 'no-execution': This will not execute any notebooks. You may receive warnings if
    specific notebooks should be executed.
- 'execute-updated-unskipped-notebooks': Execute only notebooks which have been
    updated/changed or are new, excluding notebooks flagged for skipping.
- 'execute-all-unskipped-notebooks': Execute all notebooks except those flagged for
    skipping.
- 'execute-absolutely-all-notebooks': Execute all notebooks.
"""
        ),
    )
    parser.add_argument(
        "--custom-owner-commit",
        type=str,
        help=textwrap.dedent(
            """Optionally provide a specific commit of HNN-core to use in the form of
<owner>:<commit>. For example, if you wanted to build using the commit at
https://github.com/asoplata/hnn-core/commit/92b000c597052a661d9e177b8754695446336b96 ,
you would use '--custom-owner-commit asoplata:92b000c'. This assumes that the
fork/repository name is always 'hnn-core'. This is required if you are using
'--code-version custom'.
        """
        ),
    )
    # AES Not sure we want to support this, but leaving it as an option since I assume
    # this case was the reason why `os.getcwd()` is used so much in the scripts instead
    # of absolute paths.
    parser.add_argument(
        "--custom-root-path",
        type=str,
        help="Optionally provide a different 'root' location for your textbook files",
    )
    parser.add_argument(
        "--save-indices",
        type=bool,
        help=textwrap.dedent(
            """Optionally provide whether or not to save the webpage-indexing files
            during the build process. Defaults to False."""
        ),
    )
    # ----------------------------------------------------------------------------------
    # Process CLI arguments, and set paths
    args = parser.parse_args()

    if args.custom_root_path:
        root_path = args.custom_root_path
    else:
        root_path = textbook_root_path

    content_path = Path(root_path / "content")
    hier_index_path = Path(root_path / "scripts" / "hier_index.json")
    flat_index_path = Path(root_path / "scripts" / "flat_index.json")
    nb_hash_path = Path(root_path / "scripts" / "nb_hashes.json")
    nb_skip_path = Path(root_path / "scripts" / "nbs_to_skip.json")
    templates_path = Path(root_path / "templates")

    # This "printed" variable is only used here for logging, never for actual output
    # pathing.
    if args.code_version in ("master", "custom", "no-check"):
        printed_output_dir = Path(root_path / "dev")
    else:
        printed_output_dir = content_path
    print(
        "Configuration: Choice of notebooks to execute will be based on "
        f"\n    '--execution-type={args.execution_type}'"
        "\nConfiguration: Choice of HNN version to use will be based on "
        f"\n    '--code-version={args.code_version}'"
        "\nConfiguration: Local website files will be built in "
        f"\n    '{printed_output_dir}'"
    )

    # ----------------------------------------------------------------------------------
    # Begin the actual work: First, figure out the environment and version:
    commit_hash = get_commit_hash(
        args.code_version,
        custom_owner_commit=args.custom_owner_commit,
    )

    # ----------------------------------------------------------------------------------
    # Execute appropriate Jupyter notebooks, and save their output for later webpage
    # assembly:
    execute_and_convert_nbs_to_json(
        content_path,
        nb_hash_path,
        nb_skip_path,
        args.execution_type,
        write_standalone_html=True,
        code_version=args.code_version,
        commit_hash=commit_hash,
    )

    # ----------------------------------------------------------------------------------
    # Finally, use the Markdown files and Jupyter notebook output to assemble the
    # webpages and website as a whole:
    generate_page_html(
        content_path,
        templates_path,
        save_indices=args.save_indices,
        hier_index_path=hier_index_path,
        flat_index_path=flat_index_path,
        code_version=args.code_version,
        commit_hash=commit_hash,
    )


if __name__ == "__main__":
    main()
