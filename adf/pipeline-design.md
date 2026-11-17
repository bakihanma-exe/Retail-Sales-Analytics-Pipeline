# Azure Data Factory ingestion design

## Pattern shown in the supplied document
1. Create an HTTP linked service for the GitHub raw-content host.
2. Create an ADLS Gen2 linked service and Bronze sink dataset.
3. Store one JSON configuration row per file with:
   - `p_rel_url`: source file relative URL
   - `p_sink_folder`: destination folder
   - `p_sink_file`: destination filename
4. Use Lookup to read the complete JSON array (disable First Row only when required by the dataset/output shape).
5. Pass Lookup output to ForEach.
6. Inside ForEach, execute a parameterized Copy Activity using the current item's source URL and sink path.
7. Debug the pipeline and validate the landed files in Bronze.

The example configuration is in `parameters.json`. The supplied document demonstrates parameterized file ingestion; it does not show a watermark control table or source-side incremental predicate.

## Optional incremental enhancement (not shown in the supplied document)
If a source later provides a reliable modified timestamp or change feed, add a watermark table and use a bounded incremental predicate. Do not describe this enhancement as part of the documented implementation until it is built and tested.

## Reliability checklist
- Validate each URL and sink path before starting the ForEach.
- Configure retries and timeouts for transient failures.
- Log pipeline run ID, source file, status, rows read, and rows written.
- Avoid duplicate loads on retry by defining an overwrite/replace or idempotent ingestion policy.
- Do not store credentials in JSON configuration or source control.