#!/usr/bin/env python3
import requests
import time
import logging
from datetime import datetime
import json
from typing import Dict, List, Optional
import smtplib
from email.mime.text import MIMEText
from dataclasses import dataclass, asdict

# Configure logging
logging.basicConfig(
    filename='app_health.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

@dataclass
class EndpointStatus:
    url: str
    status: str
    response_time: float
    status_code: int
    last_check: str
    error_message: Optional[str] = None

class ApplicationHealthChecker:
    def __init__(self, config_file: str):
        self.config = self.load_config(config_file)
        self.endpoints: Dict[str, EndpointStatus] = {}
        self.history: Dict[str, List[EndpointStatus]] = {}

    def load_config(self, config_file: str) -> dict:
        """Load configuration from JSON file"""
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
            logging.info('Configuration loaded successfully')
            return config
        except Exception as e:
            logging.error(f'Error loading configuration: {str(e)}')
            raise

    def check_endpoint(self, url: str) -> EndpointStatus:
        """Check the health of a single endpoint"""
        start_time = time.time()
        try:
            response = requests.get(url, timeout=self.config.get('timeout', 30))
            response_time = time.time() - start_time
            
            status = 'up' if response.status_code < 400 else 'down'
            return EndpointStatus(
                url=url,
                status=status,
                response_time=response_time,
                status_code=response.status_code,
                last_check=datetime.now().isoformat(),
                error_message=None
            )
        except requests.RequestException as e:
            return EndpointStatus(
                url=url,
                status='down',
                response_time=time.time() - start_time,
                status_code=0,
                last_check=datetime.now().isoformat(),
                error_message=str(e)
            )

    def check_all_endpoints(self) -> Dict[str, EndpointStatus]:
        """Check all configured endpoints"""
        for url in self.config['endpoints']:
            status = self.check_endpoint(url)
            self.endpoints[url] = status
            
            # Store in history
            if url not in self.history:
                self.history[url] = []
            self.history[url].append(status)
            
            # Keep history limited
            max_history = self.config.get('max_history', 100)
            if len(self.history[url]) > max_history:
                self.history[url] = self.history[url][-max_history:]
            
            # Log status
            logging.info(f'Endpoint {url} status: {status.status}')
            
            # Send alert if needed
            if status.status == 'down' and self.config.get('enable_alerts', False):
                self.send_alert(status)
        
        return self.endpoints

    def send_alert(self, status: EndpointStatus):
        """Send alert for down endpoints"""
        if not self.config.get('smtp_config'):
            logging.warning('SMTP configuration not found, skipping alert')
            return

        smtp_config = self.config['smtp_config']
        message = MIMEText(
            f"Endpoint {status.url} is down!\n"
            f"Status Code: {status.status_code}\n"
            f"Error: {status.error_message}\n"
            f"Time: {status.last_check}"
        )
        
        message['Subject'] = f'Application Health Alert - {status.url}'
        message['From'] = smtp_config['from_email']
        message['To'] = smtp_config['to_email']

        try:
            with smtplib.SMTP(smtp_config['server'], smtp_config['port']) as server:
                if smtp_config.get('use_tls', True):
                    server.starttls()
                if smtp_config.get('username'):
                    server.login(smtp_config['username'], smtp_config['password'])
                server.send_message(message)
            logging.info(f'Alert sent for {status.url}')
        except Exception as e:
            logging.error(f'Error sending alert: {str(e)}')

    def generate_report(self) -> dict:
        """Generate a health check report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'overall_status': 'up' if all(s.status == 'up' for s in self.endpoints.values()) else 'down',
            'endpoints': {url: asdict(status) for url, status in self.endpoints.items()},
            'summary': {
                'total': len(self.endpoints),
                'up': sum(1 for s in self.endpoints.values() if s.status == 'up'),
                'down': sum(1 for s in self.endpoints.values() if s.status == 'down')
            }
        }
        return report

    def save_report(self, report: dict, output_file: str):
        """Save the health check report to a file"""
        try:
            with open(output_file, 'w') as f:
                json.dump(report, f, indent=2)
            logging.info(f'Report saved to {output_file}')
        except Exception as e:
            logging.error(f'Error saving report: {str(e)}')

def main():
    import sys
    if len(sys.argv) != 3:
        print("Usage: app_health_checker.py <config_file> <output_file>")
        sys.exit(1)

    config_file = sys.argv[1]
    output_file = sys.argv[2]

    checker = ApplicationHealthChecker(config_file)
    
    try:
        checker.check_all_endpoints()
        report = checker.generate_report()
        checker.save_report(report, output_file)
        print(f"Health check complete. Report saved to {output_file}")
    except Exception as e:
        logging.error(f'Health check failed: {str(e)}')
        print("Health check failed. Check the log file for details.")

if __name__ == "__main__":
    main()