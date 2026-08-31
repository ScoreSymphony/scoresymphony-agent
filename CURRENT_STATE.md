# Current State

Status date: 2026-08-31

## IMPLEMENTED in this bootstrap branch

- repository structure for backend, frontend, tests and deployment
- FastAPI application factory and read-only control-plane query contract
- file-backed state snapshot with atomic replacement
- React/TypeScript Develop Control UI shell
- production multi-stage Dockerfile and Docker Compose localhost baseline
- backend test contracts and CI definition

## PREPARED

- adapter boundaries for workers, reviews, system metrics and future storage implementations
- Human Control Plane navigation for the target surfaces
- production authentication fail-closed configuration boundary

## NOT YET IMPLEMENTED

- real Hermes orchestration backend
- proposal/specification mutation commands
- complete Task Graph and dependency engine
- real FCC implementation adapter
- real Codex review adapter
- real Qwen/GPU adapter
- real Resource Scheduler
- real worktree lifecycle
- production authentication provider
- production reverse proxy/TLS integration
- VPS deployment

This file describes repository state only. It does not claim that anything is deployed on a VPS.
