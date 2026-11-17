-- SQL Server query used by ADF Lookup to discover dbo tables.
SELECT
    s.name AS SchemaName,
    t.name AS TableName
FROM sys.tables AS t
INNER JOIN sys.schemas AS s
    ON t.schema_id = s.schema_id
WHERE s.name = 'dbo'
ORDER BY t.name;

-- ADF ForEach items expression:
-- @activity('LookupTables').output.value
--
-- Dynamic source query inside Copy Activity:
-- @concat('SELECT * FROM ', item().SchemaName, '.', item().TableName)
--
-- Production hardening:
-- * allow-list schema names and validate identifiers
-- * exclude staging/system tables as required
-- * capture row counts and pipeline run ID
-- * define deterministic sink paths and retry-safe write behavior
