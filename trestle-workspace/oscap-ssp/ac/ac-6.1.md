---
x-trestle-add-props: []
  # Add or modify control properties here
  # Properties may be at the control or part level
  # Add control level properties like this:
  #   - name: ac1_new_prop
  #     value: new property value
  #
  # Add properties to a statement part like this, where "b." is the label of the target statement part
  #   - name: ac1_new_prop
  #     value: new property value
  #     smt-part: b.
  #
x-trestle-set-params:
  # You may set values for parameters in the assembled SSP by adding
  #
  # ssp-values:
  #   - value 1
  #   - value 2
  #
  # below a section of values:
  # The values list refers to the values in the resolved profile catalog, and the ssp-values represent new values
  # to be placed in SetParameters of the SSP.
  #
  ac-6.1_prm_2:
    aggregates:
      - ac-06.01_odp.02
      - ac-06.01_odp.03
      - ac-06.01_odp.04
    profile-param-value-origin: <REPLACE_ME>
  ac-06.01_odp.01:
    alt-identifier: ac-6.1_prm_1
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  ac-06.01_odp.02:
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  ac-06.01_odp.03:
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  ac-06.01_odp.04:
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  ac-06.01_odp.05:
    alt-identifier: ac-6.1_prm_3
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
x-trestle-global:
  profile:
    title: FedRAMP Moderate Baseline (NIST 800-53 Rev5)
    href: trestle://profiles/FedRAMP-Rev5-Moderate/profile.json
  sort-id: ac-06.01
---

# ac-6.1 - \[Access Control\] Authorize Access to Security Functions

## Control Statement

Authorize access for [individuals and roles] to:

- \[(a)\] [organization-defined security functions (deployed in hardware, software, and firmware)] ; and

- \[(b)\] [security-relevant information].

## Control Assessment Objective

- \[AC-06(01)(a)\]

  - \[AC-06(01)(a)[01]\] access is authorized for [individuals and roles] to [security functions (deployed in hardware)];
  - \[AC-06(01)(a)[02]\] access is authorized for [individuals and roles] to [security functions (deployed in software)];
  - \[AC-06(01)(a)[03]\] access is authorized for [individuals and roles] to [security functions (deployed in firmware)];

- \[AC-06(01)(b)\] access is authorized for [individuals and roles] to [security-relevant information].

## Control guidance

Security functions include establishing system accounts, configuring access authorizations (i.e., permissions, privileges), configuring settings for events to be audited, and establishing intrusion detection parameters. Security-relevant information includes filtering rules for routers or firewalls, configuration parameters for security services, cryptographic key management information, and access control lists. Authorized personnel include security administrators, system administrators, system security officers, system programmers, and other privileged users.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

<!-- Add implementation prose for the main This System component for control: ac-6.1 -->

#### Implementation Status: planned

______________________________________________________________________
