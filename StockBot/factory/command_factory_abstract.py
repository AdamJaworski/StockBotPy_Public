class CommandFactory:
    """
    Abstract class that holds base commands
    """
    API_NAME: str
    """Name of API used by this class"""

    def login(self, user_id: str, password: str):
        raise NotImplementedError

    def logout(self):
        print("Logging off.")
        raise NotImplementedError

    def get_chart_data(self, chart: str, start_date: int, end_date: int, period: int):
        raise NotImplementedError
