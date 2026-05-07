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
  si-4.4_prm_1:
    values:
      - continuously
    aggregates:
      - si-04.04_odp.01
      - si-04.04_odp.03
  si-4.4_prm_2:
    aggregates:
      - si-04.04_odp.02
      - si-04.04_odp.04
    profile-param-value-origin: <REPLACE_ME>
  si-04.04_odp.01:
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  si-04.04_odp.02:
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  si-04.04_odp.03:
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  si-04.04_odp.04:
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
x-trestle-global:
  profile:
    title: FedRAMP Moderate Baseline (NIST 800-53 Rev5)
    href: trestle://profiles/FedRAMP-Rev5-Moderate/profile.json
  sort-id: si-04.04
---

# si-4.4 - \[System and Information Integrity\] Inbound and Outbound Communications Traffic

## Control Statement

- \[(a)\] Determine criteria for unusual or unauthorized activities or conditions for inbound and outbound communications traffic;

- \[(b)\] Monitor inbound and outbound communications traffic [continuously] for [organization-defined unusual or unauthorized activities or conditions].

## Control Assessment Objective

- \[SI-04(04)(a)\]

  - \[SI-04(04)(a)[01]\] criteria for unusual or unauthorized activities or conditions for inbound communications traffic are defined;
  - \[SI-04(04)(a)[02]\] criteria for unusual or unauthorized activities or conditions for outbound communications traffic are defined;

- \[SI-04(04)(b)\]

  - \[SI-04(04)(b)[01]\] inbound communications traffic is monitored [frequency] for [unusual or unauthorized activities or conditions];
  - \[SI-04(04)(b)[02]\] outbound communications traffic is monitored [frequency] for [unusual or unauthorized activities or conditions].

## Control guidance

Unusual or unauthorized activities or conditions related to system inbound and outbound communications traffic includes internal traffic that indicates the presence of malicious code or unauthorized use of legitimate code or credentials within organizational systems or propagating among system components, signaling to external systems, and the unauthorized exporting of information. Evidence of malicious code or unauthorized use of legitimate code or credentials is used to identify potentially compromised systems or system components.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

<!-- Add implementation prose for the main This System component for control: si-4.4 -->

#### Implementation Status: planned

______________________________________________________________________
