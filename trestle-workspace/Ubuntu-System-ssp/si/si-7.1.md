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
  si-7.1_prm_1:
    values:
      - selection to include security relevant events
      - at least monthly
    aggregates:
      - si-07.01_odp.01
      - si-07.01_odp.05
      - si-07.01_odp.09
  si-7.1_prm_2:
    aggregates:
      - si-07.01_odp.02
      - si-07.01_odp.06
      - si-07.01_odp.10
    profile-param-value-origin: <REPLACE_ME>
  si-7.1_prm_3:
    aggregates:
      - si-07.01_odp.03
      - si-07.01_odp.07
      - si-07.01_odp.11
    profile-param-value-origin: <REPLACE_ME>
  si-7.1_prm_4:
    aggregates:
      - si-07.01_odp.04
      - si-07.01_odp.08
      - si-07.01_odp.12
    profile-param-value-origin: <REPLACE_ME>
  si-07.01_odp.01:
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  si-07.01_odp.02:
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  si-07.01_odp.03:
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  si-07.01_odp.04:
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  si-07.01_odp.05:
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  si-07.01_odp.06:
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  si-07.01_odp.07:
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  si-07.01_odp.08:
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  si-07.01_odp.09:
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  si-07.01_odp.10:
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  si-07.01_odp.11:
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  si-07.01_odp.12:
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
x-trestle-global:
  profile:
    title: FedRAMP Moderate Baseline (NIST 800-53 Rev5)
    href: trestle://profiles/FedRAMP-Rev5-Moderate/profile.json
  sort-id: si-07.01
---

# si-7.1 - \[System and Information Integrity\] Integrity Checks

## Control Statement

Perform an integrity check of [selection to include security relevant events, at least monthly] [Selection (one or more): at startup; at [organization-defined transitional states or security-relevant events] ; [organization-defined frequency] ].

## Control Assessment Objective

- \[SI-07(01)[01]\] an integrity check of [software] is performed [Selection (one or more): at startup; at [transitional states or security-relevant events] ; [frequency] ];

- \[SI-07(01)[02]\] an integrity check of [firmware] is performed [Selection (one or more): at startup; at [transitional states or security-relevant events] ; [frequency] ];

- \[SI-07(01)[03]\] an integrity check of [information] is performed [Selection (one or more): at startup; at [transitional states or security-relevant events] ; [frequency] ].

## Control guidance

Security-relevant events include the identification of new threats to which organizational systems are susceptible and the installation of new hardware, software, or firmware. Transitional states include system startup, restart, shutdown, and abort.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

<!-- Add implementation prose for the main This System component for control: si-7.1 -->

#### Implementation Status: planned

______________________________________________________________________
