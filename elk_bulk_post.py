import requests
import json
from time import time
import re

url = 'http://192.168.15.140:9200/'

def bulk_post_ksdf_metric_to_els(rate_dict):
    try:
        pattern_sw='sw*'
        pattern2='[0-9]+[0-9]*'
        found_list=[]
       
        #metric_data=requests.get(url="http://192.168.15.131:8000/api/ksdf/packet_counter/per_tp")
        #rate_dict=metric_data.json()['cur_pkt_rate']
        doc_list=[]
        port_ag_dict={}
        for sw_id in rate_dict:
            port_ag_dict[sw_id]={}
            for port_id in rate_dict[sw_id]:
                cur_metric_dict=rate_dict[sw_id][port_id]

                if re.match(pattern_sw, port_id):
                    ag_port_id="sw%sp%s" % tuple(re.findall(pattern2, port_id)[0:2])
                    #print(ag_port_id)
                else:
                    ag_port_id=port_id
                
                if not ag_port_id in port_ag_dict:
                    port_ag_dict[sw_id][ag_port_id]={
                    "@timestamp":int(time()*1000),
                    "sw_id":sw_id,
                    "port_id":ag_port_id,
                    "rx_bytes":cur_metric_dict['RxBytes'],
                    "rx_packets":cur_metric_dict['RxPackets'],
                    "drop_bytes":cur_metric_dict['DroppedBytes'],
                    "tx_bytes":cur_metric_dict['TxBytes'],
                    "tx_packets":cur_metric_dict['TxPackets'],
                    "drop_packets":cur_metric_dict['DroppedPackets']
                    }
                else:
                    cur_port_ag_dict=port_ag_dict[sw_id][ag_port_id]
                    cur_port_ag_dict={
                        "@timestamp":int(time()*1000),
                        "sw_id": sw_id,
                        "port_id": ag_port_id,
                        "rx_bytes": cur_port_ag_dict["rx_bytes"] + cur_metric_dict['RxBytes'],
                        "rx_packets": cur_port_ag_dict["rx_packets"] + cur_metric_dict['RxPackets'],
                        "drop_bytes": cur_port_ag_dict["drop_bytes"] + cur_metric_dict['DroppedBytes'],
                        "tx_bytes": cur_port_ag_dict["tx_bytes"] + cur_metric_dict['TxBytes'],
                        "tx_packets": cur_port_ag_dict["tx_packets"] + cur_metric_dict['TxPackets'],
                        "drop_packets": cur_port_ag_dict["drop_packets"] + cur_metric_dict['DroppedPackets']
                    }
        for sw_id in port_ag_dict:
            for ag_port_id in port_ag_dict[sw_id]:
                doc_list.append(port_ag_dict[sw_id][ag_port_id])
        
        #print(doc_list)
        json_str=""
        metric_str=json.dumps({"index":{"_index":"ksdf_metric_idx_creation"}})
        for doc in doc_list:
            doc_str=json.dumps(doc)
            json_str=json_str + metric_str + '\n' + doc_str + '\n'
        #print(json_str)
    except:
        return({"error":"sth is wrong with the metric data"})
    try:
        x=requests.post(url + '/_bulk', headers={"Content-Type": "application/x-ndjson"}, data=json_str)
        return x.json()
    except:
        return({"error":"sth is wrong with the bulk posting to els"})