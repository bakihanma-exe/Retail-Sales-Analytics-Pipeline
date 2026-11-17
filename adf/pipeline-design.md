# Azure Data Factory incremental ingestion design

## Pipeline pattern
1. **Lookup previous watermark** from a control table for the selected source.
2. **Lookup current upper bound** from the source (for example, MAX(ModifiedDate)).
3. **ForEach** configured source table / entity.
4. **Copy Activity** extracts rows in the incremental range and writes them to the ADLS Gen2 Bronze landing area.
5. **Update watermark** only after the required copy activities have succeeded.

## Incremental predicate
Use a half-open interval to avoid re-reading the previous boundary:

```sql
WHERE ModifiedDate > @PreviousWatermark
  AND ModifiedDate <= @CurrentWatermark
```

For sources without a reliable modified timestamp, use a source-specific strategy such as change tracking, CDC, or a full snapshot.

## Reliability
- Configure retries and timeouts for transient failures.
- Do not advance the watermark when a copy fails.
- Log source name, lower/upper bound, run ID, status, rows read, and rows written.
- Make downstream writes idempotent; use stable business keys and MERGE/upsert when reprocessing is possible.
- Plan for late-arriving updates and deletes; a timestamp watermark alone may not capture hard deletes.
- Parameterize linked services, datasets, table names, and sink paths. Validate dynamic SQL identifiers against an allow-list.
