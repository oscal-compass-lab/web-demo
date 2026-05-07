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
  cm-5.5_prm_1:
    values:
      - at least quarterly
    aggregates:
      - cm-05.05_odp.01
      - cm-05.05_odp.02
  cm-05.05_odp.01:
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  cm-05.05_odp.02:
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
x-trestle-global:
  profile:
    title: FedRAMP Moderate Baseline (NIST 800-53 Rev5)
    href: trestle://profiles/FedRAMP-Rev5-Moderate/profile.json
  sort-id: cm-05.05
---

# cm-5.5 - \[Configuration Management\] Privilege Limitation for Production and Operation

## Control Statement

- \[(a)\] Limit privileges to change system components and system-related information within a production or operational environment; and

- \[(b)\] Review and reevaluate privileges [at least quarterly].

## Control Assessment Objective

- \[CM-05(05)(a)\]

  - \[CM-05(05)(a)[01]\] privileges to change system components within a production or operational environment are limited;
  - \[CM-05(05)(a)[02]\] privileges to change system-related information within a production or operational environment are limited;

- \[CM-05(05)(b)\]

  - \[CM-05(05)(b)[01]\] privileges are reviewed [frequency];
  - \[CM-05(05)(b)[02]\] privileges are reevaluated [frequency].

## Control guidance

In many organizations, systems support multiple mission and business functions. Limiting privileges to change system components with respect to operational systems is necessary because changes to a system component may have far-reaching effects on mission and business processes supported by the system. The relationships between systems and mission/business processes are, in some cases, unknown to developers. System-related information includes operational procedures.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

<!-- Add implementation prose for the main This System component for control: cm-5.5 -->

#### Implementation Status: planned

______________________________________________________________________
