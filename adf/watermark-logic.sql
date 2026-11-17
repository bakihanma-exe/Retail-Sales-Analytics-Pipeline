-- Illustrative SQL Server control-table pattern.
-- Adapt column names and data types to your source system.

CREATE TABLE dbo.IngestionWatermark
(
    SourceName       varchar(200) NOT NULL PRIMARY KEY,
    LastWatermark    datetime2(7) NOT NULL,
    UpdatedAtUtc     datetime2(7) NOT NULL
        CONSTRAINT DF_IngestionWatermark_UpdatedAtUtc DEFAULT SYSUTCDATETIME()
);

-- Read the lower bound before starting a pipeline run.
SELECT SourceName, LastWatermark
FROM dbo.IngestionWatermark
WHERE SourceName = @SourceName;

-- Obtain the upper bound from the source before copying.
-- Example only:
-- SELECT @CurrentWatermark = MAX(ModifiedDate) FROM dbo.SourceTable;

-- Update only after the corresponding copy activity succeeds.
UPDATE dbo.IngestionWatermark
SET LastWatermark = @CurrentWatermark,
    UpdatedAtUtc = SYSUTCDATETIME()
WHERE SourceName = @SourceName
  AND LastWatermark = @PreviousWatermark;

-- Check @@ROWCOUNT = 1; otherwise investigate a concurrent pipeline run.
