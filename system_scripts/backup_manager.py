#!/usr/bin/env python3
import os
import shutil
import datetime
import logging
import sys
import boto3
from botocore.exceptions import ClientError

# Configure logging
logging.basicConfig(
    filename='backup.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class BackupManager:
    def __init__(self, source_dir, backup_dir, s3_bucket=None):
        self.source_dir = os.path.abspath(source_dir)
        self.backup_dir = os.path.abspath(backup_dir)
        self.s3_bucket = s3_bucket
        self.timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        self.backup_name = f'backup_{self.timestamp}'

    def create_local_backup(self):
        """Create a local backup of the source directory"""
        try:
            backup_path = os.path.join(self.backup_dir, self.backup_name)
            shutil.copytree(self.source_dir, backup_path)
            logging.info(f'Local backup created successfully at {backup_path}')
            return True
        except Exception as e:
            logging.error(f'Local backup failed: {str(e)}')
            return False

    def upload_to_s3(self, local_backup_path):
        """Upload backup to S3 bucket"""
        if not self.s3_bucket:
            logging.info('No S3 bucket configured, skipping cloud backup')
            return True

        try:
            s3_client = boto3.client('s3')
            for root, _, files in os.walk(local_backup_path):
                for file in files:
                    local_path = os.path.join(root, file)
                    relative_path = os.path.relpath(local_path, local_backup_path)
                    s3_path = f'{self.backup_name}/{relative_path}'
                    
                    s3_client.upload_file(local_path, self.s3_bucket, s3_path)
            
            logging.info(f'Backup uploaded to S3 bucket: {self.s3_bucket}/{self.backup_name}')
            return True
        except ClientError as e:
            logging.error(f'S3 upload failed: {str(e)}')
            return False

    def cleanup_old_backups(self, keep_days=7):
        """Remove backups older than specified days"""
        try:
            for item in os.listdir(self.backup_dir):
                item_path = os.path.join(self.backup_dir, item)
                if os.path.isdir(item_path) and item.startswith('backup_'):
                    creation_time = os.path.getctime(item_path)
                    if (time.time() - creation_time) // (24 * 3600) >= keep_days:
                        shutil.rmtree(item_path)
                        logging.info(f'Removed old backup: {item}')
        except Exception as e:
            logging.error(f'Cleanup failed: {str(e)}')

    def generate_report(self, success):
        """Generate backup report"""
        report = {
            'timestamp': self.timestamp,
            'source_directory': self.source_dir,
            'backup_directory': self.backup_dir,
            'status': 'Success' if success else 'Failed',
            'backup_name': self.backup_name
        }
        
        report_path = os.path.join(self.backup_dir, f'backup_report_{self.timestamp}.txt')
        with open(report_path, 'w') as f:
            for key, value in report.items():
                f.write(f'{key}: {value}\n')
        
        logging.info(f'Backup report generated: {report_path}')
        return report

def main():
    if len(sys.argv) < 3:
        print("Usage: backup.py <source_directory> <backup_directory> [s3_bucket_name]")
        sys.exit(1)

    source_dir = sys.argv[1]
    backup_dir = sys.argv[2]
    s3_bucket = sys.argv[3] if len(sys.argv) > 3 else None

    backup_manager = BackupManager(source_dir, backup_dir, s3_bucket)
    
    # Create local backup
    local_success = backup_manager.create_local_backup()
    
    # Upload to S3 if configured
    cloud_success = True
    if local_success and s3_bucket:
        cloud_success = backup_manager.upload_to_s3(
            os.path.join(backup_dir, backup_manager.backup_name)
        )
    
    # Generate report
    success = local_success and cloud_success
    backup_manager.generate_report(success)
    
    # Cleanup old backups
    backup_manager.cleanup_old_backups()

if __name__ == "__main__":
    main()