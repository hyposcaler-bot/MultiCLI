#!/usr/bin/python
###########################################################################
# Description: Custom CLI plugin for Arista EOS 'show bgp evpn' command
#
# Copyright (c) 2020 Nokia
###########################################################################
from srlinux import data
from srlinux.mgmt.cli import CliPlugin, RequiredPlugin, KeyCompleter
from srlinux.syntax import Syntax
from srlinux.location import build_path
from srlinux import strings
from srlinux.data import Data, Formatter, ColumnFormatter, print_line, Indent, Border
from srlinux.data.utilities import timedelta_str
from srlinux.mgmt.cli import ParseError 
from srlinux.strings import split_before
import ipaddress
import logging
from enum import Enum, auto
from srlinux.data.utilities import get_indentation_string as spacing
from srlinux.schema import FixedSchemaRoot


class Plugin(CliPlugin):

    __slots__ = (
        '_header_string',
        '_netinst',
        '_arguments',
        '_netinst_data',
        '_current_netinst',
        '_used_routes',
        '_valid_routes',
        '_received_count',
        '_attrSets_dict',
        '_route_type',
        '_rd',
        '_mac_address',
        '_ip_address',
        '_ip_prefix',
        '_esi',
        '_ethernet_tag',
        '_originating_router',
        '_neighbor',
        '_multicast_source_address',
        '_multicast_group_address',
        '_bgp_rib'
    )

    def load(self, cli, **_kwargs):
        syntax = Syntax('bgp', help='display bgp information')
        bgp = cli.show_mode.add_command(syntax, update_location=True)
        evpn = bgp.add_command(
            Syntax('evpn', help='show EVPN information'),
            update_location=True)
        summary = evpn.add_command(
            Syntax('summary', help='Show all EVPN Route Types')
            .add_named_argument('vrf', default='*', help = 'network instance (VRF) name', suggestions=KeyCompleter('/network-instance[name=*]')),
            update_location=False,
            callback=self._print_all,
            schema=self.get_data_schema_all())
        route_type = evpn.add_command(Syntax('route-type', help='specify the EVPN route type'))
        rt_mac_ip = route_type.add_command(
            Syntax('mac-ip')
            .add_named_argument('vrf', default='*', help = 'network instance name', suggestions=KeyCompleter('/network-instance[name=*]'))
            .add_unnamed_argument('mac-address', default='*', help = 'MAC address'),
            callback = self._print_2,
            schema=self.get_data_schema_all())
        rt_imet = route_type.add_command(
            Syntax('imet')
            .add_named_argument('vrf', default='*', help = 'network instance name', suggestions=KeyCompleter('/network-instance[name=*]'))
            .add_unnamed_argument('origin-router', default='*', help = 'Originating router IPv4 or IPv6 address'),
            callback = self._print_3,
            schema=self.get_data_schema_all())
        rt_ip_prefix = route_type.add_command(
            Syntax('ip-prefix')
            .add_named_argument('vrf', default='*', help = 'network instance name', suggestions=KeyCompleter('/network-instance[name=*]'))
            .add_unnamed_argument('ip-address', default='*', help = 'IPv4 or IPv6 address prefix'),
            callback = self._print_5,
            schema=self.get_data_schema_all())                
          

    def __init__(self):
        self._rd = '*'
        self._esi = '*'
        self._mac_address = '*'
        self._ip_address = '*'
        self._ip_prefix = '*'
        self._originating_router = '*'
        self._ethernet_tag = '*'
        self._neighbor = '*'
        self._multicast_source_address = '*'
        self._multicast_group_address = '*'
        self._bgp_rib = None
        self._attrSets_dict = {}

    def get_data_schema_all(self):
        '''
            Return the Schema describing the data-model of the show routine.
            Think of this as the output of 'tree' - which is the data-model of the configuration.
        '''
        root_summary = FixedSchemaRoot()

        header = root_summary.add_child('summary_all', key='Header_all', fields=['net-inst', 'Router-id', 'global-as'])
        header.add_child('eth_ad',
                         keys=['VRF', 'Status', 'Route-distinguisher', 'ESI', 'Tag-ID', 'neighbor'],
                         fields=['Next-hop', 'Local-Pref', 'Origin'],
                         )
        header.add_child('mac_ip',
                         keys=['VRF', 'Status', 'Route-distinguisher', 'MAC-address', 'IP-address', 'Neighbor'],
                         fields=['Next-Hop', 'Local-Pref', 'Origin'],
                         )
        header.add_child('imeth',
                         keys=['VRF', 'Status', 'Route-distinguisher', 'Tag-ID', 'Originator-IP', 'neighbor'],
                         fields=['Next-Hop', 'Local-Pref', 'Origin'],
                         )
        header.add_child('eth_segment',
                         keys=['VRF', 'Status', 'Route-distinguisher', 'ESI', 'originating-router', 'neighbor'],
                         fields=['Next-Hop', 'Local-Pref', 'Origin'],
                         )
        header.add_child('ip_prefix',
                         keys=['VRF', 'Status', 'Route-distinguisher', 'Tag-ID', 'IP-address', 'neighbor'],
                         fields=['Next-Hop', 'Local-Pref', 'Origin'],
                         )
        header.add_child('smet',
                         keys=['VRF', 'Status', 'Route-distinguisher', 'Tag-ID', 'multicast-source-address', 'multicast-group-address', 'Originating-router', 'neighbor'],
                         fields=['Next-Hop', 'Local-Pref', 'Origin'],
                         )
        header.add_child('mcast_report',
                         keys=['VRF', 'Status', 'Route-distinguisher', 'ESI', 'Tag-ID', 'multicast-source-address', 'multicast-group-address', 'Originating-router', 'neighbor'],
                         fields=['Next-Hop', 'Local-Pref', 'Origin'],
                         )
        header.add_child('mcast_leave',
                         keys=['VRF', 'Status', 'Route-distinguisher', 'ESI', 'Tag-ID', 'multicast-source-address', 'multicast-group-address', 'Originating-router', 'neighbor'],
                         fields=['Next-Hop', 'Local-Pref', 'Origin'],
                         )
        header.add_child('stats', key='route_type',
                         fields=[ 'received count', 'used count', 'valid count']
                         )
        return root_summary

    def reset_counters(self):
        self._used_routes = 0
        self._valid_routes = 0
        self._received_count = 0

    def _print_all(self, state, arguments, output, **_kwargs):
        self._route_type = '*'
        self._arguments = arguments
        self._netinst = self._arguments.get('summary', 'vrf')
        self._bgp_rib = self._getRibInOut(state)
        self._print(state, arguments, output, **_kwargs)

    def _print_2(self, state, arguments, output, **_kwargs):
        self._route_type = '2'
        self._arguments = arguments
        self._netinst = self._arguments.get('mac-ip', 'vrf')
        self._mac_address = self._arguments.get('mac-ip', 'mac-address')
        self._bgp_rib = self._getRibRoute2(state)
        self._print(state, arguments, output, **_kwargs)    

    def _print_3(self, state, arguments, output, **_kwargs):
        self._route_type = '3'
        self._arguments = arguments
        self._netinst = self._arguments.get('imet', 'vrf')
        self._originating_router = self._arguments.get('imet', 'origin-router')
        self._bgp_rib = self._getRibRoute3(state)
        self._print(state, arguments, output, **_kwargs)

    def _print_5(self, state, arguments, output, **_kwargs):
        self._route_type = '5'
        self._arguments = arguments
        self._netinst = self._arguments.get('ip-prefix', 'vrf')
        self._ip_prefix = self._arguments.get('ip-prefix', 'ip-address')
        self._bgp_rib = self._getRibRoute5(state)
        self._print(state, arguments, output, **_kwargs)

    def _print(self, state, arguments, output, **_kwargs):
        self._attrSets_dict = {}
        result = Data(arguments.schema)
        self._set_formatters(result)
        with output.stream_data(result):
            self._populate_data(result, state)

    def _populate_data(self, data_root, state):
        proto_bgp = self._getBgpSummary(state)

        summary_header = data_root.summary_all.create(self._netinst)
        summary_header.net_inst = self._netinst
        for entry in proto_bgp.get_descendants('/network-instance/protocols/bgp'):
            summary_header.router_id = entry.router_id
            summary_header.global_as = entry.autonomous_system
        summary_header.synchronizer.flush_fields(summary_header)

        for netinst in self._bgp_rib.network_instance.items():
            if state.system_features.bgp_rib_afi_safi_list_for_evpn:
                evpn_routes = netinst.bgp_rib.get().afi_safi.get().evpn.get().rib_in_out.get()
            else:
                evpn_routes = netinst.bgp_rib.get().evpn.get().rib_in_out.get()

            evpn_rib_in_post = evpn_routes.rib_in_post.get()

            # Type 1 Ethernet auto discovery routes
            if self._route_type == '*' or self._route_type == '1':
                self.reset_counters()
                if state.system_features.bgp_rib_afi_safi_list_for_evpn:
                    rttable = evpn_rib_in_post.ethernet_ad_route
                else:
                    rttable = evpn_rib_in_post.ethernet_ad_routes

                for route in rttable.items():
                    if (self._esi != '*' and route.esi != self._esi) or \
                       (self._rd != '*' and route.route_distinguisher != self._rd) or \
                       (self._ethernet_tag != '*' and str(route.ethernet_tag_id) != self._ethernet_tag) or \
                       (self._neighbor != '*' and route.neighbor != self._neighbor):
                        continue
                    status = self._set_status_code(route)
                    result = summary_header.eth_ad.create(netinst.name,
                                                          status,
                                                          route.route_distinguisher,
                                                          route.esi, route.ethernet_tag_id, route.neighbor)
                    self._received_count += 1
                    self._populate_route_attrs(state, result, netinst.name, route.attr_id)
                    result.synchronizer.flush_fields(result)

                stats = summary_header.stats.create('Ethernet Auto-Discovery routes')
                stats.received_count = self._received_count
                stats.valid_count = self._valid_routes
                stats.used_count = self._used_routes
            summary_header.synchronizer.flush_children(summary_header.eth_ad)

            # Type 2 MAC IP routes
            if self._route_type == '*' or self._route_type == '2':
                self.reset_counters()
                if state.system_features.bgp_rib_afi_safi_list_for_evpn:
                    rttable = evpn_rib_in_post.mac_ip_route
                else:
                    rttable = evpn_rib_in_post.mac_ip_routes

                for route in rttable.items():
                    if (self._mac_address != '*' and route.mac_address != self._mac_address) or \
                       (self._rd != '*' and route.route_distinguisher != self._rd) or \
                        (self._ip_address != '*' and route.ip_address != self._ip_address) or \
                        (self._ethernet_tag != '*' and str(route.ethernet_tag_id) != self._ethernet_tag) or \
                        (self._neighbor != '*' and route.neighbor != self._neighbor):
                        continue
                    status = self._set_status_code(route)
                    result = summary_header.mac_ip.create(netinst.name,
                                                          status,
                                                          route.route_distinguisher,
                                                          route.mac_address,
                                                          route.ip_address, route.neighbor)
                        
                    #result.esi = route.esi
                    self._received_count += 1
                    self._populate_route_attrs(state, result, netinst.name, route.attr_id, '2')
                    result.synchronizer.flush_fields(result)

                stats = summary_header.stats.create('MAC-IP Advertisement routes')
                stats.received_count = self._received_count
                stats.valid_count = self._valid_routes
                stats.used_count = self._used_routes
            summary_header.synchronizer.flush_children(summary_header.mac_ip)

            # Type 3 Inclusive Multicast Ethernet
            if self._route_type == '*' or self._route_type == '3':
                self.reset_counters()
                if state.system_features.bgp_rib_afi_safi_list_for_evpn:
                    rttable = evpn_rib_in_post.imet_route
                else:
                    rttable = evpn_rib_in_post.imet_routes

                for route in rttable.items():
                    if (self._originating_router != '*' and route.originating_router != self._originating_router) or \
                       (self._rd != '*' and route.route_distinguisher != self._rd) or \
                        (self._ethernet_tag != '*' and str(route.ethernet_tag_id) != self._ethernet_tag) or \
                        (self._neighbor != '*' and route.neighbor != self._neighbor):
                        continue
                    status = self._set_status_code(route)
                    result = summary_header.imeth.create(netinst.name,
                                                         status,
                                                         route.route_distinguisher,
                                                         route.ethernet_tag_id,
                                                         route.originating_router, route.neighbor)
                    self._received_count += 1
                    self._populate_route_attrs(state, result, netinst.name, route.attr_id)
                    result.synchronizer.flush_fields(result)

                stats = summary_header.stats.create('Inclusive Multicast Ethernet Tag routes')
                stats.received_count = self._received_count
                stats.valid_count = self._valid_routes
                stats.used_count = self._used_routes
            summary_header.synchronizer.flush_children(summary_header.imeth)

            # Type 4 Ethernet Segment routes
            if self._route_type == '*' or self._route_type == '4':
                self.reset_counters()
                if state.system_features.bgp_rib_afi_safi_list_for_evpn:
                    rttable = evpn_rib_in_post.ethernet_segment_route
                else:
                    rttable = evpn_rib_in_post.ethernet_segment_routes

                for route in rttable.items():
                    if (self._esi != '*' and route.esi != self._esi) or \
                       (self._rd != '*' and route.route_distinguisher != self._rd) or \
                        (self._originating_router != '*' and route.originating_router != self._originating_router) or \
                        (self._neighbor != '*' and route.neighbor != self._neighbor):
                        continue
                    status = self._set_status_code(route)
                    result = summary_header.eth_segment.create(netinst.name,
                                                             status,
                                                             route.route_distinguisher,
                                                             route.esi, route.originating_router, route.neighbor)
                    self._received_count += 1
                    self._populate_route_attrs(state, result, netinst.name, route.attr_id)
                    result.synchronizer.flush_fields(result)

                stats = summary_header.stats.create('Ethernet Segment routes')
                stats.received_count = self._received_count
                stats.valid_count = self._valid_routes
                stats.used_count = self._used_routes
            summary_header.synchronizer.flush_children(summary_header.eth_segment)

            # Type 5 IP prefix routes
            if self._route_type == '*' or self._route_type == '5':
                self.reset_counters()
                if state.system_features.bgp_rib_afi_safi_list_for_evpn:
                    rttable = evpn_rib_in_post.ip_prefix_route
                else:
                    rttable = evpn_rib_in_post.ip_prefix_routes

                for route in rttable.items():
                    if (self._ip_prefix != '*' and route.ip_prefix != self._ip_prefix) or \
                       (self._rd != '*' and route.route_distinguisher != self._rd) or \
                       (self._ethernet_tag != '*' and str(route.ethernet_tag_id) != self._ethernet_tag) or \
                       (self._neighbor != '*' and route.neighbor != self._neighbor):
                        continue
                    status = self._set_status_code(route)
                    result = summary_header.ip_prefix.create(netinst.name,
                                                             status,
                                                             route.route_distinguisher,
                                                             route.ethernet_tag_id,
                                                             route.ip_prefix, route.neighbor)

                    self._received_count += 1
                    self._populate_route_attrs(state, result, netinst.name, route.attr_id)
                    result.synchronizer.flush_fields(result)

                stats = summary_header.stats.create('IP Prefix routes')
                stats.received_count = self._received_count
                stats.valid_count = self._valid_routes
                stats.used_count = self._used_routes
            summary_header.synchronizer.flush_children(summary_header.ip_prefix)

            # Type 6 Smet routes
            if self._route_type == '*' or self._route_type == '6':
                self.reset_counters()
                if state.system_features.bgp_rib_afi_safi_list_for_evpn:
                    rttable = evpn_rib_in_post.smet_route
                else:
                    rttable = evpn_rib_in_post.smet_routes

                for route in rttable.items():
                    if (self._rd != '*' and route.route_distinguisher != self._rd) or \
                       (self._ethernet_tag != '*' and str(route.ethernet_tag_id) != self._ethernet_tag) or \
                       (self._multicast_source_address != '*' and route.multicast_source_address != self._multicast_source_address) or \
                       (self._multicast_group_address != '*' and route.multicast_group_address != self._multicast_group_address) or \
                       (self._originating_router != '*' and route.originating_router != self._originating_router) or \
                       (self._neighbor != '*' and route.neighbor != self._neighbor):
                        continue

                    status = self._set_status_code(route)
                    result = summary_header.smet.create(netinst.name,
                                                        status,
                                                        route.route_distinguisher,
                                                        route.ethernet_tag_id,
                                                        route.multicast_source_address,
                                                        route.multicast_group_address,
                                                        route.originating_router,
                                                        route.neighbor)
                    self._received_count += 1
                    self._populate_route_attrs(state, result, netinst.name, route.attr_id)
                    result.synchronizer.flush_fields(result)

                stats = summary_header.stats.create('Selective Multicast Ethernet Tag routes')
                stats.received_count = self._received_count
                stats.valid_count = self._valid_routes
                stats.used_count = self._used_routes
            summary_header.synchronizer.flush_children(summary_header.smet)

            # Type 7 multicast membership report sync routes
            if self._route_type == '*' or self._route_type == '7':
                self.reset_counters()
                if state.system_features.bgp_rib_afi_safi_list_for_evpn:
                    rttable = evpn_rib_in_post.multicast_membership_report_synch_route
                else:
                    rttable = evpn_rib_in_post.multicast_membership_report_synch_routes

                for route in rttable.items():
                    if (self._rd != '*' and route.route_distinguisher != self._rd) or \
                       (self._esi != '*' and route.esi != self._esi) or \
                       (self._ethernet_tag != '*' and str(route.ethernet_tag_id) != self._ethernet_tag) or \
                       (self._multicast_source_address != '*' and route.multicast_source_address != self._multicast_source_address) or \
                       (self._multicast_group_address != '*' and route.multicast_group_address != self._multicast_group_address) or \
                       (self._originating_router != '*' and route.originating_router != self._originating_router) or \
                       (self._neighbor != '*' and route.neighbor != self._neighbor):
                        continue

                    status = self._set_status_code(route)
                    result = summary_header.mcast_report.create(netinst.name,
                                                              status,
                                                              route.route_distinguisher,
                                                              route.esi,
                                                              route.ethernet_tag_id,
                                                              route.multicast_source_address,
                                                              route.multicast_group_address,
                                                              route.originating_router,
                                                              route.neighbor)
                    self._received_count += 1
                    self._populate_route_attrs(state, result, netinst.name, route.attr_id)
                    result.synchronizer.flush_fields(result)

                stats = summary_header.stats.create('Selective Multicast Membership Report Sync routes')
                stats.received_count = self._received_count
                stats.valid_count = self._valid_routes
                stats.used_count = self._used_routes
            summary_header.synchronizer.flush_children(summary_header.mcast_report)

            # Type 8 multicast leave sync routes
            if self._route_type == '*' or self._route_type == '8':
                self.reset_counters()
                if state.system_features.bgp_rib_afi_safi_list_for_evpn:
                    rttable = evpn_rib_in_post.multicast_leave_synch_route
                else:
                    rttable = evpn_rib_in_post.multicast_leave_synch_routes

                for route in rttable.items():
                    if (self._rd != '*' and route.route_distinguisher != self._rd) or \
                       (self._esi != '*' and route.esi != self._esi) or \
                       (self._ethernet_tag != '*' and str(route.ethernet_tag_id) != self._ethernet_tag) or \
                       (self._multicast_source_address != '*' and route.multicast_source_address != self._multicast_source_address) or \
                       (self._multicast_group_address != '*' and route.multicast_group_address != self._multicast_group_address) or \
                       (self._originating_router != '*' and route.originating_router != self._originating_router) or \
                       (self._neighbor != '*' and route.neighbor != self._neighbor):
                        continue

                    status = self._set_status_code(route)
                    result = summary_header.mcast_leave.create(netinst.name,
                                                               status,
                                                               route.route_distinguisher,
                                                               route.esi,
                                                               route.ethernet_tag_id,
                                                               route.multicast_source_address,
                                                               route.multicast_group_address,
                                                               route.originating_router,
                                                               route.neighbor)
                    self._received_count += 1
                    self._populate_route_attrs(state, result, netinst.name, route.attr_id)
                    result.synchronizer.flush_fields(result)

                stats = summary_header.stats.create('Selective Multicast Leave Sync routes')
                stats.received_count = self._received_count
                stats.valid_count = self._valid_routes
                stats.used_count = self._used_routes
            summary_header.synchronizer.flush_children(summary_header.mcast_leave)

        summary_header.synchronizer.flush_children(summary_header.stats)

    def _getRibInOut(self, state):
        if state.system_features.bgp_rib_afi_safi_list_for_evpn:
            path = build_path('/network-instance[name={name}]/bgp-rib/afi-safi[afi-safi-name=evpn]/evpn/rib-in-out/rib-in-post', name=self._netinst)
        else:
            path = build_path('/network-instance[name={name}]/bgp-rib/evpn/rib-in-out/rib-in-post', name=self._netinst)
        return state.server_data_store.stream_data(path, recursive=True, include_container_children=True)

    def _getRibRoute1(self, state):
        if state.system_features.bgp_rib_afi_safi_list_for_evpn:
            path = build_path('/network-instance[name={name}]/bgp-rib/afi-safi[afi-safi-name=evpn]/evpn/rib-in-out/rib-in-post/ethernet-ad-route[route-distinguisher={rd}][esi={esi}][ethernet-tag-id={etag}][neighbor={neigh}]',
                    name=self._netinst,
                    rd=self._rd,
                    esi=self._esi,
                    etag=self._ethernet_tag,
                    neigh=self._neighbor
                )
        else:
            path = build_path('/network-instance[name={name}]/bgp-rib/evpn/rib-in-out/rib-in-post/ethernet-ad-routes[route-distinguisher={rd}][esi={esi}][ethernet-tag-id={etag}][neighbor={neigh}]',
                    name=self._netinst,
                    rd=self._rd,
                    esi=self._esi,
                    etag=self._ethernet_tag,
                    neigh=self._neighbor
                )
        return state.server_data_store.stream_data(path, recursive=False, include_container_children=True)

    def _getRibRoute2(self, state):
        if state.system_features.bgp_rib_afi_safi_list_for_evpn:
            path = build_path('/network-instance[name={name}]/bgp-rib/afi-safi[afi-safi-name=evpn]/evpn/rib-in-out/rib-in-post/mac-ip-route[route-distinguisher={rd}][mac-length=*][mac-address={mac}][ip-address={ip}][ethernet-tag-id={etag}][neighbor={neigh}]',
                name=self._netinst,
                rd=self._rd,
                mac=self._mac_address,
                ip=self._ip_address,
                etag=self._ethernet_tag,
                neigh=self._neighbor
            )
        else:
            path = build_path('/network-instance[name={name}]/bgp-rib/evpn/rib-in-out/rib-in-post/mac-ip-routes[route-distinguisher={rd}][mac-length=*][mac-address={mac}][ip-address={ip}][ethernet-tag-id={etag}][neighbor={neigh}]',
                    name=self._netinst,
                    rd=self._rd,
                    mac=self._mac_address,
                    ip=self._ip_address,
                    etag=self._ethernet_tag,
                    neigh=self._neighbor
                )
        return state.server_data_store.stream_data(path, recursive=False, include_container_children=True)

    def _getRibRoute3(self, state):
        if state.system_features.bgp_rib_afi_safi_list_for_evpn:
            path = build_path('/network-instance[name={name}]/bgp-rib/afi-safi[afi-safi-name=evpn]/evpn/rib-in-out/rib-in-post/imet-route[route-distinguisher={rd}][originating-router={orouter}][ethernet-tag-id={etag}][neighbor={neigh}]',
                name=self._netinst,
                rd=self._rd,
                orouter=self._originating_router,
                etag=self._ethernet_tag,
                neigh=self._neighbor
            )
        else:
            path = build_path('/network-instance[name={name}]/bgp-rib/evpn/rib-in-out/rib-in-post/imet-routes[route-distinguisher={rd}][originating-router={orouter}][ethernet-tag-id={etag}][neighbor={neigh}]',
                    name=self._netinst,
                    rd=self._rd,
                    orouter=self._originating_router,
                    etag=self._ethernet_tag,
                    neigh=self._neighbor
                )
        return state.server_data_store.stream_data(path, recursive=False, include_container_children=True)

    def _getRibRoute4(self, state):
        if state.system_features.bgp_rib_afi_safi_list_for_evpn:
            path = build_path('/network-instance[name={name}]/bgp-rib/afi-safi[afi-safi-name=evpn]/evpn/rib-in-out/rib-in-post/ethernet-segment-route[route-distinguisher={rd}][esi={esi}][originating-router={orouter}][neighbor={neigh}]',
                name=self._netinst,
                rd=self._rd,
                esi=self._esi,
                orouter=self._originating_router,
                neigh=self._neighbor
            )
        else:
            path = build_path('/network-instance[name={name}]/bgp-rib/evpn/rib-in-out/rib-in-post/ethernet-segment-routes[route-distinguisher={rd}][esi={esi}][originating-router={orouter}][neighbor={neigh}]',
                    name=self._netinst,
                    rd=self._rd,
                    esi=self._esi,
                    orouter=self._originating_router,
                    neigh=self._neighbor
                )
        return state.server_data_store.stream_data(path, recursive=False, include_container_children=True)

    def _getRibRoute5(self, state):
        if state.system_features.bgp_rib_afi_safi_list_for_evpn:
            path = build_path('/network-instance[name={name}]/bgp-rib/afi-safi[afi-safi-name=evpn]/evpn/rib-in-out/rib-in-post/ip-prefix-route[route-distinguisher={rd}][ethernet-tag-id={etag}][ip-prefix-length=*][ip-prefix={prefix}][neighbor={neigh}]',
                name=self._netinst,
                rd=self._rd,
                etag=self._ethernet_tag,
                prefix=self._ip_prefix,
                neigh=self._neighbor
            )
        else:
            path = build_path('/network-instance[name={name}]/bgp-rib/evpn/rib-in-out/rib-in-post/ip-prefix-routes[route-distinguisher={rd}][ethernet-tag-id={etag}][ip-prefix-length=*][ip-prefix={prefix}][neighbor={neigh}]',
                    name=self._netinst,
                    rd=self._rd,
                    etag=self._ethernet_tag,
                    prefix=self._ip_prefix,
                    neigh=self._neighbor
                )
        return state.server_data_store.stream_data(path, recursive=False, include_container_children=True)

    def _getRibRoute6(self, state):
        if state.system_features.bgp_rib_afi_safi_list_for_evpn:
            path = build_path('/network-instance[name={name}]/bgp-rib/afi-safi[afi-safi-name=evpn]/evpn/rib-in-out/rib-in-post/smet-route[route-distinguisher={rd}][ethernet-tag-id={etag}][multicast-source-length=*][multicast-source-address={multicast_source_address}][multicast-group-length=*][multicast-group-address={multicast_group_address}][originating-router={orouter}][neighbor={neigh}]',
                name=self._netinst,
                rd=self._rd,
                etag=self._ethernet_tag,
                multicast_source_address=self._multicast_source_address,
                multicast_group_address=self._multicast_group_address,
                orouter=self._originating_router,
                neigh=self._neighbor
            )
        else:
            path = build_path('/network-instance[name={name}]/bgp-rib/evpn/rib-in-out/rib-in-post/smet-routes[route-distinguisher={rd}][ethernet-tag-id={etag}][multicast-source-length=*][multicast-source-address={multicast_source_address}][multicast-group-length=*][multicast-group-address={multicast_group_address}][originating-router={orouter}][neighbor={neigh}]',
                    name=self._netinst,
                    rd=self._rd,
                    etag=self._ethernet_tag,
                    multicast_source_address=self._multicast_source_address,
                    multicast_group_address=self._multicast_group_address,
                    orouter=self._originating_router,
                    neigh=self._neighbor
                )
        return state.server_data_store.stream_data(path, recursive=False, include_container_children=True)

    def _getRibRoute7(self, state):
        if state.system_features.bgp_rib_afi_safi_list_for_evpn:
            path = build_path('/network-instance[name={name}]/bgp-rib/afi-safi[afi-safi-name=evpn]/evpn/rib-in-out/rib-in-post/multicast-membership-report-synch-route[route-distinguisher={rd}][esi={esi}][ethernet-tag-id={etag}][multicast-source-length=*][multicast-source-address={multicast_source_address}][multicast-group-length=*][multicast-group-address={multicast_group_address}][originating-router={orouter}][neighbor={neigh}]',
                name=self._netinst,
                rd=self._rd,
                esi=self._esi,
                etag=self._ethernet_tag,
                multicast_source_address=self._multicast_source_address,
                multicast_group_address=self._multicast_group_address,
                orouter=self._originating_router,
                neigh=self._neighbor
            )
        else:
            path = build_path('/network-instance[name={name}]/bgp-rib/evpn/rib-in-out/rib-in-post/multicast-membership-report-synch-routes[route-distinguisher={rd}][esi={esi}][ethernet-tag-id={etag}][multicast-source-length=*][multicast-source-address={multicast_source_address}][multicast-group-length=*][multicast-group-address={multicast_group_address}][originating-router={orouter}][neighbor={neigh}]',
                    name=self._netinst,
                    rd=self._rd,
                    esi=self._esi,
                    etag=self._ethernet_tag,
                    multicast_source_address=self._multicast_source_address,
                    multicast_group_address=self._multicast_group_address,
                    orouter=self._originating_router,
                    neigh=self._neighbor
                )
        return state.server_data_store.stream_data(path, recursive=False, include_container_children=True)

    def _getRibRoute8(self, state):
        if state.system_features.bgp_rib_afi_safi_list_for_evpn:
            path = build_path('/network-instance[name={name}]/bgp-rib/afi-safi[afi-safi-name=evpn]/evpn/rib-in-out/rib-in-post/multicast-leave-synch-route[route-distinguisher={rd}][esi={esi}][ethernet-tag-id={etag}][multicast-source-length=*][multicast-source-address={multicast_source_address}][multicast-group-length=*][multicast-group-address={multicast_group_address}][originating-router={orouter}][neighbor={neigh}]',
                name=self._netinst,
                rd=self._rd,
                esi=self._esi,
                etag=self._ethernet_tag,
                multicast_source_address=self._multicast_source_address,
                multicast_group_address=self._multicast_group_address,
                orouter=self._originating_router,
                neigh=self._neighbor
            )
        else:
            path = build_path('/network-instance[name={name}]/bgp-rib/evpn/rib-in-out/rib-in-post/multicast-leave-synch-routes[route-distinguisher={rd}][esi={esi}][ethernet-tag-id={etag}][multicast-source-length=*][multicast-source-address={multicast_source_address}][multicast-group-length=*][multicast-group-address={multicast_group_address}][originating-router={orouter}][neighbor={neigh}]',
                    name=self._netinst,
                    rd=self._rd,
                    esi=self._esi,
                    etag=self._ethernet_tag,
                    multicast_source_address=self._multicast_source_address,
                    multicast_group_address=self._multicast_group_address,
                    orouter=self._originating_router,
                    neigh=self._neighbor
                )
        return state.server_data_store.stream_data(path, recursive=False, include_container_children=True)

    def _getBgpSummary(self, state):
        path = build_path( '/network-instance[name={name}]/protocols/bgp', name=self._netinst)
        return state.server_data_store.get_data(path, recursive=False)

    def _set_status_code(self, route):
        status = ""
        if route.used_route:
            status = "u"
            self._used_routes += 1
        if route.stale_route:
            status += "x"
            self._statle_routes += 1
        if route.valid_route:
            status += "*"
            self._valid_routes += 1
        if route.best_route:
            status += ">"
        return status or '-'

    def _populate_route_attrs(self, state, route_entry, netinst_name, attr_id, route_type='*'):
        if not attr_id in self._attrSets_dict:
            path = build_path('/network-instance[name={vrf}]/bgp-rib/attr-sets/attr-set[index={atr}]',
                              vrf=netinst_name, atr=str(attr_id))

            attrSets = state.server_data_store.stream_data(path, recursive=True, include_container_children=True)
            self._attrSets_dict[attr_id] = attrSets
        else:
            attrSets = self._attrSets_dict[attr_id]

        for attr in attrSets.get_descendants('/network-instance/bgp-rib/attr-sets/attr-set'):
            route_entry.next_hop = attr.next_hop
            route_entry.local_pref = attr.local_pref
            route_entry.origin = attr.origin
            #route_entry.vrf = netinst_name
            #if route_type == '2':
                #for comm in attr.communities.get().ext_community:
                    #route_entry.mac_mobility = comm[len('mac-mobility')+1:] if comm.find('mac-mobility') != -1 else '-'

    def _set_formatters(self, data):
        data.set_formatter('/summary_all', StatisticsFormatter_header())
        data.set_formatter('/summary_all/eth_ad', ColumnFormatter(ancestor_keys=False, print_on_data=True,
                                                              widths={'Status' : 6,
                                                                      }
                                                              ))
        data.set_formatter('/summary_all/mac_ip', ColumnFormatter(ancestor_keys=False, print_on_data=True,
                                                              widths={'Status' : 6,
                                                                      'MAC-address' : 17,
                                                                      }
                                                              ))
        data.set_formatter('/summary_all/imeth', ColumnFormatter(ancestor_keys=False, print_on_data=True,
                                                              widths={'Status' : 6,
                                                                      'Originator-IP' : 19,
                                                                      }
                                                             ))
        data.set_formatter('/summary_all/eth_segment', ColumnFormatter(ancestor_keys=False, print_on_data=True,
                                                              widths={'Status' : 6,
                                                                      }
                                                                   ))
        data.set_formatter('/summary_all/ip_prefix', ColumnFormatter(ancestor_keys=False, print_on_data=True,
                                                              widths={'Status' : 6,
                                                                      'IP-address' : 19,
                                                                      }
                                                                 ))
        data.set_formatter('/summary_all/smet', ColumnFormatter(ancestor_keys=False, print_on_data=True,
                                                              widths={'Status' : 6,
                                                                      'multicast-source-address' : 19,
                                                                      }
                                                                 ))                                     
        data.set_formatter('/summary_all/mcast_report', ColumnFormatter(ancestor_keys=False, print_on_data=True,
                                                              widths={'Status' : 6,
                                                                      'multicast-source-address' : 19,
                                                                      }
                                                                 ))                                     
        data.set_formatter('/summary_all/mcast_leave', ColumnFormatter(ancestor_keys=False, print_on_data=True,
                                                              widths={'Status' : 6,
                                                                      'multicast-source-address' : 19,
                                                                      }
                                                                 ))                                     
        data.set_formatter('/summary_all/stats', StatisticsFormatter_footer())

class StatisticsFormatter_header(Formatter):

    def iter_format(self, entry, max_width):
        yield from self._format_header_line(max_width)
        yield f'Show report for the BGP route table of network-instance "{entry.net_inst}"'
        yield from self._format_header(max_width)
        yield from self._format_header_line(max_width)
        yield f'BGP Router ID: {entry.router_id} {spacing(4)} AS: {entry.global_as} {spacing(4)} Local AS: {entry.global_as}'
        yield from self._format_header_line(max_width)

        if entry.eth_ad.exists():
            yield from self._format_header_line(max_width)
            yield f'Type 1 Ethernet Auto-Discovery Routes'
            yield from entry.eth_ad.iter_format(max_width)

        if entry.mac_ip.exists():
            yield f'Type 2 MAC-IP Advertisement Routes'
            yield from entry.mac_ip.iter_format(max_width)
            yield from self._format_header_line(max_width)

        if entry.imeth.exists():
            yield f'Type 3 Inclusive Multicast Ethernet Tag Routes'
            yield from entry.imeth.iter_format(max_width)
            yield from self._format_header_line(max_width)

        if entry.eth_segment.exists():
            yield f'Type 4 Ethernet Segment Routes'
            yield from entry.eth_segment.iter_format(max_width)
            yield from self._format_header_line(max_width)

        if entry.ip_prefix.exists():
            yield f'Type 5 IP Prefix Routes'
            yield from entry.ip_prefix.iter_format(max_width)
            yield from self._format_header_line(max_width)

        if entry.smet.exists():
            yield f'Type 6 Selective Multicast Ethernet Tag Routes'
            yield from entry.smet.iter_format(max_width)
            yield from self._format_header_line(max_width)

        if entry.mcast_report.exists():
            yield f'Type 7 Selective Multicast Membership Report Sync Routes'
            yield from entry.mcast_report.iter_format(max_width)
            yield from self._format_header_line(max_width)

        if entry.mcast_leave.exists():
            yield f'Type 8 Selective Multicast Leave Sync Routes'
            yield from entry.mcast_leave.iter_format(max_width)
            yield from self._format_header_line(max_width)

        yield from entry.stats.iter_format(max_width)
        yield from self._format_header_line(max_width)

    def _format_header_line(self, width):
        return (
            data.print_line(width),
        )

    def _format_header(self, width):
        return (
            data.print_line(width),
            'Status codes: u=used, *=valid, >=best, x=stale',
            'Origin codes: i=IGP, e=EGP, ?=incomplete',
        )


class StatisticsFormatter_footer(Formatter):

    def iter_format(self, entry, max_width):
        yield f'{entry.received_count} {entry.route_type} {entry.used_count} used, {entry.valid_count} valid'

    def _format_header_line(self, width):
        return (
            data.print_line(width),
        )
