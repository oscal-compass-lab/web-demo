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
  mp-03_odp.01:
    guidelines:
      - prose: types of system media exempt from marking when remaining in 
          controlled areas are defined;
    values:
      - no removable media types
    alt-identifier: mp-3_prm_1
    profile-param-value-origin: <REPLACE_ME>
  mp-03_odp.02:
    guidelines:
      - prose: controlled areas where media is exempt from marking are defined;
    values:
      - organization-defined security safeguards not applicable
    alt-identifier: mp-3_prm_2
    profile-param-value-origin: <REPLACE_ME>
x-trestle-global:
  profile:
    title: FedRAMP Moderate Baseline (NIST 800-53 Rev5)
    href: trestle://profiles/FedRAMP-Rev5-Moderate/profile.json
  sort-id: mp-03
---

# mp-3 - \[Media Protection\] Media Marking

## Control Statement

- \[a.\] Mark system media indicating the distribution limitations, handling caveats, and applicable security markings (if any) of the information; and

- \[b.\] Exempt [no removable media types] from marking if the media remain within [organization-defined security safeguards not applicable].

## Control Assessment Objective

- \[MP-03a.\] system media is marked to indicate distribution limitations, handling caveats, and applicable security markings (if any) of the information;

- \[MP-03b.\] [no removable media types] remain within [organization-defined security safeguards not applicable].

## Control guidance

Security marking refers to the application or use of human-readable security attributes. Digital media includes diskettes, magnetic tapes, external or removable hard disk drives (e.g., solid state, magnetic), flash drives, compact discs, and digital versatile discs. Non-digital media includes paper and microfilm. Controlled unclassified information is defined by the National Archives and Records Administration along with the appropriate safeguarding and dissemination requirements for such information and is codified in [32 CFR 2002](#91f992fb-f668-4c91-a50f-0f05b95ccee3) . Security markings are generally not required for media that contains information determined by organizations to be in the public domain or to be publicly releasable. Some organizations may require markings for public information indicating that the information is publicly releasable. System media marking reflects applicable laws, executive orders, directives, policies, regulations, standards, and guidelines.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

<!-- Add implementation prose for the main This System component for control: mp-3 -->

#### Implementation Status: planned

______________________________________________________________________
