import os

from zappa.asynchronous import task

from .logger import log_exception


def async_function(function, **kwargs):
    if os.getenv("ENVIRONMENT", "prod") == "local":
        function(**kwargs)
    else:
        async_task(function, **kwargs)


@task
def async_task(function, **kwargs):
    try:
        function(**kwargs)
    except Exception as error:
        log_exception(error, dict(args=kwargs.items()))
        return True
