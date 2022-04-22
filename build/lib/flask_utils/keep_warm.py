import os
import time
from flask_utils import log_info
from zappa.asynchronous import task


@task
def keep_warm_task(lambda_count):
    log_info(f"Lambda keep warm {lambda_count}")
    if lambda_count < os.getenv("KEEP_WARM_LAMBDAS", ""):
        keep_warm_task(lambda_count + 1)
        time.sleep(3)
