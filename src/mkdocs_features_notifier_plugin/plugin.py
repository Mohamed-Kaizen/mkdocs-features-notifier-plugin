"""A Plugin for mkdocs to add way to notify user for new docs file or feature."""
from typing import Tuple

from mkdocs.config import Config
from mkdocs.config.config_options import Type as MkType
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import Files

from .utils import append_config, get_config, update_features_file


class FeaturesNotifier(BasePlugin):
    """The class for FeaturesNotifier that inherited from mkdocs plugins."""

    config_scheme: Tuple[Tuple[str, MkType]] = (
        ("features_file", MkType(str, default="features.md")),  # type: ignore
        ("config_file", MkType(str, default="config.toml")),
    )

    def on_files(self: "FeaturesNotifier", files: Files, config: Config) -> Files:
        """Overriding the on_files method."""
        current_pages = []
        docs_dir = config.get("docs_dir")
        features_file = self.config.get("features_file")
        config_file = self.config.get("config_file")

        for file in files:
            if file.src_path.endswith("md"):
                current_pages.append(file.src_path)

            if file.src_path == features_file:
                features_file = f"{docs_dir}/{file.src_path}"
        initial_pages, write_mode = get_config(
            docs_dir=docs_dir, config_file=config_file, current_pages=current_pages
        )

        new_pages = [
            f"{docs_dir}/{page}" for page in current_pages if page not in initial_pages
        ]
        if new_pages and not write_mode:
            append_config(
                docs_dir=docs_dir, config_file=config_file, current_pages=current_pages
            )
            update_features_file(
                docs_dir=docs_dir, features_file=features_file, new_pages=new_pages
            )

        return files
