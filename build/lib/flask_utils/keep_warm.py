import os

import time
from zappa.asynchronous import task

from flask_utils import log_info


@task
def keep_warm_task(lambda_count):
    log_info(f"Lambda keep warm {lambda_count}")
    max_lambda_count = os.getenv("KEEP_WARM_LAMBDAS", 1)
    if lambda_count < max_lambda_count:
        keep_warm_task(lambda_count + 1)
        if lambda_count + 1 < max_lambda_count:
            time.sleep(3)
