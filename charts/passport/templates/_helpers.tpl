{{/*
Set apiVersion based on .Capabilities.APIVersions
*/}}
{{- define "rbacAPIVersion" -}}
{{- if .Capabilities.APIVersions.Has "rbac.authorization.k8s.io/v1beta1" -}}
rbac.authorization.k8s.io/v1beta1
{{- else if .Capabilities.APIVersions.Has "rbac.authorization.k8s.io/v1alpha1" -}}
rbac.authorization.k8s.io/v1alpha1
{{- else -}}
rbac.authorization.k8s.io/v1
{{- end -}}
{{- end -}}

{{/* Generate passport deployment envs */}}
{{- define "passport.envs" -}}
env:
- name: "TZ"
  value: {{ .Values.time_zone | default "UTC" | quote }}
{{- if (.Values.database_url) }}
- name: DRYCC_DATABASE_URL
  valueFrom:
    secretKeyRef:
      name: passport-creds
      key: database_url
{{- else if eq .Values.global.database_location "on-cluster"  }}
- name: DRYCC_DATABASE_USER
  valueFrom:
    secretKeyRef:
      name: database-creds
      key: user
- name: DRYCC_DATABASE_PASSWORD
  valueFrom:
    secretKeyRef:
      name: database-creds
      key: password
- name: DRYCC_DATABASE_NAME
  valueFrom:
    secretKeyRef:
      name: database-creds
      key: passport_db_name
- name: DRYCC_DATABASE_URL
  value: "postgres://$(DRYCC_DATABASE_USER):$(DRYCC_DATABASE_PASSWORD)@$(DRYCC_DATABASE_SERVICE_HOST):$(DRYCC_DATABASE_SERVICE_PORT)/$(DRYCC_DATABASE_NAME)"
{{- end }}
- name: WORKFLOW_NAMESPACE
  valueFrom:
    fieldRef:
    fieldPath: metadata.namespace
{{- range $key, $value := .Values.environment }}
- name: {{ $key }}
  value: {{ $value | quote }}
{{- end }}
{{- end }}

{{/* Generate passport deployment volumeMounts */}}
{{- define "passport.volumeMounts" }}
volumeMounts:
  - mountPath: /etc/oidc.key
    name: oidc-key
    readOnly: true
{{- end }}

{{/* Generate passport deployment volumes */}}
{{- define "passport.volumes" }}
volumes:
  - name: oidc-key
    secret:
      secretName: oidc-key
{{- end }}

{{/* Generate passport deployment limits */}}
{{- define "passport.limits" -}}
{{- if or (.Values.limits_cpu) (.Values.limits_memory) }}
resources:
  limits:
{{- if (.Values.limits_cpu) }}
    cpu: {{.Values.limits_cpu}}
{{- end }}
{{- if (.Values.limits_memory) }}
    memory: {{.Values.limits_memory}}
{{- end }}
{{- end }}
{{- end }}