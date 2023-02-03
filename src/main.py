from git import Repo
import shutil
import os

class GithubHelper:
    def __init__(self, repo_name, username, password) -> None:
        self.username = username
        self.password = password
        self.repo_name = repo_name

        # self.remote = "https://{username}:{password}@github.com/amagimedia/{repo_name}.git".format(username, password, repo_name)
        self.remote = "https://{}:{}@github.com/karansingh-amagi/{}.git".format(username, password, repo_name)


    def clone_and_copy(self, copy_dir):
        if os.path.isdir(self.repo_name):
            shutil.rmtree(os.path.join(os.getcwd(), self.repo_name))

        Repo.clone_from(self.remote, self.repo_name)
        dest = str(os.path.join(os.getcwd(), self.repo_name))
        shutil.copytree(copy_dir, dest, dirs_exist_ok=True, ignore=shutil.ignore_patterns('.*', '_*'))


    def commit_push_delete(self, commit_msg: str, branch_name: str):
        repo = Repo(self.repo_name)
        repo.git.checkout('-B', branch_name)
        repo.git.add(".")
        repo.git.commit(m=commit_msg)
        repo.git.push('--set-upstream', repo.remote().name, branch_name)
        
        shutil.rmtree(os.path.join(os.getcwd(), self.repo_name))

