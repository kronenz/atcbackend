import openstack

###Openstack SDK Connection 
conn = openstack.connect(cloud='admin')

def get_ostck_topology_servers_on_hosts():
    host_server_dict={}
    for server in conn.compute.servers(all_projects=True):
        server_info=server.to_dict()
        server_sum = {
            "name":server_info['name'],
            "vm_id":server_info['id'],
            "vm_state":server_info['vm_state'],
            "location":server_info['location'],
            "addresses":server_info['addresses'],
            #"hostname":server_info['hostname'],
            #"host_id":server_info['host_id']
        }
        host=server_info["compute_host"]
        if host not in host_server_dict:
            host_server_dict[host]=[]
        host_server_dict[host].append(server_sum)
    return host_server_dict

def get_ostck_topology_server_info(server_id):
    try:
        server_info=conn.compute.get_server(server_id)
    except: 
        server_info={"error":"cannot fetch the server info"}
    return server_info

def get_ostck_topology_hypervisors_info(details=False):
    hypervisor_array=[]
    for hypervisor in conn.compute.hypervisors(details=details):
        hypervisor_info=hypervisor.to_dict()
        hypervisor_array.append(hypervisor)
    return hypervisor_array

