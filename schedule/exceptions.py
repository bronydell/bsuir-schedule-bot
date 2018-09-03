class NoSchedule(Exception):
    def __init__(self, message):

        # Call the base class constructor with the parameters it needs
        super(NoSchedule, self).__init__(message)