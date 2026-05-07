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
  mp-5_prm_2:
    values:
      - 'prior to leaving secure/controlled environment: for digital media, encryption
        in compliance with Federal requirements and utilizes FIPS validated or NSA
        approved cryptography (see SC-13.); for non-digital media, secured in locked
        container'
    aggregates:
      - mp-05_odp.02
      - mp-05_odp.03
  mp-05_odp.01:
    guidelines:
      - prose: types of system media to protect and control during transport 
          outside of controlled areas are defined;
    values:
      - all media with sensitive information
    alt-identifier: mp-5_prm_1
    profile-param-value-origin: <REPLACE_ME>
  mp-05_odp.02:
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  mp-05_odp.03:
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
x-trestle-global:
  profile:
    title: FedRAMP Moderate Baseline (NIST 800-53 Rev5)
    href: trestle://profiles/FedRAMP-Rev5-Moderate/profile.json
  sort-id: mp-05
---

# mp-5 - \[Media Protection\] Media Transport

## Control Statement

- \[a.\] Protect and control [all media with sensitive information] during transport outside of controlled areas using [prior to leaving secure/controlled environment: for digital media, encryption in compliance with Federal requirements and utilizes FIPS validated or NSA approved cryptography (see SC-13.); for non-digital media, secured in locked container];

- \[b.\] Maintain accountability for system media during transport outside of controlled areas;

- \[c.\] Document activities associated with the transport of system media; and

- \[d.\] Restrict the activities associated with the transport of system media to authorized personnel.

## Control Assessment Objective

- \[MP-05a.\]

  - \[MP-05a.[01]\] [all media with sensitive information] are protected during transport outside of controlled areas using [controls];
  - \[MP-05a.[02]\] [all media with sensitive information] are controlled during transport outside of controlled areas using [controls];

- \[MP-05b.\] accountability for system media is maintained during transport outside of controlled areas;

- \[MP-05c.\] activities associated with the transport of system media are documented;

- \[MP-05d.\]

  - \[MP-05d.[01]\] personnel authorized to conduct media transport activities is/are identified;
  - \[MP-05d.[02]\] activities associated with the transport of system media are restricted to identified authorized personnel.

## Control guidance

System media includes digital and non-digital media. Digital media includes flash drives, diskettes, magnetic tapes, external or removable hard disk drives (e.g., solid state and magnetic), compact discs, and digital versatile discs. Non-digital media includes microfilm and paper. Controlled areas are spaces for which organizations provide physical or procedural controls to meet requirements established for protecting information and systems. Controls to protect media during transport include cryptography and locked containers. Cryptographic mechanisms can provide confidentiality and integrity protections depending on the mechanisms implemented. Activities associated with media transport include releasing media for transport, ensuring that media enters the appropriate transport processes, and the actual transport. Authorized transport and courier personnel may include individuals external to the organization. Maintaining accountability of media during transport includes restricting transport activities to authorized personnel and tracking and/or obtaining records of transport activities as the media moves through the transportation system to prevent and detect loss, destruction, or tampering. Organizations establish documentation requirements for activities associated with the transport of system media in accordance with organizational assessments of risk. Organizations maintain the flexibility to define record-keeping methods for the different types of media transport as part of a system of transport-related records.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

<!-- Add implementation prose for the main This System component for control: mp-5 -->

#### Implementation Status: planned

______________________________________________________________________
