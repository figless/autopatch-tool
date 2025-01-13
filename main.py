import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.actions_handler import ConfigReader
from src.tools.git import GitRepository


# TEST PART
config = ConfigReader("/Users/eduardabdullin/Desktop/job/regular_work/git.almalinux.org/autopatch/kernel/config.yaml")
config.apply_actions("/Users/eduardabdullin/Desktop/job/regular_work/git.almalinux.org/rpms/kernel")


# /Users/eduardabdullin/Desktop/job/regular_work/autopatch-tool/tests/results/clufter

# FULL PART

# config = ConfigReader("/Users/eduardabdullin/Desktop/job/regular_work/git.almalinux.org/autopatch/anaconda/config.yaml")
# 
# git_repo = GitRepository("git@git.almalinux.org:rpms/anaconda.git")
# git_repo.pull()
# git_repo.reset_to_base_branch("c10s", "a10s")
# 
# config.apply_actions('/Users/eduardabdullin/Desktop/job/regular_work/autopatch-tool/anaconda')
# 
# git_repo.commit("AlmaLinux changes")
# git_repo.create_tag("changed/a10s/anaconda-40.22.3.20-1.el10.alma.1")
# git_repo.push("a10s")
# hash = git_repo.notarize_commit()
# 
# print(f"Commit notarization hash: {hash}")
