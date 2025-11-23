"""Cloud Function entry point for Chief Agent daily briefing."""

import logging

import functions_framework
from flask import Request

from .agent import chief_agent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@functions_framework.http
def trigger_daily_briefing(request: Request) -> tuple[dict, int]:
    """HTTP Cloud Function to trigger daily briefing.

    Args:
        request: Flask request object

    Returns:
        Response tuple (data, status_code)
    """
    try:
        logger.info("Triggered daily intelligence briefing")

        # Run the briefing
        result = chief_agent.run_daily_briefing()

        logger.info(f"Daily briefing result: {result}")

        if result["status"] == "success":
            return result, 200
        else:
            return result, 500

    except Exception as e:
        logger.error(f"Error in trigger_daily_briefing: {e}", exc_info=True)
        return {"status": "error", "error": str(e)}, 500
