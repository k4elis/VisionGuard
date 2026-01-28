# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability in VisionGuard, please report it by:

1. **DO NOT** open a public issue
2. Email the security details to the project maintainers
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

We will respond within 48 hours and work with you to address the issue.

## Security Best Practices

### Production Deployment

1. **Authentication**
   - Change default credentials immediately
   - Use strong passwords (minimum 12 characters, mixed case, numbers, symbols)
   - Rotate passwords regularly

2. **Secret Keys**
   - Generate unique secret keys for each environment
   - Never commit secrets to version control
   - Use environment variables for sensitive data
   - Rotate keys periodically

3. **Network Security**
   - Use HTTPS in production (set up SSL/TLS certificates)
   - Configure firewall rules to restrict access
   - Use VPN or private networks for camera connections
   - Implement rate limiting on API endpoints

4. **Docker Security**
   - Run containers as non-root user
   - Keep Docker and images updated
   - Scan images for vulnerabilities
   - Use minimal base images

5. **Camera Security**
   - Use secure camera credentials
   - Change default camera passwords
   - Isolate camera network from internet
   - Enable camera authentication

6. **Data Protection**
   - Encrypt recordings at rest (if storing sensitive data)
   - Implement access controls for recordings
   - Set up automated backup and retention policies
   - Securely delete old recordings

7. **Monitoring**
   - Enable logging
   - Monitor for suspicious activity
   - Set up alerts for authentication failures
   - Regularly review access logs

### Discord Bot Security

1. Keep bot token secure and private
2. Use minimal required permissions
3. Restrict bot to specific channels
4. Regularly rotate bot token

### Updates

- Keep all dependencies updated
- Monitor security advisories for:
  - Python packages
  - Node.js packages
  - Docker images
  - Operating system

### Vulnerability Scanning

Regularly scan for vulnerabilities:
```bash
# Python dependencies
pip-audit

# Node.js dependencies
npm audit

# Docker images
docker scan visionguard-backend
docker scan visionguard-frontend
```

## Known Security Considerations

1. **MJPEG Streams**: Ensure camera streams are on a secure network
2. **Session Management**: JWT tokens expire after configured time
3. **File Upload**: System does not accept file uploads, only camera streams
4. **XSS Protection**: Frontend sanitizes user inputs
5. **CSRF Protection**: API uses token-based authentication

## Security Updates

We will release security updates as needed. Subscribe to the repository to receive notifications of security updates.

## Compliance

Users are responsible for ensuring their use of VisionGuard complies with:
- Local privacy laws
- Data protection regulations (GDPR, CCPA, etc.)
- Workplace surveillance laws
- Recording consent requirements

## Contact

For security concerns, contact the maintainers through GitHub.
