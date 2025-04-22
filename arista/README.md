# Custom CLI Plugins for Arista EOS

The following CLI plugins are available in this repo:

> [!NOTE]
> At the time releasing these scripts, SR Linux did not support a custom CLI path that was loaded on top of an existing native path. Due to this reason, some EOS commands start with the syntax `show eos`. This will be fixed in a future release.

| Command | Contributor |
|---|---|
| `show eos interface` | [mfzhsn](https://github.com/mfzhsn) |
| `show eos interface status` | [mfzhsn](https://github.com/mfzhsn) |
| `show arp` | [mfzhsn](https://github.com/mfzhsn) |
| `show ip bgp summary` | [sajusal](https://github.com/sajusal) |
| `show bgp evpn route-type auto-discovery` | [sajusal](https://github.com/sajusal) |
| `show bgp evpn route-type mac-ip` | [sajusal](https://github.com/sajusal) |
| `show bgp evpn route-type imet` | [sajusal](https://github.com/sajusal) |
| `show bgp evpn route-type ethernet-segment` | [sajusal](https://github.com/sajusal) |
| `show bgp evpn route-type ethernet-segment` | [sajusal](https://github.com/sajusal) |
| `show bgp evpn route-type ip-prefix` | [sajusal](https://github.com/sajusal) |
| `show bgp evpn summary` | [sajusal](https://github.com/sajusal) |

## Testing

Deploy the EVPN lab. Login to any leaf or spine node using `auser/auser` and try any of the above commands.
