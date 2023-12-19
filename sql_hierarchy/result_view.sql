USE admission;
GO

CREATE OR ALTER VIEW final_enroll_view_all AS
SELECT accept_enroll.c_id, accept_enroll.c_group, c_enroll, accept_enroll.c_adjust, c_score FROM accept_enroll INNER JOIN candidates ON accept_enroll.c_id = candidates.c_id;
GO

CREATE OR ALTER PROCEDURE final_accept_list
    @adjust CHAR(1)
AS
BEGIN
        IF(@adjust = 'Y')
            SELECT * FROM final_enroll_view_all WHERE c_adjust = 'Y';
        ELSE
            SELECT * FROM final_enroll_view_all WHERE c_adjust = 'N';
END