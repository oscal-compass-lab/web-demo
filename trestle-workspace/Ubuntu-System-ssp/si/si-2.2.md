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
  si-02.02_odp.01:
    guidelines:
      - prose: automated mechanisms to determine if applicable security-relevant
          software and firmware updates are installed on system components are 
          defined;
    values:
      - at least monthly
    alt-identifier: si-2.2_prm_1
    profile-param-value-origin: <REPLACE_ME>
  si-02.02_odp.02:
    alt-identifier: si-2.2_prm_2
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
x-trestle-global:
  profile:
    title: FedRAMP Moderate Baseline (NIST 800-53 Rev5)
    href: trestle://profiles/FedRAMP-Rev5-Moderate/profile.json
  sort-id: si-02.02
---

# si-2.2 - \[System and Information Integrity\] Automated Flaw Remediation Status

## Control Statement

Determine if system components have applicable security-relevant software and firmware updates installed using [at least monthly] [frequency].

## Control Assessment Objective

system components have applicable security-relevant software and firmware updates installed [frequency] using [at least monthly].

## Control guidance

Automated mechanisms can track and determine the status of known flaws for system components.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

<!-- Add implementation prose for the main This System component for control: si-2.2 -->

#### Implementation Status: planned

______________________________________________________________________
