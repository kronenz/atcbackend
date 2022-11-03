from ksdf_netconf import *
import time

#Kaloom Packet Counter 관련

#const
counter_name_itrst=['RxBytes', 'TxBytes','DroppedBytes', 'RxPackets', 'TxPackets','DroppedPackets', 'Timestamp']

#functions
def get_ksdf_all_packet_counters():
    rpc = """<GetPacketCounters xmlns="urn:kaloom:faas:fabrics"></GetPacketCounters>"""
    return kaloom_netconf_rpc(rpc)['fabrics:Results']

def ksdf_all_node_tp_ids_oper():
    tp_dict={}
    rpc="""<get><filter type="subtree"><top xmlns="urn:kaloom:faas:fabrics"/><Fabric><FabricID>123</FabricID>
<Node><Role></Role><TerminationPoint><OperState>UP</OperState><TpID/></TerminationPoint></Node></Fabric></filter></get>""" 
    tp_oper=kaloom_netconf_rpc(rpc)['data']['top']['fabrics:Fabric']['fabrics:Node']
    for node in tp_oper:
        node_id=node['fabrics:NodeID']
        tp_dict[node_id]=[]
        for tp in node['fabrics:TerminationPoint']:
            tp_dict[node_id].append(tp['fabrics:TpID'])
    return tp_dict

global_tps=ksdf_all_node_tp_ids_oper()

def update_global_tps():
    ksdf_all_node_tp_ids_oper()

def get_cur_counter():
    counters=get_ksdf_all_packet_counters()

    counter_dict={}

    for counter in counters:
        node_id = counter['fabrics:NodeID']
        tp_id = counter['fabrics:TpID']
        if tp_id in global_tps[node_id]:
            if not node_id in counter_dict:
                counter_dict[node_id]={'ports':{}}
            if not tp_id in counter_dict[node_id]['ports']:
                counter_dict[node_id]['ports'][tp_id]={}
            for counter_name in counter_name_itrst:
                counter_dict[node_id]['ports'][tp_id][counter_name]=counter['fabrics:' + counter_name]
    return counter_dict

def get_counter_diff(counter1, counter2):
    diff_dict={}
    for node_id in global_tps:
        diff_dict[node_id]={}
        for tp in global_tps[node_id]:
            diff_dict[node_id][tp]={}
            for counter_name in counter_name_itrst:
                diff_dict[node_id][tp][counter_name]=int(counter1[node_id]['ports'][tp][counter_name])-int(counter2[node_id]['ports'][tp][counter_name])
    return (diff_dict)

def get_counter_rate(time_interval):
    counters=get_ksdf_all_packet_counters()
    cur_counter=get_cur_counter(global_tps)
    time.sleep(time_interval)
    counters=get_ksdf_all_packet_counters()
    cur_counter2=get_cur_counter(global_tps)
    gcd=get_counter_diff(global_tps,cur_counter,cur_counter2)

def get_rate_from_gcd(gcd):
    gcd_rate_dict={}
    for node_id in global_tps:
        gcd_rate_dict[node_id]={}
        for tp in global_tps[node_id]:
            gcd_rate_dict[node_id][tp]={}
            timestamp_delta=gcd[node_id][tp]['Timestamp']/1E9
            for counter in counter_name_itrst[:-1]:
                gcd_rate_dict[node_id][tp][counter]=gcd[node_id][tp][counter]/timestamp_delta
    return gcd_rate_dict