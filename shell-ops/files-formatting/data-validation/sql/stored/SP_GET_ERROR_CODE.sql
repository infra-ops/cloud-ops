------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
/**
 * This procedure is used to  calculate the acutal error code that will be reported to PRCSS_EXCPTN table
 * based on the given batch ID and error index
 *
 *   Revision History                                                   
 *
 *   Date          By Whom                   Description                                   
 *   08/01/2007    Helen Li                  Initial version
 *   04/03/2008    Helen Li                  Enhanced CONTINUE handler and standardized error codes
 *   08/08/2011	                             Initial Implementation
 **/
 
REPLACE PROCEDURE $.SP_GET_ERROR_CODE       (
	IN batch_id	 INTEGER, 	/* batch ID of the  reporting process */
	IN ods_error_index INTEGER, /*  error index reported by the calling process*/
	OUT ods_error_code INTEGER)	 /* Final ODS error code */
	
BEGIN
	
 	DECLARE errorCodeBase INTEGER DEFAULT -1000;
 	DECLARE sqlStateCode VARCHAR(10) DEFAULT NULL;
 	DECLARE sqlErrorMsg VARCHAR(4000) DEFAULT NULL;
 
 	DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
 	BEGIN
 
  		IF sqlStateCode IS NULL
  		THEN
     			SET sqlStateCode = SQLSTATE;
   			/* Get error message for the SQLSTATE code */
   			CALL SysDBA.SQLSTATE_Desc(sqlStateCode, sqlErrorMsg);
    		END IF;

    		/* report error to CRTCL_PRCSS_EXCPTN table */
    		CALL FL_P_SP.SP_INSERT_CRITICAL_EXCEPTION(
     				batch_id
     				,1002
     				,'Failed to calculate error code for exception reported by batch ID ' || batch_id
				,sqlStateCode
				,sqlErrorMsg);
            
 		END;

	MAIN_BODY:
	BEGIN
		/** First find out the error code base for the calling process to calculate the actual ODS error code */
		SELECT ERR_CD_BS
	 	INTO errorCodeBase
 		FROM FL_P.PRCSS_CNTRL  PC 
  		INNER JOIN   
   			FL_P.PRCSS_DEF   PD
  		ON PC.BTCH_ID = batch_id AND PC.PRCSS_ID = PD.PRCSS_ID;
 
 		IF ACTIVITY_COUNT = 0
 		THEN
	  		SET sqlStateCode = 'U0002';
 	 		SET sqlErrorMsg = 'Error code based not defined for process associated with batch ID' || batch_id;   
  			CALL SysDBA.Set_SQLSTATE(sqlStateCode, sqlErrorMsg);    
 		END IF;

	 	SET ods_error_code = errorCodeBase + ods_error_index -1;
	 	
	 END;

END;











