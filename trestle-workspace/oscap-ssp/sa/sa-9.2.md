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
  sa-09.02_odp:
    guidelines:
      - prose: external system services that require the identification of 
          functions, ports, protocols, and other services are defined;
    values:
      - all external systems where federal customer data is processed or stored
    alt-identifier: sa-9.2_prm_1
    profile-param-value-origin: <REPLACE_ME>
x-trestle-global:
  profile:
    title: FedRAMP Moderate Baseline (NIST 800-53 Rev5)
    href: trestle://profiles/FedRAMP-Rev5-Moderate/profile.json
  sort-id: sa-09.02
---

# sa-9.2 - \[System and Services Acquisition\] Identification of Functions, Ports, Protocols, and Services

## Control Statement

Require providers of the following external system services to identify the functions, ports, protocols, and other services required for the use of such services: [all external systems where federal customer data is processed or stored].

## Control Assessment Objective

providers of [all external systems where federal customer data is processed or stored] are required to identify the functions, ports, protocols, and other services required for the use of such services.

## Control guidance

Information from external service providers regarding the specific functions, ports, protocols, and services used in the provision of such services can be useful when the need arises to understand the trade-offs involved in restricting certain functions and services or blocking certain ports and protocols.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

<!-- Add implementation prose for the main This System component for control: sa-9.2 -->

#### Implementation Status: planned

______________________________________________________________________
