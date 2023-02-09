from pathlib import Path
import os
import uuid
from ruamel.yaml import YAML
from gh_helper import GithubHelper

class TestInit:
    def __init__(self) -> None:
        gh = GithubHelper("argocd_deploy", "karansingh-amagi", "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")
        gh.clone()
        repo_path = os.path.join(os.getcwd(), "argocd_deploy")
        self.new_automation(repo_path, "aapvtss15/deployment/operator/aws-use1/iota-pss15/automationy155s-automation/automation/automationy155s-automation.yaml", "karansingh-amagi@gmail.com", "karansingh-amagi+support@gmail.com")

    def new_automation(self, deploy_repo_path:str, crd_template_path: str, admin_email: str, support_email: str):
        crd_template_path = Path(crd_template_path)
        crd_template_path = os.path.join(deploy_repo_path, crd_template_path)
        crd_template_name = os.path.basename(crd_template_path)
        crd_template_dir = os.path.dirname(crd_template_path)
        crd_automation_name = crd_template_name.split("-")[0]
        unique_automation_name = str(uuid.uuid4())
        new_automation_path = os.path.join(crd_template_dir, unique_automation_name + ".yaml")

        yaml_loader = YAML()
        yaml_loader.preserve_quotes = True

        with open(crd_template_path, "r") as fin:
            with open(new_automation_path, "w") as fout:
                for line in fin:
                    fout.write(line.replace(crd_automation_name, unique_automation_name))

        with open(new_automation_path, 'r') as buf:
            try:
                loaded = yaml_loader.load(buf)
            except Exception as e:
                raise e
        current_admin_email = loaded['spec']['customer']['adminEmail'] 
        current_support_email = loaded['spec']['customer']['supportEmail']
        loaded['spec']['customer']['adminEmail'] = admin_email
        loaded['spec']['customer']['supportEmail'] = support_email

        ### Use for extracting information about the automation nodes and services
        cp_automation_config = yaml_loader.load(loaded['spec']['cp-automation'])

        cp_automation_string = loaded['spec']['cp-automation']
        loaded['spec']['cp-automation'] = cp_automation_string.replace(current_admin_email, admin_email).replace(current_support_email, support_email)

        with open(new_automation_path, 'w') as stream:
            try:
                yaml_loader.dump(loaded, stream)
            except Exception as e:
                raise e

        return cp_automation_config

    
new_test = TestInit()
# new_automation("/Users/wolf/Karan/work/blip_test/argocd_deploy", "aapvtss15/deployment/operator/aws-use1/iota-pss15/automationy155s-automation/automation/automationy155s-automation.yaml", admin_email="karansingh-amagi@gmail.com", support_email='karansingh-amagi+support@gmail.com')
