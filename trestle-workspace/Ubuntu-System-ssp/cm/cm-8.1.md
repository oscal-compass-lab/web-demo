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
  sort-id: cm-08.01
---

# cm-8.1 - \[Configuration Management\] Updates During Installation and Removal

## Control Statement

Update the inventory of system components as part of component installations, removals, and system updates.

## Control Assessment Objective

- \[CM-08(01)[01]\] the inventory of system components is updated as part of component installations;

- \[CM-08(01)[02]\] the inventory of system components is updated as part of component removals;

- \[CM-08(01)[03]\] the inventory of system components is updated as part of system updates.

## Control guidance

Organizations can improve the accuracy, completeness, and consistency of system component inventories if the inventories are updated as part of component installations or removals or during general system updates. If inventories are not updated at these key times, there is a greater likelihood that the information will not be appropriately captured and documented. System updates include hardware, software, and firmware components.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

<!-- Add implementation prose for the main This System component for control: cm-8.1 -->

#### Implementation Status: planned

______________________________________________________________________
