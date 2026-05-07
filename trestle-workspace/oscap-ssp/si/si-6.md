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
  si-6_prm_1:
    aggregates:
      - si-06_odp.01
      - si-06_odp.02
    profile-param-value-origin: <REPLACE_ME>
  si-06_odp.01:
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  si-06_odp.02:
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  si-06_odp.03:
    alt-identifier: si-6_prm_2
    profile-param-value-origin: <REPLACE_ME>
  si-06_odp.04:
    alt-identifier: si-6_prm_3
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  si-06_odp.05:
    alt-identifier: si-6_prm_4
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  si-06_odp.06:
    guidelines:
      - prose: personnel or roles to be alerted of failed security and privacy 
          verification tests is/are defined;
    values:
      - to include system administrators and security personnel
    alt-identifier: si-6_prm_5
    profile-param-value-origin: <REPLACE_ME>
  si-06_odp.07:
    alt-identifier: si-6_prm_6
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  si-06_odp.08:
    alt-identifier: si-6_prm_7
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
x-trestle-global:
  profile:
    title: FedRAMP Moderate Baseline (NIST 800-53 Rev5)
    href: trestle://profiles/FedRAMP-Rev5-Moderate/profile.json
  sort-id: si-06
---

# si-6 - \[System and Information Integrity\] Security and Privacy Function Verification

## Control Statement

- \[a.\] Verify the correct operation of [organization-defined security and privacy functions];

- \[b.\] Perform the verification of the functions specified in SI-6a [Selection (one or more): [system transitional states]; upon command by user with appropriate privilege; [frequency]];

- \[c.\] Alert [to include system administrators and security personnel] to failed security and privacy verification tests; and

- \[d.\] [Selection (one or more): shut the system down; restart the system; [alternative action(s)]] when anomalies are discovered.

## Control Assessment Objective

- \[SI-06a.\]

  - \[SI-06a.[01]\] [security functions] are verified to be operating correctly;
  - \[SI-06a.[02]\] [privacy functions] are verified to be operating correctly;

- \[SI-06b.\]

  - \[SI-06b.[01]\] [security functions] are verified [Selection (one or more): [system transitional states]; upon command by user with appropriate privilege; [frequency]];
  - \[SI-06b.[02]\] [privacy functions] are verified [Selection (one or more): [system transitional states]; upon command by user with appropriate privilege; [frequency]];

- \[SI-06c.\]

  - \[SI-06c.[01]\] [to include system administrators and security personnel] is/are alerted to failed security verification tests;
  - \[SI-06c.[02]\] [to include system administrators and security personnel] is/are alerted to failed privacy verification tests;

- \[SI-06d.\] [Selection (one or more): shut the system down; restart the system; [alternative action(s)]] is/are initiated when anomalies are discovered.

## Control guidance

Transitional states for systems include system startup, restart, shutdown, and abort. System notifications include hardware indicator lights, electronic alerts to system administrators, and messages to local computer consoles. In contrast to security function verification, privacy function verification ensures that privacy functions operate as expected and are approved by the senior agency official for privacy or that privacy attributes are applied or used as expected.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

<!-- Add implementation prose for the main This System component for control: si-6 -->

#### Implementation Status: planned

______________________________________________________________________
