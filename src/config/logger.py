import logging  # For logging and debugging messages
import sys

logging.basicConfig(
    level=logging.DEBUG,  # Setting the logging level to DEBUG for detailed output.
    format="[%(asctime)s] %(levelname)s - %(name)s - %(message)s",  # Log format includes time, level, name and message.
    datefmt="%Y-%m-%d %H:%M:%S",  # Date format for the logs.
    handlers=[
        logging.StreamHandler(sys.stdout),  # Log to stdout
        logging.FileHandler("log/sqlite_mcp_server.log"),  # Also log to a file
    ],
)
logger = logging.getLogger("sqlite_mcp_server")
logger.debug("Logging is configured.")
