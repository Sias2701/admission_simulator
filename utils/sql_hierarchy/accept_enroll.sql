USE admission;

CREATE TABLE accept_enroll(
    c_id CHAR(14) PRIMARY KEY FOREIGN KEY REFERENCES candidates(c_id) ON UPDATE CASCADE,
    c_enroll CHAR(12) NOT NULL FOREIGN KEY REFERENCES majors(m_id) ON UPDATE NO ACTION,
    c_group CHAR(3) NOT NULL FOREIGN KEY REFERENCES major_groups(g_id) ON UPDATE NO ACTION,
    c_adjust CHAR(1) NOT NULL CHECK(c_adjust IN ('Y', 'N'))
);
