""" A UserResourceController Module """

from masonite.controllers import Controller


class UserResourceController(Controller):
    """Class Docstring Description
    """

    def show(self):
        """Show a single resource listing
        ex. Model.find('id')
            Get().route("/show", UserResourceController)
        """

        return ''

    def index(self):
        """Show several resource listings
        ex. Model.all()
            Get().route("/index", UserResourceController)
        """

        return ''

    def create(self):
        """Show form to create new resource listings
         ex. Get().route("/create", UserResourceController)
        """

        return ''

    def store(self):
        """Create a new resource listing
        ex. Post target to create new Model
            Post().route("/store", UserResourceController)
        """

        return ''

    def edit(self):
        """Show form to edit an existing resource listing
        ex. Get().route("/edit", UserResourceController)
        """

        return ''

    def update(self):
        """Edit an existing resource listing
        ex. Post target to update new Model
            Post().route("/update", UserResourceController)
        """

        return ''

    def destroy(self):
        """Delete an existing resource listing
        ex. Delete().route("/destroy", UserResourceController)
        """

        return ''