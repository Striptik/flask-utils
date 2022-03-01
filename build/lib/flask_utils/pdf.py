import os


import jinja2
import pdfkit

import config
from flask import url_for


def generate_pdf(
        template_file,
        file_name,
        page_size="A4",
        margin_top="0.35in",
        margin_bottom="0.75in",
        margin_x="0.75in",
        **kwargs,
):
    template_loader = jinja2.FileSystemLoader(searchpath="./assets")
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template(template_file)
    output_text = template.render(url_for=url_for, **kwargs)

    html_path = f"./temp/{file_name}.html"
    html_file = open(html_path, "w")
    html_file.write(output_text)
    html_file.close()
    pdf_path = f"./temp/{file_name}.pdf"
    html2pdf(
        html_path=html_path,
        pdf_path=pdf_path,
        page_size=page_size,
        margin_top=margin_top,
        margin_bottom=margin_bottom,
        margin_x=margin_x,
    )

def html2pdf(html_path, pdf_path, page_size, margin_top, margin_bottom, margin_x):
    options = {
        "page-size": page_size,
        "margin-top": margin_top,
        "margin-right": margin_x,
        "margin-bottom": margin_bottom,
        "margin-left": margin_x,
        "encoding": "UTF-8",
        "orientation": "Portrait",
        "dpi": 600,
        "no-outline": None,
        "no-stop-slow-scripts": True,
        "enable-local-file-access": None,
    }

    configuration = (
        pdfkit.configuration(wkhtmltopdf="/opt/bin/wkhtmltopdf")
        if config.WKHTMLTOPDF_PATH
        else pdfkit.configuration()
    )
    with open(html_path) as f:
        pdfkit.from_file(f, pdf_path, options=options, configuration=configuration)


def remove_files(filenames):
    for filename in filenames:
        os.remove("{}/temp/{}".format(os.path.abspath(os.getcwd()), filename))
