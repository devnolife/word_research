"""
Logging configuration for Word Research Analyzer
"""
import logging
import logging.handlers
from pathlib import Path
from typing import Optional
import os

def setup_logging(
    log_level: str = "INFO",
    log_file: Optional[str] = None,
    log_dir: Optional[str] = None,
    max_file_size_mb: int = 10,
    backup_count: int = 5,
    console_logging: bool = True
) -> logging.Logger:
    """
    Set up comprehensive logging configuration
    
    Args:
        log_level: Logging level ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')
        log_file: Log file name (defaults to 'document_processing.log')
        log_dir: Log directory (defaults to 'logs' in project root)
        max_file_size_mb: Maximum log file size in MB before rotation
        backup_count: Number of backup log files to keep
        console_logging: Whether to enable console logging
        
    Returns:
        logging.Logger: Configured logger instance
    """
    # Set log level
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)
    
    # Set up log directory
    if log_dir is None:
        log_dir = Path(__file__).parent.parent / "logs"
    else:
        log_dir = Path(log_dir)
    
    log_dir.mkdir(exist_ok=True)
    
    # Set up log file
    if log_file is None:
        log_file = "document_processing.log"
    
    log_file_path = log_dir / log_file
    
    # Create logger
    logger = logging.getLogger("word_research_analyzer")
    logger.setLevel(numeric_level)
    
    # Clear existing handlers to avoid duplicates
    logger.handlers.clear()
    
    # Create formatter
    formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # File handler with rotation
    file_handler = logging.handlers.RotatingFileHandler(
        log_file_path,
        maxBytes=max_file_size_mb * 1024 * 1024,
        backupCount=backup_count,
        encoding='utf-8'
    )
    file_handler.setLevel(numeric_level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Console handler
    if console_logging:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(numeric_level)
        
        # Simplified formatter for console
        console_formatter = logging.Formatter(
            fmt='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        )
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
    
    logger.info(f"Logging initialized - Level: {log_level}, File: {log_file_path}")
    
    return logger


def get_logger(name: str = None) -> logging.Logger:
    """
    Get a logger instance for a specific module
    
    Args:
        name: Logger name (defaults to calling module name)
        
    Returns:
        logging.Logger: Logger instance
    """
    if name is None:
        name = "word_research_analyzer"
    elif not name.startswith("word_research_analyzer"):
        name = f"word_research_analyzer.{name}"
    
    return logging.getLogger(name)


# Module-level logger for immediate use
logger = get_logger(__name__)
