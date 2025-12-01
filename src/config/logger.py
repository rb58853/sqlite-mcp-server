import os
import sys
import logging  # For logging and debugging messages

ROOT_PATH = os.getcwd()
RELATIVE_PATH = "log/sqlite_mcp_server.log"
FILE_LOG_PATH = os.path.join(ROOT_PATH, RELATIVE_PATH)
os.makedirs(os.path.dirname(FILE_LOG_PATH), exist_ok=True)

logging.basicConfig(
    level=logging.DEBUG,  # Setting the logging level to DEBUG for detailed output.
    format="[%(asctime)s] %(levelname)s - %(name)s - %(message)s",  # Log format includes time, level, name and message.
    datefmt="%Y-%m-%d %H:%M:%S",  # Date format for the logs.
    handlers=[
        logging.StreamHandler(sys.stdout),  # Log to stdout
        logging.FileHandler(RELATIVE_PATH),  # Also log to a file
    ],
)
logger = logging.getLogger("sqlite_mcp_server")

logger.debug("Logging is configured.")
