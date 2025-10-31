# System Administration Scripts

This directory contains a collection of Python scripts for system administration tasks.

## Scripts Overview

### 1. System Health Monitor (`system_health_monitor.py`)
Monitors system resources and alerts on threshold violations.
```bash
python system_health_monitor.py
```
- Monitors CPU, Memory, and Disk usage
- Configurable thresholds
- Logs alerts and metrics

### 2. Backup Manager (`backup_manager.py`)
Automates backup operations with local and cloud support.
```bash
python backup_manager.py <source_dir> <backup_dir> [s3_bucket]
```
- Local directory backup
- Optional S3 cloud backup
- Backup rotation and cleanup
- Detailed backup reports

### 3. Log Analyzer (`log_analyzer.py`)
Analyzes web server logs for patterns and issues.
```bash
python log_analyzer.py <log_file> <output_file>
```
- Tracks 404 errors
- Identifies most active IPs
- Reports most requested pages
- Generates traffic patterns

### 4. Application Health Checker (`app_health_checker.py`)
Monitors application endpoints and generates health reports.
```bash
python app_health_checker.py <config_file> <output_file>
```
- HTTP endpoint monitoring
- Response time tracking
- Status code verification
- Email alerts for downtime

## Requirements

```bash
pip install -r requirements.txt
```

Required packages:
- psutil
- boto3
- requests

## Configuration

1. System Health Monitor:
   - Edit thresholds in the script
   - Configure logging settings

2. Backup Manager:
   - Set AWS credentials for S3 backup
   - Configure backup retention period

3. Log Analyzer:
   - Supports standard Apache/Nginx log formats
   - Configurable report formats

4. App Health Checker:
   - Edit config.json for endpoints
   - Configure SMTP for alerts

## Usage Examples

1. Monitor system health:
```bash
python system_health_monitor.py
```

2. Create backup with S3:
```bash
python backup_manager.py /path/to/source /path/to/backup my-s3-bucket
```

3. Analyze nginx logs:
```bash
python log_analyzer.py /var/log/nginx/access.log report.json
```

4. Check application health:
```bash
python app_health_checker.py config.json health_report.json
```

## Logging

All scripts use Python's logging module and write to their respective log files:
- system_health.log
- backup.log
- log_analyzer.log
- app_health.log

## Error Handling

- All scripts include comprehensive error handling
- Failed operations are logged
- Email alerts for critical errors (when configured)

## Maintenance

- Regular log rotation recommended
- Monitor disk space for backup storage
- Review and update thresholds as needed
- Keep configuration files updated