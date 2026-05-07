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
  cm-03_odp.01:
    alt-identifier: cm-3_prm_1
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  cm-03_odp.02:
    alt-identifier: cm-3_prm_2
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  cm-03_odp.03:
    alt-identifier: cm-3_prm_3
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  cm-03_odp.04:
    alt-identifier: cm-3_prm_4
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  cm-03_odp.05:
    alt-identifier: cm-3_prm_5
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
x-trestle-global:
  profile:
    title: FedRAMP Moderate Baseline (NIST 800-53 Rev5)
    href: trestle://profiles/FedRAMP-Rev5-Moderate/profile.json
  sort-id: cm-03
---

# cm-3 - \[Configuration Management\] Configuration Change Control

## Control Statement

- \[a.\] Determine and document the types of changes to the system that are configuration-controlled;

- \[b.\] Review proposed configuration-controlled changes to the system and approve or disapprove such changes with explicit consideration for security and privacy impact analyses;

- \[c.\] Document configuration change decisions associated with the system;

- \[d.\] Implement approved configuration-controlled changes to the system;

- \[e.\] Retain records of configuration-controlled changes to the system for [time period];

- \[f.\] Monitor and review activities associated with configuration-controlled changes to the system; and

- \[g.\] Coordinate and provide oversight for configuration change control activities through [configuration change control element] that convenes [Selection (one or more): [frequency]; when [configuration change conditions]].

## Control Assessment Objective

- \[CM-03a.\] the types of changes to the system that are configuration-controlled are determined and documented;

- \[CM-03b.\]

  - \[CM-03b.[01]\] proposed configuration-controlled changes to the system are reviewed;
  - \[CM-03b.[02]\] proposed configuration-controlled changes to the system are approved or disapproved with explicit consideration for security and privacy impact analyses;

- \[CM-03c.\] configuration change decisions associated with the system are documented;

- \[CM-03d.\] approved configuration-controlled changes to the system are implemented;

- \[CM-03e.\] records of configuration-controlled changes to the system are retained for [time period];

- \[CM-03f.\]

  - \[CM-03f.[01]\] activities associated with configuration-controlled changes to the system are monitored;
  - \[CM-03f.[02]\] activities associated with configuration-controlled changes to the system are reviewed;

- \[CM-03g.\]

  - \[CM-03g.[01]\] configuration change control activities are coordinated and overseen by [configuration change control element];
  - \[CM-03g.[02]\] the configuration control element convenes [Selection (one or more): [frequency]; when [configuration change conditions]].

## Control guidance

Configuration change control for organizational systems involves the systematic proposal, justification, implementation, testing, review, and disposition of system changes, including system upgrades and modifications. Configuration change control includes changes to baseline configurations, configuration items of systems, operational procedures, configuration settings for system components, remediate vulnerabilities, and unscheduled or unauthorized changes. Processes for managing configuration changes to systems include Configuration Control Boards or Change Advisory Boards that review and approve proposed changes. For changes that impact privacy risk, the senior agency official for privacy updates privacy impact assessments and system of records notices. For new systems or major upgrades, organizations consider including representatives from the development organizations on the Configuration Control Boards or Change Advisory Boards. Auditing of changes includes activities before and after changes are made to systems and the auditing activities required to implement such changes. See also [SA-10](#sa-10).

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

<!-- Add implementation prose for the main This System component for control: cm-3 -->

#### Implementation Status: planned

______________________________________________________________________
