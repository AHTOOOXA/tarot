import logging

import betterlogging as bl


def setup_logging():
    log_format = (
        "\033[1;36m%(filename)s:%(lineno)d\033[0m "
        "#%(levelname)-8s "
        "\033[1;32m[%(asctime)s]\033[0m "
        "- \033[1;34m%(name)s\033[0m "
        "- %(message)s"
    )
    logging.basicConfig(level=logging.INFO, format=log_format, force=True)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
