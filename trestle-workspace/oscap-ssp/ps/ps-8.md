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
  ps-08_odp.01:
    guidelines:
      - prose: personnel or roles to be notified when a formal employee 
          sanctions process is initiated is/are defined;
    values:
      - to include the ISSO and/or similar role within the organization
    alt-identifier: ps-8_prm_1
    profile-param-value-origin: <REPLACE_ME>
  ps-08_odp.02:
    guidelines:
      - prose: the time period within which organization-defined personnel or 
          roles must be notified when a formal employee sanctions process is 
          initiated is defined;
    values:
      - 24 hours
    alt-identifier: ps-8_prm_2
    profile-param-value-origin: <REPLACE_ME>
x-trestle-global:
  profile:
    title: FedRAMP Moderate Baseline (NIST 800-53 Rev5)
    href: trestle://profiles/FedRAMP-Rev5-Moderate/profile.json
  sort-id: ps-08
---

# ps-8 - \[Personnel Security\] Personnel Sanctions

## Control Statement

- \[a.\] Employ a formal sanctions process for individuals failing to comply with established information security and privacy policies and procedures; and

- \[b.\] Notify [to include the ISSO and/or similar role within the organization] within [24 hours] when a formal employee sanctions process is initiated, identifying the individual sanctioned and the reason for the sanction.

## Control Assessment Objective

- \[PS-08a.\] a formal sanctions process is employed for individuals failing to comply with established information security and privacy policies and procedures;

- \[PS-08b.\] [to include the ISSO and/or similar role within the organization] is/are notified within [24 hours] when a formal employee sanctions process is initiated, identifying the individual sanctioned and the reason for the sanction.

## Control guidance

Organizational sanctions reflect applicable laws, executive orders, directives, regulations, policies, standards, and guidelines. Sanctions processes are described in access agreements and can be included as part of general personnel policies for organizations and/or specified in security and privacy policies. Organizations consult with the Office of the General Counsel regarding matters of employee sanctions.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

<!-- Add implementation prose for the main This System component for control: ps-8 -->

#### Implementation Status: planned

______________________________________________________________________
