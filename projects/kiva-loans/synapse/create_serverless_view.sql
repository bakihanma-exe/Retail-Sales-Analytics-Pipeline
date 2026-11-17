-- Synapse Serverless SQL view-generation template.
-- The source walkthrough creates one OPENROWSET view per Gold table folder.
-- Configure storage access with managed identity / scoped credential.
-- Do not embed storage keys or SAS tokens in this script.

CREATE OR ALTER PROCEDURE dbo.CreateSQLServerlessView_gold
    @ViewName sysname
AS
BEGIN
    SET NOCOUNT ON;

    -- Restrict view names to safe identifiers. This template assumes the
    -- corresponding Gold folder has the same name.
    IF @ViewName IS NULL OR @ViewName = N''
        THROW 50001, 'View name is required.', 1;

    IF @ViewName LIKE N'%[^A-Za-z0-9_]%'
        THROW 50002, 'View name contains unsupported characters.', 1;

    DECLARE @sql nvarchar(max);
    DECLARE @quotedView nvarchar(258) = QUOTENAME(@ViewName);
    DECLARE @path nvarchar(1000) =
        N'https://<storage-account>.dfs.core.windows.net/gold/dbo/'
        + @ViewName + N'/*.csv';

    SET @sql = N'CREATE OR ALTER VIEW dbo.' + @quotedView + N' AS
        SELECT *
        FROM OPENROWSET(
            BULK ''' + REPLACE(@path,'''','''''') + N''',
            FORMAT = ''CSV'',
            PARSER_VERSION = ''2.0'',
            HEADER_ROW = TRUE
        ) AS rows;';

    EXEC sys.sp_executesql @sql;
END;
GO

-- Replace the storage account and confirm the Synapse Serverless SQL
-- OPENROWSET options supported in your workspace before deployment.
