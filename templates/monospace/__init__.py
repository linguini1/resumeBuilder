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


# Right panel list ite wrapper function
def right_panel_list_item(function):

    """Wrapper to turn the output of a component function into one wrapped by a right panel list item class div."""

    def wrapper(*args, **kwargs):
        return f'<div class="right-panel-list-item">{function(*args, **kwargs)}</div>'

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
              <p>{utils.handle_empty_date(education_item['year'])}</p>
            </div>
          </div>
    """

    return tag


@make_tag
def create_list(list_data: list, list_class: str = None) -> str:

    """Returns list data as a ul>li HTML component."""

    if list_class:
        tag = f'<ul class="{list_class}" >'
    else:
        tag = "<ul>"

    for element in list_data:
        tag += f"<li>{element}</li>"
    tag += "</ul>"

    return tag


@make_tag
@right_panel_list_item
def create_experience_item(experience_item: dict) -> str:

    """Returns a component for the experience item."""

    start_date, end_date = utils.start_and_end_date(experience_item)

    tag = f"""
    <h3 class="activity-header">{experience_item['position']}</h3>
            <div class="location-date">
              <p class="workplace">{experience_item['workplace']}</p>
              <p>|</p>
              <p class="start-date">{start_date}</p>
              <p>-</p>
              <p class="end-date">{end_date}</p>
            </div>
            {create_list(experience_item['highlights'], list_class="highlights")}
    """

    return tag


@make_tag
@right_panel_list_item
def create_extracurricular_item(extracurricular_item: dict) -> str:

    """Returns an HTML component for an extracurricular experience."""

    start_date, end_date = utils.start_and_end_date(extracurricular_item)

    tag = f"""
    <h3 class="activity-header">{extracurricular_item['activity']}</h3>
            <div class="location-date">
              <p class="organization">{extracurricular_item['organization']}</p>
              <p>|</p>
              <p class="start-date">{start_date}</p>
              <p>-</p>
              <p class="end-date">{end_date}</p>
            </div>
            {create_list(extracurricular_item['highlights'], 'highlights')}
    """

    return tag


@make_tag
@right_panel_list_item
def create_achievement_item(achievement_item: dict) -> str:

    """Returns a component for the achievement item as a string."""

    date = achievement_item['date']

    tag = f"""
    <h2 class="section-header">{achievement_item['achievement']}</h2>
            <p class="date">{utils.format_month(date['month'])} {date['year']}</p>
            {create_list(achievement_item['description'], 'highlights')}
    """

    return tag


@make_tag
def create_projects_item(project_item: dict) -> str:

    """Returns projects item HTML component as a string."""

    tag = f"""
    <div class="education-list-item">
            <p class="certification">{project_item['title']}</p>
            <p>{utils.handle_empty_date(project_item['year'])}</p>
            <p>{project_item['description']}</p>
          </div>
    """

    return tag


@make_tag
def create_reference_item(reference_item: dict) -> str:

    """Returns the reference item HTML component as a string."""

    email = reference_item['email']

    tag = f"""
    <div class="education-list-item">
            <p class="certification">{reference_item['name']}, {reference_item['position']}</p>
            <p>{reference_item['workplace']}</p>
            <p>{reference_item['phone']}</p>
            <a href="mailto:{email}">{email}</a>
          </div>
    """

    return tag
