REPLACE MACRO $.DATA_ERR (sys VARCHAR(100), activity VARCHAR(100), step VARCHAR(100), errcode VARCHAR(100), record_id VARCHAR(1000), field_nm VARCHAR(100), field_val VARCHAR(4000), severity VARCHAR(100), detail1 VARCHAR(4000), detail2 VARCHAR(4000)) AS       
(
INSERT INTO PEPCMN_P_DATA.DAT_ERR_EVNT (STEP_ID, ERR_CD, BTCH_ID, OPTNL_RCRD_ID, OPTNL_FLD_NM, OPTNL_FLD_VAL, ERR_SVRTY, ERR_DTL_1, ERR_DTL_2) 
SELECT 
   STEP_ID,
   :errcode,
   CUR_BTCH_ID,
   :record_id,
   :field_nm,
   :field_val,
   :severity,
   :detail1,
   :detail2
FROM PEPCMN_P_DATA.STEP
JOIN PEPCMN_P_DATA.ACTVTY
ON ACTVTY.ACTVTY_ID = STEP.ACTVTY_ID AND SYS_NM = :sys AND ACTVTY_NM = :activity
WHERE
   STEP_NM = :step;
)
;
