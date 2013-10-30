CREATE OR REPLACE FUNCTION library_call_analysis_analyze_function_calls(_slug varchar) RETURNS 
TABLE (
   slug varchar(50),
   sha1 varchar(40),
   patch_id int,
   start_line_number int,
   minus_code_line_num int,
   plus_code_line_num int,
   minus_code text,
   plus_code text
)
AS $$
BEGIN

RETURN QUERY
SELECT 
r.slug, p.sha1, 
d1.patch_id, d1.start_line_number, 
d1.line_number AS minus_code_line_num, d2.line_number AS plus_code_line_num, 
d1.code AS minus_code, d2.code AS plus_code 
FROM 
library_call_analysis_repository r, library_call_analysis_patch p, 
library_call_analysis_diff d1, library_call_analysis_diff d2 
WHERE TRUE
AND r.slug = _slug 
AND r.id = p.repo_id
AND p.id = d1.patch_id
AND d1.patch_id = d2.patch_id 
AND d1.start_line_number = d2.start_line_number
AND d1.type='-' AND d2.type = '+'
AND EXISTS 
(SELECT 1 FROM library_call_analysis_dotnetlibraryclass_search_string s
WHERE d1.code LIKE ('%' || s.string || '%') 
AND d2.code LIKE ('%' || s.string || '%') )
--WHERE d1.code % (s.string) 
--AND d2.code % (s.string) )
;
END
$$ LANGUAGE plpgsql;
