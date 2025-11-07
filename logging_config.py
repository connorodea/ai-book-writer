"""Logging configuration for the AI Book Generator"""
import logging
import os
from datetime import datetime
from typing import Optional

def setup_logging(
    log_level: str = "INFO",
    log_file: Optional[str] = None,
    enable_console: bool = True
) -> logging.Logger:
    """
    Set up logging for the AI Book Generator
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional file to log to (defaults to logs/book_generator.log)
        enable_console: Whether to also log to console
    
    Returns:
        Configured logger
    """
    
    # Create logs directory if it doesn't exist
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Set default log file with timestamp
    if log_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = os.path.join(log_dir, f"book_generator_{timestamp}.log")
    
    # Create logger
    logger = logging.getLogger("AI_Book_Generator")
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # File handler
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(getattr(logging, log_level.upper()))
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    # Console handler
    if enable_console:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(getattr(logging, log_level.upper()))
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    logger.info(f"Logging configured - Level: {log_level}, File: {log_file}")
    return logger

def get_logger(name: Optional[str] = None) -> logging.Logger:
    """Get a logger instance"""
    if name:
        return logging.getLogger(f"AI_Book_Generator.{name}")
    else:
        return logging.getLogger("AI_Book_Generator")