from instapy import InstaPy
import random
import yaml

## TODO: Setup check
## TODO: Install selenium
## TODO: Install selenium firefox driver
## TODO: Install selenium firefox on local machine

### Initialize
## Load config

def init():
    # Read config.yaml
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    # Read secrets.yaml
    with open('secrets.yaml', 'r') as f:
        secrets = yaml.safe_load(f)
    config['u'] = secrets['a']
    config['p'] = secrets['z']
    
    return config

def r_sleep(use_default=True):
    """
    Generate a random sleep interval in seconds.

    Parameters:
    - use_default (bool): If True, use the range 3 to 40 seconds. If False, use the range 3 to 5 seconds.

    Returns:
    int: Random sleep interval in seconds.
    """
    if use_default:
        return random.randint(2, 40)
    else:
        return random.randint(2, 4)
    
# if __name__ == "main":
session = InstaPy(username="<your_username>", password="<your_password>")
session.login()
session.like_by_tags(["bmw", "mercedes"], amount=5)
session.set_dont_like(["naked", "nsfw"])
session.set_do_follow(True, percentage=50)
session.set_do_comment(True, percentage=50)
session.set_comments(["Nice!", "Sweet!", "Beautiful :heart_eyes:"])
session.end()