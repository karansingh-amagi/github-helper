from git import Repo
from github import Github
from github import PullRequest
import shutil
import os

class GithubHelper:
    def __init__(self, repo_name: str, username: str, password: str, repo_path: str=None, org: str="amagimedia") -> None:
        self.username = username
        self.password = password
        self.repo_name = repo_name
        self.repo_path = repo_path
        self.org = org

        self.remote = "https://{}:{}@github.com/{}/{}.git".format(username, password, org, repo_name)

    def clone(self):
        try:
            if self.repo_path != None:
                shutil.rmtree(self.repo_path)
                Repo.clone_from(self.remote, self.repo_path)
            else:
                Repo.clone_from(self.remote, self.repo_name)
                self.repo_path = str(os.path.join(os.getcwd(), self.repo_name))
            ## Implement logger
            print('clone finished')

        except Exception as e:
            raise(e)

    def clone_and_copy(self, copy_dir):
        self.clone()
        try: 
            shutil.copytree(copy_dir, self.repo_path, dirs_exist_ok=True, ignore=shutil.ignore_patterns('.*', '_*'))
        except Exception as e:
            raise(e)
        
    def commit_push(self, commit_msg: str, branch_name: str):
        try: 
            if self.repo_path != None:
                repo = Repo(self.repo_path)
            else: 
                self.clone()
                repo = Repo(self.repo_path)

            repo.git.checkout('-B', branch_name)
            repo.git.add(".")
            repo.git.commit(m=commit_msg)
            repo.git.push('--set-upstream', repo.remote().name, branch_name)

            ## Implement logger
            print("commit finished")

        except Exception as e:
            raise e

    def create_pr(self, title: str, body: str, head: str, base: str = "main") -> PullRequest:
        try:
            print("Creating a Pull Request...")
            gh_api = Github(self.password)
            repo_name = self.org + '/' + self.repo_name
            print(repo_name)
            repo = gh_api.get_repo(repo_name)
            print(repo)
            pr = repo.create_pull(title=title, body=body, head=head, base=base)
            
            return pr

        except Exception as e:
            raise e

    def merge_pr(self, pr_object: PullRequest, commit_title: str, commit_message: str) -> bool:
        try:
            print("Creating a Merge Request...")
            merge_status = pr_object.merge(commit_message=commit_message, commit_title=commit_title)
            return merge_status.merged
        except Exception as e:
            raise e

    def merge_pr_by_num(self, pr_num: int, commit_message: str, commit_title: str) -> bool:
        try:
            gh_api = Github(self.password)
            repo_name = self.org + '/' + self.repo_name
            repo = gh_api.get_repo(repo_name)
            pr = repo.get_pull(pr_num)
        except Exception as e: 
            raise e

        return self.merge_pr(pr, commit_message=commit_message, commit_title=commit_title)

    def commit_push_delete(self, commit_msg: str, branch_name: str):
        self.commit_push(commit_msg, branch_name)
        try:
            shutil.rmtree(os.path.join(os.getcwd(), self.repo_name))

            ## Implement logger
            print("delete finished")

        except Exception as e:
            raise(e)
    
gh = GithubHelper("github-helper", 'karansingh-amagi', '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', '.', "karansingh-amagi")
gh.commit_push("Testing my code", "test-branch1")
pr = gh.create_pr("Testing my code", "", "test-branch1", "main")
status = gh.merge_pr(pr, "Testing my code mr", "test message")

print(status)