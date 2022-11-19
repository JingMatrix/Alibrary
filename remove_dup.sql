DELETE FROM record d
WHERE  EXISTS (
   SELECT FROM record
   WHERE  name = d.name
   AND	  size = d.size
   AND    ctid < d.ctid
   );
