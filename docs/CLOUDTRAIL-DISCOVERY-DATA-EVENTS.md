# Discovery that CloudTrail does not log by default: SQS

> Defensive configuration note, 2026-11-23. Sources: AWS documentation (`SRC-AWS-SQS-CLOUDTRAIL-LOGGING`, grade A) and a
> Mitigant emulation demo (`SRC-MITIGANT-ARTEX-KIRO-MCP`, grade C). Used by `DET-AI-047` and the TCEM case
> `CASE-ARTEX-CLOUD-SECRETS` (gap `GAP-CLOUD-SECRETS-3`).

## The gap

ARTEX-driven intrusions prove what a stolen AWS key can do by sweeping many services in seconds (`LLMI-T015`; Microsoft,
Datadog, Barracuda, Unit 42). `DET-AI-047` looks for that sweep in CloudTrail: many calls, most denied, one success.

The sweep is only visible for APIs that CloudTrail records. For Amazon SQS, AWS classifies the read-only discovery calls as
**data events**, and CloudTrail **does not log data events by default**. They don't appear in Event history either:

| SQS API | CloudTrail event type | Logged by default |
|---|---|---|
| `ListQueues`, `GetQueueUrl`, `GetQueueAttributes`, `ListQueueTags`, `ListDeadLetterSourceQueues` | Data event | No |
| `ReceiveMessage`, `SendMessage(Batch)`, `DeleteMessage(Batch)`, `ChangeMessageVisibility(Batch)` | Data event | No |
| `CreateQueue`, `DeleteQueue`, `SetQueueAttributes`, `AddPermission`, `RemovePermission`, `PurgeQueue`, `TagQueue`, `UntagQueue` | Management event | Yes |

So a key that enumerates every queue and reads their attributes (dead-letter targets, KMS keys, access policies) leaves no
record in a default trail. In its emulation of Storm-0940's ARTEX techniques against an AWS account, Mitigant reports
exactly that: the SQS queue enumeration produced no CloudTrail entry. This is a vendor demo. The underlying behaviour is
AWS's documented default, so check your own trail.

## What to turn on

You don't need every SQS data event, which would be very noisy (`SendMessage` and `ReceiveMessage` are the queue's normal
traffic). Log only the discovery calls, with an advanced event selector on the trail:

```json
[
  {
    "Name": "SQS discovery (read-only data events)",
    "FieldSelectors": [
      { "Field": "eventCategory", "Equals": ["Data"] },
      { "Field": "resources.type", "Equals": ["AWS::SQS::Queue"] },
      { "Field": "eventName", "Equals": ["ListQueues", "GetQueueUrl", "GetQueueAttributes", "ListQueueTags", "ListDeadLetterSourceQueues"] }
    ]
  }
]
```

Apply it with `aws cloudtrail put-event-selectors --trail-name <trail> --advanced-event-selectors file://sqs-discovery.json`.
Keep the selectors the trail already has: the call replaces the whole set. Data events are billed per event, so check the
volume on one account before you roll it out to the organisation trail.

## Hunting once it is on

- In `DET-AI-047`, count SQS discovery calls with the other services. A new key or role that calls `ListQueues` and then
  `GetQueueAttributes` on many queues within minutes, with no prior history, belongs in the same sweep.
- Pay most attention to `GetQueueAttributes` on queues whose policy or KMS key points to another account. That attribute
  read is the reconnaissance a cross-account pivot would need.

## Beyond SQS

Other services also put their reads in data events: S3 object-level calls, Lambda `Invoke`, and DynamoDB item calls, among
others. Each service's CloudTrail page lists its data events. Before you trust a sweep detection, list which services your
crown jewels depend on and check which of their read APIs your trail records.
