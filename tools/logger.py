"""Logger configuration for the application."""
import structlog
from rich.console import Console
import logging

console = Console()

def configure_logger():
    """Configure structlog with rich console output.
    
    Args:
        min_level: Minimum log level (default: structlog default level)
    """
    structlog.configure(
        processors=[
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.dev.ConsoleRenderer(
                colors=True,
                exception_formatter=structlog.dev.plain_traceback,
            ),
        ],
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        cache_logger_on_first_use=True,
    )
    
    return structlog.get_logger()

logger = configure_logger()
