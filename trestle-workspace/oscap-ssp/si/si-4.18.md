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
  si-04.18_odp:
    alt-identifier: si-4.18_prm_1
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
x-trestle-global:
  profile:
    title: FedRAMP Moderate Baseline (NIST 800-53 Rev5)
    href: trestle://profiles/FedRAMP-Rev5-Moderate/profile.json
  sort-id: si-04.18
---

# si-4.18 - \[System and Information Integrity\] Analyze Traffic and Covert Exfiltration

## Control Statement

Analyze outbound communications traffic at external interfaces to the system and at the following interior points to detect covert exfiltration of information: [interior points].

## Control Assessment Objective

- \[SI-04(18)[01]\] outbound communications traffic is analyzed at interfaces external to the system to detect covert exfiltration of information;

- \[SI-04(18)[02]\] outbound communications traffic is analyzed at [interior points] to detect covert exfiltration of information.

## Control guidance

Organization-defined interior points include subnetworks and subsystems. Covert means that can be used to exfiltrate information include steganography.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

<!-- Add implementation prose for the main This System component for control: si-4.18 -->

#### Implementation Status: planned

______________________________________________________________________
