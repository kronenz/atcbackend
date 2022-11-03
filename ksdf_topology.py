from ksdf_netconf import *

#Kaloom Topology Graph 관련

def get_ksdf_all_nodes_info_oper():
    rpc="""<get><filter type="subtree"><top xmlns="urn:kaloom:faas:fabrics"/>
            <Fabric><FabricID>123</FabricID><Node><Name/><Role/><DeviceID/><DeviceMAC/><OperState>UP</OperState><System/></Node></Fabric>
        </filter></get>""" 
    return kaloom_netconf_rpc(rpc)['data']['top']['fabrics:Fabric']

def get_ksdf_all_tp_oper():
    rpc="""<get><filter type="subtree"><top xmlns="urn:kaloom:faas:fabrics"/><Fabric><FabricID>123</FabricID>
        <Node><Role></Role><TerminationPoint><OperState>UP</OperState></TerminationPoint></Node></Fabric></filter></get>""" 
    return kaloom_netconf_rpc(rpc)['data']['top']['fabrics:Fabric']

def get_ksdf_min_nodes_dict():
    reg_nodes_dict={}
    nodes_dict=get_ksdf_all_nodes_info_oper()['fabrics:Node']
    for node in nodes_dict: 
        f_name=node['fabrics:Name']
        f_node_id=node['fabrics:NodeID']
        f_role=node['fabrics:Role']
        reg_nodes_dict[f_node_id]=(f_name,f_role)
    return reg_nodes_dict

def get_ksdf_topology_node_link():
    nodes_dict=get_ksdf_min_nodes_dict()
    link_dict={'fabric_link': [], 'user_link': []}

    tp_oper=get_ksdf_all_tp_oper()

    for node in tp_oper['fabrics:Node']:
        node_id = node['fabrics:NodeID']
        for tp in node['fabrics:TerminationPoint']:
            tp_id=tp['fabrics:TpID']
            assign_state=tp['fabrics:AssignmentState']
            lldp_info=get_lldp_info(tp)
            if assign_state == 'FABRIC_PORT':
                link_dict['fabric_link'].append({'src': (node_id, tp_id), 'dst': (lldp_info['LLDP:SystemName'],lldp_info['LLDP:PortID']), 'detail': lldp_info})
            elif assign_state =="USER_PORT":
                link_dict['user_link'].append({'detail':lldp_info})
            else: 
                #print(assign_state)
                #print("what's this?")
                pass
    topology_dict={'node_dict':nodes_dict, 'link_dict':link_dict}
    return topology_dict

def get_nodes_infos(reg_nodes_dict, node_id):
    return reg_nodes_dict[node_id]

def get_lldp_info(tp):
    if 'fabrics:TPAnnotations' in tp:
        anno_dict={}
        tp_annos=tp['fabrics:TPAnnotations']
        for anno in tp_annos:
            if type(anno) == str:
                anno_dict[tp_annos['fabrics:TheKey']]=tp_annos['fabrics:Value']
            else:
                anno_dict[anno['fabrics:TheKey']]=anno['fabrics:Value']
        return anno_dict