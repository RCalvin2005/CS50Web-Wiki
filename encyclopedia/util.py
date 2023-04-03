import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None


def convert(markdown):
    """ Converts markdown to HTML """

    # https://www.pythontutorial.net/python-regex/python-regex-sub/
    
    html = re.sub(
        r"\r",
        "",
        markdown,
    )

    # Headings
    html = re.sub(
        r"^(#+) *(.+)$",
        heading,
        html,
        flags=re.MULTILINE
    )

    # Boldface
    html = re.sub(
        r"\*\*(.*?)\*\*",
        r"<strong>\1</strong>",
        html,
        flags=re.DOTALL
    )

    html = re.sub(
        r"__(.*?)__",
        r"<strong>\1</strong>",
        html,
        flags=re.DOTALL
    )

    # https://stackoverflow.com/questions/44757825/python-regex-for-end-of-line

    # Unordered List (no nesting)
    html = re.sub(
        r"(?:^|\n\n+)([\*\+-] +.*?)(?:\n\n+|$)",
        ul,
        html,
        flags=re.DOTALL
    )

    # Links

    # Paragraph

    return html


def heading(match):
    """ Returns replacement str for headings """

    level = len(match.group(1))
    if level > 6:
        level = 6

    return f"<h{level}>{match.group(2)}</h{level}>\n"


def ul(match):
    """ Returns replacement str for lists """

    markdown = match.group(1)

    list_items = re.sub(
        r"[\*\+-] +(.*?)(?:\n(?=[\*\+-])|$)",
        r"<li>\1</li>\n",
        markdown,
        flags=re.DOTALL
    )

    return f"\n\n<ul>\n{list_items}</ul>\n\n"
