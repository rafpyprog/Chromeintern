class ChromeGuardException(Exception):
    '''
    Base ChromeGuard exception.
    '''

    def __init__(self, msg=None):
        self.msg = msg

    def __str__(self):
        exception_msg = 'Message: {}\n'.format(self.msg)
        return exception_msg


class NotUpdatedException(ChromeGuardException):
    '''
    Thrown when Chromedriver is not up-to-date.
    '''
    def __init__(self, local_version, latest_version):
        msg = 'Chromedriver version is {}. Latest version is {}\n.'
        self.msg = msg.format(local_version, latest_version)
