import paramiko
import json
import boto3

def lambda_handler(event, context):
  s3_client = boto3.client('s3')
  #Download the pem key from a s3 bucket
  s3_client.download_file ('bucketname', 'yourkey.pem', '/tmp/keyname.pem')
  pem_key = paramiko.RSAKey.from_private_key_file("/tmp/keyname.pem")
  
  #Creating a new client
  ssh_client = paramiko.SSHClient()
  ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

  #Put the address of the server to which you want to connect
  host = "172.0.0.0"
  print("Starting connection to:" + host)
  #Start the connection, in username type the name of the user with whom you want to login
  #In this case as I am using an Amazon Linux AMI the user is ec2-user
  ssh_client.connect (hostname = host, username = "ec2-user", pkey = pem_key)

  #Commands to display the OS information file
  so_info_commands = ["cat /etc/os-release"]
  for command in so_info_commands:
    print "Executing Command: {}".format(command)
    stdin , stdout, stderr = ssh_client.exec_command(command)
    response = stdout.readlines()
    for idx, item in enumerate(response):
      print("Output "+str(idx+1)+": "+item)
      
return{'message' : "Script execution completed. See Cloudwatch logs for complete output"}
