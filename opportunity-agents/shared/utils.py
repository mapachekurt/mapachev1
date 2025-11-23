"""Shared utility functions."""
import os
import json
from typing import Dict, Any, List
from datetime import datetime
import re


def load_env_file(filepath: str = ".env") -> Dict[str, str]:
    """
    Load environment variables from .env file.

    Args:
        filepath: Path to .env file

    Returns:
        Dictionary of environment variables
    """
    env_vars = {}

    if not os.path.exists(filepath):
        return env_vars

    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()

            # Skip comments and empty lines
            if not line or line.startswith('#'):
                continue

            # Parse KEY=VALUE
            if '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()

                # Remove quotes if present
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                elif value.startswith("'") and value.endswith("'"):
                    value = value[1:-1]

                env_vars[key] = value

    return env_vars


def format_currency(amount: float) -> str:
    """
    Format number as currency.

    Args:
        amount: Amount to format

    Returns:
        Formatted currency string
    """
    if amount >= 1_000_000_000:
        return f"${amount/1_000_000_000:.2f}B"
    elif amount >= 1_000_000:
        return f"${amount/1_000_000:.2f}M"
    elif amount >= 1_000:
        return f"${amount/1_000:.2f}K"
    else:
        return f"${amount:.2f}"


def format_percentage(value: float) -> str:
    """
    Format decimal as percentage.

    Args:
        value: Decimal value (e.g., 0.15 for 15%)

    Returns:
        Formatted percentage string
    """
    return f"{value * 100:.1f}%"


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename by removing invalid characters.

    Args:
        filename: Original filename

    Returns:
        Sanitized filename
    """
    # Remove invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)

    # Replace spaces with underscores
    filename = filename.replace(' ', '_')

    # Limit length
    if len(filename) > 255:
        filename = filename[:255]

    return filename


def save_json(data: Any, filepath: str, indent: int = 2):
    """
    Save data to JSON file.

    Args:
        data: Data to save
        filepath: Path to save file
        indent: JSON indentation
    """
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=indent, default=str)


def load_json(filepath: str) -> Any:
    """
    Load data from JSON file.

    Args:
        filepath: Path to JSON file

    Returns:
        Loaded data
    """
    with open(filepath, 'r') as f:
        return json.load(f)


def calculate_score(
    metrics: Dict[str, float],
    weights: Dict[str, float]
) -> float:
    """
    Calculate weighted score from metrics.

    Args:
        metrics: Dictionary of metric values
        weights: Dictionary of weights (must sum to 1.0)

    Returns:
        Weighted score
    """
    if abs(sum(weights.values()) - 1.0) > 0.01:
        raise ValueError("Weights must sum to 1.0")

    score = 0.0
    for metric, value in metrics.items():
        if metric in weights:
            score += value * weights[metric]

    return score


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Truncate text to maximum length.

    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated

    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text

    return text[:max_length - len(suffix)] + suffix


def extract_domain(url: str) -> str:
    """
    Extract domain from URL.

    Args:
        url: Full URL

    Returns:
        Domain name
    """
    # Remove protocol
    domain = re.sub(r'https?://', '', url)

    # Remove path
    domain = domain.split('/')[0]

    # Remove www
    domain = re.sub(r'^www\.', '', domain)

    return domain


def batch_list(items: List, batch_size: int) -> List[List]:
    """
    Split list into batches.

    Args:
        items: List to batch
        batch_size: Size of each batch

    Returns:
        List of batches
    """
    batches = []
    for i in range(0, len(items), batch_size):
        batches.append(items[i:i + batch_size])

    return batches


def merge_dicts(*dicts: Dict) -> Dict:
    """
    Merge multiple dictionaries.

    Args:
        *dicts: Dictionaries to merge

    Returns:
        Merged dictionary
    """
    result = {}
    for d in dicts:
        result.update(d)

    return result


def get_timestamp() -> str:
    """
    Get current timestamp in ISO format.

    Returns:
        ISO timestamp string
    """
    return datetime.now().isoformat()


def days_ago_to_date(days: int) -> datetime:
    """
    Convert days ago to datetime.

    Args:
        days: Number of days ago

    Returns:
        Datetime object
    """
    from datetime import timedelta
    return datetime.now() - timedelta(days=days)


class ColoredOutput:
    """Helper for colored terminal output."""

    COLORS = {
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'magenta': '\033[95m',
        'cyan': '\033[96m',
        'white': '\033[97m',
        'reset': '\033[0m',
        'bold': '\033[1m'
    }

    @classmethod
    def print(cls, text: str, color: str = 'white', bold: bool = False):
        """
        Print colored text.

        Args:
            text: Text to print
            color: Color name
            bold: Whether to make text bold
        """
        color_code = cls.COLORS.get(color, cls.COLORS['white'])
        bold_code = cls.COLORS['bold'] if bold else ''
        reset_code = cls.COLORS['reset']

        print(f"{bold_code}{color_code}{text}{reset_code}")

    @classmethod
    def success(cls, text: str):
        """Print success message."""
        cls.print(f"✓ {text}", 'green')

    @classmethod
    def error(cls, text: str):
        """Print error message."""
        cls.print(f"✗ {text}", 'red')

    @classmethod
    def warning(cls, text: str):
        """Print warning message."""
        cls.print(f"⚠ {text}", 'yellow')

    @classmethod
    def info(cls, text: str):
        """Print info message."""
        cls.print(f"ℹ {text}", 'blue')
