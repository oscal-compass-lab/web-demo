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
  ac-02.03_odp.01:
    guidelines:
      - prose: time period within which to disable accounts is defined;
    values:
      - 24 hours for user accounts
    alt-identifier: ac-2.3_prm_1
    profile-param-value-origin: <REPLACE_ME>
  ac-02.03_odp.02:
    guidelines:
      - prose: time period for account inactivity before disabling is defined;
    values:
      - ninety (90) days
    alt-identifier: ac-2.3_prm_2
    profile-param-value-origin: <REPLACE_ME>
x-trestle-global:
  profile:
    title: FedRAMP Moderate Baseline (NIST 800-53 Rev5)
    href: trestle://profiles/FedRAMP-Rev5-Moderate/profile.json
  sort-id: ac-02.03
---

# ac-2.3 - \[Access Control\] Disable Accounts

## Control Statement

Disable accounts within [24 hours for user accounts] when the accounts:

- \[(a)\] Have expired;

- \[(b)\] Are no longer associated with a user or individual;

- \[(c)\] Are in violation of organizational policy; or

- \[(d)\] Have been inactive for [ninety (90) days].

## Control Assessment Objective

- \[AC-02(03)(a)\] accounts are disabled within [24 hours for user accounts] when the accounts have expired;

- \[AC-02(03)(b)\] accounts are disabled within [24 hours for user accounts] when the accounts are no longer associated with a user or individual;

- \[AC-02(03)(c)\] accounts are disabled within [24 hours for user accounts] when the accounts are in violation of organizational policy;

- \[AC-02(03)(d)\] accounts are disabled within [24 hours for user accounts] when the accounts have been inactive for [ninety (90) days].

## Control guidance

Disabling expired, inactive, or otherwise anomalous accounts supports the concepts of least privilege and least functionality which reduce the attack surface of the system.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

<!-- Add implementation prose for the main This System component for control: ac-2.3 -->

#### Implementation Status: planned

______________________________________________________________________
