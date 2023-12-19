USE admission;

CREATE TABLE majors(
    m_id CHAR(12) PRIMARY KEY,
    m_name CHAR(50) NOT NULL,
    m_group CHAR(3) NOT NULL FOREIGN KEY REFERENCES major_groups(g_id) ON UPDATE CASCADE,
    m_faculty CHAR(6) NOT NULL FOREIGN KEY REFERENCES faculties(f_id) ON UPDATE CASCADE,
    m_max_enroll INT CHECK(m_max_enroll >= 0),
    m_primary CHAR(1) CHECK(m_primary IN (NULL, 'P', 'H')),
    m_secondary CHAR(1) CHECK(m_secondary IN (NULL, 'B', 'C', 'G', 'O'))
);

CREATE INDEX major_group ON majors(m_group);
CREATE INDEX major_faculty ON majors(m_faculty);
CREATE INDEX major_primary ON majors(m_primary);