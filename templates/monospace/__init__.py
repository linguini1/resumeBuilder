# Components for Monospace resume template
__author__ = "Matteo Golin"

# Imports
from bs4 import BeautifulSoup
import resumeBuilder.templates.utils as utils


# Tag wrapper function
def make_tag(function):

    def wrapper(*args, **kwargs):
        return BeautifulSoup(function(*args, **kwargs), 'html.parser')

    return wrapper


# Components
@make_tag
def create_education_item(education_item: dict) -> str:

    """Returns an education item as an HTML component from the dict data."""

    location = f"{education_item['location']['city'].capitalize()}, " \
               f"{education_item['location']['province'].upper()}"

    tag = f"""
    <div class="education-list-item">
            <p class="certification">{education_item['certification']}</p>
            <p class="institution">{education_item['institution']}</p>
            <div class="location-date">
              <p class="location">{location}</p>
              <p>|</p>
              <p class="date">{utils.handle_empty_date(education_item['year'])}</p>
            </div>
          </div>
    """

    return tag


@make_tag
def create_list(list_data: list) -> str:

    """Returns list data as a ul>li HTML component."""

    tag = "<ul>"
    for element in list_data:
        tag += f"<li>{element}</li>"
    tag += "</ul>"

    return tag
