------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
REPLACE VIEW $.EMPL_ATTR
--############################################################
--# MODIFICATIONS:
--# Date            	Name     	Description of Change 
--# 11/14/2011	     Sonali Karle	Initial Implementation
--############################################################
(
empl_ctry_code                
,empl_co_code                  
,empl_nbr                      
,empl_attr_eff_dt              
,empl_type_code                
,empl_loa_flg                  
,empl_attr_end_dt              
,phy_inv_certf_flg             
,empl_comm_type                
,empl_bank_acct                
,empl_bank_payrl               
,empl_cost_ctr                 
,batch_id                      
,row_revis_nbr            
)  AS 
LOCKING ROW FOR ACCESS 
SELECT 
empl_ctry_code                
,empl_co_code                  
,empl_nbr                      
,empl_attr_eff_dt              
,empl_type_code                
,empl_loa_flg                  
,empl_attr_end_dt              
,phy_inv_certf_flg             
,empl_comm_type                
,empl_bank_acct                
,empl_bank_payrl               
,empl_cost_ctr                 
,batch_id                      
,row_revis_nbr
FROM FL_P_MSTR.EMPL_ATTR
;;

