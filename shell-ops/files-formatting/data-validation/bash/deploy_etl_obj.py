######################################
# Function call - Deploy ETL Objects #
######################################
deploy_etl_objects()
{
 tail -n +2 ${BASE_DIR}/deploy_etl_obj_list.txt | while IFS=\| read SRC_USER SRC_HOST SRC_DIR SRC_OBJ DEST_USER DEST_HOST DEST_DIR DEST_OBJ
  do
   scp ${SRC_USER}@${SRC_HOST}:${SRC_DIR}/${SRC_OBJ} ${DEST_USER}@${DEST_HOST}:${DEST_DIR}/${DEST_OBJ}

#   scp ${SRC_DIR}/${SRC_OBJ} ${DEST_USER}@${DEST_HOST}:${DEST_DIR}/${DEST_OBJ}
    if [[ $? -ne 0 ]]
     then
      echo "Deployment of object ${SRC_OBJ} failed."
      #exit 99
    fi
  done
}


########################
# Start of Main script #
########################

##########################
# Initialize variables   #
##########################
. ./etl_env.sh

export DATE=$(date +%Y%m%d)

deploy_etl_objects
