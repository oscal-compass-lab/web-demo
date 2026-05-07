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
  ca-02.03_odp.01:
    guidelines:
      - prose: external organization(s) from which the results of control 
          assessments are leveraged are defined;
    values:
      - any independent assessor
    alt-identifier: ca-2.3_prm_1
    profile-param-value-origin: <REPLACE_ME>
  ca-02.03_odp.02:
    alt-identifier: ca-2.3_prm_2
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  ca-02.03_odp.03:
    alt-identifier: ca-2.3_prm_3
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
x-trestle-global:
  profile:
    title: FedRAMP Moderate Baseline (NIST 800-53 Rev5)
    href: trestle://profiles/FedRAMP-Rev5-Moderate/profile.json
  sort-id: ca-02.03
---

# ca-2.3 - \[Assessment, Authorization, and Monitoring\] Leveraging Results from External Organizations

## Control Statement

Leverage the results of control assessments performed by [any independent assessor] on [system] when the assessment meets [requirements].

## Control Assessment Objective

the results of control assessments performed by [any independent assessor] on [system] are leveraged when the assessment meets [requirements].

## Control guidance

Organizations may rely on control assessments of organizational systems by other (external) organizations. Using such assessments and reusing existing assessment evidence can decrease the time and resources required for assessments by limiting the independent assessment activities that organizations need to perform. The factors that organizations consider in determining whether to accept assessment results from external organizations can vary. Such factors include the organization’s past experience with the organization that conducted the assessment, the reputation of the assessment organization, the level of detail of supporting assessment evidence provided, and mandates imposed by applicable laws, executive orders, directives, regulations, policies, standards, and guidelines. Accredited testing laboratories that support the Common Criteria Program [ISO 15408-1](#6afc1b04-c9d6-4023-adbc-f8fbe33a3c73) , the NIST Cryptographic Module Validation Program (CMVP), or the NIST Cryptographic Algorithm Validation Program (CAVP) can provide independent assessment results that organizations can leverage.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

<!-- Add implementation prose for the main This System component for control: ca-2.3 -->

#### Implementation Status: planned

______________________________________________________________________
