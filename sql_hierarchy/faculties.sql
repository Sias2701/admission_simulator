USE admission;

CREATE TABLE faculties(
    f_id CHAR(6) NOT NULL PRIMARY KEY,
    f_name CHAR(40) NOT NULL,
    f_location CHAR(20) NOT NULL
)