from exceptionite.actions import Action


class MasoniteDebugAction(Action):
    name = "Share with Masonite Support"
    icon = "SupportIcon"
    id = "masonite-debug"
    component = "MasoniteSupport"

    def run(self, options={}):
        data = self.handler.get_last_exception_data()
        id = "123456"
        return (
            f"Error page has been shared at https://debug.masoniteproject.com/{id}/ !"
        )


class PostStackOverflowAction(Action):
    name = "Post on Stackoverflow"
    icon = "ChatAlt2Icon"
    id = "masonite-stackoverflow"
    component = "MasoniteSupport"

    def run(self, options={}):
        return f"Stack overflow !"


class CreateMasoniteIssueAction(Action):
    name = "Report issue on Masonite GitHub"
    icon = "ExclamationCircleIcon"
    id = "masonite-github-report"
    component = "GitHubSupport"

    def run(self, options={}):
        import pdb

        pdb.set_trace()
        return f"GitHub !"
