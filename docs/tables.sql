CREATE TABLE Gspread(
    id              INT             NOT NULL,
    fishno          INT             NOT NULL,
    loc             VARCHAR(20)     NOT NULL,
    is_updated      BIT             NOT NULL    DEFAULT 0,
    is_deleted      BIT             NOT NULL    DEFAULT 0
)