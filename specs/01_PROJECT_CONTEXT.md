# 01 — Project Context

## Hackathon

**ImagineHack 2026 — Track 2 by HILTI: Secure & Energy-Aware Cloud Platforms for Construction Tech.**

## Problem

Construction-tech runs on cloud workloads (field apps, project dashboards, IoT monitoring,
BIM processing, reporting, document storage, databases, CI/CD). Once deployed these become
blind spots: teams cannot continuously connect **security risk + energy use + carbon impact +
cloud cost + workload efficiency + construction-workflow importance** into one decision layer.
The result is hidden vulnerabilities, wasted spend, higher emissions, and risk to construction
operations.

## Solution

A secure, energy-aware **cloud intelligence platform** that continuously monitors construction-tech
cloud workloads, detects anomalies and inefficiencies, **explains why they matter**, recommends the
next best action with a **projected cost/energy/carbon forecast**, and then **safely auto-fixes,
asks approval, or escalates** through a guardrailed remediation workflow — with full audit trail.

```text
Detection & Insight → Next Best Action → Guardrailed Self-Healing
```

## Product name

Product name **Clover** (HILTI Track 2). Architecture does not
depend on the final name.

## Track relevance

| Track outcome | How we address it |
|---|---|
| Improved cloud security | Detect exposed services, public storage, vulnerabilities, access anomalies |
| Reduced energy consumption | Find idle / overprovisioned / inefficient workloads |
| Lower carbon footprint | Forecast carbon and recommend lower-carbon optimization |
| Automated alerts | Alert system + alert-ready recommendation objects |
| Smart recommendations | Rule-based Next Best Action engine |
| Cost optimization | XGBoost projected-savings forecast + optimization workflow |
| Continuous optimization | Monitoring loop, repeated telemetry ingestion, self-healing cycle |
| Construction workflow support | Workflow criticality factored into prioritization |
| Operational efficiency | Auto-fix, approval workflow, escalation, audit reports |

## Winning angle

Not "another cloud dashboard" — an **explainable AI decision layer** combining cloud monitoring,
GreenOps, FinOps, DevSecOps, explainable ML, agentic remediation, and human-in-the-loop safety.

## MVP honesty

No access to real HILTI infrastructure. Everything runs on **synthetic cloud telemetry** from a
live mock data generator/controller. Models are trained/demonstrated on synthetic data and framed
honestly: "this is how the system behaves when connected to real cloud telemetry."
