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
  ac-02.09_odp:
    guidelines:
      - prose: conditions for establishing shared and group accounts are 
          defined;
    values:
      - organization-defined need with justification statement that explains why
        such accounts are necessary
    alt-identifier: ac-2.9_prm_1
    profile-param-value-origin: <REPLACE_ME>
x-trestle-global:
  profile:
    title: FedRAMP Moderate Baseline (NIST 800-53 Rev5)
    href: trestle://profiles/FedRAMP-Rev5-Moderate/profile.json
  sort-id: ac-02.09
---

# ac-2.9 - \[Access Control\] Restrictions on Use of Shared and Group Accounts

## Control Statement

Only permit the use of shared and group accounts that meet [organization-defined need with justification statement that explains why such accounts are necessary].

## Control Assessment Objective

the use of shared and group accounts is only permitted if [organization-defined need with justification statement that explains why such accounts are necessary] are met.

## Control guidance

Before permitting the use of shared or group accounts, organizations consider the increased risk due to the lack of accountability with such accounts.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

<!-- Add implementation prose for the main This System component for control: ac-2.9 -->

#### Implementation Status: planned

______________________________________________________________________
