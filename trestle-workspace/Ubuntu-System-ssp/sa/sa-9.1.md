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
  sa-09.01_odp:
    alt-identifier: sa-9.1_prm_1
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
x-trestle-global:
  profile:
    title: FedRAMP Moderate Baseline (NIST 800-53 Rev5)
    href: trestle://profiles/FedRAMP-Rev5-Moderate/profile.json
  sort-id: sa-09.01
---

# sa-9.1 - \[System and Services Acquisition\] Risk Assessments and Organizational Approvals

## Control Statement

- \[(a)\] Conduct an organizational assessment of risk prior to the acquisition or outsourcing of information security services; and

- \[(b)\] Verify that the acquisition or outsourcing of dedicated information security services is approved by [personnel or roles].

## Control Assessment Objective

- \[SA-09(01)(a)\] an organizational assessment of risk is conducted prior to the acquisition or outsourcing of information security services;

- \[SA-09(01)(b)\] [personnel or roles] approve the acquisition or outsourcing of dedicated information security services.

## Control guidance

Information security services include the operation of security devices, such as firewalls or key management services as well as incident monitoring, analysis, and response. Risks assessed can include system, mission or business, security, privacy, or supply chain risks.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

<!-- Add implementation prose for the main This System component for control: sa-9.1 -->

#### Implementation Status: planned

______________________________________________________________________
