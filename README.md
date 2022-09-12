# resumeBuilder
### Matteo Golin

Creates an HTML resume from a `resume.json` configuration file.

## Requirements
- Python 3.10.0+
- pdfkit
- wkhtmltopdf installation
- bs4 (BeautifulSoup)

## Notes
This works best for single page resumes and currently only really supports HTML output.
Unfortunately, wkhtmltopdf does not seem to support flexbox styling.

If you create a single page resume with this application, you can
turn it into a PDF on [sejda.com](https://www.sejda.com/html-to-pdf).

Resumes are outputted on legal paper size.

## Themes
### Monospace
- Uses Jetbrains Mono font, total black and white.
- Margins are 0.5in top and bottom, 0.3in left and right.