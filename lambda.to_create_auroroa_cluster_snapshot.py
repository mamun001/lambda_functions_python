
import boto3
import datetime
import os

def lambda_handler(event, context):
   
    # ENVs
    # ENV = dev
    # CLUSTER_name = insert_cluster_name_here 
    #cluster_name = "foo-pre-prod-aurora-cluster-dev"
    cluster_name = os.environ['CLUSTER_NAME']
    # DBClusterSnapshotIdentifier='foo-pre-prod-aurora-cluster-dev-%s' % datetime.datetime.now().strftime("%y-%m-%d-%H-1"),
    snapshot_name = (cluster_name + datetime.datetime.now().strftime("%y-%m-%d-%H"))
    
    
    print("Connecting to RDS")
    client = boto3.client('rds')
    
    
    print("RDS snapshot backups stated at %s...\n" % datetime.datetime.now())
    client.create_db_cluster_snapshot(
        DBClusterIdentifier=(cluster_name), 
        DBClusterSnapshotIdentifier=(snapshot_name)
    )
    
    
