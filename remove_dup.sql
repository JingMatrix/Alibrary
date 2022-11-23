DELETE FROM book d
WHERE  EXISTS (
   SELECT FROM book
   WHERE  name = d.name
   AND	  size = d.size
   AND    ctid < d.ctid
   );

DELETE FROM collection d
WHERE  EXISTS (
   SELECT FROM collection
   WHERE  name = d.name
   AND	  size = d.size
   AND    ctid < d.ctid
   );
