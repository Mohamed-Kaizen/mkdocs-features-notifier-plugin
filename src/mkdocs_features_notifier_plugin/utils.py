"""Collection of utils."""
from datetime import datetime
from typing import List, Tuple

import toml


def get_date() -> str:
    """Get today date."""
    date_time = datetime.today()
    return f"{date_time.year}.{date_time.month}.{date_time.day}"


def get_config(
    *, docs_dir: str, config_file: str, current_pages: List[str]
) -> Tuple[List, bool]:
    """Getting the config file.

    Args:
        docs_dir: A path to the docs folder.
        config_file: The config file name.
        current_pages: List of the pages in the docs.

    Returns:
        List of markdown file or empty list.

    """
    try:
        data = toml.load(f"{docs_dir}/{config_file}")
        return data.get("docs", []).get("date", []).popitem()[1].get("pages", []), False

    except (FileNotFoundError, toml.TomlDecodeError, AttributeError, KeyError):
        data = {"docs": {"date": {f"{get_date()}": {"pages": current_pages}}}}

        with open(f"{docs_dir}/{config_file}", "w") as f:
            toml.dump(data, f)

        return [], True


def append_config(*, docs_dir: str, config_file: str, current_pages: List[str]) -> None:
    """Append data into config file.

    Args:
        docs_dir: A path to the docs folder.
        config_file: The config file name.
        current_pages: List of the pages in the docs.

    """
    data = toml.load(f"{docs_dir}/{config_file}")

    data["docs"]["date"][f"{get_date()}"] = {"pages": current_pages}

    with open(f"{docs_dir}/{config_file}", "a") as f:
        toml.dump(data, f)


def get_description(*, content: str) -> str:
    """Getting description from the content of the file."""
    try:
        description = content.split("description:")[1].split("\n")[0].strip()
    except IndexError:
        description = "No description"
    return description


def get_path(*, content: str, default: str) -> str:
    """Getting path of the file from the content of the file.

    Args:
        content: File string content.
        default: Fallback in case the permalink doesn't exists inside the file.

    Returns:
        A path from permalink or the default value.
    """
    try:
        path = content.split("permalink:")[1].split("\n")[0].strip()
    except IndexError:
        path = f"/{default}"
    return path


def get_title(*, content: str, default: str) -> str:
    """Getting title of the file from the content of the file.

    Args:
        content: File string content.
        default: Fallback in case the title doesn't exists inside the file.

    Returns:
        A title from title or the default value.
    """
    try:
        title = content.split("title:")[1].split("\n")[0].strip()
    except IndexError:
        title = f"{default}".capitalize()
    return title


def update_content(*, docs_dir: str, new_pages: List[str]) -> str:
    """Updating content inside the feature file.

    Args:
        docs_dir: A path to the docs folder.
        new_pages: List of all new add pages.

    Returns:
        The updated content of the feature file.
    """
    header = f"# New in version {get_date()} \n\n--------"
    message = ""

    for page in new_pages:
        with open(page, "r") as documentation_file:
            documentation_content = documentation_file.read()

        description = get_description(content=documentation_content)

        name = page.replace(f"{docs_dir}/", "").split(".")[0]

        path = get_path(content=documentation_content, default=name)

        title = get_title(content=documentation_content, default=name)

        message += f"\n- [{title}]({path})\n\n\t> {description}\n\n"

    return header + message


def update_features_file(
    *, docs_dir: str, features_file: str, new_pages: List[str]
) -> None:
    """Update the feature file.

    Args:
        docs_dir: A path to the docs folder.
        features_file: The feature file name.
        new_pages: List of the new pages in the docs.

    """
    try:
        with open(features_file, "r") as file_r:
            features_file_read = file_r.read()

    except FileNotFoundError:
        features_file = f"{docs_dir}/{features_file}"

    finally:
        with open(features_file, "w") as file_w:
            message = update_content(docs_dir=docs_dir, new_pages=new_pages)
            file_w.write(f"{message}\n{features_file_read}")
