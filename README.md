# Drycc Passport

[![Build Status](https://drone.drycc.cc/api/badges/drycc/passport/status.svg)](https://drone.drycc.cc/drycc/passport)
[![codecov.io](https://codecov.io/github/drycc/passport/coverage.svg?branch=main)](https://codecov.io/github/drycc/passport?branch=main)

Drycc (pronounced DAY-iss) Workflow is an open source Platform as a Service (PaaS) that adds a developer-friendly layer to any [Kubernetes](http://kubernetes.io) cluster, making it easy to deploy and manage applications on your own servers.

For more information about the Drycc Workflow, please visit the main project page at https://github.com/drycc/workflow.

We welcome your input! If you have feedback, please [submit an issue][issues]. If you'd like to participate in development, please read the "Development" section below and [submit a pull request][prs].

# About

The Passport is the Oauth2.0 API server for [Drycc Workflow][workflow].

# Before Installation

Creating a oidc.key in you location.
How and What's the use.
see: https://django-oauth-toolkit.readthedocs.io/en/latest/oidc.html?highlight=oidc.key#creating-rsa-private-key

## In kubernetes create secret oidc-key.
kubectl create ns drycc
kubectl create secret generic oidc-key --from-file=oidc.key -n drycc

## In docker, we need mount oidc.key to /etc/oidc.key
eg: docker run --rm -v oidc.key:/etc/oidc.key docker.io/drycc/passport:canary
