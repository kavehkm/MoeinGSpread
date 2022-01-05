------------
-- DELETE --
------------
CREATE TRIGGER GspreadInvoiceDelete
ON Factor1
AFTER DELETE
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE Gspread
    SET is_deleted = 1
    FROM Gspread AS gs
    INNER JOIN deleted AS d ON d.ID = gs.id
END


------------
-- UPDATE --
------------
CREATE TRIGGER GspreadInvoiceUpdate
ON Factor1
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE Gspread
    SET is_updated = 1
    FROM Gspread AS gs
    INNER JOIN inserted AS i ON i.ID = gs.id
END
