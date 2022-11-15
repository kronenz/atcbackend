import openstack
conn = openstack.connect(cloud='admin')

#ports on vms
def get_ports_on_servers():
    vm_id_dict={}
    for server in conn.compute.servers(all_projects=True):
        vm_info=server.to_dict()
        vm_id=vm_info['id']
        vm_id_dict[vm_id]={'name':vm_info['name'], 'ports': []}

    ports=conn.network.ports()
    for port in ports: 
        dev_id=port['device_id']
        if dev_id in vm_id_dict:
            port_id=port['id']
            port_ip=port['fixed_ips'][0]['ip_address']
            port_subnet=port['fixed_ips'][0]['subnet_id']
            port_network_id=port['network_id']
            port_info={"id": port_id,
                    "ip": port_ip,
                    "subnet_id": port_subnet,
                    "net_id": port_network_id}
            vm_id_dict[dev_id]['ports'].append(port_info)
            #pp.pprint((dev_id, vm_id_dict[dev_id]['name']))
        else:
            pass
    
    return vm_id_dict

def get_subnets_on_networks():
    networks=conn.network.networks()
    subnets=conn.network.subnets()

    network_dict={}
    subnet_dict={}

    for subnet in subnets:
        subnet_id=subnet['id']
        subnet_cidr=subnet['cidr']
        subnet_name=subnet['name']
        subnet_gw=subnet['gateway_ip']
        
        subnet_dict[subnet_id]={}
        subnet_dict[subnet_id]['cidr']=subnet_cidr
        subnet_dict[subnet_id]['name']=subnet_name
        subnet_dict[subnet_id]['gw']=subnet_gw

    for network in networks: 
        network_id=network['id']
        network_location=network['location']
        network_name=network['name']
        network_subnet_list=network['subnet_ids']
        
        network_dict[network_id]={}
        cur_dict=network_dict[network_id]
        cur_dict['name']=network_name
        cur_dict['location']=network_location
        cur_dict['subnet_dict']={}
        for subnet_id in network_subnet_list:
            subnet_info=subnet_dict[subnet_id]
            cur_dict['subnet_dict'][subnet_id]=subnet_info
    
    return network_dict
