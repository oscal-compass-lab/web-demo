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
  ma-03.03_odp:
    guidelines:
      - prose: personnel or roles who can authorize removal of equipment from 
          the facility is/are defined;
    values:
      - the information owner
    alt-identifier: ma-3.3_prm_1
    profile-param-value-origin: <REPLACE_ME>
x-trestle-global:
  profile:
    title: FedRAMP Moderate Baseline (NIST 800-53 Rev5)
    href: trestle://profiles/FedRAMP-Rev5-Moderate/profile.json
  sort-id: ma-03.03
---

# ma-3.3 - \[Maintenance\] Prevent Unauthorized Removal

## Control Statement

Prevent the removal of maintenance equipment containing organizational information by:

- \[(a)\] Verifying that there is no organizational information contained on the equipment;

- \[(b)\] Sanitizing or destroying the equipment;

- \[(c)\] Retaining the equipment within the facility; or

- \[(d)\] Obtaining an exemption from [the information owner] explicitly authorizing removal of the equipment from the facility.

## Control Assessment Objective

- \[MA-03(03)(a)\] the removal of maintenance equipment containing organizational information is prevented by verifying that there is no organizational information contained on the equipment; or

- \[MA-03(03)(b)\] the removal of maintenance equipment containing organizational information is prevented by sanitizing or destroying the equipment; or

- \[MA-03(03)(c)\] the removal of maintenance equipment containing organizational information is prevented by retaining the equipment within the facility; or

- \[MA-03(03)(d)\] the removal of maintenance equipment containing organizational information is prevented by obtaining an exemption from [the information owner] explicitly authorizing removal of the equipment from the facility.

## Control guidance

Organizational information includes all information owned by organizations and any information provided to organizations for which the organizations serve as information stewards.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

<!-- Add implementation prose for the main This System component for control: ma-3.3 -->

#### Implementation Status: planned

______________________________________________________________________
