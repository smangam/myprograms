import boto3

# create a session object
session = boto3.Session(profile_name='astracodes-smangam')
ec2cli = session.client('ec2')
ec2res = session.resource('ec2')

def describe_az():
  response = ec2cli.describe_availability_zones()
  print "%-20s %-20s %-20s" %('RegionName','ZoneName','State')
  for az in response['AvailabilityZones']:
     print "%-20s %-20s %-20s" %(az['RegionName'],az['ZoneName'],az['State'])

def describe_vpcs():
  response = ec2cli.describe_vpcs()
  print "%-40s %-20s %-10s" %('VpcId','CidrBlock','IsDefault')
  for i in response[u'Vpcs']:
      print "%-40s %-20s %-10s" %(i[u'VpcId'],i[ u'CidrBlock'],i[u'IsDefault'])

def list_vpc_route_tables(vpc_id):
  vpc = ec2res.Vpc(vpc_id)
  route_tables_list = vpc.route_tables.all()
  for i in route_tables_list:
     route_table = ec2res.RouteTable(i.id)
     print "\n%s %-20s " %("Route Table Id: ", route_table.route_table_id)
     for m in route_table.associations_attribute:
        if (m[u'Main']):
           print "%s %s %s" %(m[u'RouteTableId']," is the main route table for VPC ",vpc_id)
     print "\nList of Routes in routing table ",route_table.route_table_id
     print "%-20s %-35s %-20s" %("DestinationCIDR","Target","Status")
     for j in route_table.routes_attribute:
        print "%-20s %-35s %-20s" %(j[u'DestinationCidrBlock'],j[u'GatewayId'],j[u'State'])
     print "\nSubnets Assigned to this Route Table"
     print "%-40s %-30s %-20s" %("SubnetId","RouteTableId","IsMainTable?")
     for k in route_table.associations_attribute:
        if (not k[u'Main']):
           print "%-40s %-30s %-20s" %(k[u'SubnetId'],k[u'RouteTableId'],k[u'Main'])

def list_subnets(vpc_id):
  vpc = ec2res.Vpc(vpc_id)
  subnet_list = vpc.subnets.all()
  print "%-30s %-20s %-20s %-20s %-10s" %("subnet_id","CIDR","AZ","Available_Pvt_IP","Public_Subnet?")
  for i in subnet_list:
    subnet = ec2res.Subnet(i.id)
    print "%-30s %-20s %-20s %-20s %-10s" %(i.id,subnet.cidr_block,subnet.availability_zone,subnet.available_ip_address_count, subnet.map_public_ip_on_launch)


def subnet_details(subnet_id):
  subnet = ec2res.Subnet(subnet_id)
  print "subnet AZ :",subnet.availability_zone
  print "subnet CIDR :",subnet.cidr_block

def describe_security_groups(vpc_id):
  response = ec2cli.describe_security_groups()
  for i in response['SecurityGroups']:
     #print i
     if i['VpcId'] == vpc_id:
       print "\n%s %-20s %-20s %-10s" %("SG Name:",i['GroupName'],i['GroupId'],i['VpcId'])
       print "Inbound Rules"
       for j in i['IpPermissions']:
          print "%s" %(j)
       print "Outbound (Egress) Rules"
       for k in i['IpPermissionsEgress']:
          print "%s" %(k)
       #security_group = ec2res.SecurityGroup(i['GroupId'])
       #print "Inbound Rules"
       #print "%-50s" %(security_group.ip_permissions)
       #print "Outbound Rules"
       #print "%-50s" %(security_group.ip_permissions_egress)



def menu():
   menu_str = """Select from the following:
   VPC
     1. List AZs
     2. List VPCs
     5. List VPC route table(s) for a VPC and route entries
     3. List subnets in a VPC
     4. List details about a subnet
   SG
    10. List Security Groups
   EXIT
     0. Exit"""
   print(menu_str)
   choice = int(raw_input("Enter Choice:"))
   return choice

while True:
  choice = menu()
  if choice == 1:
    describe_az()
  elif choice == 2:
    describe_vpcs()
  elif choice == 5:
    vpc_id = raw_input("enter vpc id:")
    list_vpc_route_tables(vpc_id)
  elif choice == 3:
    vpc_id = raw_input("enter vpc id:")
    list_subnets(vpc_id)
  elif choice == 4:
    subnet_id = raw_input("enter subnet id:")
    subnet_details(subnet_id)
  elif choice == 10:
    vpc_id = raw_input("enter vpc id:")
    describe_security_groups(vpc_id)
  elif choice == 0:
    break
