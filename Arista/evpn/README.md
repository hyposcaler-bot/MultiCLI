# SR Linux Custom CLI plugins for Arista EOS EVPN Commands

This section contains SR Linux custom CLI python scripts for the following Arista EOS EVPN show commands.

Refer to the **Details** section for outputs using the standard SR Linux command and the custom CLI plugin.

Use the **Lab** to test the custom CLI plugin. The lab comes with options to configure EVPN by following a step-by-step guide or [deploy a fully configured EVPN fabric](https://github.com/srlinuxamericas/N92-evpn/blob/main/README.md#explore-this-lab-with-everything-pre-configured).

|   |   |   |   |
|---|---|---|---|
| `show mac address-table` | [Details]() | [Script]() | [Lab](https://github.com/srlinuxamericas/N92-evpn) |
| `show vxlan address-table` | [Details]() | [Script]() | [Lab](https://github.com/srlinuxamericas/N92-evpn) |
| `show bgp evpn route-type mac-ip` | [Details](#show-bgp-evpn-route-type-mac-ip) | [Script](A_show_bgp_evpn.py) | [Lab](https://github.com/srlinuxamericas/N92-evpn) |
| `show bgp evpn route-type imet` | [Details](#show-bgp-evpn-route-type-imet) | [Script](A_show_bgp_evpn.py) | [Lab](https://github.com/srlinuxamericas/N92-evpn) |
| `show bgp evpn route-type ip-prefix` | [Details](#show-bgp-evpn-route-type-ip-prefix) | [Script](A_show_bgp_evpn.py) | [Lab](https://github.com/srlinuxamericas/N92-evpn) |
| `show bgp evpn summary` | [Details](#show-bgp-evpn-summary) | [Script](A_show_bgp_evpn.py) | [Lab](https://github.com/srlinuxamericas/N92-evpn) |

## show mac address-table


## show vxlan address-table


## show bgp evpn route-type mac-ip

The standard SR Linux command to display EVPN Route Type 2 (MAC-IP) is:

```srl
show network-instance default protocols bgp routes evpn route-type 2 summary
```

Expected output:

```srl
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Show report for the BGP route table of network-instance "default"
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Status codes: u=used, *=valid, >=best, x=stale
Origin codes: i=IGP, e=EGP, ?=incomplete
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
BGP Router ID: 1.1.1.1      AS: 64501      Local AS: 64501
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Type 2 MAC-IP Advertisement Routes
+--------+------------------+------------+-------------------+------------------+------------------+------------------+------------------+--------------------------------+------------------+
| Status |      Route-      |   Tag-ID   |    MAC-address    |    IP-address    |     neighbor     |     Next-Hop     |      Label       |              ESI               |   MAC Mobility   |
|        |  distinguisher   |            |                   |                  |                  |                  |                  |                                |                  |
+========+==================+============+===================+==================+==================+==================+==================+================================+==================+
| u*>    | 2.2.2.2:100      | 0          | AA:C1:AB:FF:E1:F2 | 0.0.0.0          | 2.2.2.2          | 2.2.2.2          | 100              | 00:00:00:00:00:00:00:00:00:00  | -                |
| *      | 2.2.2.2:100      | 0          | AA:C1:AB:FF:E1:F2 | 0.0.0.0          | 2001::2          | 2.2.2.2          | 100              | 00:00:00:00:00:00:00:00:00:00  | -                |
+--------+------------------+------------+-------------------+------------------+------------------+------------------+------------------+--------------------------------+------------------+
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
2 MAC-IP Advertisement routes 1 used, 2 valid
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
```

With the custom CLI plugin, we are removing the `Label`, `ESI`, and `MAC Mobility` columns and adding `VRF`, `Local-Pref` and `Origin` columns.

For the command syntax, we will follow the EOS command with the option to add `vrf` name at the end that equates to `network-instance` in SR Linux. An unnamed argument to filter on a specific `mac-address` is also added.

Since specifying `vrf` is optional, by default, the command will search for routes in all VRFs (network instances) and the `VRF` column in the output helps to identify the VRF name of each route.

The custom CLI command help section (type `?` to display help) looks like:

```srl
A:leaf1# show bgp evpn route-type mac-ip ?
usage: mac-ip [<mac-address>] [vrf <value>]

Positional arguments:
  mac-address       MAC address

Named arguments:
  vrf               network instance name
```


Let's take a look the custom CLI plugin output. The command is:

```srl
show bgp evpn route-type mac-ip
```

Expected output:

```srl
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Show report for the BGP route table of network-instance "*"
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Status codes: u=used, *=valid, >=best, x=stale
Origin codes: i=IGP, e=EGP, ?=incomplete
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
BGP Router ID: 1.1.1.1      AS: 64501      Local AS: 64501
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Type 2 MAC-IP Advertisement Routes
+----------------------+--------+----------------------+-------------------+----------------------+----------------------+----------------------+----------------------+----------------------+
|         VRF          | Status | Route-distinguisher  |    MAC-address    |      IP-address      |       Neighbor       |       Next-Hop       |      Local-Pref      |        Origin        |
+======================+========+======================+===================+======================+======================+======================+======================+======================+
| default              | u*>    | 2.2.2.2:100          | AA:C1:AB:FF:E1:F2 | 0.0.0.0              | 2.2.2.2              | 2.2.2.2              | 100                  | igp                  |
| default              | *      | 2.2.2.2:100          | AA:C1:AB:FF:E1:F2 | 0.0.0.0              | 2001::2              | 2.2.2.2              | 100                  | igp                  |
+----------------------+--------+----------------------+-------------------+----------------------+----------------------+----------------------+----------------------+----------------------+
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
2 MAC-IP Advertisement routes 1 used, 2 valid
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
```

As you can see, the new columns `VRF`, `Local-Pref` and `Origin` are now displayed.

Optionally you may also run:
- `show bgp evpn route-type mac-ip <mac-address>`
- `show bgp evpn route-type mac-ip vrf <vrf-name>`
- `show bgp evpn route-type mac-ip <mac-address> vrf <vrf-name>`

## show bgp evpn route-type imet

The standard SR Linux command to display EVPN Route Type 3 (IMET) is:

```srl
show network-instance default protocols bgp routes evpn route-type 3 summary
```

Expected output:

```srl
------------------------------------------------------------------------------------------------------------------------
Show report for the BGP route table of network-instance "default"
------------------------------------------------------------------------------------------------------------------------
Status codes: u=used, *=valid, >=best, x=stale
Origin codes: i=IGP, e=EGP, ?=incomplete
------------------------------------------------------------------------------------------------------------------------
BGP Router ID: 1.1.1.1      AS: 64501      Local AS: 64501
------------------------------------------------------------------------------------------------------------------------
Type 3 Inclusive Multicast Ethernet Tag Routes
+--------+------------------------+------------+---------------------+------------------------+------------------------+
| Status |  Route-distinguisher   |   Tag-ID   |    Originator-IP    |        neighbor        |        Next-Hop        |
+========+========================+============+=====================+========================+========================+
| u*>    | 2.2.2.2:100            | 0          | 2.2.2.2             | 2.2.2.2                | 2.2.2.2                |
| *      | 2.2.2.2:100            | 0          | 2.2.2.2             | 2001::2                | 2.2.2.2                |
+--------+------------------------+------------+---------------------+------------------------+------------------------+
------------------------------------------------------------------------------------------------------------------------
2 Inclusive Multicast Ethernet Tag routes 1 used, 2 valid
------------------------------------------------------------------------------------------------------------------------+
```

With the custom CLI plugin, we are adding `VRF`, `Local-Pref` and `Origin` columns.

For the command syntax, we will follow the EOS command with the option to add `vrf` name at the end that equates to `network-instance` in SR Linux. An unnamed argument to filter on a specific `origin-router` IP is also added.

Since specifying `vrf` is optional, by default, the command will search for routes in all VRFs (network instances) and the `VRF` column in the output helps to identify the VRF name of each route.

The custom CLI command help section (type `?` to display help) looks like:

```srl
A:leaf1# show bgp evpn route-type imet ?
usage: imet [<origin-router>] [vrf <value>]

Positional arguments:
  origin-router     Originating router IPv4 or IPv6 address

Named arguments:
  vrf               network instance name
```

Let's take a look the custom CLI plugin output. The command is:

```srl
show bgp evpn route-type imet
```

Expected output:

```srl
------------------------------------------------------------------------------------------------------------------------------------------------
Show report for the BGP route table of network-instance "*"
------------------------------------------------------------------------------------------------------------------------------------------------
Status codes: u=used, *=valid, >=best, x=stale
Origin codes: i=IGP, e=EGP, ?=incomplete
------------------------------------------------------------------------------------------------------------------------------------------------
BGP Router ID: 1.1.1.1      AS: 64501      Local AS: 64501
------------------------------------------------------------------------------------------------------------------------------------------------
Type 3 Inclusive Multicast Ethernet Tag Routes
+---------------+--------+---------------+---------------+---------------------+---------------+---------------+---------------+---------------+
|      VRF      | Status |    Route-     |    Tag-ID     |    Originator-IP    |   neighbor    |   Next-Hop    |  Local-Pref   |    Origin     |
|               |        | distinguisher |               |                     |               |               |               |               |
+===============+========+===============+===============+=====================+===============+===============+===============+===============+
| default       | u*>    | 2.2.2.2:100   | 0             | 2.2.2.2             | 2.2.2.2       | 2.2.2.2       | 100           | igp           |
| default       | *      | 2.2.2.2:100   | 0             | 2.2.2.2             | 2001::2       | 2.2.2.2       | 100           | igp           |
+---------------+--------+---------------+---------------+---------------------+---------------+---------------+---------------+---------------+
------------------------------------------------------------------------------------------------------------------------------------------------
2 Inclusive Multicast Ethernet Tag routes 1 used, 2 valid
------------------------------------------------------------------------------------------------------------------------------------------------
```

Optionally you may also run:
- `show bgp evpn route-type imet <origin-ip>`
- `show bgp evpn route-type imet vrf <vrf-name>`
- `show bgp evpn route-type imet <origin-ip> vrf <vrf-name>`

## show bgp evpn route-type ip-prefix

The standard SR Linux command to display EVPN Route Type 5 (ip-prefix) is:

```srl
show network-instance default protocols bgp routes evpn route-type 5 summary
```

Expected output:

```srl
------------------------------------------------------------------------------------------------------------------------------------------------
Show report for the BGP route table of network-instance "default"
------------------------------------------------------------------------------------------------------------------------------------------------
Status codes: u=used, *=valid, >=best, x=stale
Origin codes: i=IGP, e=EGP, ?=incomplete
------------------------------------------------------------------------------------------------------------------------------------------------
BGP Router ID: 1.1.1.1      AS: 64501      Local AS: 64501
------------------------------------------------------------------------------------------------------------------------------------------------
Type 5 IP Prefix Routes
+--------+------------------+------------+---------------------+------------------+------------------+------------------+------------------+
| Status |      Route-      |   Tag-ID   |     IP-address      |     neighbor     |     Next-Hop     |      Label       |     Gateway      |
|        |  distinguisher   |            |                     |                  |                  |                  |                  |
+========+==================+============+=====================+==================+==================+==================+==================+
| u*>    | 2.2.2.2:200      | 0          | 10.90.1.0/24        | 2.2.2.2          | 2.2.2.2          | 200              | 0.0.0.0          |
| *      | 2.2.2.2:200      | 0          | 10.90.1.0/24        | 2001::2          | 2.2.2.2          | 200              | 0.0.0.0          |
| u*>    | 2.2.2.2:200      | 0          | 10:90:1::/64        | 2.2.2.2          | 2.2.2.2          | 200              | ::               |
| *      | 2.2.2.2:200      | 0          | 10:90:1::/64        | 2001::2          | 2.2.2.2          | 200              | ::               |
+--------+------------------+------------+---------------------+------------------+------------------+------------------+------------------+
------------------------------------------------------------------------------------------------------------------------------------------------
4 IP Prefix routes 2 used, 4 valid
------------------------------------------------------------------------------------------------------------------------------------------------
```

With the custom CLI plugin, we are removing `Label`, `Gateway` and adding `VRF`, `Local-Pref` and `Origin` columns.

For the command syntax, we will follow the EOS command with the option to add `vrf` name at the end that equates to `network-instance` in SR Linux. An unnamed argument to filter on a specific `ip-address` is also added.

Since specifying `vrf` is optional, by default, the command will search for routes in all VRFs (network instances) and the `VRF` column in the output helps to identify the VRF name of each route.

The custom CLI command help section (type `?` to display help) looks like:

```srl
A:leaf1# show bgp evpn route-type ip-prefix ?
usage: ip-prefix [<ip-address>] [vrf <value>]

Positional arguments:
  ip-address        IPv4 or IPv6 address prefix

Named arguments:
  vrf               network instance name
```

Let's take a look the custom CLI plugin output. The command is:

```srl
show bgp evpn route-type ip-prefix
```

Expected output:

```srl
------------------------------------------------------------------------------------------------------------------------------------------------
Show report for the BGP route table of network-instance "*"
------------------------------------------------------------------------------------------------------------------------------------------------
Status codes: u=used, *=valid, >=best, x=stale
Origin codes: i=IGP, e=EGP, ?=incomplete
------------------------------------------------------------------------------------------------------------------------------------------------
BGP Router ID: 1.1.1.1      AS: 64501      Local AS: 64501
------------------------------------------------------------------------------------------------------------------------------------------------
Type 5 IP Prefix Routes
+---------------+--------+---------------+---------------+---------------------+---------------+---------------+---------------+---------------+
|      VRF      | Status |    Route-     |    Tag-ID     |     IP-address      |   neighbor    |   Next-Hop    |  Local-Pref   |    Origin     |
|               |        | distinguisher |               |                     |               |               |               |               |
+===============+========+===============+===============+=====================+===============+===============+===============+===============+
| default       | u*>    | 2.2.2.2:200   | 0             | 10.90.1.0/24        | 2.2.2.2       | 2.2.2.2       | 100           | igp           |
| default       | *      | 2.2.2.2:200   | 0             | 10.90.1.0/24        | 2001::2       | 2.2.2.2       | 100           | igp           |
| default       | u*>    | 2.2.2.2:200   | 0             | 10:90:1::/64        | 2.2.2.2       | 2.2.2.2       | 100           | igp           |
| default       | *      | 2.2.2.2:200   | 0             | 10:90:1::/64        | 2001::2       | 2.2.2.2       | 100           | igp           |
+---------------+--------+---------------+---------------+---------------------+---------------+---------------+---------------+---------------+
------------------------------------------------------------------------------------------------------------------------------------------------
4 IP Prefix routes 2 used, 4 valid
------------------------------------------------------------------------------------------------------------------------------------------------
```

Optionally you may also run:
- `show bgp evpn route-type ip-prefix <ip-address>`
- `show bgp evpn route-type ip-prefix vrf <vrf-name>`
- `show bgp evpn route-type ip-prefix <ip-address> vrf <vrf-name>`

## show bgp evpn summary

The standard SR Linux command to display EVPN Route Type summary is:

```srl
show network-instance default protocols bgp routes evpn route-type summary
```

Expected output:

```srl
------------------------------------------------------------------------------------------------------------------------------------------------
Show report for the BGP route table of network-instance "default"
------------------------------------------------------------------------------------------------------------------------------------------------
Status codes: u=used, *=valid, >=best, x=stale
Origin codes: i=IGP, e=EGP, ?=incomplete
------------------------------------------------------------------------------------------------------------------------------------------------
BGP Router ID: 1.1.1.1      AS: 64501      Local AS: 64501
------------------------------------------------------------------------------------------------------------------------------------------------
Type 2 MAC-IP Advertisement Routes
+-------+------------+----------+----------------+------------+------------+------------+------------+---------------------------+------------+
| Statu | Route-dist |  Tag-ID  |  MAC-address   | IP-address |  neighbor  |  Next-Hop  |   Label    |            ESI            |    MAC     |
|   s   | inguisher  |          |                |            |            |            |            |                           |  Mobility  |
+=======+============+==========+================+============+============+============+============+===========================+============+
| u*>   | 2.2.2.2:10 | 0        | AA:C1:AB:FF:E1 | 0.0.0.0    | 2.2.2.2    | 2.2.2.2    | 100        | 00:00:00:00:00:00:00:00:0 | -          |
|       | 0          |          | :F2            |            |            |            |            | 0:00                      |            |
| *     | 2.2.2.2:10 | 0        | AA:C1:AB:FF:E1 | 0.0.0.0    | 2001::2    | 2.2.2.2    | 100        | 00:00:00:00:00:00:00:00:0 | -          |
|       | 0          |          | :F2            |            |            |            |            | 0:00                      |            |
+-------+------------+----------+----------------+------------+------------+------------+------------+---------------------------+------------+
------------------------------------------------------------------------------------------------------------------------------------------------
Type 3 Inclusive Multicast Ethernet Tag Routes
+--------+--------------------------------+------------+---------------------+--------------------------------+--------------------------------+
| Status |      Route-distinguisher       |   Tag-ID   |    Originator-IP    |            neighbor            |            Next-Hop            |
+========+================================+============+=====================+================================+================================+
| u*>    | 2.2.2.2:100                    | 0          | 2.2.2.2             | 2.2.2.2                        | 2.2.2.2                        |
| *      | 2.2.2.2:100                    | 0          | 2.2.2.2             | 2001::2                        | 2.2.2.2                        |
+--------+--------------------------------+------------+---------------------+--------------------------------+--------------------------------+
------------------------------------------------------------------------------------------------------------------------------------------------
Type 5 IP Prefix Routes
+--------+------------------+------------+---------------------+------------------+------------------+------------------+------------------+
| Status |      Route-      |   Tag-ID   |     IP-address      |     neighbor     |     Next-Hop     |      Label       |     Gateway      |
|        |  distinguisher   |            |                     |                  |                  |                  |                  |
+========+==================+============+=====================+==================+==================+==================+==================+
| u*>    | 2.2.2.2:200      | 0          | 10.90.1.0/24        | 2.2.2.2          | 2.2.2.2          | 200              | 0.0.0.0          |
| *      | 2.2.2.2:200      | 0          | 10.90.1.0/24        | 2001::2          | 2.2.2.2          | 200              | 0.0.0.0          |
| u*>    | 2.2.2.2:200      | 0          | 10:90:1::/64        | 2.2.2.2          | 2.2.2.2          | 200              | ::               |
| *      | 2.2.2.2:200      | 0          | 10:90:1::/64        | 2001::2          | 2.2.2.2          | 200              | ::               |
+--------+------------------+------------+---------------------+------------------+------------------+------------------+------------------+
------------------------------------------------------------------------------------------------------------------------------------------------
0 Ethernet Auto-Discovery routes 0 used, 0 valid
2 MAC-IP Advertisement routes 1 used, 2 valid
2 Inclusive Multicast Ethernet Tag routes 1 used, 2 valid
0 Ethernet Segment routes 0 used, 0 valid
4 IP Prefix routes 2 used, 4 valid
0 Selective Multicast Ethernet Tag routes 0 used, 0 valid
0 Selective Multicast Membership Report Sync routes 0 used, 0 valid
0 Selective Multicast Leave Sync routes 0 used, 0 valid
------------------------------------------------------------------------------------------------------------------------------------------------
```

With the custom CLI plugin, we are adding `VRF`, `Local-Pref` and `Origin` columns for route types.

For the command syntax, we will follow the EOS command with the option to add `vrf` name at the end that equates to `network-instance` in SR Linux.

Since specifying `vrf` is optional, by default, the command will search for routes in all VRFs (network instances) and the `VRF` column in the output helps to identify the VRF name of each route.

The custom CLI command help section (type `?` to display help) looks like:

```srl
A:leaf1# show bgp evpn summary ?
usage: summary [vrf <value>]

Show all EVPN Route Types

Named arguments:
  vrf               network instance (VRF) name
```

Let's take a look the custom CLI plugin output. The command is:

```srl
show bgp evpn summary
```

Expected output:

```srl
-----------------------------------------------------------------------------------------------------------------------------------------------------------------
Show report for the BGP route table of network-instance "*"
-----------------------------------------------------------------------------------------------------------------------------------------------------------------
Status codes: u=used, *=valid, >=best, x=stale
Origin codes: i=IGP, e=EGP, ?=incomplete
-----------------------------------------------------------------------------------------------------------------------------------------------------------------
BGP Router ID: 1.1.1.1      AS: 64501      Local AS: 64501
-----------------------------------------------------------------------------------------------------------------------------------------------------------------
Type 2 MAC-IP Advertisement Routes
+-----------------+--------+-----------------+-------------------+-----------------+-----------------+-----------------+-----------------+-----------------+
|       VRF       | Status |     Route-      |    MAC-address    |   IP-address    |    Neighbor     |    Next-Hop     |   Local-Pref    |     Origin      |
|                 |        |  distinguisher  |                   |                 |                 |                 |                 |                 |
+=================+========+=================+===================+=================+=================+=================+=================+=================+
| default         | u*>    | 2.2.2.2:100     | AA:C1:AB:FF:E1:F2 | 0.0.0.0         | 2.2.2.2         | 2.2.2.2         | 100             | igp             |
| default         | *      | 2.2.2.2:100     | AA:C1:AB:FF:E1:F2 | 0.0.0.0         | 2001::2         | 2.2.2.2         | 100             | igp             |
+-----------------+--------+-----------------+-------------------+-----------------+-----------------+-----------------+-----------------+-----------------+
-----------------------------------------------------------------------------------------------------------------------------------------------------------------
Type 3 Inclusive Multicast Ethernet Tag Routes
+-----------------+--------+-----------------+-----------------+---------------------+-----------------+-----------------+-----------------+-----------------+
|       VRF       | Status |     Route-      |     Tag-ID      |    Originator-IP    |    neighbor     |    Next-Hop     |   Local-Pref    |     Origin      |
|                 |        |  distinguisher  |                 |                     |                 |                 |                 |                 |
+=================+========+=================+=================+=====================+=================+=================+=================+=================+
| default         | u*>    | 2.2.2.2:100     | 0               | 2.2.2.2             | 2.2.2.2         | 2.2.2.2         | 100             | igp             |
| default         | *      | 2.2.2.2:100     | 0               | 2.2.2.2             | 2001::2         | 2.2.2.2         | 100             | igp             |
+-----------------+--------+-----------------+-----------------+---------------------+-----------------+-----------------+-----------------+-----------------+
-----------------------------------------------------------------------------------------------------------------------------------------------------------------
Type 5 IP Prefix Routes
+-----------------+--------+-----------------+-----------------+---------------------+-----------------+-----------------+-----------------+-----------------+
|       VRF       | Status |     Route-      |     Tag-ID      |     IP-address      |    neighbor     |    Next-Hop     |   Local-Pref    |     Origin      |
|                 |        |  distinguisher  |                 |                     |                 |                 |                 |                 |
+=================+========+=================+=================+=====================+=================+=================+=================+=================+
| default         | u*>    | 2.2.2.2:200     | 0               | 10.90.1.0/24        | 2.2.2.2         | 2.2.2.2         | 100             | igp             |
| default         | *      | 2.2.2.2:200     | 0               | 10.90.1.0/24        | 2001::2         | 2.2.2.2         | 100             | igp             |
| default         | u*>    | 2.2.2.2:200     | 0               | 10:90:1::/64        | 2.2.2.2         | 2.2.2.2         | 100             | igp             |
| default         | *      | 2.2.2.2:200     | 0               | 10:90:1::/64        | 2001::2         | 2.2.2.2         | 100             | igp             |
+-----------------+--------+-----------------+-----------------+---------------------+-----------------+-----------------+-----------------+-----------------+
-----------------------------------------------------------------------------------------------------------------------------------------------------------------
0 Ethernet Auto-Discovery routes 0 used, 0 valid
2 MAC-IP Advertisement routes 1 used, 2 valid
2 Inclusive Multicast Ethernet Tag routes 1 used, 2 valid
0 Ethernet Segment routes 0 used, 0 valid
4 IP Prefix routes 2 used, 4 valid
0 Selective Multicast Ethernet Tag routes 0 used, 0 valid
0 Selective Multicast Membership Report Sync routes 0 used, 0 valid
0 Selective Multicast Leave Sync routes 0 used, 0 valid
-----------------------------------------------------------------------------------------------------------------------------------------------------------------
```

Optionally you may also run:
- `show bgp evpn summary vrf <vrf-name>`



