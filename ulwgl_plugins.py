import os
from pathlib import Path
from typing import Dict, Set


def enable_steam_game_drive(env: Dict[str, str]) -> Dict[str, str]:
    """Enable Steam Game Drive functionality.

    Expects STEAM_COMPAT_INSTALL_PATH to be set
    STEAM_RUNTIME_LIBRARY_PATH will not be set if the exe directory does not exist
    """
    paths: Set[str] = set()
    root: Path = Path("/")

    # Check for mount points going up toward the root
    # NOTE: Subvolumes can be mount points
    for path in Path(env["STEAM_COMPAT_INSTALL_PATH"]).parents:
        if path.is_mount() and path != root:
            if env["STEAM_COMPAT_LIBRARY_PATHS"]:
                env["STEAM_COMPAT_LIBRARY_PATHS"] = (
                    env["STEAM_COMPAT_LIBRARY_PATHS"] + ":" + path.as_posix()
                )
            else:
                env["STEAM_COMPAT_LIBRARY_PATHS"] = path.as_posix()
            break

    if "LD_LIBRARY_PATH" in os.environ:
        paths.add(Path(os.environ["LD_LIBRARY_PATH"]).as_posix())

    if env["STEAM_COMPAT_INSTALL_PATH"]:
        paths.add(env["STEAM_COMPAT_INSTALL_PATH"])

    # Hard code for now because these paths seem to be pretty standard
    # This way we avoid shelling to ldconfig
    paths.add("/usr/lib")
    paths.add("/usr/lib32")
    env["STEAM_RUNTIME_LIBRARY_PATH"] = ":".join(list(paths))

    return env
