from pathlib import Path
import shutil
from typing import Optional
import os

from immudb_wrapper import ImmudbWrapper

from tools.logger import logger
from tools.tools import (
    run_command,
    load_cas_credentials,
)


class DirectoryManager:
    def __init__(self, path):
        self.new_path = Path(path)
        self.previous_path = Path.cwd()

    def __enter__(self):
        try:
            self.new_path.mkdir(parents=True, exist_ok=True)
            logger.debug(f"Switching to directory {self.new_path}")
            os.chdir(self.new_path)
        except Exception as e:
            logger.error(f"Error changing directory: {e}")
            raise

    def __exit__(self, exc_type, exc_val, exc_tb):
        logger.debug(f"Reverting to directory {self.previous_path}")
        os.chdir(self.previous_path)

class GitRepositoryError(Exception):
    """Base class for exceptions in this module."""
    def __init__(self, message):
        self.message = message
        super().__init__(message)

class GitRepository:
    def __init__(self, url, clone: bool = True):
        self.url = url
        self.name = self.url.split("/")[-1].replace(".git", "")
        if clone:
            self.__clone()

    def __clone(self):
        logger.info(f"Cloning repository {self.url}")
        if Path(self.name).exists():
            shutil.rmtree(self.name)
        run_command(["git", "clone", self.url])

    def run_in_repo(self, *command, shell=False):
        with DirectoryManager(self.name):
            run_command(list(command), shell=shell)

    def pull(self):
        logger.info(f"Pulling repository {self.url}")
        self.run_in_repo("git", "pull")

    def pull_branch(self, branch: str):
        logger.info(f"Pulling repository {self.url} branch {branch}")
        self.run_in_repo("git", "pull", "origin", branch)

    def create_tag(self, tag: str):
        logger.info(f"Creating tag {tag}")
        self.run_in_repo("git", "tag", tag)

    def push_tags(self):
        logger.info(f"Pushing tag new tags to {self.name}")
        self.run_in_repo("git", "push", "--tags")

    def push(self, branch: str, force: bool = False):
        logger.info(f"Pushing to repository {self.url}")
        command = ["git", "push", "origin", branch]
        if force:
            command.append("-f")
        self.run_in_repo(*command)
        self.push_tags()

    def commit(self, message: str):
        logger.info(f"Committing changes to {self.url}")
        self.run_in_repo("git", "add", ".")
        self.run_in_repo("git", "commit", "-m", message)

    def checkout_branch(self, branch: str):
        logger.info(f"Checking out branch {branch}")
        with DirectoryManager(self.name):
            result = run_command(["git", "checkout", branch], raise_on_failure=False)
            if result.returncode != 0:
                logger.info(f"Branch {branch} does not exist, creating it.")
                run_command(["git", "checkout", "--orphan", branch])
    
    def replace_file(self, replacing_branch: str, file: str):
        logger.info(f"Replacing file {file} with {replacing_branch}")
        self.run_in_repo("git", "checkout", replacing_branch, "--", file)

    def notarize_commit(self) -> Optional[str]:
        immudb_wrapper = ImmudbWrapper(**load_cas_credentials())
        response = immudb_wrapper.notarize_git_repo(
            self.name,
            user_metadata={'sbom_api_ver': '0.2'},
        )
        if response.get('verified') != True:
            logger.error(f"Failed to notarize commit: {response}")
            raise GitRepositoryError("Failed to notarize commit")
        return response.get('value', {}).get('Hash')
    
    def merge_branch(self, branch: str, strategy: str = None, no_commit: bool = False):
        command = ["git", "merge", branch]

        if 'ours' not in strategy and 'theirs' not in strategy:
            logger.error(f"Invalid strategy: {strategy}")
            raise GitRepositoryError("Invalid strategy")

        if strategy:
            command.extend(["-X", strategy])
        if no_commit:
            command.append("--no-commit")

        logger.debug(f"Merging branch {branch} with options: strategy={strategy}, no_commit={no_commit}")
        self.run_in_repo(*command)

    def clean_repodir(self):
        with DirectoryManager(self.name):
            if os.path.exists('.'):
                for item in os.listdir('.'):
                    if item.startswith('.'):
                        logger.debug(f"Skipping hidden file: {item}")
                        continue
                    item_path = os.path.join('.', item)
                    if os.path.isfile(item_path):
                        os.remove(item_path)
                        logger.debug(f"Deleted file: {item_path}")
                    elif os.path.isdir(item_path):
                        shutil.rmtree(item_path)
                        logger.debug(f"Deleted folder: {item_path}")
            else:
                logger.error(f"Directory is empty: {self.name}")

    def reset_to_base_branch(self, base_branch: str, target_branch: str, no_commit: bool = False):
        self.checkout_branch(base_branch)
        self.checkout_branch(target_branch)

        self.merge_branch(base_branch, strategy='theirs', no_commit=True)
        # All files in the target branch should be replaced with the files in the base branch
        self.clean_repodir()
        self.run_in_repo("ls", "-la")
        self.replace_file(base_branch, '.')

        if not no_commit:
            self.commit(f"Merge '{base_branch}' into '{target_branch}'")
