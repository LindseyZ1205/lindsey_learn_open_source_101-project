# -*- coding: utf-8 -*-

import os
import sys
import contextlib
import subprocess
from pathlib import Path

__version__ = "0.2.1"


@contextlib.contextmanager
def temp_cwd(path: Path):
    """
    Temporarily set the current working directory (CWD) and automatically
    switch back when it's done.
    """
    cwd = os.getcwd()
    os.chdir(str(path))
    try:
        yield path
    finally:
        os.chdir(cwd)


def run_unit_test(
    script: str,
    root_dir: str,
):
    """
    Run ``pytest -s --tb=native /path/to/script.py`` Command.

    :param script: the path to test script
    :param root_dir: the dir you want to temporarily set as cwd
    """
    bin_pytest = Path(sys.executable).parent / "pytest"
    args = [
        f"{bin_pytest}",
        "-s",
        "--tb=native",
        script,
    ]
    with temp_cwd(Path(root_dir)):
        subprocess.run(args)


def run_cov_test(
    script: str,
    module: str,
    root_dir: str,
    htmlcov_dir: str,
    preview: bool = False,
    is_folder: bool = False,
):
    """
    Run pytest with coverage for a specific module or folder.

    :param script: the test script absolute path
    :param module: the dot notation to the python module you want to calculate coverage
    :param root_dir: the dir to dump coverage results binary file
    :param htmlcov_dir: the dir to dump HTML output
    :param preview: whether to open the HTML output in web browser after the test
    :param is_folder: whether the module is a folder
    """
    bin_pytest = Path(sys.executable).parent / "pytest"
    if is_folder:
        script = f"{Path(script).parent}"
    if module.endswith(".py"):  # pragma: no cover
        module = module[:-3]
    args = [
        f"{bin_pytest}",
        "-s",
        "--tb=native",
        f"--rootdir={root_dir}",
        f"--cov={module}",
        "--cov-report",
        "term-missing",
        "--cov-report",
        f"html:{htmlcov_dir}",
        script,
    ]
    with temp_cwd(Path(root_dir)):
        subprocess.run(args)
    if preview:  # pragma: no cover
        platform = sys.platform
        if platform in ["win32", "cygwin"]:
            open_command = "start"
        elif platform in ["darwin", "linux"]:
            open_command = "open"
        else:
            raise NotImplementedError
        subprocess.run([open_command, f"{Path(htmlcov_dir).joinpath('index.html')}"])
