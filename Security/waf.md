- Owasp 10
1. injection
2. broken authentication
3. sensitive data exposure
4. xml external entities
5. broken access control
6. security misconfiguration
7. cross site scripting
8. insecure deserialization
9. using components with know vulnerability
10. insufficient logging and monitoring
- HTTP Flood
- cache busting attack
- common weakness enumeration

Web Application Firewall
- Application Layer Protection


WAF Integrate with
1. ALB
2. CloudFront 
3. API Gateway


Help to protect you web application
1. Create Security rules
2. Control Bot Traffic
3. SQL Injection or cross-site scripting


Web ACL
1. Containers of rule and rule group
Rule
- Block
- Allow
- Count
Check
- IP add mach
- originated country
- Request header and string appear in header
- Regex pattern sets
- lenght of request
- presence od SQL code
- Presence of script

Customize Rule to filter traffic pattern
1. AWS managed rule
2. Aws market place vendor
3. OWASP 10 significant security risk
4. CVE

How can I detect false positives caused by AWS Managed Rules and add them to a safe list?
REf https://aws.amazon.com/premiumsupport/knowledge-center/waf-detect-false-positives-from-amrs/



