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
  ac-4.21_prm_1:
    aggregates:
      - ac-04.21_odp.01
      - ac-04.21_odp.02
    profile-param-value-origin: <REPLACE_ME>
  ac-04.21_odp.01:
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  ac-04.21_odp.02:
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  ac-04.21_odp.03:
    alt-identifier: ac-4.21_prm_2
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
x-trestle-global:
  profile:
    title: FedRAMP Moderate Baseline (NIST 800-53 Rev5)
    href: trestle://profiles/FedRAMP-Rev5-Moderate/profile.json
  sort-id: ac-04.21
---

# ac-4.21 - \[Access Control\] Physical or Logical Separation of Information Flows

## Control Statement

Separate information flows logically or physically using [organization-defined mechanisms and/or techniques] to accomplish [required separations].

## Control Assessment Objective

- \[AC-04(21)[01]\] information flows are separated logically using [mechanisms and/or techniques] to accomplish [required separations];

- \[AC-04(21)[02]\] information flows are separated physically using [mechanisms and/or techniques] to accomplish [required separations].

## Control guidance

Enforcing the separation of information flows associated with defined types of data can enhance protection by ensuring that information is not commingled while in transit and by enabling flow control by transmission paths that are not otherwise achievable. Types of separable information include inbound and outbound communications traffic, service requests and responses, and information of differing security impact or classification levels.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

<!-- Add implementation prose for the main This System component for control: ac-4.21 -->

#### Implementation Status: planned

______________________________________________________________________
