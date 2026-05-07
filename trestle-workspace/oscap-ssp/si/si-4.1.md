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
x-trestle-global:
  profile:
    title: FedRAMP Moderate Baseline (NIST 800-53 Rev5)
    href: trestle://profiles/FedRAMP-Rev5-Moderate/profile.json
  sort-id: si-04.01
---

# si-4.1 - \[System and Information Integrity\] System-wide Intrusion Detection System

## Control Statement

Connect and configure individual intrusion detection tools into a system-wide intrusion detection system.

## Control Assessment Objective

- \[SI-04(01)[01]\] individual intrusion detection tools are connected to a system-wide intrusion detection system;

- \[SI-04(01)[02]\] individual intrusion detection tools are configured into a system-wide intrusion detection system.

## Control guidance

Linking individual intrusion detection tools into a system-wide intrusion detection system provides additional coverage and effective detection capabilities. The information contained in one intrusion detection tool can be shared widely across the organization, making the system-wide detection capability more robust and powerful.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

<!-- Add implementation prose for the main This System component for control: si-4.1 -->

#### Implementation Status: planned

______________________________________________________________________
