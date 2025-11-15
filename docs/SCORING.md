# SCORING.md

# Scoring Methodology

This document outlines the scoring methodology used in the WithSecure Assessor project. The scoring system is designed to provide a transparent and deterministic evaluation of products based on various risk factors.

## Risk Score Components

The risk score is calculated based on the following components:

1. **Exposure (30%)**
   - This component assesses the exposure of the product to vulnerabilities, including:
     - Number of Known Exploited Vulnerabilities (KEV)
     - Recent critical Common Vulnerabilities and Exposures (CVEs)
     - CVE velocity over the last 12 months

2. **Controls (20%)**
   - This component evaluates the security controls implemented by the vendor, such as:
     - Single Sign-On (SSO), Multi-Factor Authentication (MFA), Security Assertion Markup Language (SAML)
     - Role-Based Access Control (RBAC) and System for Cross-domain Identity Management (SCIM)
     - Audit logs and encryption posture

3. **Vendor Posture (15%)**
   - This component examines the vendor's security posture, including:
     - Presence of a Product Security Incident Response Team (PSIRT)
     - Depth of the vendor's security page
     - Availability of a bug bounty program and Service Level Agreements (SLAs)

4. **Compliance (15%)**
   - This component assesses the vendor's compliance with industry standards, such as:
     - SOC 2 Type II
     - ISO 27001/27701
     - Data Protection Agreement (DPA) adequacy

5. **Incidents (10%)**
   - This component evaluates the history of public breaches or incidents in the last 36 months, focusing on:
     - Quality of remediation efforts

6. **Data Handling (10%)**
   - This component assesses the vendor's data handling practices, including:
     - Data locality and retention policies
     - Transparency regarding subprocessors

## Scoring Process

The scoring process follows these steps:

1. **Data Collection**
   - Data is collected from various sources, including:
     - Vulnerability databases (NVD, CISA KEV)
     - Vendor security pages and compliance documentation
     - Independent security advisories

2. **Normalization**
   - Collected data is normalized to ensure consistency in scoring.

3. **Weighting**
   - Each component is assigned a weight based on its importance in the overall risk assessment.

4. **Calculation**
   - The final risk score is calculated using the formula:
     - Risk Score = (Exposure * 0.30) + (Controls * 0.20) + (Vendor Posture * 0.15) + (Compliance * 0.15) + (Incidents * 0.10) + (Data Handling * 0.10)

5. **Confidence Assessment**
   - A confidence scalar (0.7 to 1.0) is applied based on the diversity and recency of the evidence collected.

## Transparency and Reporting

The scoring methodology is designed to be transparent, with all claims backed by citations. The scoring results, including individual component scores and the final risk score, are reported in a clear and concise manner, allowing stakeholders to understand the basis for the assessment.

## Conclusion

The WithSecure Assessor's scoring methodology aims to provide a reliable and comprehensive evaluation of products, helping organizations make informed decisions regarding their security posture.