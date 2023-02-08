from git import Repo
from github import Github
import shutil
import os
class GithubHelper:
    def __init__(self, repo_name, username, password, org="amagimedia") -> None:
        self.username = username
        self.password = password
        self.repo_name = repo_name
        self.org = org

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

    def create_pr(self, title: str, head: str, base: str = "main", body: str = None) -> Github.PullRequest:
        gh_api = Github(self.password)
        repo_name = self.org + '/' + self.repo_name
        repo = gh_api.get_repo(repo_name)
        pr = repo.create_pull(title=title, body=body, head=head, base=base)
        
        return pr

    def merge_pr(self, pr_object: Github.PullRequest, commit_message: str, commit_title: str) -> bool:
        merge_status = pr_object.merge(commit_message=commit_message, commit_title=commit_title)
        return merge_status.merged
        

    def merge_pr_by_num(self, pr_num: int, commit_message: str, commit_title: str) -> bool:
        gh_api = Github(self.password)
        repo_name = self.org + '/' + self.repo_name
        repo = gh_api.get_repo(repo_name)
        pr = repo.get_pull(pr_num)

        return self.merge_pr(pr, commit_message=commit_message, commit_title=commit_title)



    def commit_push_delete(self, commit_msg: str, branch_name: str):
        self.commit_push(commit_msg, branch_name)
        try:
            shutil.rmtree(os.path.join(os.getcwd(), self.repo_name))

            ## Implement logger
            print("delete finished")

        except Exception as e:
            raise(e)
    