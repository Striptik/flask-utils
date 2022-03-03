import os

import jinja2
import pdfkit
import tempfile
from flask import render_template, url_for

import config


def price(value):
    return "{}€".format(round(value / 100, 2))


def add_pdf_header(header_html, options, **kwargs):
    if header_html is None:
        return
    with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as header:
        options["header-html"] = header.name
        header.write(render_template(header_html, **kwargs).encode("utf-8"))
    return


def add_pdf_footer(footer_html, options, **kwargs):
    if footer_html is None:
        return
    with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as footer:
        options["footer-html"] = footer.name
        footer.write(render_template(footer_html, **kwargs).encode("utf-8"))
    return


def generate_pdf(
        template_file,
        file_name,
        header_html=None,
        footer_html=None,
        page_size="A4",
        margin_top="2in",
        margin_bottom="0.75in",
        margin_x="0.75in",
        **kwargs,
):
    template_loader = jinja2.FileSystemLoader(searchpath="./assets")
    template_env = jinja2.Environment(loader=template_loader)
    template_env.filters["price"] = price
    main_template = template_env.get_template(template_file)
    main_content = main_template.render(url_for=url_for, **kwargs)

    html_path = f"./temp/{file_name}.html"
    html_file = open(html_path, "w")
    html_file.write(main_content)
    html_file.close()

    options = {
        "page-size": page_size,
        "margin-top": margin_top,
        "margin-right": margin_x,
        "margin-bottom": margin_bottom,
        "margin-left": margin_x,
        "encoding": "UTF-8",
        "orientation": "Portrait",
        "dpi": 300,
        "no-outline": None,
        "no-stop-slow-scripts": True,
        "enable-local-file-access": True,
    }
    add_pdf_header(header_html, options, **kwargs)
    add_pdf_footer(footer_html, options, **kwargs)

    configuration = (
        pdfkit.configuration(wkhtmltopdf="/opt/bin/wkhtmltopdf")
        if config.WKHTMLTOPDF_PATH
        else pdfkit.configuration()
    )
    pdfkit.from_string(
        main_content,
        f"./temp/{file_name}.pdf",
        options=options,
        configuration=configuration,
    )


def remove_files(filenames):
    for filename in filenames:
        os.remove("{}/temp/{}".format(os.path.abspath(os.getcwd()), filename))
