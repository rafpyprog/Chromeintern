import re
from subprocess import PIPE, Popen

from .chromedriver import ChromeDriver


class GoogleChrome():
    def __init__(self, executable_path='google-chrome'):
        self.executable_path = executable_path

    def parse_chrome_version(self, string):
        GOOGLE_CHROME_VERSION_PATTERN = '[0-9]{2}'
        version = int(re.search(GOOGLE_CHROME_VERSION_PATTERN, string).group())
        return version

    @property
    def version(self):
        cmd = [self.executable_path, '--version']
        proc = Popen(cmd, stdout=PIPE, encoding='utf-8')
        out, err = proc.communicate()
        if err is not None:
            raise SystemError(err)
        return self.parse_chrome_version(out)

    @property
    def compatible_chromedriver_version(self):
        driver = ChromeDriver()
        return driver.find_compatible_chromedriver_version(self.version)
