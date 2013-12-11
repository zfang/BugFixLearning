CREATE TEMP TABLE library_call_analysis_ckeyword_temp (
   keyword character varying(30) NOT NULL
);

\copy library_call_analysis_ckeyword_temp FROM '/home/zfang/BugFixLearning/script/library_call_analysis/c/c_keyword.dat' WITH DELIMITER AS ' ';

INSERT INTO library_call_analysis_ckeyword (keyword) SELECT * FROM library_call_analysis_ckeyword_temp;
