from ksdf_netconf import *

def set_ksdf_telemetry_configure(enabled):
    if enabled:
        rpc = """<configure-telemetry-system xmlns="urn:kaloom:faas:fabrics-telemetry">
    <enabled> true </enabled>
    </configure-telemetry-system>"""
    else:
        rpc = """<configure-telemetry-system xmlns="urn:kaloom:faas:fabrics-telemetry">
    <enabled> false </enabled>
    </configure-telemetry-system>"""
    if 'ok' in kaloom_netconf_rpc(rpc):
        return {'ok': True}
    else: 
        return {'ok': False}

def set_ksdf_telemetry_add_flow(flow_name, priority_num, ethernet_num, sample_percentage, cidr):
    rpc="""<configure-telemetry-flow xmlns="urn:kaloom:faas:fabrics-telemetry">
  <name>{flow_name}</name>
  <priority>{prior_num}</priority>
  <ethernet-type>{eth_num}</ethernet-type>
  <destination-address-prefix>{cidr}</destination-address-prefix>
  <exclude-filter>false</exclude-filter>
  <sample-percentage>{sample_perc}</sample-percentage>
</configure-telemetry-flow>""".format(flow_name=flow_name, prior_num=priority_num, cidr=cidr,
                                      eth_num=ethernet_num, sample_perc=sample_percentage)
    try:
        res=kaloom_netconf_rpc(rpc)
        if 'ok' in res: 
            return {'ok': True}
        else: 
            return {'ok': False}
    except:
        print({"error":True})
        return {'error': "something's wrong"}

def set_ksdf_telemetry_remove_flow(flow_name):
    rpc="""<remove-telemetry-flow xmlns="urn:kaloom:faas:fabrics-telemetry">
      <name>{flow_name}</name>
    </remove-telemetry-flow>""".format(flow_name=flow_name)

    try:
        res=kaloom_netconf_rpc(rpc)
        if 'ok' in (res):
            return {"ok": True}
        else:
            return {"ok": False}
    except:
        return({"error":True})
