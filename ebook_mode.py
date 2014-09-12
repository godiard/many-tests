import os
import subprocess
import logging

def _is_tablet_mode():
    if not os.path.exists('/dev/input/event4'):
        return False
    try:
        output = subprocess.call(
            ['/bin/evtest', '--query', '/dev/input/event4', 'EV_SW',
             'SW_TABLET_MODE'])
    except subprocess.CalledProcessError:
        return False
    logging.error('output %s',output)
    if output == '10':
        return True
    return False


_is_tablet_mode()
