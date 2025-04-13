# DevSecOps Flask Demo Application

This repository contains a simple Flask application designed for demonstrating DevSecOps principles, including SAST (Static Application Security Testing), DAST (Dynamic Application Security Testing), and release management.

## Overview

This application demonstrates several common security vulnerabilities including:
- SQL Injection
- Cross-Site Scripting (XSS)
- Insecure configuration

## Prerequisites

- Python 3.x
- Docker (optional)
- Git

## Installation

### Local Setup

1. Clone this repository:
```
git clone https://github.com/yourusername/DevSecOps-Demo.git
cd DevSecOps-Demo
```

2. Install the required dependencies:
```
pip install -r requirements.txt
```

3. Run the application:
```
python app.py
```

The application will be available at `http://localhost:5000`.

### Docker Setup

1. Build the Docker image:
```
docker build -t devsecops-demo .
```

2. Run the container:
```
docker run -p 5000:5000 devsecops-demo
```

## Security Testing

### Static Application Security Testing (SAST) with Semgrep

SAST helps identify security vulnerabilities in source code before deployment.

#### Running Semgrep Locally

```
docker run -it -v $(pwd):/src semgrep/semgrep semgrep scan --config=auto
```

#### Running Semgrep with Cloud Integration

```
docker run -it -v $(pwd):/src -e SEMGREP_APP_TOKEN=YOUR_TOKEN -e SEMGREP_REPO_URL=https://github.com/yourusername/DevSecOps-Demo semgrep/semgrep semgrep ci
```

### Dynamic Application Security Testing (DAST) with OWASP ZAP

DAST identifies vulnerabilities in running applications, simulating attacks against your app.

#### Running ZAP Docker Scan

```
docker run -t owasp/zap2docker-stable zap-baseline.py -t http://host.docker.internal:5000 -r dast-report.html
```

For a more comprehensive scan:

```
docker run -t owasp/zap2docker-stable zap-full-scan.py -t http://host.docker.internal:5000 -r dast-full-report.html
```


```

The GitHub Actions workflow will automatically build, test, scan, and prepare the release.

## GitHub Actions Integration

This repository includes GitHub Actions workflows for:
- SAST scanning with Semgrep
- DAST scanning with OWASP ZAP
- Automated build and release pipeline

See the `.github/workflows` directory for details.

## Educational Purpose

**IMPORTANT**: This application intentionally contains security vulnerabilities for educational purposes. DO NOT use it in production or expose it to the internet.

## License

MIT
saa
