import os

from tools.logger import logger
from actions_handler import ConfigReader
from tools.git import GitRepository, GitAlmaLinux, DirectoryManager

BRANCH_NOT_MODIFIED = "Branch is not modified"
PACKAGE_NOT_MODIFIED = "Package is not modified"
SUCCESS = "Debranding applied"


def apply_modifications(
    package,
    branch,
    set_custom_tag: str = "",
    no_tag: bool = False
):
    autopatch_working_dir = os.getcwd() + "/autopatch-namespace"
    rpms_working_dir = os.getcwd() + "/rpms-namespace"
    al_branch = branch.replace("c", "a", 1)


    if package not in GitAlmaLinux.get_list_of_modified_packages():
        logger.info(f"Package {package} is not modified")
        return PACKAGE_NOT_MODIFIED

    if al_branch not in GitAlmaLinux.get_branches_from_package(package):
        logger.info(f"Branch {al_branch} does not exist")
        return BRANCH_NOT_MODIFIED

    with DirectoryManager(autopatch_working_dir):
        config_repo = GitRepository(f"git@{GitAlmaLinux._almalinux_git}:{GitAlmaLinux._autopatch_namespace}/{package}.git")
        config_repo.checkout_branch(al_branch)
        config_repo.pull()

    config = ConfigReader(autopatch_working_dir + f"/{package}/config.yaml")

    with DirectoryManager(rpms_working_dir):
        git_repo = GitRepository(f"git@{GitAlmaLinux._almalinux_git}:{GitAlmaLinux._rpms_namespace}/{package}.git")
        git_repo.checkout_branch(branch)
        if not set_custom_tag:
            tag = git_repo.get_latest_tag().replace("imports/c", "changed/a", 1) + config.get_release_suffix()
        else:
            tag = set_custom_tag
        git_repo.pull()
        upstream_hash = git_repo.get_sbom_hash()

        git_repo.reset_to_base_branch(branch, al_branch, no_commit=True)
        config.apply_actions(rpms_working_dir + f"/{package}")

        changelog_entries, name, email = config.get_changelog()

        git_repo.commit(changelog_entries, name, email)
        if not no_tag:
            git_repo.create_tag(tag)
        git_repo.push(al_branch)
        git_repo.notarize_commit(upstream_hash)

    return SUCCESS
