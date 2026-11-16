# AWS deployment roadmap (not yet provisioned)

## Phase 0 — local proof of concept

Use Docker Compose with Redpanda + PostgreSQL. Generate drafts and review them locally. Do not expose FastAPI publicly.

## Phase 1 — budget-constrained cloud pilot

Recommended AWS services:

- EventBridge Scheduler: daily trigger.
- ECS Fargate: run the container as a one-off task for production and a separate small review API service only if needed.
- SQS + DLQ: cloud job queue during the low-budget phase (Kafka-compatible event contract retained in application code).
- S3 private bucket: rendered MP4s, audio and thumbnails; server-side encryption and lifecycle expiry.
- Secrets Manager: OpenAI API key and later platform OAuth refresh tokens.
- CloudWatch: logs, alarms and cost monitoring.
- Database: choose a persistent low-cost PostgreSQL-compatible service only after checking current regional pricing; do not leave a local laptop database as a cloud dependency.

This pilot requires an SQS publisher/consumer adapter, S3 artifact adapter, persistent cloud database configuration, authentication for the review API, and an ECS task definition. Those AWS adapters are not implemented in v0.1.

## Phase 2 — Kafka in AWS

Move to Amazon MSK only when workload and budget justify it, or run a self-managed Kafka-compatible broker with an explicit availability/backup plan. MSK Serverless has a material fixed hourly charge and is not appropriate for a ₹2,000/month experiment.

## Deployment sequence

1. Pick an AWS region and create an AWS Budget alert before provisioning.
2. Create a private S3 bucket with block-public-access enabled, encryption, versioning if required, and lifecycle expiry.
3. Create an SQS queue and dead-letter queue with least-privilege IAM policies.
4. Build and push the Docker image to ECR.
5. Create an ECS cluster and task definition. Inject secrets from Secrets Manager; never bake keys into the image.
6. Configure EventBridge Scheduler to invoke the ECS task or enqueue a run message.
7. Configure a persistent database and run `sql/schema.sql` as a migration.
8. Add Cognito/OIDC authentication to the review UI/API before public access.
9. Add S3 upload/download signing and the cloud queue adapter; test idempotency and retries.
10. Only then configure YouTube/Meta OAuth and a separately permissioned publisher. Keep publishing disabled until human approval is recorded.

No AWS resources are created by this repository. Review current pricing and region availability before deployment.
