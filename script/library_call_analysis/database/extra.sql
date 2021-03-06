CREATE EXTENSION pg_trgm;
CREATE INDEX trgm_idx ON library_call_analysis_diff USING gist (code gist_trgm_ops);

CREATE OR REPLACE VIEW library_call_analysis_dotnetlibraryclass_search_string AS
SELECT 
l.classname || '.' || l.function
AS string
FROM library_call_analysis_dotnetlibraryclass l;

CREATE OR REPLACE VIEW library_call_analysis_librarycallchangediffview AS
SELECT d.*
FROM library_call_analysis_diff d, library_call_analysis_librarycallchangediff l
WHERE d.id = l.diff_id;
