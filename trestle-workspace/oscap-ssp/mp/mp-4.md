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
  mp-4_prm_1:
    values:
      - all types of digital and non-digital media with sensitive information
    aggregates:
      - mp-04_odp.01
      - mp-04_odp.02
      - mp-04_odp.03
      - mp-04_odp.04
  mp-4_prm_2:
    values:
      - see additional FedRAMP requirements and guidance
    aggregates:
      - mp-04_odp.05
      - mp-04_odp.06
  mp-04_odp.01:
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  mp-04_odp.02:
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  mp-04_odp.03:
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  mp-04_odp.04:
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  mp-04_odp.05:
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  mp-04_odp.06:
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
x-trestle-global:
  profile:
    title: FedRAMP Moderate Baseline (NIST 800-53 Rev5)
    href: trestle://profiles/FedRAMP-Rev5-Moderate/profile.json
  sort-id: mp-04
---

# mp-4 - \[Media Protection\] Media Storage

## Control Statement

- \[a.\] Physically control and securely store [all types of digital and non-digital media with sensitive information] within [see additional FedRAMP requirements and guidance] ; and

- \[b.\] Protect system media types defined in MP-4a until the media are destroyed or sanitized using approved equipment, techniques, and procedures.

## Control Assessment Objective

- \[MP-04a.\]

  - \[MP-04a.[01]\] [types of digital media] are physically controlled;
  - \[MP-04a.[02]\] [types of non-digital media] are physically controlled;
  - \[MP-04a.[03]\] [types of digital media] are securely stored within [controlled areas];
  - \[MP-04a.[04]\] [types of non-digital media] are securely stored within [controlled areas];

- \[MP-04b.\] system media types (defined in MP-04_ODP[01], MP-04_ODP[02], MP-04_ODP[03], MP-04_ODP[04]) are protected until the media are destroyed or sanitized using approved equipment, techniques, and procedures.

## Control guidance

System media includes digital and non-digital media. Digital media includes flash drives, diskettes, magnetic tapes, external or removable hard disk drives (e.g., solid state, magnetic), compact discs, and digital versatile discs. Non-digital media includes paper and microfilm. Physically controlling stored media includes conducting inventories, ensuring procedures are in place to allow individuals to check out and return media to the library, and maintaining accountability for stored media. Secure storage includes a locked drawer, desk, or cabinet or a controlled media library. The type of media storage is commensurate with the security category or classification of the information on the media. Controlled areas are spaces that provide physical and procedural controls to meet the requirements established for protecting information and systems. Fewer controls may be needed for media that contains information determined to be in the public domain, publicly releasable, or have limited adverse impacts on organizations, operations, or individuals if accessed by other than authorized personnel. In these situations, physical access controls provide adequate protection.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

<!-- Add implementation prose for the main This System component for control: mp-4 -->

#### Implementation Status: planned

______________________________________________________________________
