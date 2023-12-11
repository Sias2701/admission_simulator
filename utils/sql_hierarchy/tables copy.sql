USE admission;

CREATE TABLE candidate_type(
    t_id CHAR(3) NOT NULL
);

CREATE TABLE groups(
    g_id CHAR(6) PRIMARY KEY,
    g_type CHAR(3) NOT NULL FOREIGN KEY REFERENCES candidate_type(t_id) ON UPDATE CASCADE
);

CREATE TABLE faculties(
    f_id CHAR(5) PRIMARY KEY
    f_name VARCHAR NOT NULL
);

CREATE TABLE majors(
    m_id CHAR(16) PRIMARY KEY,
    m_name VARCHAR NOT NULL,
    m_group CHAR(6) NOT NULL FOREIGN KEY REFERENCES groups(g_id) ON UPDATE CASCADE,
    m_faculty CHAR(5) NOT NULL FOREIGN KEY REFERENCES faculties(f_id) ON UPDATE CASCADE,
    m_plain INT NOT NULL CHECK(m_plain > 0),
    m_current_enroll INT NOT NULL CHECK(m_plain >= m_current_enroll) DEFAULT 0,
    m_primary CHAR(1) CHECK(m_primary IN (NULL, 'P', 'H')),
    m_secondary CHAR(1) CHECK(m_secondary IN (NULL, 'B', 'C', 'G', 'O')),
);

CREATE TABLE candidate_infos(
    exam_id CHAR(14) PRIMARY KEY,
    c_name VARCHAR NOT NULL,
    c_rank INT NOT NULL CHECK(c_rank > 0),
    c_score FLOAT NOT NULL CHECK(c_score > 0),
    c_adjust CHAR(1) NOT NULL CHECK(c_adjust IN ('Y','N')),
    c_type CHAR(3) NOT NULL FOREIGN KEY REFERENCES candidate_type(t_id) ON UPDATE CASCADE,
    c_primary CHAR(1) NOT NULL CHECK(c_primary IN ('P', 'H')),
    c_secondary CHAR(2) NOT NULL CHECK(c_secondary IN ('B', 'C', 'G', 'O')),
    c_group CHAR(6) NOT NULL FOREIGN KEY REFERENCES groups(g_id) ON UPDATE CASCADE CHECK(c_group IN (SELECT g_id FROM groups WHERE g_type = c_type)),
    c_enroll1 CHAR(16) NOT NULL FOREIGN KEY REFERENCES majors(m_id),
    c_enroll2 CHAR(16) FOREIGN KEY REFERENCES majors(m_id),
    c_enroll3 CHAR(16) FOREIGN KEY REFERENCES majors(m_id),
    c_enroll4 CHAR(16) FOREIGN KEY REFERENCES majors(m_id),
    c_enroll5 CHAR(16) FOREIGN KEY REFERENCES majors(m_id),
    c_enroll6 CHAR(16) FOREIGN KEY REFERENCES majors(m_id)
)

CREATE TABLE final_enroll(
    exam_id CHAR(14)
)