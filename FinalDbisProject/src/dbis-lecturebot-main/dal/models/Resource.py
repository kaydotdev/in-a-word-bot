class Resource:
    def __init__(self, url, description, user_login, creation_date, times_visited=1):
        self.URL = url
        self.Description = description
        self.TimesVisited = times_visited
        self.Creation_Date = creation_date

        self.User_Login = user_login
