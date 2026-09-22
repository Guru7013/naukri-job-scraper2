from http.server import BaseHTTPRequestHandler


class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Naukri Job Scraper</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 40px;
                    background: #f5f5f5;
                }

                .container {
                    max-width: 900px;
                    margin: auto;
                    background: white;
                    padding: 30px;
                    border-radius: 10px;
                }

                h1 {
                    color: #333;
                }

                .box {
                    padding: 20px;
                    background: #eeeeee;
                    border-radius: 8px;
                    margin-top: 20px;
                }
            </style>
        </head>

        <body>
            <div class="container">

                <h1>Naukri Job Scraper</h1>

                <p>
                    Python + Playwright Job Scraping Project
                </p>

                <div class="box">
                    <h2>Project Details</h2>

                    <p><b>Search:</b> Python Developer</p>
                    <p><b>Location:</b> Chennai</p>
                    <p><b>Technology:</b> Python, Playwright, Pandas</p>
                    <p><b>Output:</b> Excel</p>

                    <p>
                        The project scrapes job title, company,
                        location, experience, skills, posted date
                        and job URL.
                    </p>

                    <p>
                        Duplicate jobs are avoided using the Job URL.
                    </p>
                </div>

            </div>
        </body>
        </html>
        """

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        self.wfile.write(html.encode("utf-8"))