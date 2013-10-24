SELECT 
r.slug, p.sha1, 
d1.patch_id, d1.start_line_number, 
d1.line_number AS minus_code_line_num, d2.line_number AS plus_code_line_num, 
d1.code AS minus_code, d2.code AS plus_code
FROM 
library_call_analysis_repository r, library_call_analysis_patch p, 
library_call_analysis_diff d1, library_call_analysis_diff d2 
WHERE TRUE
--AND r.slug='Nancy'
AND r.id = p.repo_id
AND p.id = d1.patch_id
AND d1.patch_id = d2.patch_id 
AND d1.start_line_number = d2.start_line_number
AND d1.type='-' AND d2.type = '+'
AND EXISTS 
(SELECT 1 FROM library_call_analysis_dotnetlibraryclass l
WHERE d1.code % (l.classname ||'.'|| l.function)
AND d2.code % (l.classname ||'.'|| l.function))
;
