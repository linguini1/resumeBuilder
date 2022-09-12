# Resume template class
__author__ = "Matteo Golin"

# Imports
import json
import os
from datetime import datetime as dt
from abc import ABC, abstractmethod
import pdfkit
from bs4 import BeautifulSoup
import resumeBuilder.templates.utils as utils

# Monospace snippets
import resumeBuilder.templates.monospace as monospace

# Constants
WKHTMLTOPDF_PATH = "C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe"


# Class
class ResumeTemplate(ABC):

    PARSER = 'html.parser'
    THEME_NAME: str
    OPTIONS = {
        "dpi": 300,
        "page-size": "A5",
        "margin-top": "0",
        "margin-bottom": "0",
        "margin-left": "0",
        "margin-right": "0",
        "encoding": "UTF-8",
        "no-outline": None,
    }

    def __init__(self, data_file_path: str):
        self.data = self.__load_resume_data(data_file_path)
        self.file_path = f"{os.getcwd()}\\Resume_{self.data['profile']['name']}_{dt.today().date()}"  # Resume filepath
        self.template = self.__load_html()

    @staticmethod
    def __load_resume_data(file_path: str) -> dict:

        """Returns the resume data from the specified JSON file as a dictionary object."""

        with open(file_path, 'r') as json_file:
            data = json.load(json_file)

        return data

    def __load_html(self) -> BeautifulSoup:

        """Returns the soup of the HTML template."""

        with open(f"./templates/{self.THEME_NAME}/{self.THEME_NAME}.html", 'r') as html:
            soup = BeautifulSoup(html.read(), self.PARSER)

        return soup

    def __add_css_styles(self) -> None:

        """Adds the CSS styles to template."""

        with open(f"./templates/{self.THEME_NAME}/{self.THEME_NAME}.css", 'r') as css:
            styles = f"<style>{css.read()}</style>"

        style_tag = BeautifulSoup(styles, self.PARSER)
        self.template.find("body").append(style_tag)

    def __str__(self) -> None:
        return f"{self.data['profile']['name']}'s resume - {self.THEME_NAME.capitalize()} theme."

    def __save_as_pdf(self) -> None:

        """Saves the template as a PDF."""

        # Config
        config = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_PATH)

        try:
            pdfkit.from_file(
                f"{self.file_path}.html", f"{self.file_path}.pdf",
                options=self.OPTIONS,
                configuration=config
            )
        except OSError:  # Protocol unknown error
            pass

    def save_as(self, pdf=False, html=True) -> None:

        """Saves the template as an HTML file or PDF file based on parameters."""

        # Populate data
        self._populate()
        self.__add_css_styles()

        # Save obligatory HTML file
        with open(f"{self.file_path}.html", "w") as html_file:
            html_file.write(str(self.template))

        if pdf:  # Save PDF if selected
            self.__save_as_pdf()

        if not html:  # If HTML not desired, delete it after PDF is saved
            os.remove(f"{self.file_path}.html")

    # Helper functions
    @staticmethod
    def _replace_text(element: BeautifulSoup, new_text: str) -> None:

        """Replaces the element's text with new text."""

        element.string.replace_with(new_text)

    def _search_by_attribute(self, attribute: str, value: str) -> BeautifulSoup:

        """Searches the template for elements with the passed attribute and returns the element."""

        return self.template.find(attrs={attribute: value})

    # Abstract
    @abstractmethod
    def _populate(self) -> None:
        """Populates the resume template with data from the data file."""
        ...


class MonospaceResume(ResumeTemplate):

    THEME_NAME = "monospace"

    def __profile(self) -> None:

        """Populates the profile section."""

        # Get elements
        candidate_name = self._search_by_attribute("id", "candidate-name")
        candidate_descriptor = self._search_by_attribute("id", "candidate-descriptor")
        candidate_description = self._search_by_attribute("id", "description")

        # Replace text
        self._replace_text(candidate_name, self.data['profile']['name'])
        self._replace_text(candidate_descriptor, self.data['profile']['descriptor'])
        self._replace_text(candidate_description, self.data['profile']['description'])

    def __contact(self) -> None:

        """Populates the contact section."""

        contact = self.data['contact']

        # Get elements
        phone = self._search_by_attribute("id", "phone")
        email = self._search_by_attribute("id", "email")
        address = self._search_by_attribute("id", "address")
        github = self._search_by_attribute("id", "github")
        linkedin = self._search_by_attribute("id", "linkedin")

        # Replace text
        self._replace_text(phone, contact['phone'])
        self._replace_text(email, contact['email'])
        self._replace_text(address, utils.format_address(contact['address']))
        self._replace_text(github, contact['github'])
        self._replace_text(linkedin, contact['linkedin'])

    def __education(self) -> None:

        """Populates education."""

        # Get education section
        education_section = self._search_by_attribute("id", "education")

        for education_item in self.data['education']:
            education_item_tag = monospace.create_education_item(education_item)
            education_section.append(education_item_tag)

    def __skills(self):

        """Populates skills."""

        # Data
        tools = self.data['skills']['tools']
        abilities = self.data['skills']['abilities']

        # Elements
        tools_section = self._search_by_attribute("id", "tools")
        abilities_section = self._search_by_attribute("id", "abilities")

        # Append skills
        tools_section.append(monospace.create_list(tools))
        abilities_section.append(monospace.create_list(abilities))

    def _populate(self) -> None:

        self.__profile()
        self.__contact()
        self.__education()
        self.__skills()
