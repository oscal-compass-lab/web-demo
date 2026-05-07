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
  ma-05.01_odp:
    alt-identifier: ma-5.1_prm_1
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
x-trestle-global:
  profile:
    title: FedRAMP Moderate Baseline (NIST 800-53 Rev5)
    href: trestle://profiles/FedRAMP-Rev5-Moderate/profile.json
  sort-id: ma-05.01
---

# ma-5.1 - \[Maintenance\] Individuals Without Appropriate Access

## Control Statement

- \[(a)\] Implement procedures for the use of maintenance personnel that lack appropriate security clearances or are not U.S. citizens, that include the following requirements:

  - \[(1)\] Maintenance personnel who do not have needed access authorizations, clearances, or formal access approvals are escorted and supervised during the performance of maintenance and diagnostic activities on the system by approved organizational personnel who are fully cleared, have appropriate access authorizations, and are technically qualified; and
  - \[(2)\] Prior to initiating maintenance or diagnostic activities by personnel who do not have needed access authorizations, clearances or formal access approvals, all volatile information storage components within the system are sanitized and all nonvolatile storage media are removed or physically disconnected from the system and secured; and

- \[(b)\] Develop and implement [alternate controls] in the event a system component cannot be sanitized, removed, or disconnected from the system.

## Control Assessment Objective

- \[MA-05(01)(a)\]

  - \[MA-05(01)(a)(01)\] procedures for the use of maintenance personnel who lack appropriate security clearances or are not U.S. citizens are implemented and include approved organizational personnel who are fully cleared, have appropriate access authorizations, and are technically qualified escorting and supervising maintenance personnel without the needed access authorization during the performance of maintenance and diagnostic activities;
  - \[MA-05(01)(a)(02)\] procedures for the use of maintenance personnel who lack appropriate security clearances or are not U.S. citizens are implemented and include all volatile information storage components within the system being sanitized and all non-volatile storage media being removed or physically disconnected from the system and secured prior to initiating maintenance or diagnostic activities;

- \[MA-05(01)(b)\] [alternate controls] are developed and implemented in the event that a system cannot be sanitized, removed, or disconnected from the system.

## Control guidance

Procedures for individuals who lack appropriate security clearances or who are not U.S. citizens are intended to deny visual and electronic access to classified or controlled unclassified information contained on organizational systems. Procedures for the use of maintenance personnel can be documented in security plans for the systems.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

<!-- Add implementation prose for the main This System component for control: ma-5.1 -->

#### Implementation Status: planned

______________________________________________________________________
