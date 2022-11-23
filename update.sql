ALTER INDEX record_pkey RENAME TO book_pkey;
ALTER INDEX record_idx RENAME TO book_idx;
ALTER TABLE record RENAME TO book;
