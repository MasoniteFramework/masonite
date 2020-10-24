import pdb
from cleo import Command
import os
import shutil
import zipfile
import requests

from ..exceptions import ProjectLimitReached, ProjectProviderTimeout, ProjectProviderHttpError


class NewCommand(Command):
    """
    Creates a new Masonite project

    new
        {name? : Name of your Masonite project}
        {target? : Path of you Masonite project}
        {--b|--branch=False : Specify which branch from the Masonite repo you would like to install}
        {--r|--release=False : Specify which version of Masonite you would like to install}
        {--rp|--repo=MasoniteFramework/cookie-cutter : Specify from which repository you want to craft your project}
        {--p|--provider=github : Specify from which repository you want to craft your project [github, gitlab] }
    """

    providers = ["github", "gitlab"]
    # timeout in seconds for requests made to providers
    TIMEOUT = 20

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.api_base_url = None

    def handle(self):
        name = self.argument("name")
        if not name:
            name = "project"

        target = self.argument("target")

        if not target:
            target = "."

        branch = self.option("branch")
        version = self.option("release")
        repo = self.option("repo")
        provider = self.option("provider")
        if os.path.isdir(os.path.join(os.getcwd(), name)):
            self.comment(
                "Directory {0} already exists. Please choose another project name".format(
                    name
                )
            )
            exit(-1)

        from io import BytesIO

        for directory in os.listdir(os.getcwd()):
            if directory.startswith("masonite-"):
                return self.comment(
                    'There is a folder that starts with "masonite-" and therefore craft cannot create a new project'
                )
        try:
            if repo and provider not in self.providers:
                return self.error("'provider' option must be in {}".format(",".join(self.providers)))

            self.set_api_provider_url_for_repo(provider, repo)

            if branch != "False":
                branch_data = self.get_branch_provider_data(provider, branch)
                if "name" not in branch_data:
                    return self.error("Branch {0} does not exist.".format(branch))

                zipball = self.get_branch_archive_url(provider, repo, branch)
            elif version != "False":
                releases_data = self.get_releases_provider_data(provider)
                zipball = False

                for release in releases_data:
                    if "tag_name" in release and release["tag_name"].startswith(
                        "v{0}".format(version)
                    ):
                        self.info(
                            "Installing version {0}".format(release["tag_name"])
                        )
                        self.line("")
                        zipball = self.get_release_archive_url_from_release_data(provider, release)
                        break

                if zipball is False:
                    return self.error(
                        "Version {0} could not be found".format(version)
                    )
            else:
                tags_data = self.get_releases_provider_data(provider)

                # try to find all releases which are not prereleases
                tags = []
                for release in tags_data:
                    if release["prerelease"] is False:
                        tag_key = "tag_name" if provider == "github" else "name"
                        tags.append(release[tag_key].replace("v", ""))

                tags = sorted(
                    tags, key=lambda v: [int(i) for i in v.split(".")], reverse=True
                )
                # get url from latest tagged version
                if not tags:
                    self.warning("No tags has been found, using latest commit on master.")
                    zipball = self.get_branch_archive_url(provider, repo, "master")
                else:
                    zipball = self.get_tag_archive_url(provider, repo, tags[0])
        except ProjectLimitReached:
            raise ProjectLimitReached(
                "You have reached your hourly limit of creating new projects with {0}. Try again in 1 hour.".format(provider)
            )
        except requests.Timeout:
            raise ProjectProviderTimeout(
                "{0} provider seems not reachable, request timed out after {1} seconds".format(provider, self.TIMEOUT)
            )
        except Exception as e:
            self.error("The following error happened when crafting your project. Verify options are correct else open an issue at https://github.com/MasoniteFramework/masonite.")
            raise e
        success = False

        zipurl = zipball

        self.info("Crafting Application ...")

        try:
            # Python 3
            from urllib.request import urlopen

            with urlopen(zipurl) as zipresp:
                with zipfile.ZipFile(BytesIO(zipresp.read())) as zfile:
                    zfile.extractall(os.getcwd())

            success = True
        except ImportError:
            # Python 2
            import urllib

            r = urllib.urlopen(zipurl)
            with zipfile.ZipFile(BytesIO(r.read())) as z:
                z.extractall(os.getcwd())

            success = True
        except Exception as e:
            self.error("An error occured when downloading {0}".format(zipurl))
            raise e

        if success:
            for directory in os.listdir(os.getcwd()):
                if directory.startswith(
                    "MasoniteFramework-cookie-cutter"
                ) or directory.startswith("cookie-cutter-"):
                    if target == ".":
                        from_dir = os.path.join(
                            os.getcwd(), "{0}".format(directory)
                        )
                        to_dir = os.path.abspath(os.path.expanduser(target))

                        for file in os.listdir(from_dir):
                            shutil.move(os.path.join(from_dir, file), to_dir)
                        os.rmdir(from_dir)
                    else:
                        os.rename(
                            os.path.join(os.getcwd(), "{0}".format(directory)),
                            os.path.join(os.getcwd(), target),
                        )

                    self.info("Application Created Successfully!")
                    self.info("Installing Dependencies ")
                    if target == ".":
                        self.call("install")

                        self.info(
                            "Installed Successfully. Just Run `craft serve` To Start Your Application."
                        )
                    else:
                        self.info(
                            "Project Created Successfully. You now will have to CD into your new '{}' directory and run `craft install` to complete the installation".format(
                                target
                            )
                        )

                    return

        else:
            self.comment("Could Not Create Application :(")

    def set_api_provider_url_for_repo(self, provider, repo):
        if provider == "github":
            self.api_base_url =  "https://api.github.com/repos/{0}".format(repo)
        elif provider == "gitlab":
            import urllib.parse
            repo_encoded_url =urllib.parse.quote(repo, safe="")
            self.api_base_url = "https://gitlab.com/api/v4/projects/{0}".format(repo_encoded_url)

    def get_branch_provider_data(self, provider, branch):
        if provider == "github":
            branch_data = self._get(
                "{0}/branches/{1}".format(
                    self.api_base_url, branch
                )
            )
        elif provider == "gitlab":
            branch_data = self._get(
                "{0}/repository/branches/{1}".format(
                    self.api_base_url, branch
                )
            )
        return branch_data.json()

    def get_branch_archive_url(self, provider, repo, branch):
        if provider == "github":
            return "https://github.com/{0}/archive/{1}.zip".format(repo, branch)
        elif provider == "gitlab":
            # here we can provide commit, branch name or tag
            return "{0}/repository/archive.zip?sha={1}.zip".format(self.api_base_url, branch)

    def get_tag_archive_url(self, provider, repo, version):
        if provider == "github":
            tag_data = self._get(
                "{0}/releases/tags/v{1}".format(
                    self.api_base_url, version
                )
            )
            return tag_data.json()["zipball_url"]
        elif provider == "gitlab":
            return self.get_branch_archive_url("gitlab", repo, "v" + version)

    def get_releases_provider_data(self, provider):
        if provider == "github":
            releases_data = self._get(
                "{0}/releases".format(self.api_base_url)
            )
        elif provider == "gitlab":
            releases_data = self._get(
                "{0}/releases".format(self.api_base_url)
            )
        return releases_data.json()

    def get_release_archive_url_from_release_data(self, provider, release):
        if provider == "github":
            return release["zipball_url"]
        elif provider == "gitlab":
            return [x for x in release["assets"]["sources"] if x["format"] == "zip" ][0]["url"]
            # could also do
            # return "{0}/repository/archive.zip?sha={1}.zip".format(self.api_base_url, branch)

    def get_tags_provider_data(self, provider):
        if provider == "github":
            releases_data = self._get(
                "{0}/releases".format(self.api_base_url)
            )
        elif provider == "gitlab":
            releases_data = self._get(
                "{0}/repository/tags".format(self.api_base_url)
            )
        return releases_data.json()

    def _get(self, request):
        print(f"debug: {request}")
        data = requests.get(request, timeout=self.TIMEOUT)
        print(f"done: {data.status_code}")
        if data.status_code != 200:
            if data.reason == "rate limit exceeded":
                raise ProjectLimitReached()
            else:
                raise ProjectProviderHttpError("{0}({1}) at {2}".format(
                    data.reason, data.status_code, data.url
                ))
        return data
