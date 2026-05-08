# FedRAMP Control Baseline Analysis and XCCDF Mapping Recommendations

## Executive Summary

This document analyzes FedRAMP control baseline differences and provides recommendations for extending component definitions and XCCDF checks to support FedRAMP Moderate and High baselines.

**Key Findings:**
- **167 controls** appear in FedRAMP Moderate but NOT in Low
- **87 controls** appear in FedRAMP High but NOT in Moderate
- Selected **14 Moderate-specific** and **10 High-specific** controls for technical validation
- **24 new XCCDF rules** will enable these Moderate-only and High-only controls to be mapped via component definitions
- These controls are suitable for "software" (Ubuntu_Linux_24_04_LTS) and "validation" (oscap) component mappings

## How the 24 New Rules Enable Control Mapping

**The Mapping Flow:**
1. **XCCDF Rules** → Define technical checks (e.g., `account_automated_provisioning_enabled`)
2. **Software Component** → References rules via `Rule_Id` properties (what to check)
3. **Validation Component** → References rules via `Check_Id` properties (how to check via OSCAP)
4. **Control Implementation** → Maps rules to NIST 800-53 controls (e.g., AC-2.1)

**Result:** The 24 new XCCDF rules enable automated validation of 14 FedRAMP Moderate-only controls and 10 FedRAMP High-only controls that were previously not covered by existing XCCDF checks.

---

## 1. FedRAMP Baseline Control Differences

### 1.1 Controls in FedRAMP Moderate but NOT in Low (167 total)

**Selected 14 controls for software/validation mapping:**

| Control ID | Control Name | Rationale for Selection |
|------------|--------------|-------------------------|
| **ac-2.1** | Account Management \| Automated System Account Management | Can validate automated account provisioning/deprovisioning |
| **ac-2.2** | Account Management \| Automated Temporary and Emergency Account Management | Can check for automated temporary account expiration |
| **ac-2.3** | Account Management \| Disable Accounts | Can verify inactive account disabling mechanisms |
| **ac-6.1** | Least Privilege \| Authorize Access to Security Functions | Can validate sudo/privilege escalation configurations |
| **ac-6.2** | Least Privilege \| Non-Privileged Access for Nonsecurity Functions | Can check that non-security functions don't require elevated privileges |
| **ac-11** | Device Lock | Can verify screen lock timeout configurations |
| **ac-11.1** | Device Lock \| Pattern-Hiding Displays | Can check for screen blanking/pattern hiding settings |
| **ac-17.1** | Remote Access \| Monitoring and Control | Can validate SSH logging and monitoring configurations |
| **au-3.1** | Content of Audit Records \| Additional Audit Information | Can verify extended audit record content (user IDs, timestamps, etc.) |
| **au-6.1** | Audit Record Review, Analysis, and Reporting \| Automated Process Integration | Can check for automated log analysis tool configurations |
| **cm-3.2** | Configuration Change Control \| Testing, Validation, and Documentation | Can verify change control documentation requirements |
| **cm-7.1** | Least Functionality \| Periodic Review | Can validate periodic service/package review processes |
| **si-2.2** | Flaw Remediation \| Automated Flaw Remediation Status | Can check for automated patch management tool configurations |
| **si-4.2** | System Monitoring \| Automated Tools for Real-Time Analysis | Can verify intrusion detection/monitoring tool presence |

### 1.2 Controls in FedRAMP High but NOT in Moderate (87 total)

**Selected 10 controls for software/validation mapping:**

| Control ID | Control Name | Rationale for Selection |
|------------|--------------|-------------------------|
| **ac-4.4** | Information Flow Enforcement \| Flow Control of Encrypted Information | Can validate encrypted traffic inspection capabilities |
| **ac-6.3** | Least Privilege \| Network Access to Privileged Commands | Can check network-based privilege restrictions |
| **ac-10** | Concurrent Session Control | Can verify session limit configurations |
| **au-5.1** | Response to Audit Logging Process Failures \| Storage Capacity Warning | Can check audit storage threshold alerting |
| **au-5.2** | Response to Audit Logging Process Failures \| Real-Time Alerts | Can verify real-time audit failure alerting |
| **au-6.4** | Audit Record Review, Analysis, and Reporting \| Central Review and Analysis | Can validate centralized logging configurations |
| **au-9.2** | Protection of Audit Information \| Store on Separate Physical Systems | Can check for remote/separate audit log storage |
| **au-9.3** | Protection of Audit Information \| Cryptographic Protection | Can verify audit log encryption/signing |
| **au-10** | Non-repudiation | Can validate digital signature capabilities for critical actions |
| **au-12.1** | Audit Record Generation \| System-Wide Time-Correlated Audit Trail | Can check for synchronized time sources and correlation |

---

## 2. Proposed XCCDF Checks for Selected Controls

### 2.1 FedRAMP Moderate Controls - New XCCDF Checks

#### AC-2.1: Automated System Account Management
```
Rule ID: account_automated_provisioning_enabled
Check: Verify presence of automated account management tools (e.g., LDAP, Active Directory integration)
Files: /etc/sssd/sssd.conf, /etc/pam.d/common-account
Validation: Check for automated provisioning service configuration
```

#### AC-2.2: Automated Temporary Account Management
```
Rule ID: account_temporary_expiration_configured
Check: Verify temporary account expiration is automated
Files: /etc/login.defs (INACTIVE setting), /etc/default/useradd
Validation: INACTIVE value should be <= 35 days
```

#### AC-2.3: Disable Inactive Accounts
```
Rule ID: account_disable_inactive_accounts
Check: Verify inactive account disabling mechanism
Files: /etc/login.defs, cron jobs for account auditing
Validation: Check for automated scripts or tools that disable inactive accounts
```

#### AC-6.1: Authorize Access to Security Functions
```
Rule ID: sudo_security_function_authorization
Check: Verify sudo configuration restricts security functions
Files: /etc/sudoers, /etc/sudoers.d/*
Validation: Check that security-related commands require explicit authorization
```

#### AC-6.2: Non-Privileged Access for Nonsecurity Functions
```
Rule ID: service_nonprivileged_user_execution
Check: Verify services run as non-root users
Command: ps aux | grep -v root
Validation: Check that application services don't run as root
```

#### AC-11: Device Lock
```
Rule ID: screen_lock_timeout_configured
Check: Verify screen lock timeout is configured
Files: /etc/gdm3/greeter.dconf-defaults, /etc/X11/xorg.conf.d/
Validation: Screen lock timeout <= 15 minutes
```

#### AC-11.1: Pattern-Hiding Displays
```
Rule ID: screen_lock_pattern_hiding_enabled
Check: Verify screen blanking on lock
Files: /etc/gdm3/greeter.dconf-defaults
Validation: Check for blank-screen or pattern-hiding configuration
```

#### AC-17.1: Remote Access Monitoring
```
Rule ID: sshd_logging_enabled
Check: Verify SSH logging is enabled and comprehensive
Files: /etc/ssh/sshd_config
Validation: LogLevel should be INFO or VERBOSE
```

#### AU-3.1: Additional Audit Information
```
Rule ID: auditd_extended_information_enabled
Check: Verify extended audit information is captured
Files: /etc/audit/auditd.conf, /etc/audit/rules.d/*.rules
Validation: Check for comprehensive audit rules including user, timestamp, outcome
```

#### AU-6.1: Automated Process Integration
```
Rule ID: log_analysis_tool_configured
Check: Verify automated log analysis tool is configured
Files: /etc/logwatch/, /etc/logrotate.d/, /etc/rsyslog.d/
Validation: Check for log analysis tool configuration (logwatch, SIEM agent, etc.)
```

#### CM-3.2: Testing and Validation of Changes
```
Rule ID: change_control_documentation_required
Check: Verify change control process documentation
Files: /etc/ansible/, /etc/puppet/, /var/log/dpkg.log
Validation: Check for configuration management tool presence and logging
```

#### CM-7.1: Periodic Review of Functionality
```
Rule ID: service_periodic_review_enabled
Check: Verify periodic service review process
Files: /etc/cron.d/, /etc/cron.daily/
Validation: Check for automated service inventory/review scripts
```

#### SI-2.2: Automated Flaw Remediation Status
```
Rule ID: package_update_automation_configured
Check: Verify automated patch management
Files: /etc/apt/apt.conf.d/50unattended-upgrades
Validation: Unattended-Upgrade::Allowed-Origins should include security updates
```

#### SI-4.2: Automated Real-Time Analysis
```
Rule ID: intrusion_detection_tool_installed
Check: Verify IDS/IPS tool is installed and running
Commands: systemctl status aide, systemctl status ossec
Validation: Check for AIDE, OSSEC, or similar tool running
```

### 2.2 FedRAMP High Controls - New XCCDF Checks

#### AC-4.4: Flow Control of Encrypted Information
```
Rule ID: encrypted_traffic_inspection_configured
Check: Verify encrypted traffic inspection capability
Files: /etc/iptables/, /etc/nftables/
Validation: Check for SSL/TLS inspection or proxy configuration
```

#### AC-6.3: Network Access to Privileged Commands
```
Rule ID: privileged_command_network_restriction
Check: Verify network-based restrictions on privileged commands
Files: /etc/security/access.conf, /etc/hosts.allow, /etc/hosts.deny
Validation: Check for network-based access controls on privileged operations
```

#### AC-10: Concurrent Session Control
```
Rule ID: concurrent_session_limit_configured
Check: Verify concurrent session limits
Files: /etc/security/limits.conf, /etc/systemd/logind.conf
Validation: maxlogins or UserTasksMax should be configured
```

#### AU-5.1: Storage Capacity Warning
```
Rule ID: auditd_storage_threshold_alert
Check: Verify audit storage threshold alerting
Files: /etc/audit/auditd.conf
Validation: space_left_action should be EMAIL or SYSLOG
```

#### AU-5.2: Real-Time Alerts
```
Rule ID: auditd_realtime_alerts_enabled
Check: Verify real-time audit failure alerts
Files: /etc/audit/auditd.conf
Validation: admin_space_left_action should be HALT or SINGLE
```

#### AU-6.4: Central Review and Analysis
```
Rule ID: centralized_logging_configured
Check: Verify centralized logging is configured
Files: /etc/rsyslog.conf, /etc/rsyslog.d/*.conf
Validation: Check for remote syslog server configuration
```

#### AU-9.2: Store on Separate Physical Systems
```
Rule ID: audit_logs_remote_storage
Check: Verify audit logs are sent to remote system
Files: /etc/audit/auditd.conf, /etc/audit/plugins.d/syslog.conf
Validation: Check for remote audit log forwarding
```

#### AU-9.3: Cryptographic Protection
```
Rule ID: audit_logs_encrypted
Check: Verify audit log encryption/signing
Files: /etc/audit/auditd.conf
Validation: Check for log_format = ENRICHED or encryption configuration
```

#### AU-10: Non-repudiation
```
Rule ID: critical_action_signing_enabled
Check: Verify digital signatures for critical actions
Files: /etc/audit/rules.d/*.rules
Validation: Check for audit rules with key fields for non-repudiation
```

#### AU-12.1: System-Wide Time-Correlated Audit Trail
```
Rule ID: time_synchronization_configured
Check: Verify NTP/chrony is configured and running
Files: /etc/chrony/chrony.conf, /etc/ntp.conf
Validation: systemctl status chronyd should show active
```

---

## 3. Component Definition Mapping Strategy

### 3.1 Software Component (Ubuntu_Linux_24_04_LTS)

Add the following Rule_Id properties to the software component:

**For FedRAMP Moderate:**
- account_automated_provisioning_enabled
- account_temporary_expiration_configured
- account_disable_inactive_accounts
- sudo_security_function_authorization
- service_nonprivileged_user_execution
- screen_lock_timeout_configured
- screen_lock_pattern_hiding_enabled
- sshd_logging_enabled
- auditd_extended_information_enabled
- log_analysis_tool_configured
- change_control_documentation_required
- service_periodic_review_enabled
- package_update_automation_configured
- intrusion_detection_tool_installed

**For FedRAMP High (additional):**
- encrypted_traffic_inspection_configured
- privileged_command_network_restriction
- concurrent_session_limit_configured
- auditd_storage_threshold_alert
- auditd_realtime_alerts_enabled
- centralized_logging_configured
- audit_logs_remote_storage
- audit_logs_encrypted
- critical_action_signing_enabled
- time_synchronization_configured

### 3.2 Validation Component (oscap)

Add corresponding Check_Id properties to the validation component:

**Format:** `xccdf_org.ssgproject.content_rule_<rule_id>`

Example:
- xccdf_org.ssgproject.content_rule_account_automated_provisioning_enabled
- xccdf_org.ssgproject.content_rule_account_temporary_expiration_configured
- etc.

---

## 4. Implementation Recommendations

### 4.1 Immediate Actions

1. **Create new XCCDF rule definitions** for the 24 selected controls (14 Moderate + 10 High)
2. **Update component definitions** to include new Rule_Id and Check_Id properties
3. **Generate revised XCCDF benchmark files** with new rules
4. **Update SSP generation** to include new control implementations

### 4.2 XCCDF Benchmark Structure

The revised XCCDF files should include:

```xml
<Rule id="xccdf_org.ssgproject.content_rule_account_automated_provisioning_enabled" 
      selected="true" severity="medium">
  <title>Automated System Account Management Enabled</title>
  <description>
    Verify that automated account management is configured...
  </description>
  <reference href="https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final">
    NIST 800-53 Rev 5 AC-2(1)
  </reference>
  <check system="http://oval.mitre.org/XMLSchema/oval-definitions-5">
    <check-content-ref name="oval:ssg:def:account_automated_provisioning_enabled" 
                       href="ssg-ubuntu2404-oval.xml"/>
  </check>
</Rule>
```

### 4.3 Testing Strategy

1. **Unit Testing**: Test each new XCCDF rule individually
2. **Integration Testing**: Run full scans with updated benchmarks
3. **Validation**: Verify control mappings in generated SSPs
4. **Compliance Verification**: Ensure FedRAMP Moderate and High baselines are complete

---

## 5. Next Steps

1. ✅ Analyze FedRAMP baseline differences
2. ✅ Identify controls in Moderate but not Low (167 controls)
3. ✅ Identify controls in High but not Moderate (87 controls)
4. ✅ Select technical controls for mapping (24 total)
5. ✅ Document XCCDF check requirements
6. ⏳ Generate revised XCCDF benchmark files
7. ⏳ Update component definitions with new mappings
8. ⏳ Test and validate new checks
9. ⏳ Update SSP generation scripts

---

## Appendix A: Full Control Lists

### A.1 All 167 Controls in Moderate but NOT in Low

(Available upon request - includes all control IDs from the analysis)

### A.2 All 87 Controls in High but NOT in Moderate

(Available upon request - includes all control IDs from the analysis)

---

**Document Version:** 1.0  
**Date:** 2026-05-08  
**Author:** OSCAL Compass Analysis Tool