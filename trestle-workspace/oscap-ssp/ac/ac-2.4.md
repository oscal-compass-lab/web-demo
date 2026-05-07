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
  sort-id: ac-02.04
---

# ac-2.4 - \[Access Control\] Automated Audit Actions

## Control Statement

Automatically audit account creation, modification, enabling, disabling, and removal actions.

## Control Assessment Objective

- \[AC-02(04)[01]\] account creation is automatically audited;

- \[AC-02(04)[02]\] account modification is automatically audited;

- \[AC-02(04)[03]\] account enabling is automatically audited;

- \[AC-02(04)[04]\] account disabling is automatically audited;

- \[AC-02(04)[05]\] account removal actions are automatically audited.

## Control guidance

Account management audit records are defined in accordance with [AU-02](#au-2) and reviewed, analyzed, and reported in accordance with [AU-06](#au-6).

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

<!-- Add implementation prose for the main This System component for control: ac-2.4 -->

#### Implementation Status: planned

______________________________________________________________________
