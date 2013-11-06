CREATE OR REPLACE FUNCTION library_call_analysis_check_code() 
RETURNS TRIGGER AS $$
DECLARE 
c1 CURSOR FOR 
(
   SELECT 1 FROM library_call_analysis_diff
   WHERE patch_id = NEW.patch_id
   AND start_line_number = NEW.start_line_number
   AND line_number = NEW.line_number
   AND code = NEW.code
   AND type != NEW.type
   LIMIT 1
);
c2 CURSOR FOR 
(
   SELECT 1 FROM library_call_analysis_dotnetlibraryclass s
   WHERE NEW.code LIKE ('%' || s.classname || '%') 
   LIMIT 1
);
BEGIN
   OPEN c1;
   MOVE c1;
   IF FOUND THEN
      DELETE FROM library_call_analysis_diff WHERE CURRENT OF c1;
      RETURN NULL;
   END IF; 
   CLOSE c1;

   OPEN c2;
   MOVE c2;
   IF NOT FOUND THEN
      RETURN NULL;
   END IF; 
   CLOSE c2;

   RETURN NEW;
END;
$$ LANGUAGE 'plpgsql';

CREATE TRIGGER library_call_analysis_check_code BEFORE INSERT OR UPDATE ON library_call_analysis_diff
FOR EACH ROW 
EXECUTE PROCEDURE library_call_analysis_check_code();
