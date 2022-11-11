import openstack

###Openstack SDK Connection 
conn = openstack.connect(cloud='admin')

def ostck_topology_servers_on_hosts():
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