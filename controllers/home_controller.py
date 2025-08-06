from flask import render_template

class Home:
    """
    Handles rendering of the home or welcome page based on user presence.

    Dependencies:
        - get_name: Object with method load_name() that returns a dict with user info.
    """

    def __init__(self, get_name):
        """
        Initializes the Home handler.

        Args:
            get_name: Object responsible for loading user name data.
        """
        self.get_name = get_name

    def get_home(self):
        """
        Determines which template to render based on whether a user name is stored.

        Returns:
            Response: Renders 'home.html' if user name exists,
                      otherwise renders 'welcome.html'.
        """
        user = self.get_name.load_name()
        name = user.get('name')
        if name:
            return render_template("home.html")
        else:
            return render_template("welcome.html")