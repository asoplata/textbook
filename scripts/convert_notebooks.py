# %%
import os
import base64
import html
import re
import json
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
from bs4 import BeautifulSoup


def execute_notebook(notebook_path):
    """Executes a Jupyter notebook and returns the
    executed notebook object."""
    with open(notebook_path, "r", encoding="utf-8") as f:
        notebook = nbformat.read(f, as_version=4)

    ep = ExecutePreprocessor(timeout=600, kernel_name="python3")
    ep.preprocess(
        notebook, {"metadata": {"path": os.path.dirname(notebook_path)}}
    )
    return notebook


def save_plot_as_image(img_data, img_filename, output_dir):
    """Saves the plot image to the specified directory."""
    img_path = os.path.join(output_dir, img_filename)
    with open(img_path, "wb") as img_file:
        img_file.write(base64.b64decode(img_data))
    return


def html_to_hierarchical_json(
        html: str,
        filename: str,
        ):
    soup = BeautifulSoup(html, 'html.parser')
    hierarchy = {filename: {}}
    stack = []

    for tag in soup.find_all(re.compile(r'h[1-6]')):
        level = int(tag.name[1])
        title = tag.get_text(strip=True)
        contents = str(tag) + ''.join(
            str(sibling) for sibling in tag.find_next_siblings()
            if not re.match(r'h[1-6]', sibling.name)
        )
        section = {"contents": contents}

        while stack and stack[-1][1] >= level:
            stack.pop()

        if stack:
            parent = stack[-1][0]
            if "sections" not in parent:
                parent["sections"] = {}
            parent["sections"][title] = section
        else:
            hierarchy[filename][title] = section

        stack.append((section, level))

    return hierarchy


def extract_html_from_notebook(
        notebook,
        input_dir,  # changed
        filename,
        use_base64=False
        ):
    """Extracts HTML for cell contents and outputs,
    including code and markdown."""

    html_output = []
    fig_id = 0
    delim = os.path.sep
    aggregated_output = ""

    for cell in notebook["cells"]:
        if cell["cell_type"] == "code":
            # add code cell contents
            html_output.append(
                "<div class='code-cell'>"
                "\n\t<code class='language-python'>"
                f"\n\t\t{cell['source']}"
                "\n\t</code>"
                "\n</div>"
            )

            # add code cell outputs
            for output in cell.get("outputs", []):
                # handle plain outputs (e.g., function returns)
                if "text/plain" in output.get("data", {}):
                    text_output = output["data"]["text/plain"]
                    # escape the '<' and '>' characters which can be
                    # incorrectly interpreted as HTML tags
                    escaped_text_output = html.escape(text_output)

                    # Aggregate plain text outputs
                    aggregated_output += f"\n\t\t{escaped_text_output}"

                # handle stdout (e.g., outputs from print statements)
                if output.get("output_type") == "stream" \
                        and output.get("name") == "stdout":
                    stream_output = output.get("text", "")
                    # escape < and > characters
                    escaped_stream_output = html.escape(stream_output)

                    aggregated_output += f"\n\t\t{escaped_stream_output}"

                # handle image outputs (e.g., plots) using either Base64
                # encoding or .png files
                if "image/png" in output.get("data", {}):
                    # If there are accumulated outputs, output them first
                    if aggregated_output:
                        html_output.append(
                            "<div class='output-cell'>"
                            "<div class='output-label'>"
                            "\n\tOut:"
                            "\n</div>"
                            "\n\t<div class='output-code'>"
                            f"{aggregated_output}"
                            "\n\t</div>"
                            "\n</div>"
                        )
                        aggregated_output = ""

                    img_data = output["data"]["image/png"]

                    if use_base64:
                        # optional Base64 encoding for image embedding
                        html_output.append(
                            "<div class='output-cell'>"
                            "\n\t<img src='data:image/png;base64,"
                            f"{img_data}'/>"
                            "\n</div>"
                        )
                    else:
                        # save the image as a file and reference it in HTML
                        fig_id += 1
                        if fig_id <= 10:
                            img_filename = f"fig_0{fig_id}.png"
                        else:
                            img_filename = f"fig_{fig_id}.png"

                        output_folder = "output_nb_" + \
                            f"{filename.split('.ipynb')[0]}"

                        output_dir = f"{input_dir}{delim}{output_folder}"

                        if not os.path.exists(output_dir):
                            os.makedirs(output_dir)

                        save_plot_as_image(
                            img_data,
                            img_filename,
                            output_dir,
                        )
                        html_output.append(
                            "<div class='output-cell'>"
                            f"\n\t<img src='{output_folder}{delim}"
                            f"{img_filename}'/>"
                            "\n</div>"
                        )

                # handle errors
                if output.get("output_type") == "error":
                    error_message = "\n".join(output.get("traceback", []))
                    html_output.append(
                        "<div class='output-cell error'>"
                        "\n\t<pre>"
                        f"\n\t\t{error_message}"
                        "\n\t</pre>"
                        "\n</div>"
                    )

            # If there are any accumulated outputs after processing all
            # outputs for the cell
            if aggregated_output:
                html_output.append(
                    "<div class='output-cell'>"
                    "<div class='output-label'>"
                    "\n\tOut:"
                    "\n</div>"
                    "\n\t<div class='output-code'>"
                    f"{aggregated_output}"
                    "\n\t</div>"
                    "\n</div>"
                )
                aggregated_output = ""

        elif cell["cell_type"] == "markdown":
            # escape < and > characters
            markdown_content = html.escape(cell["source"])

            # Identify header sections
            # -------------------------
            # Assume a header cell will only contain the header text
            # and no additional text content, though there may be extra
            # new lines or spaces that should be removed when determining
            # if a cell is a header cell

            # get lines with content, removing empty new lines
            lines = [
                line.strip() for line in markdown_content.splitlines()
                if line.strip()
            ]

            # handle header sections
            if (len(lines) == 1) and lines[0].startswith("#"):

                header_level = markdown_content.count("#")
                markdown_content = markdown_content.split("# ")[-1]

                html_output.append(
                    "<div class='markdown-cell'>"
                    f"\n\t<h{header_level}>"
                    f"\n\t\t{markdown_content}"
                    f"\n\t</h{header_level}>"
                    "\n</div>"
                )

            # handle non-header sections
            else:
                html_output.append(
                    "<div class='markdown-cell'>"
                    f"\n\t{markdown_content}"
                    "\n</div>"
                )

    html_output = "\n".join(html_output)

    return html_output


def convert_notebooks_to_html(
    input_folder,
    # output_folder,
    use_base64=False,
    write_html=False,
):
    """Executes and converts .ipynb files in the input folder to HTML."""
    # if not os.path.exists(output_folder):
    #     os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        path = os.path.join(input_folder, filename)
        if filename.endswith(".ipynb"):
            print(f"Processing notebook: {filename}")
            executed_notebook = execute_notebook(path)

            html_content = extract_html_from_notebook(
                executed_notebook,
                input_folder,  # changed
                filename,
                use_base64
            )

            if write_html:
                output_file = os.path.join(
                    input_folder, f"{os.path.splitext(filename)[0]}.html"
                )
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write("<html><body>\n")
                    f.write(html_content)
                    f.write("\n</body></html>")

            nb_html_json = html_to_hierarchical_json(
                html_content,
                filename,
            )

            output_json = os.path.join(
                input_folder, f"{os.path.splitext(filename)[0]}.json"
            )

            with open(output_json, "w") as f:
                json.dump(nb_html_json, f)

            print(f"Successfully converted '{filename}'")


# %%
def test_nb_conversion():

    input_folder = "../content/05_erps"

    convert_notebooks_to_html(
        input_folder,
        use_base64=False,
        write_html=True,
    )


test_nb_conversion()

# %%
