# SR Linux Custom CLI plugins for Arista EOS EVPN Commands

This section contains SR Linux custom CLI python scripts for the following Arista EOS EVPN show commands.

Refer to the **Details** section for outputs using the standard SR Linux command and the custom CLI plugin.

Use the **Lab** to test the custom CLI plugin. The lab comes with options to configure EVPN by following a step-by-step guide or [deploy a fully configured EVPN fabric](https://github.com/srlinuxamericas/N92-evpn/blob/main/README.md#explore-this-lab-with-everything-pre-configured).

|   |   |   |   |
|---|---|---|---|
| `show mac address-table` | [Details]() | [Script]() | [Lab](https://github.com/srlinuxamericas/N92-evpn) |
| `show vxlan address-table` | [Details]() | [Script]() | [Lab](https://github.com/srlinuxamericas/N92-evpn) |
| `show bgp evpn route-type mac-ip` | [Details]() | [Script]() | [Lab](https://github.com/srlinuxamericas/N92-evpn) |
| `show bgp evpn route-type imet` | [Details]() | [Script]() | [Lab](https://github.com/srlinuxamericas/N92-evpn) |
| `show bgp evpn route-type ip-prefix` | [Details]() | [Script]() | [Lab](https://github.com/srlinuxamericas/N92-evpn) |
| `show bgp evpn summary` | [Details]() | [Script]() | [Lab](https://github.com/srlinuxamericas/N92-evpn) |

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

For the command syntax, we will follow the Arista command with the option to add `vrf` name at the end that equates to `network-instance` in SR Linux. An unnamed argument to filter on a specific `mac-address` is also added.

Since specifying `vrf` is optional, by default, the command will search for routes in all VRFs (network instances) and the `VRF` column in the output helps to identify the VRF name of each route.

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



