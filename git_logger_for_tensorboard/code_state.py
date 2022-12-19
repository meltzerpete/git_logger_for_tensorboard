# code adapted from https://github.com/wandb/wandb/blob/e3e7a53537f637f470051fec732df0331b2d6865/wandb/sdk/internal
# /system/system_info.py
# MIT license
import logging
import subprocess
import sys
from io import StringIO

from git_logger_for_tensorboard.git_repo import GitRepo

logger = logging.getLogger(__name__)


class CodeState:
    def __init__(self, repo: GitRepo):
        self.git = repo
        self.patch = None
        self.upstream_patch = None
        self._save_patches()

    def _save_patches(self) -> None:

        """Save the current state of this repository to one or more patches.

        Makes one patch against HEAD and another one against the most recent
        commit that occurs in an upstream branch. This way we can be robust
        to history editing as long as the user never does "push -f" to break
        history on an upstream branch.

        Writes the first patch to <files_dir>/<DIFF_FNAME> and the second to
        <files_dir>/upstream_diff_<commit_id>.patch.

        """

        if not self.git.enabled:
            return None

        logger.debug("Saving git patches")
        try:
            root = self.git.root
            diff_args = ["git", "diff"]
            if self.git.has_submodule_diff:
                diff_args.append("--submodule=diff")

            if self.git.dirty:
                # patch_path = os.path.join(self.files_dir, 'diff.patch')
                # with open(patch_path, "wb") as patch:
                # we diff against HEAD to ensure we get changes in the index
                self.patch = subprocess.check_output(
                    diff_args + ["HEAD"], cwd=root, timeout=5
                ).decode('utf-8')

            upstream_commit = self.git.get_upstream_fork_point()  # type: ignore
            if upstream_commit and upstream_commit != self.git.repo.head.commit:
                sha = upstream_commit.hexsha
                # upstream_patch_path = os.path.join(
                #     self.files_dir, f"upstream_diff_{sha}.patch"
                # )
                # with open(upstream_patch_path, "wb") as upstream_patch:
                self.upstream_patch = subprocess.check_output(
                    diff_args + [sha], cwd=root, timeout=5
                ).decode('utf-8')

        # TODO: A customer saw `ValueError: Reference at 'refs/remotes/origin/foo'
        #  does not exist` so we now catch ValueError. Catching this error feels
        #  too generic.
        except (
                ValueError,
                subprocess.CalledProcessError,
                subprocess.TimeoutExpired,
        ) as e:
            logger.error("Error generating diff: %s" % e)
        logger.debug("Saving git patches done")
