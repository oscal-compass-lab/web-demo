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
  cm-8.3_prm_1:
    values:
      - automated mechanisms with a maximum five-minute delay in detection.
    aggregates:
      - cm-08.03_odp.01
      - cm-08.03_odp.02
      - cm-08.03_odp.03
  cm-08.03_odp.01:
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  cm-08.03_odp.02:
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  cm-08.03_odp.03:
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  cm-08.03_odp.04:
    guidelines:
      - prose: frequency at which automated mechanisms are used to detect the 
          presence of unauthorized system components within the system is 
          defined;
    values:
      - continuously
    alt-identifier: cm-8.3_prm_2
    profile-param-value-origin: <REPLACE_ME>
  cm-08.03_odp.05:
    alt-identifier: cm-8.3_prm_3
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  cm-08.03_odp.06:
    alt-identifier: cm-8.3_prm_4
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
x-trestle-global:
  profile:
    title: FedRAMP Moderate Baseline (NIST 800-53 Rev5)
    href: trestle://profiles/FedRAMP-Rev5-Moderate/profile.json
  sort-id: cm-08.03
---

# cm-8.3 - \[Configuration Management\] Automated Unauthorized Component Detection

## Control Statement

- \[(a)\] Detect the presence of unauthorized hardware, software, and firmware components within the system using [automated mechanisms with a maximum five-minute delay in detection.] [continuously] ; and

- \[(b)\] Take the following actions when unauthorized components are detected: [Selection (one or more): disable network access by unauthorized components; isolate unauthorized components; notify [personnel or roles] ].

## Control Assessment Objective

- \[CM-08(03)(a)\]

  - \[CM-08(03)(a)[01]\] the presence of unauthorized hardware within the system is detected using [automated mechanisms] [continuously];
  - \[CM-08(03)(a)[02]\] the presence of unauthorized software within the system is detected using [automated mechanisms] [continuously];
  - \[CM-08(03)(a)[03]\] the presence of unauthorized firmware within the system is detected using [automated mechanisms] [continuously];

- \[CM-08(03)(b)\]

  - \[CM-08(03)(b)[01]\] [Selection (one or more): disable network access by unauthorized components; isolate unauthorized components; notify [personnel or roles] ] are taken when unauthorized hardware is detected;
  - \[CM-08(03)(b)[02]\] [Selection (one or more): disable network access by unauthorized components; isolate unauthorized components; notify [personnel or roles] ] are taken when unauthorized software is detected;
  - \[CM-08(03)(b)[03]\] [Selection (one or more): disable network access by unauthorized components; isolate unauthorized components; notify [personnel or roles] ] are taken when unauthorized firmware is detected.

## Control guidance

Automated unauthorized component detection is applied in addition to the monitoring for unauthorized remote connections and mobile devices. Monitoring for unauthorized system components may be accomplished on an ongoing basis or by the periodic scanning of systems for that purpose. Automated mechanisms may also be used to prevent the connection of unauthorized components (see [CM-7(9)](#cm-7.9) ). Automated mechanisms can be implemented in systems or in separate system components. When acquiring and implementing automated mechanisms, organizations consider whether such mechanisms depend on the ability of the system component to support an agent or supplicant in order to be detected since some types of components do not have or cannot support agents (e.g., IoT devices, sensors). Isolation can be achieved , for example, by placing unauthorized system components in separate domains or subnets or quarantining such components. This type of component isolation is commonly referred to as "sandboxing."

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

<!-- Add implementation prose for the main This System component for control: cm-8.3 -->

#### Implementation Status: planned

______________________________________________________________________
