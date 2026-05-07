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
  cm-6.1_prm_2:
    aggregates:
      - cm-06.01_odp.02
      - cm-06.01_odp.03
      - cm-06.01_odp.04
    profile-param-value-origin: <REPLACE_ME>
  cm-06.01_odp.01:
    alt-identifier: cm-6.1_prm_1
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  cm-06.01_odp.02:
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  cm-06.01_odp.03:
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  cm-06.01_odp.04:
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
x-trestle-global:
  profile:
    title: FedRAMP Moderate Baseline (NIST 800-53 Rev5)
    href: trestle://profiles/FedRAMP-Rev5-Moderate/profile.json
  sort-id: cm-06.01
---

# cm-6.1 - \[Configuration Management\] Automated Management, Application, and Verification

## Control Statement

Manage, apply, and verify configuration settings for [system components] using [organization-defined automated mechanisms].

## Control Assessment Objective

- \[CM-06(01)[01]\] configuration settings for [system components] are managed using [automated mechanisms];

- \[CM-06(01)[02]\] configuration settings for [system components] are applied using [automated mechanisms];

- \[CM-06(01)[03]\] configuration settings for [system components] are verified using [automated mechanisms].

## Control guidance

Automated tools (e.g., hardening tools, baseline configuration tools) can improve the accuracy, consistency, and availability of configuration settings information. Automation can also provide data aggregation and data correlation capabilities, alerting mechanisms, and dashboards to support risk-based decision-making within the organization.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

<!-- Add implementation prose for the main This System component for control: cm-6.1 -->

#### Implementation Status: planned

______________________________________________________________________
