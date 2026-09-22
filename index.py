import pandas as pd
from pathlib import Path
from http.server import BaseHTTPRequestHandler
import html


class handler(BaseHTTPRequestHandler):

    def do_GET(self):

        try:
            excel_file = Path(__file__).parent.parent / "naukri_jobs.xlsx"

            df = pd.read_excel(excel_file)

            # Replace empty values
            df = df.fillna("")

            rows = ""

            for _, job in df.iterrows():

                rows += f"""
                <tr>
                    <td>{html.escape(str(job.get("Title", "")))}</td>
                    <td>{html.escape(str(job.get("Company", "")))}</td>
                    <td>{html.escape(str(job.get("Location", "")))}</td>
                    <td>{html.escape(str(job.get("Experience", "")))}</td>
                    <td>{html.escape(str(job.get("Skills", "")))}</td>
                    <td>{html.escape(str(job.get("Posted Date", "")))}</td>
                    <td>
                        <a href="{html.escape(str(job.get("Job URL", "")))}"
                           target="_blank">
                            Apply / View Job
                        </a>
                    </td>
                </tr>
                """

            page = f"""
            <!DOCTYPE html>
            <html>

            <head>

                <title>Naukri Job Scraper</title>

                <meta name="viewport"
                      content="width=device-width, initial-scale=1">

                <style>

                    body {{
                        font-family: Arial, sans-serif;
                        margin: 0;
                        background: #f5f5f5;
                    }}

                    .header {{
                        background: #ffffff;
                        padding: 25px;
                        text-align: center;
                        border-bottom: 1px solid #ddd;
                    }}

                    h1 {{
                        margin: 0;
                        color: #222;
                    }}

                    .subtitle {{
                        margin-top: 8px;
                        color: #666;
                    }}

                    .container {{
                        padding: 25px;
                        overflow-x: auto;
                    }}

                    .count {{
                        margin-bottom: 15px;
                        font-size: 18px;
                        font-weight: bold;
                    }}

                    table {{
                        width: 100%;
                        border-collapse: collapse;
                        background: white;
                    }}

                    th {{
                        background: #333;
                        color: white;
                        padding: 12px;
                        text-align: left;
                    }}

                    td {{
                        padding: 10px;
                        border-bottom: 1px solid #ddd;
                    }}

                    tr:hover {{
                        background: #f1f1f1;
                    }}

                    a {{
                        color: #0066cc;
                        text-decoration: none;
                        font-weight: bold;
                    }}

                </style>

            </head>

            <body>

                <div class="header">

                    <h1>Naukri Job Scraper</h1>

                    <div class="subtitle">
                        Python Developer Jobs - Chennai
                    </div>

                </div>

                <div class="container">

                    <div class="count">
                        Total Jobs: {len(df)}
                    </div>

                    <table>

                        <thead>

                            <tr>
                                <th>Title</th>
                                <th>Company</th>
                                <th>Location</th>
                                <th>Experience</th>
                                <th>Skills</th>
                                <th>Posted Date</th>
                                <th>Job URL</th>
                            </tr>

                        </thead>

                        <tbody>

                            {rows}

                        </tbody>

                    </table>

                </div>

            </body>

            </html>
            """

            self.send_response(200)
            self.send_header(
                "Content-Type",
                "text/html; charset=utf-8"
            )
            self.end_headers()

            self.wfile.write(
                page.encode("utf-8")
            )

        except Exception as e:

            self.send_response(500)
            self.send_header(
                "Content-Type",
                "text/html; charset=utf-8"
            )
            self.end_headers()

            error_page = f"""
            <h1>Error loading jobs</h1>
            <p>{html.escape(str(e))}</p>
            """

            self.wfile.write(
                error_page.encode("utf-8")
            )