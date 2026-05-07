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
  sort-id: ia-02.05
---

# ia-2.5 - \[Identification and Authentication\] Individual Authentication with Group Authentication

## Control Statement

When shared accounts or authenticators are employed, require users to be individually authenticated before granting access to the shared accounts or resources.

## Control Assessment Objective

users are required to be individually authenticated before granting access to the shared accounts or resources when shared accounts or authenticators are employed.

## Control guidance

Individual authentication prior to shared group authentication mitigates the risk of using group accounts or authenticators.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

<!-- Add implementation prose for the main This System component for control: ia-2.5 -->

#### Implementation Status: planned

______________________________________________________________________
