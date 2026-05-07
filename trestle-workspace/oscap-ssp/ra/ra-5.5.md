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
  ra-05.05_odp.01:
    guidelines:
      - prose: system components to which privileged access is authorized for 
          selected vulnerability scanning activities are defined;
    values:
      - all components that support authentication
      - all scans
    alt-identifier: ra-5.5_prm_1
    profile-param-value-origin: <REPLACE_ME>
  ra-05.05_odp.02:
    alt-identifier: ra-5.5_prm_2
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
x-trestle-global:
  profile:
    title: FedRAMP Moderate Baseline (NIST 800-53 Rev5)
    href: trestle://profiles/FedRAMP-Rev5-Moderate/profile.json
  sort-id: ra-05.05
---

# ra-5.5 - \[Risk Assessment\] Privileged Access

## Control Statement

Implement privileged access authorization to [all components that support authentication, all scans] for [vulnerability scanning activities].

## Control Assessment Objective

privileged access authorization is implemented to [all components that support authentication, all scans] for [vulnerability scanning activities].

## Control guidance

In certain situations, the nature of the vulnerability scanning may be more intrusive, or the system component that is the subject of the scanning may contain classified or controlled unclassified information, such as personally identifiable information. Privileged access authorization to selected system components facilitates more thorough vulnerability scanning and protects the sensitive nature of such scanning.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

<!-- Add implementation prose for the main This System component for control: ra-5.5 -->

#### Implementation Status: planned

______________________________________________________________________
