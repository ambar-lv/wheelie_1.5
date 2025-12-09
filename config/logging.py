def get_logging_config(is_debug: bool) -> dict:
    level = "DEBUG" if is_debug else "INFO"

    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "colored": {
                "()": "colorlog.ColoredFormatter",
                "format": "%(log_color)s%(levelname)-8s%(reset)s %(blue)s%(asctime)s%(reset)s %(message)s",
                "datefmt": "%m.%d.%y %H:%M:%S",
                "log_colors": {
                    "DEBUG": "cyan",
                    "INFO": "green",
                    "WARNING": "yellow",
                    "ERROR": "red",
                    "CRITICAL": "red,bg_white",
                },
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "colored",
                "level": level,
            },
        },
        "loggers": {
            "django": {
                "handlers": ["console"],
                "level": "INFO" if is_debug else "WARNING",
                "propagate": False,
            },
        },
        "root": {
            "handlers": ["console"],
            "level": level,
        },
    }
