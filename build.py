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

    # accept command line arguments
    parser = argparse.ArgumentParser(
        description="Generate html pages for deployment",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "--execution-filter",
        action="store",
        default="no-execution",
        choices=[
            "no-execution",
            "execute-updated-unskipped-notebooks",
            "execute-all-unskipped-notebooks",
            "execute-absolutely-all-notebooks",
        ],
        help=textwrap.dedent(
"""Specify different criteria for which notebooks you want to execute before converting
them to HTML. The default is 'no-execution'. The four options are below, in order of
more execution:
- 'no-execution': This will not execute any notebooks. You may receive warnings if
    specific notebooks should be executed.
- 'execute-updated-unskipped-notebooks': Execute only notebooks which have been
    updated/changed or are new, excluding notebooks flagged for skipping.
- 'execute-all-unskipped-notebooks': Execute all notebooks except those flagged for
    skipping.
- 'execute-absolutely-all-notebooks': Execute all notebooks.
"""),
    )
    parser.add_argument(
        "--build-on-dev",
        type=str,
        help="Optionally provide the commit from upstream/master",
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
        "--build-type",
        action="store",
        default="stable",
        choices=[
            "stable",
            "master",
            "custom",
        ],
        help=textwrap.dedent(
"""Specify which version of HNN-core you want to use for building the textbook. The
default is 'stable'. This ASSUMES you have the correct version installed in your local
environment. The three options are below:
- 'stable': This builds the textbook using the latest stable version of HNN-Core, as
    detected from a request to PyPI.
- 'master': This builds the textbook using the latest development version of HNN-Core
    from the 'master' branch, as detected from a request to Github.
- 'custom': This builds the textbook using a custom commit and, optionally, a custom
    repository-owner's version of HNN-Core. If using this option, you must provide the
    repository-owner and/or commit you want using the '--custom-repo-commit' argument.
"""
        ),
    )
    parser.add_argument(
        "--custom-owner-commit",
        type=str,
        help=textwrap.dedent(
""" Optionally provide a specific commit of HNN-core to use in the form of
<owner>:<commit>. For example, if you wanted to build using the commit at
https://github.com/asoplata/hnn-core/commit/92b000c597052a661d9e177b8754695446336b96 ,
you would use '--custom-owner-commit asoplata:92b000c'. This assumes that the
fork/repository name is always 'hnn-core'. This is required if you are using
'--build-type custom'.
        """),
    )

    # add all above arguments to the parser
    args = parser.parse_args()

    if args.custom_root_path:
        root_path = args.custom_root_path
    else:
        root_path = textbook_root_path

    content_path = Path(root_path / "content")
    index_path = Path(root_path / "index.json")
    nb_hash_path = Path(root_path / "scripts" / "nb_hashes.json")
    nb_skip_path = Path(root_path / "scripts" / "nbs_to_skip.json")
    templates_path = Path(root_path / "templates")

    print(textwrap.dedent(
        f"""
Configuration: Choosing notebooks based on '--execution-filter={args.execution_filter}'
Configuration: Building notebooks based on '--build-type={args.build_type}'
        """
    ))

    # commit_hash = get_commit_hash(
    #     args.build_on_dev,
    #     args.build_type,
    #     args.custom_owner_commit,
    # )

    # execute_and_convert_nbs_to_json(
    #     content_path,
    #     nb_hash_path,
    #     nb_skip_path,
    #     args.execution_filter,
    #     dev_build=commit_hash,
    #     write_standalone_html=True,
    # )

    generate_page_html(
        content_path,
        index_path,
        templates_path,
        dev_build=args.build_on_dev,
    )


if __name__ == "__main__":
    main()
