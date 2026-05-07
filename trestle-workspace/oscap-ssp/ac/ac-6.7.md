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
  ac-06.07_odp.01:
    guidelines:
      - prose: the frequency at which to review the privileges assigned to roles
          or classes of users is defined;
    values:
      - at a minimum, annually
    alt-identifier: ac-6.7_prm_1
    profile-param-value-origin: <REPLACE_ME>
  ac-06.07_odp.02:
    guidelines:
      - prose: roles or classes of users to which privileges are assigned are 
          defined;
    values:
      - all users with privileges
    alt-identifier: ac-6.7_prm_2
    profile-param-value-origin: <REPLACE_ME>
x-trestle-global:
  profile:
    title: FedRAMP Moderate Baseline (NIST 800-53 Rev5)
    href: trestle://profiles/FedRAMP-Rev5-Moderate/profile.json
  sort-id: ac-06.07
---

# ac-6.7 - \[Access Control\] Review of User Privileges

## Control Statement

- \[(a)\] Review [at a minimum, annually] the privileges assigned to [all users with privileges] to validate the need for such privileges; and

- \[(b)\] Reassign or remove privileges, if necessary, to correctly reflect organizational mission and business needs.

## Control Assessment Objective

- \[AC-06(07)(a)\] privileges assigned to [all users with privileges] are reviewed [at a minimum, annually] to validate the need for such privileges;

- \[AC-06(07)(b)\] privileges are reassigned or removed, if necessary, to correctly reflect organizational mission and business needs.

## Control guidance

The need for certain assigned user privileges may change over time to reflect changes in organizational mission and business functions, environments of operation, technologies, or threats. A periodic review of assigned user privileges is necessary to determine if the rationale for assigning such privileges remains valid. If the need cannot be revalidated, organizations take appropriate corrective actions.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

<!-- Add implementation prose for the main This System component for control: ac-6.7 -->

#### Implementation Status: planned

______________________________________________________________________
