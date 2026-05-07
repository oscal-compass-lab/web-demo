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
  ma-06_odp.01:
    guidelines:
      - prose: system components for which maintenance support and/or spare 
          parts are obtained are defined;
    values:
      - a timeframe to support advertised uptime and availability
    alt-identifier: ma-6_prm_1
    profile-param-value-origin: <REPLACE_ME>
  ma-06_odp.02:
    alt-identifier: ma-6_prm_2
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
x-trestle-global:
  profile:
    title: FedRAMP Moderate Baseline (NIST 800-53 Rev5)
    href: trestle://profiles/FedRAMP-Rev5-Moderate/profile.json
  sort-id: ma-06
---

# ma-6 - \[Maintenance\] Timely Maintenance

## Control Statement

Obtain maintenance support and/or spare parts for [a timeframe to support advertised uptime and availability] within [time period] of failure.

## Control Assessment Objective

maintenance support and/or spare parts are obtained for [a timeframe to support advertised uptime and availability] within [time period] of failure.

## Control guidance

Organizations specify the system components that result in increased risk to organizational operations and assets, individuals, other organizations, or the Nation when the functionality provided by those components is not operational. Organizational actions to obtain maintenance support include having appropriate contracts in place.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

<!-- Add implementation prose for the main This System component for control: ma-6 -->

#### Implementation Status: planned

______________________________________________________________________
