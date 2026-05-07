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
  ia-02.06_odp.01:
    alt-identifier: ia-2.6_prm_1
    profile-param-value-origin: <REPLACE_ME>
  ia-02.06_odp.02:
    alt-identifier: ia-2.6_prm_2
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  ia-02.06_odp.03:
    guidelines:
      - prose: the strength of mechanism requirements to be enforced by a device
          separate from the system gaining access to accounts is defined;
    values:
      - FIPS-validated or NSA-approved cryptography
    alt-identifier: ia-2.6_prm_3
    profile-param-value-origin: <REPLACE_ME>
x-trestle-global:
  profile:
    title: FedRAMP Moderate Baseline (NIST 800-53 Rev5)
    href: trestle://profiles/FedRAMP-Rev5-Moderate/profile.json
  sort-id: ia-02.06
---

# ia-2.6 - \[Identification and Authentication\] Access to Accounts —separate Device

## Control Statement

Implement multi-factor authentication for [Selection (one or more): local; network; remote] access to [Selection (one or more): privileged accounts; non-privileged accounts] such that:

- \[(a)\] One of the factors is provided by a device separate from the system gaining access; and

- \[(b)\] The device meets [FIPS-validated or NSA-approved cryptography].

## Control Assessment Objective

- \[IA-02(06)(a)\] multi-factor authentication is implemented for [Selection (one or more): local; network; remote] access to [Selection (one or more): privileged accounts; non-privileged accounts] such that one of the factors is provided by a device separate from the system gaining access;

- \[IA-02(06)(b)\] multi-factor authentication is implemented for [Selection (one or more): local; network; remote] access to [Selection (one or more): privileged accounts; non-privileged accounts] such that the device meets [FIPS-validated or NSA-approved cryptography].

## Control guidance

The purpose of requiring a device that is separate from the system to which the user is attempting to gain access for one of the factors during multi-factor authentication is to reduce the likelihood of compromising authenticators or credentials stored on the system. Adversaries may be able to compromise such authenticators or credentials and subsequently impersonate authorized users. Implementing one of the factors on a separate device (e.g., a hardware token), provides a greater strength of mechanism and an increased level of assurance in the authentication process.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

<!-- Add implementation prose for the main This System component for control: ia-2.6 -->

#### Implementation Status: planned

______________________________________________________________________
