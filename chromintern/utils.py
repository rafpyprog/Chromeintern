import re
from subprocess import Popen, PIPE


def parse_chromedriver_version(cmd_stdout):
    '''
        cmd_stdout (string): Output from chromedriver -v
    '''
    CHROMEDRIVER_VERSION_PATTERN = '\d+\.\d+'
    version = re.search(CHROMEDRIVER_VERSION_PATTERN, cmd_stdout)
    if version:
        return version.group()
    else:
        raise Exception('Unable to parse Chromedriver version {}'
                        .format(cmd_stdout))


def powershell_rest_request(URL):
    cmd = 'powershell -Command Invoke-RestMethod -Uri {}'.format(URL)
    proc = Popen(cmd, stdout=PIPE)
    stdout, stderr = proc.communicate()
    content = stdout.decode()
    return content


def powershell_get_latest_release():
    API_URL = 'https://chromedriver.storage.googleapis.com/LATEST_RELEASE'
    release = powershell_rest_request(API_URL).strip().replace(',', '.')
    return release
