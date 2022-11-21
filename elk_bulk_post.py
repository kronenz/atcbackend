import requests
import json
from time import time

url = 'http://192.168.15.140:9200/'

def bulk_post_ksdf_metric_to_els(rate_dict):
    try:
        #metric_data=requests.get(url="http://192.168.15.131:8000/api/ksdf/packet_counter/per_tp")
        #rate_dict=metric_data.json()['cur_pkt_rate']
        doc_list=[]
        for sw_id in rate_dict:
            for port_id in rate_dict[sw_id]:
                cur_metric_dict=rate_dict[sw_id][port_id]
                cur_doc={
                    "@timestamp":str(int(time())),
                    "sw_id":sw_id,
                    "port_id":port_id,
                    "rx_bytes":cur_metric_dict['RxBytes'],
                    "rx_packets":cur_metric_dict['RxPackets'],
                    "drop_bytes":cur_metric_dict['DroppedBytes'],
                    "tx_bytes":cur_metric_dict['TxBytes'],
                    "tx_packets":cur_metric_dict['TxPackets'],
                    "drop_packets":cur_metric_dict['DroppedPackets']
                }
                doc_list.append(cur_doc)
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