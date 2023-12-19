USE admission;

CREATE TABLE candidates(
    c_id CHAR(14) NOT NULL UNIQUE,
    c_score FLOAT NOT NULL CHECK(c_score >= 0),
    c_rank INT NOT NULL CHECK(c_rank > 0),
    c_adjust CHAR(1) NOT NULL CHECK(c_adjust IN ('A', 'R')),
    c_type CHAR(3) NOT NULL FOREIGN KEY REFERENCES candidate_type_info(t_id) ON UPDATE CASCADE,
    c_primary CHAR(1) NOT NULL CHECK(c_primary IN ('P', 'H')),
    c_secondary CHAR(2) NOT NULL,
    c_group CHAR(3) NOT NULL FOREIGN KEY REFERENCES major_groups(g_id),
    c_enroll1 CHAR(12) NOT NULL FOREIGN KEY REFERENCES majors(m_id),
    c_enroll2 CHAR(12) FOREIGN KEY REFERENCES majors(m_id),
    c_enroll3 CHAR(12) FOREIGN KEY REFERENCES majors(m_id),
    c_enroll4 CHAR(12) FOREIGN KEY REFERENCES majors(m_id),
    c_enroll5 CHAR(12) FOREIGN KEY REFERENCES majors(m_id),
    c_enroll6 CHAR(12) FOREIGN KEY REFERENCES majors(m_id),
    PRIMARY KEY CLUSTERED(c_rank ASC),
    CHECK(c_type IN (SELECT t_id FROM candidate_type_info)),
    CHECK(c_group IN (SELECT g_id FROM major_groups WHERE g_type = c_type))
);

