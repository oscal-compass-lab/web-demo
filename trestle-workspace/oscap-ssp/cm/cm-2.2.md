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
  cm-02.02_odp:
    alt-identifier: cm-2.2_prm_1
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
x-trestle-global:
  profile:
    title: FedRAMP Moderate Baseline (NIST 800-53 Rev5)
    href: trestle://profiles/FedRAMP-Rev5-Moderate/profile.json
  sort-id: cm-02.02
---

# cm-2.2 - \[Configuration Management\] Automation Support for Accuracy and Currency

## Control Statement

Maintain the currency, completeness, accuracy, and availability of the baseline configuration of the system using [automated mechanisms].

## Control Assessment Objective

- \[CM-02(02)[01]\] the currency of the baseline configuration of the system is maintained using [automated mechanisms];

- \[CM-02(02)[02]\] the completeness of the baseline configuration of the system is maintained using [automated mechanisms];

- \[CM-02(02)[03]\] the accuracy of the baseline configuration of the system is maintained using [automated mechanisms];

- \[CM-02(02)[04]\] the availability of the baseline configuration of the system is maintained using [automated mechanisms].

## Control guidance

Automated mechanisms that help organizations maintain consistent baseline configurations for systems include configuration management tools, hardware, software, firmware inventory tools, and network management tools. Automated tools can be used at the organization level, mission and business process level, or system level on workstations, servers, notebook computers, network components, or mobile devices. Tools can be used to track version numbers on operating systems, applications, types of software installed, and current patch levels. Automation support for accuracy and currency can be satisfied by the implementation of [CM-8(2)](#cm-8.2) for organizations that combine system component inventory and baseline configuration activities.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

<!-- Add implementation prose for the main This System component for control: cm-2.2 -->

#### Implementation Status: planned

______________________________________________________________________
