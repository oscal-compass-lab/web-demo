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
  ac-02.12_odp.01:
    alt-identifier: ac-2.12_prm_1
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  ac-02.12_odp.02:
    guidelines:
      - prose: personnel or roles to report atypical usage is/are defined;
    values:
      - at a minimum, the ISSO and/or similar role within the organization
    alt-identifier: ac-2.12_prm_2
    profile-param-value-origin: <REPLACE_ME>
x-trestle-global:
  profile:
    title: FedRAMP Moderate Baseline (NIST 800-53 Rev5)
    href: trestle://profiles/FedRAMP-Rev5-Moderate/profile.json
  sort-id: ac-02.12
---

# ac-2.12 - \[Access Control\] Account Monitoring for Atypical Usage

## Control Statement

- \[(a)\] Monitor system accounts for [atypical usage] ; and

- \[(b)\] Report atypical usage of system accounts to [at a minimum, the ISSO and/or similar role within the organization].

## Control Assessment Objective

- \[AC-02(12)(a)\] system accounts are monitored for [atypical usage];

- \[AC-02(12)(b)\] atypical usage of system accounts is reported to [at a minimum, the ISSO and/or similar role within the organization].

## Control guidance

Atypical usage includes accessing systems at certain times of the day or from locations that are not consistent with the normal usage patterns of individuals. Monitoring for atypical usage may reveal rogue behavior by individuals or an attack in progress. Account monitoring may inadvertently create privacy risks since data collected to identify atypical usage may reveal previously unknown information about the behavior of individuals. Organizations assess and document privacy risks from monitoring accounts for atypical usage in their privacy impact assessment and make determinations that are in alignment with their privacy program plan.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

<!-- Add implementation prose for the main This System component for control: ac-2.12 -->

#### Implementation Status: planned

______________________________________________________________________
