# web-demo
web-demo

Presented are a complete set of OSCAL documents covering:

- 2 regulations: DORA and FedRAMP (Low, Moderate, and High levels)
- 10 inventory items:
  - 6 Ubuntu 24.04 LTS servers (web, database, application, management)
  - 4 Kubernetes 1.28 nodes (1 control plane, 3 workers)

The documents have been constructed using OSCAL Compass Compliance-trestle.

## Multi-Platform Compliance Demonstration

This project demonstrates comprehensive compliance across different technology stacks:

- **Ubuntu Servers**: OpenSCAP security compliance scanning (187 rules)
- **Kubernetes Cluster**: CIS Kubernetes Benchmark validation via kube-bench (61 rules)

### Total OSCAL Documents Generated

- **32 OSCAL documents** across 4 regulatory profiles
- **8 documents per profile** (SSP, AP, AR, POA&M for both Ubuntu and Kubernetes)
- **248 unique security rules** evaluated

See [KUBERNETES_INTEGRATION.md](KUBERNETES_INTEGRATION.md) for detailed information about the Kubernetes cluster integration.

## Quick Start

Generate all artifacts:

```bash
make artifacts
```

This creates XCCDF results, SSPs, assessment plans, assessment results, and POA&Ms for both Ubuntu servers and Kubernetes nodes.
