import os

import click
import traceback

import config

from .datadog_http_handler import DatadogSingletonHttpHandler


def get_logger():
    return DatadogSingletonHttpHandler(
        api_key=os.getenv("DATADOG_API_KEY", ""),
        raise_exception=False,
        service=os.getenv("DATADOG_SERVICE", ""),
        logger_name="main",
    ).logger


def log_info(message, metas=None):
    if config.LOGS_DISABLED:
        return True
    if config.DEBUG:
        click.echo(message)
    if metas is None:
        get_logger().info(message)
    else:
        get_logger().info(message, metas)


def log_exception(exception: Exception, metas=None):
    if config.LOGS_DISABLED:
        return True
    e_traceback = traceback.format_exception(
        exception.__class__, exception, exception.__traceback__
    )
    traceback_lines = []
    for line in [line.rstrip("\n") for line in e_traceback]:
        traceback_lines.extend(line.splitlines())
    _metas = metas
    _metas["traceback_lines"] = traceback_lines
    get_logger().error(exception.__class__.__name__, _metas)


def log_error(error, metas=None):
    if config.LOGS_DISABLED:
        return True
    _metas = metas
    if config.DEBUG:
        click.echo(error)
    if metas is None:
        get_logger().info(error)
    else:
        get_logger().error(error, metas)
