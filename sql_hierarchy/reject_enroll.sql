USE admission;

CREATE TABLE reject_enroll(
    c_id CHAR(14) PRIMARY KEY FOREIGN KEY REFERENCES candidates(c_id) ON UPDATE CASCADE,
    reject_term CHAR(100) NOT NULL
);
