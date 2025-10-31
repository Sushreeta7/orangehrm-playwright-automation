#!/usr/bin/env python3
import re
from collections import Counter, defaultdict
from datetime import datetime
import json
import logging

# Configure logging
logging.basicConfig(
    filename='log_analyzer.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class LogAnalyzer:
    def __init__(self, log_file):
        self.log_file = log_file
        self.ip_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
        self.datetime_pattern = r'\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2}'
        self.request_pattern = r'"(GET|POST|PUT|DELETE|HEAD|OPTIONS|PATCH) ([^"]*)"'
        self.status_code_pattern = r'" (\d{3}) '
        
        # Initialize counters
        self.ip_counts = Counter()
        self.status_codes = Counter()
        self.request_paths = Counter()
        self.hourly_traffic = defaultdict(int)
        self.errors_404 = []
        self.total_requests = 0

    def parse_line(self, line):
        """Parse a single log line"""
        try:
            # Extract IP address
            ip = re.search(self.ip_pattern, line)
            if ip:
                self.ip_counts[ip.group()] += 1

            # Extract datetime
            datetime_str = re.search(self.datetime_pattern, line)
            if datetime_str:
                hour = datetime.strptime(datetime_str.group(), '%d/%b/%Y:%H:%M:%S').strftime('%H')
                self.hourly_traffic[hour] += 1

            # Extract request details
            request = re.search(self.request_pattern, line)
            if request:
                self.request_paths[request.group(2)] += 1

            # Extract status code
            status = re.search(self.status_code_pattern, line)
            if status:
                status_code = status.group(1)
                self.status_codes[status_code] += 1
                if status_code == '404':
                    self.errors_404.append(line)

            self.total_requests += 1

        except Exception as e:
            logging.error(f'Error parsing line: {str(e)}')

    def analyze(self):
        """Analyze the log file"""
        try:
            with open(self.log_file, 'r') as f:
                for line in f:
                    self.parse_line(line)
            return self.generate_report()
        except Exception as e:
            logging.error(f'Error analyzing log file: {str(e)}')
            return None

    def generate_report(self):
        """Generate analysis report"""
        report = {
            'summary': {
                'total_requests': self.total_requests,
                'unique_ips': len(self.ip_counts),
                'total_404_errors': len(self.errors_404)
            },
            'top_ips': dict(self.ip_counts.most_common(10)),
            'status_code_distribution': dict(self.status_codes),
            'most_requested_paths': dict(self.request_paths.most_common(10)),
            'hourly_traffic': dict(sorted(self.hourly_traffic.items())),
            'recent_404_errors': self.errors_404[-10:] if self.errors_404 else []
        }
        
        return report

    def save_report(self, report, output_file):
        """Save the report to a file"""
        try:
            with open(output_file, 'w') as f:
                json.dump(report, f, indent=2)
            logging.info(f'Report saved to {output_file}')
        except Exception as e:
            logging.error(f'Error saving report: {str(e)}')

def main():
    import sys
    if len(sys.argv) != 3:
        print("Usage: log_analyzer.py <log_file> <output_file>")
        sys.exit(1)

    log_file = sys.argv[1]
    output_file = sys.argv[2]

    analyzer = LogAnalyzer(log_file)
    report = analyzer.analyze()
    
    if report:
        analyzer.save_report(report, output_file)
        print(f"Analysis complete. Report saved to {output_file}")
    else:
        print("Analysis failed. Check the log file for details.")

if __name__ == "__main__":
    main()