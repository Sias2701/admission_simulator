CREATE ROLE admission_admin_role;
CREATE ROLE admission_guest_role;

CREATE LOGIN aadmin_login WITH PASSWORD = 'admin@123'
CREATE LOGIN aguest_login WITH PASSWORD = 'guest@456'

USE admission;
GO

CREATE USER aadmin FOR LOGIN aadmin_login
CREATE USER aguest FOR LOGIN aguest_login

ALTER ROLE admission_admin_role ADD MEMBER aadmin;
ALTER ROLE admission_guest_role ADD MEMBER aguest;

GRANT SELECT ON accept_enroll TO admission_guest_role;
GRANT SELECT ON final_enroll_view_all TO admission_guest_role;
GRANT SELECT ON final_accept_adjust TO admission_guest_role;
GRANT SELECT ON accept_list_stat_faculty TO admission_guest_role;
GRANT EXEC ON accept_list_stat_all TO admission_guest_role;

GRANT INSERT,DELETE ON candidates TO admission_admin_role;
GRANT EXEC ON apply_enroll TO admission_admin_role;
GRANT SELECT ON accept_enroll TO admission_admin_role;
GRANT SELECT ON final_enroll_view_all TO admission_admin_role;
GRANT SELECT ON final_accept_adjust TO admission_admin_role;
GRANT SELECT ON accept_list_stat_faculty TO admission_admin_role;
GRANT EXEC ON accept_list_stat_all TO admission_admin_role
GRANT SELECT ON faculties TO admission_admin_role;
GRANT SELECT ON majors TO admission_admin_role;

