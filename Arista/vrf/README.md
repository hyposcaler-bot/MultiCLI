# SR Linux Custom CLI plugins for Arista EOS VRF Commands

This section contains SR Linux custom CLI python scripts for the following Arista EOS VRF show commands.

Refer to the **Details** section for outputs using the standard SR Linux command and the custom CLI plugin.

Use the **Lab** to test the custom CLI plugin. The lab comes with options to configure EVPN by following a step-by-step guide or [deploy a fully configured EVPN fabric](https://github.com/srlinuxamericas/N92-evpn/blob/main/README.md#explore-this-lab-with-everything-pre-configured).

|   |   |   |   |
|---|---|---|---|
| `show ip route vrf <vrf-name>` | [Details](#show-ip-route-vrf) | [Script]() | [Lab](https://github.com/srlinuxamericas/N92-evpn) |

## show ip route vrf

The standard SR Linux command to display VRF (network instance) route table is:

```srl
show network-instance ip-vrf-1 route-table
```

Expected output:

```srl
-----------------------------------------------------------------------------------------------------------------------------------------------------------------
IPv4 unicast route table of network instance ip-vrf-1
-----------------------------------------------------------------------------------------------------------------------------------------------------------------
+------------------+------+-----------+--------------------+---------+---------+--------+-----------+------------+------------+------------+---------------+
|      Prefix      |  ID  |   Route   |    Route Owner     | Active  | Origin  | Metric |   Pref    |  Next-hop  |  Next-hop  |   Backup   | Backup Next-  |
|                  |      |   Type    |                    |         | Network |        |           |   (Type)   | Interface  |  Next-hop  | hop Interface |
|                  |      |           |                    |         | Instanc |        |           |            |            |   (Type)   |               |
|                  |      |           |                    |         |    e    |        |           |            |            |            |               |
+==================+======+===========+====================+=========+=========+========+===========+============+============+============+===============+
| 10.80.1.0/24     | 3    | local     | net_inst_mgr       | True    | ip-     | 0      | 0         | 10.80.1.2  | ethernet-  |            |               |
|                  |      |           |                    |         | vrf-1   |        |           | (direct)   | 1/11.0     |            |               |
| 10.80.1.2/32     | 3    | host      | net_inst_mgr       | True    | ip-     | 0      | 0         | None       | None       |            |               |
|                  |      |           |                    |         | vrf-1   |        |           | (extract)  |            |            |               |
| 10.80.1.255/32   | 3    | host      | net_inst_mgr       | True    | ip-     | 0      | 0         | None (broa |            |            |               |
|                  |      |           |                    |         | vrf-1   |        |           | dcast)     |            |            |               |
| 10.90.1.0/24     | 0    | bgp-evpn  | bgp_evpn_mgr       | True    | ip-     | 0      | 170       | 2.2.2.2/32 |            |            |               |
|                  |      |           |                    |         | vrf-1   |        |           | (indirect/ |            |            |               |
|                  |      |           |                    |         |         |        |           | vxlan)     |            |            |               |
+------------------+------+-----------+--------------------+---------+---------+--------+-----------+------------+------------+------------+---------------+
-----------------------------------------------------------------------------------------------------------------------------------------------------------------
IPv4 routes total                    : 4
IPv4 prefixes with active routes     : 4
IPv4 prefixes with active ECMP routes: 0
-----------------------------------------------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------------------------------------------
IPv6 unicast route table of network instance ip-vrf-1
-----------------------------------------------------------------------------------------------------------------------------------------------------------------
+------------------+------+-----------+--------------------+---------+---------+--------+-----------+------------+------------+------------+---------------+
|      Prefix      |  ID  |   Route   |    Route Owner     | Active  | Origin  | Metric |   Pref    |  Next-hop  |  Next-hop  |   Backup   | Backup Next-  |
|                  |      |   Type    |                    |         | Network |        |           |   (Type)   | Interface  |  Next-hop  | hop Interface |
|                  |      |           |                    |         | Instanc |        |           |            |            |   (Type)   |               |
|                  |      |           |                    |         |    e    |        |           |            |            |            |               |
+==================+======+===========+====================+=========+=========+========+===========+============+============+============+===============+
| 10:80:1::/64     | 3    | local     | net_inst_mgr       | True    | ip-     | 0      | 0         | 10:80:1::2 | ethernet-  |            |               |
|                  |      |           |                    |         | vrf-1   |        |           | (direct)   | 1/11.0     |            |               |
| 10:80:1::2/128   | 3    | host      | net_inst_mgr       | True    | ip-     | 0      | 0         | None       | None       |            |               |
|                  |      |           |                    |         | vrf-1   |        |           | (extract)  |            |            |               |
| 10:90:1::/64     | 0    | bgp-evpn  | bgp_evpn_mgr       | True    | ip-     | 0      | 170       | 2.2.2.2/32 |            |            |               |
|                  |      |           |                    |         | vrf-1   |        |           | (indirect/ |            |            |               |
|                  |      |           |                    |         |         |        |           | vxlan)     |            |            |               |
+------------------+------+-----------+--------------------+---------+---------+--------+-----------+------------+------------+------------+---------------+
-----------------------------------------------------------------------------------------------------------------------------------------------------------------
IPv6 routes total                    : 3
IPv6 prefixes with active routes     : 3
IPv6 prefixes with active ECMP routes: 0
-----------------------------------------------------------------------------------------------------------------------------------------------------------------
```

We will be using CLI alias for the equivalent EOS command.

```srl
```


Let's take a look the custom CLI plugin output. The command is:

```srl

```

Expected output:

```srl

```
