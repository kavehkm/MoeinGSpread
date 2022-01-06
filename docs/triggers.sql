--------------------
-- INVOICE-UPDATE --
--------------------
CREATE TRIGGER MGSInvoiceUpdate
ON Factor1
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    INSERT INTO MGS(id, subject, act)
    SELECT id, 1, 2
    FROM inserted
    WHERE type = 2 AND FishNo IS NOT NULL
END
--------------------
-- INVOICE-DELETE --
--------------------
CREATE TRIGGER MGSInvoiceDelete
ON Factor1
AFTER DELETE
AS
BEGIN
    SET NOCOUNT ON;
    INSERT INTO MGS(id, subject, act)
    SELECT id, 1, 3
    FROM deleted
    WHERE type = 2 AND FishNo IS NOT NULL
END