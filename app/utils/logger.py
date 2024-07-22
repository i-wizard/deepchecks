import logging


class CustomLogger:
    @classmethod
    def error(cls, message, extra):
        # Implement logging to third party like Rollbar or Sentry
        logging.error(message, extra=extra)
