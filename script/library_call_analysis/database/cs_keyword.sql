CREATE TEMP TABLE library_call_analysis_csharpkeyword_temp (
   keyword character varying(30) NOT NULL
);

\copy library_call_analysis_csharpkeyword_temp FROM '/home/zfang/BugFixLearning/script/library_call_analysis/dotnetclass/cs_keyword.dat' WITH DELIMITER AS ' ';

INSERT INTO library_call_analysis_csharpkeyword (keyword) SELECT * FROM library_call_analysis_csharpkeyword_temp;
