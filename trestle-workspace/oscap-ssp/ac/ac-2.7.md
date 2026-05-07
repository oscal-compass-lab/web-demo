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
  ac-02.07_odp:
    alt-identifier: ac-2.7_prm_1
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
x-trestle-global:
  profile:
    title: FedRAMP Moderate Baseline (NIST 800-53 Rev5)
    href: trestle://profiles/FedRAMP-Rev5-Moderate/profile.json
  sort-id: ac-02.07
---

# ac-2.7 - \[Access Control\] Privileged User Accounts

## Control Statement

- \[(a)\] Establish and administer privileged user accounts in accordance with [Selection: a role-based access scheme; an attribute-based access scheme];

- \[(b)\] Monitor privileged role or attribute assignments;

- \[(c)\] Monitor changes to roles or attributes; and

- \[(d)\] Revoke access when privileged role or attribute assignments are no longer appropriate.

## Control Assessment Objective

- \[AC-02(07)(a)\] privileged user accounts are established and administered in accordance with [Selection: a role-based access scheme; an attribute-based access scheme];

- \[AC-02(07)(b)\] privileged role or attribute assignments are monitored;

- \[AC-02(07)(c)\] changes to roles or attributes are monitored;

- \[AC-02(07)(d)\] access is revoked when privileged role or attribute assignments are no longer appropriate.

## Control guidance

Privileged roles are organization-defined roles assigned to individuals that allow those individuals to perform certain security-relevant functions that ordinary users are not authorized to perform. Privileged roles include key management, account management, database administration, system and network administration, and web administration. A role-based access scheme organizes permitted system access and privileges into roles. In contrast, an attribute-based access scheme specifies allowed system access and privileges based on attributes.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

<!-- Add implementation prose for the main This System component for control: ac-2.7 -->

#### Implementation Status: planned

______________________________________________________________________
