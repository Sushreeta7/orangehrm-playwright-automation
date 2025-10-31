#!/usr/bin/env python3
import psutil
import time
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    filename='system_health.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Define thresholds
THRESHOLDS = {
    'cpu_percent': 80.0,
    'memory_percent': 80.0,
    'disk_percent': 85.0
}

def check_cpu():
    """Monitor CPU usage"""
    cpu_percent = psutil.cpu_percent(interval=1)
    if cpu_percent > THRESHOLDS['cpu_percent']:
        logging.warning(f'High CPU Usage: {cpu_percent}%')
    return cpu_percent

def check_memory():
    """Monitor memory usage"""
    memory = psutil.virtual_memory()
    if memory.percent > THRESHOLDS['memory_percent']:
        logging.warning(f'High Memory Usage: {memory.percent}%')
    return memory.percent

def check_disk():
    """Monitor disk usage"""
    disk = psutil.disk_usage('/')
    if disk.percent > THRESHOLDS['disk_percent']:
        logging.warning(f'High Disk Usage: {disk.percent}%')
    return disk.percent

def check_processes():
    """Monitor running processes"""
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            process_info = proc.info
            if process_info['cpu_percent'] > 50 or process_info['memory_percent'] > 50:
                processes.append(process_info)
                logging.warning(f'High Resource Usage Process: {process_info}')
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return processes

def main():
    """Main monitoring loop"""
    logging.info('System Health Monitoring Started')
    try:
        while True:
            # Collect system metrics
            metrics = {
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'cpu_usage': check_cpu(),
                'memory_usage': check_memory(),
                'disk_usage': check_disk(),
                'high_usage_processes': check_processes()
            }
            
            # Log overall system status
            logging.info(
                f"System Status - CPU: {metrics['cpu_usage']}%, "
                f"Memory: {metrics['memory_usage']}%, "
                f"Disk: {metrics['disk_usage']}%"
            )
            
            # Wait before next check
            time.sleep(60)  # Check every minute
            
    except KeyboardInterrupt:
        logging.info('Monitoring stopped by user')
    except Exception as e:
        logging.error(f'Monitoring error: {str(e)}')

if __name__ == "__main__":
    main()