from git import Repo
import shutil
import os
'''
Testing changes
'''
class GithubHelper:
    def __init__(self, repo_name, username, password, org="amagimedia") -> None:
        self.username = username
        self.password = password
        self.repo_name = repo_name

        self.remote = "https://{}:{}@github.com/{}/{}.git".format(username, password, org, repo_name)

    def clone(self):
        try:
            if os.path.isdir(self.repo_name):
                shutil.rmtree(os.path.join(os.getcwd(), self.repo_name))
            Repo.clone_from(self.remote, self.repo_name)

            ## Implement logger
            print('clone finished')

        except Exception as e:
            raise(e)

    def clone_and_copy(self, copy_dir):
        self.clone()
        try: 
            dest = str(os.path.join(os.getcwd(), self.repo_name))
            shutil.copytree(copy_dir, dest, dirs_exist_ok=True, ignore=shutil.ignore_patterns('.*', '_*'))
        except Exception as e:
            raise(e)
        
    def commit_push(self, commit_msg: str, branch_name: str):
        try: 
            repo = Repo(self.repo_name)
            repo.git.checkout('-B', branch_name)
            repo.git.add(".")
            repo.git.commit(m=commit_msg)
            repo.git.push('--set-upstream', repo.remote().name, branch_name)

            ## Implement logger
            print("commit finished")

        except Exception as e:
            raise(e)

    def commit_push_delete(self, commit_msg: str, branch_name: str):
        self.commit_push(commit_msg, branch_name)
        try:
            shutil.rmtree(os.path.join(os.getcwd(), self.repo_name))

            ## Implement logger
            print("delete finished")

        except Exception as e:
            raise(e)
    