CREATE TEMP TABLE library_call_analysis_dotnetlibraryclass_temp (
   namespace character varying(255) NOT NULL,
   classname character varying(255) NOT NULL,
   function character varying(255) NOT NULL
);

\copy library_call_analysis_dotnetlibraryclass_temp FROM '/home/zfang/BugFixLearning/script/library_call_analysis/dotnetclass/system_class.dat' WITH DELIMITER AS ' ';

INSERT INTO library_call_analysis_dotnetlibraryclass (namespace, classname, function) SELECT * FROM library_call_analysis_dotnetlibraryclass_temp;