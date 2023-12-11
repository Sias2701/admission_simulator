USE admission;

CREATE TABLE major_groups(
    g_id CHAR(3) NOT NULL PRIMARY KEY,
    g_type CHAR(3) NOT NULL FOREIGN KEY REFERENCES candidate_type_info(t_id) ON UPDATE CASCADE
);