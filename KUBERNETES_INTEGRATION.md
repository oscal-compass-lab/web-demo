# Kubernetes Cluster Integration

This document describes the integration of a synthesized Kubernetes cluster into the OSCAL compliance demonstration system.

## Overview

We've added a 4-node Kubernetes cluster (1 control plane + 3 workers) to complement the existing 6 Ubuntu servers, creating a comprehensive multi-platform compliance demonstration.

## Components Added

### 1. Kubernetes Cluster Configuration (`server_config.py`)

Added 4 Kubernetes nodes with the following characteristics:

- **k8s-control-01**: Control plane node (92% compliance)
  - IP: 192.168.2.101
  - Kubernetes version: 1.28.0
  - Role: control-plane

- **k8s-worker-01**: Worker node (88% compliance)
  - IP: 192.168.2.102
  - Kubernetes version: 1.28.0
  - Role: worker

- **k8s-worker-02**: Worker node (85% compliance)
  - IP: 192.168.2.103
  - Kubernetes version: 1.28.0
  - Role: worker

- **k8s-worker-03**: Worker node (90% compliance)
  - IP: 192.168.2.104
  - Kubernetes version: 1.28.0
  - Role: worker

### 2. Kubernetes Component Definition

Created `source-data/component-definitions/Kubernetes_1_28/component-definition.json` with:

- **Software Component**: Kubernetes 1.28 platform
- **Validation Component**: kube-bench (CIS Kubernetes Benchmark validator)
- **61 Security Rules** covering:
  - API Server configuration (32 rules)
  - Scheduler configuration (2 rules)
  - Controller Manager configuration (7 rules)
  - Worker Node/Kubelet configuration (11 rules)
  - etcd configuration (7 rules)
  - Network and Pod Security Policies (2 rules)

### 3. XCCDF Results Generation

Updated `python/create_xccdf_results.py` to:
- Generate kube-bench XCCDF scan results for all K8s nodes
- Use CIS Kubernetes Benchmark format
- Include node-specific metadata (K8s version, node type)
- Apply compliance rates per node configuration
- Force specific rules to fail for demonstration purposes

### 4. System Security Plans (SSPs)

Updated `python/create_ssps.py` to:
- Create separate SSPs for Kubernetes cluster (suffix: `-k8s`)
- Support both Ubuntu and Kubernetes inventory items
- Generate 4 Kubernetes SSPs (one per profile):
  - `Ubuntu-System-ssp-fedramp-low-k8s`
  - `Ubuntu-System-ssp-fedramp-moderate-k8s`
  - `Ubuntu-System-ssp-fedramp-high-k8s`
  - `Ubuntu-System-ssp-dora-k8s`

### 5. Assessment Plans, Results, POA&Ms, and Charts

Updated the following scripts to handle both Ubuntu and Kubernetes generically:
- `python/create_assessment_plans.py` - Creates assessment plans for all SSPs
- `python/create_assessment_results.py` - Processes all XCCDF results
- `python/create_poams.py` - Generates POA&Ms from all assessment results
- `python/create_assessment_result_charts.py` - Creates charts for all results

## Total Inventory

The system now includes:

- **6 Ubuntu 24.04 LTS servers** (web, database, application, management)
- **4 Kubernetes 1.28 nodes** (1 control plane, 3 workers)
- **Total: 10 inventory items**

## OSCAL Documents Generated

For each of the 4 profiles (FedRAMP Low/Moderate/High, DORA):

### Ubuntu Fleet:
- 1 SSP (System Security Plan)
- 1 AP (Assessment Plan)
- 1 AR (Assessment Results)
- 1 POA&M (Plan of Action and Milestones)

### Kubernetes Cluster:
- 1 SSP (System Security Plan)
- 1 AP (Assessment Plan)
- 1 AR (Assessment Results)
- 1 POA&M (Plan of Action and Milestones)

**Total: 32 OSCAL documents** (8 per profile × 4 profiles)

## Security Rules

- **Ubuntu servers**: 187 OSCAP rules (OpenSCAP)
- **Kubernetes nodes**: 61 kube-bench rules (CIS Kubernetes Benchmark)
- **Total: 248 unique security rules**

## Usage

Generate all artifacts including Kubernetes:

```bash
make artifacts
```

This will:
1. Create XCCDF results for all 10 inventory items (6 Ubuntu + 4 K8s)
2. Generate component definitions for both platforms
3. Create SSPs for both Ubuntu and Kubernetes
4. Generate assessment plans, results, and POA&Ms
5. Create compliance charts

## File Structure

```
source-data/
├── component-definitions/
│   ├── Ubuntu_Linux_24_04_LTS/
│   │   └── component-definition.json
│   ├── Kubernetes_1_28/
│   │   └── component-definition.json
│   └── oscap/
│       └── component-definition.json
└── xccdf-results/
    ├── ubuntu-web-01-xccdf-results.xml
    ├── ubuntu-web-02-xccdf-results.xml
    ├── ubuntu-web-03-xccdf-results.xml
    ├── ubuntu-db-01-xccdf-results.xml
    ├── ubuntu-app-01-xccdf-results.xml
    ├── ubuntu-mgmt-01-xccdf-results.xml
    ├── k8s-control-01-xccdf-results.xml
    ├── k8s-worker-01-xccdf-results.xml
    ├── k8s-worker-02-xccdf-results.xml
    └── k8s-worker-03-xccdf-results.xml

trestle-workspace/
├── system-security-plans/
│   ├── Ubuntu-System-ssp-fedramp-low/
│   ├── Ubuntu-System-ssp-fedramp-moderate/
│   ├── Ubuntu-System-ssp-fedramp-high/
│   ├── Ubuntu-System-ssp-dora/
│   ├── Ubuntu-System-ssp-fedramp-low-k8s/
│   ├── Ubuntu-System-ssp-fedramp-moderate-k8s/
│   ├── Ubuntu-System-ssp-fedramp-high-k8s/
│   └── Ubuntu-System-ssp-dora-k8s/
├── assessment-plans/
│   └── (8 assessment plans)
├── assessment-results/
│   └── (8 assessment results)
└── plan-of-action-and-milestones/
    └── (8 POA&Ms)
```

## Key Features

1. **Multi-Platform Compliance**: Demonstrates compliance across different technology stacks
2. **Realistic Scenarios**: Different compliance rates per node/server
3. **Industry Standards**: Uses CIS Kubernetes Benchmark and OpenSCAP
4. **Complete OSCAL Workflow**: Full document lifecycle from component definitions to POA&Ms
5. **Regulatory Coverage**: FedRAMP (Low/Moderate/High) and EU DORA

## Technical Details

### Kubernetes Security Rules Categories

1. **API Server Security** (32 rules)
   - Authentication and authorization
   - Admission control plugins
   - Audit logging
   - TLS/encryption configuration

2. **Scheduler Security** (2 rules)
   - Profiling and bind address

3. **Controller Manager Security** (7 rules)
   - Service account management
   - Certificate rotation
   - Resource management

4. **Worker Node Security** (11 rules)
   - Kubelet configuration
   - Anonymous authentication
   - TLS certificates
   - Kernel defaults

5. **etcd Security** (7 rules)
   - Client authentication
   - Peer communication
   - Certificate management

6. **Network & Pod Security** (2 rules)
   - Network policies
   - Pod security policies

### XCCDF Format Differences

- **Ubuntu**: Uses OpenSCAP format with NIST references
- **Kubernetes**: Uses kube-bench format with CIS Benchmark references

Both formats are properly parsed and converted to OSCAL assessment results.

## Benefits

1. **Comprehensive Coverage**: Demonstrates compliance for both traditional VMs and container orchestration
2. **Real-World Relevance**: Kubernetes is widely used in modern cloud-native applications
3. **Regulatory Alignment**: Shows how different platforms map to the same regulatory requirements
4. **Scalability**: Easy to add more nodes or different Kubernetes versions

## Future Enhancements

Potential additions:
- Multiple Kubernetes clusters (dev, staging, prod)
- Different Kubernetes distributions (EKS, GKE, AKS, OpenShift)
- Container-specific security rules
- Service mesh security (Istio, Linkerd)
- Additional CIS Benchmark levels

---

**Made with Bob** - AI-assisted development