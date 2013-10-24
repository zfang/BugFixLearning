CREATE EXTENSION pg_trgm;
CREATE INDEX trgm_idx ON library_call_analysis_diff USING gist (code gist_trgm_ops);
