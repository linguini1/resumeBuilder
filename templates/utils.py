# Utility functions
__author__ = "Matteo Golin"

# Imports


# Functions
def format_month(month: str) -> str:

    """Returns three letter abbreviation for month."""

    return month.capitalize()[:3]


def handle_empty_date(date: str) -> str:

    """If the date is empty, the string will read 'Present'."""

    if not date or not date.strip():
        return "Present"
    else:
        return date


def format_address(address: dict) -> str:

    """Formats address JSON into an address string and returns it."""

    street = address['street']
    postal_code = address['postal_code'].upper()
    city = address['city'].capitalize()
    province = address['province'].upper()
    country = address['country'].capitalize()

    address_str = f"{street}, {postal_code}. {city}, {province}, {country}"

    return address_str


def start_and_end_date(data_packet: dict) -> tuple[str, str]:

    """Returns the formatted start and end dates."""

    start_date = data_packet['start_date']
    end_date = data_packet['end_date']

    start_date_str = f"{format_month(start_date['month'])} {start_date['year']}"
    end_date_str = f"{format_month(end_date['month'])} {end_date['year']}"

    return start_date_str, handle_empty_date(end_date_str)
