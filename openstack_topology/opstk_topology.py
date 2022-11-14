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

def live_migrate(vm_id, host=None):
    #vm_id="2ae44f46-7f04-4280-87f7-0fdf10f75a29"
    #mg_result=conn.compute.live_migrate_server("2ae44f46-7f04-4280-87f7-0fdf10f75a29", host="compute1.forwiz-os.com", force=False, block_migration=None)
    try:
        mg_result=conn.compute.live_migrate_server(vm_id, host=host, force=False, block_migration=None)
        return {"ok":True}
    except openstack.exceptions.BadRequestException as err:
        return {"error":err}
    except openstack.exceptions.ResourceNotFound as err:
        return(err)
    except:
        return {"error": "something's not okay"}

    #https://www.mirantis.com/blog/block-live-migration-openstack-environment/ 
    #https://docs.openstack.org/openstacksdk/latest/user/proxies/compute.html
    print(mg_result)