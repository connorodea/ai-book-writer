"""Performance monitoring and optimization for AI Book Generator"""
import time
import psutil
import asyncio
from typing import Dict, Any, Optional
from contextlib import contextmanager
from logging_config import get_logger

logger = get_logger("performance")

class PerformanceMonitor:
    """Monitor system performance during book generation"""
    
    def __init__(self):
        self.metrics = {
            'start_time': None,
            'end_time': None,
            'chapters_generated': 0,
            'memory_usage': [],
            'cpu_usage': [],
            'generation_times': [],
            'errors': []
        }
        
    def start_monitoring(self):
        """Start performance monitoring"""
        self.metrics['start_time'] = time.time()
        logger.info("Performance monitoring started")
        
    def stop_monitoring(self):
        """Stop performance monitoring and log summary"""
        self.metrics['end_time'] = time.time()
        duration = self.metrics['end_time'] - self.metrics['start_time']
        
        logger.info(f"Performance monitoring stopped. Total duration: {duration:.2f}s")
        logger.info(f"Chapters generated: {self.metrics['chapters_generated']}")
        logger.info(f"Average chapter time: {self.get_average_chapter_time():.2f}s")
        logger.info(f"Peak memory usage: {max(self.metrics['memory_usage']) if self.metrics['memory_usage'] else 0:.1f}MB")
        logger.info(f"Average CPU usage: {sum(self.metrics['cpu_usage'])/len(self.metrics['cpu_usage']) if self.metrics['cpu_usage'] else 0:.1f}%")
        
    @contextmanager
    def monitor_chapter_generation(self, chapter_number: int):
        """Context manager to monitor individual chapter generation"""
        start_time = time.time()
        start_memory = psutil.virtual_memory().used / 1024 / 1024  # MB
        
        logger.info(f"Starting Chapter {chapter_number} generation")
        
        try:
            yield
            
            # Success
            end_time = time.time()
            chapter_time = end_time - start_time
            end_memory = psutil.virtual_memory().used / 1024 / 1024  # MB
            
            self.metrics['chapters_generated'] += 1
            self.metrics['generation_times'].append(chapter_time)
            self.metrics['memory_usage'].append(end_memory)
            self.metrics['cpu_usage'].append(psutil.cpu_percent())
            
            logger.info(f"Chapter {chapter_number} completed in {chapter_time:.2f}s")
            logger.info(f"Memory usage: {end_memory:.1f}MB (Δ{end_memory - start_memory:+.1f}MB)")
            
        except Exception as e:
            # Error occurred
            error_info = {
                'chapter': chapter_number,
                'time': time.time(),
                'error': str(e)
            }
            self.metrics['errors'].append(error_info)
            logger.error(f"Chapter {chapter_number} generation failed: {str(e)}")
            raise
            
    def get_average_chapter_time(self) -> float:
        """Get average time per chapter"""
        if not self.metrics['generation_times']:
            return 0.0
        return sum(self.metrics['generation_times']) / len(self.metrics['generation_times'])
        
    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get comprehensive metrics summary"""
        duration = 0
        if self.metrics['start_time'] and self.metrics['end_time']:
            duration = self.metrics['end_time'] - self.metrics['start_time']
            
        return {
            'total_duration': duration,
            'chapters_completed': self.metrics['chapters_generated'],
            'average_chapter_time': self.get_average_chapter_time(),
            'peak_memory_mb': max(self.metrics['memory_usage']) if self.metrics['memory_usage'] else 0,
            'average_cpu_percent': sum(self.metrics['cpu_usage'])/len(self.metrics['cpu_usage']) if self.metrics['cpu_usage'] else 0,
            'total_errors': len(self.metrics['errors']),
            'error_rate': len(self.metrics['errors']) / max(1, self.metrics['chapters_generated'])
        }

# Global performance monitor instance
performance_monitor = PerformanceMonitor()

class ResourceOptimizer:
    """Optimize resource usage during generation"""
    
    @staticmethod
    def check_system_resources() -> Dict[str, Any]:
        """Check current system resources"""
        memory = psutil.virtual_memory()
        cpu_percent = psutil.cpu_percent(interval=1)
        
        return {
            'memory_available_gb': memory.available / 1024 / 1024 / 1024,
            'memory_percent_used': memory.percent,
            'cpu_percent': cpu_percent,
            'disk_usage_percent': psutil.disk_usage('/').percent
        }
    
    @staticmethod
    def should_proceed_with_generation() -> bool:
        """Check if system has enough resources to proceed"""
        resources = ResourceOptimizer.check_system_resources()
        
        # Check if we have at least 1GB available memory and CPU usage is reasonable
        if resources['memory_available_gb'] < 1.0:
            logger.warning(f"Low memory warning: {resources['memory_available_gb']:.1f}GB available")
            return False
            
        if resources['cpu_percent'] > 90:
            logger.warning(f"High CPU usage: {resources['cpu_percent']:.1f}%")
            return False
            
        if resources['memory_percent_used'] > 90:
            logger.warning(f"High memory usage: {resources['memory_percent_used']:.1f}%")
            return False
            
        return True
    
    @staticmethod
    async def throttle_if_needed(delay: float = 1.0):
        """Add delay if system resources are strained"""
        resources = ResourceOptimizer.check_system_resources()
        
        if resources['memory_percent_used'] > 80 or resources['cpu_percent'] > 80:
            logger.info(f"Throttling generation due to high resource usage")
            await asyncio.sleep(delay)
            
    @staticmethod
    def cleanup_resources():
        """Cleanup any unnecessary resources"""
        import gc
        gc.collect()
        logger.debug("Resource cleanup completed")