# PolyGlot

Welcome to the PolyGlot project for Nokia SR Linux.

As you know, [SR Linux](https://learn.srlinux.dev/) is the industry's most modern Network Operating System enabling unmatched automation and programmability features.

One of the capabilities is the ability to customize the CLI on SR Linux.

All SR Linux CLI commands shipped with the software are written in executable python scripts leveraging the config and state yang models.

Users are allowed take those python scripts, modify them to fit their use case or build a brand new CLI command leveraging the same config and state models.

These customized CLI scripts are called **Custom CLI plugins** in SR Linux.

Since everything is modeled in yang from the ground up, this allows the user to use CLI to access any object or attribute in the system and display it in the format they are familiar with.

So how does this benefit the user? There are few use cases that we could think of like:
- Use the same MOP and command set that you previously used for another provider
- Use the same automation or monitoring scripts that was written for another provider
- allow users to start using SR Linux using the same commands they used for another provider

All these are CLI heavy use cases. You may have more use cases in your mind.

This is awesome! But how do i put this into action?

## What is PolyGlot about?

The mission of PolyGlot is to get you started with SR Linux CLI customization feature for your environment.

Over the next few months, we will be contributing python scripts that will enable SR Linux custom CLI commands that you are already familiar with from another provider.

The user community is free to take these scripts, use them as is or modify them based on their end goal. We will also be happy to accept new script contributions from the community.

SR Linux also supports command aliases which can be saved on a per-user basis or globally for all users. Aliases are easy to implement and beneficial when the requirement is to only have a different command with the same format of output of a standard SR Linux command. We will use also aliases for some of the commands in this project.

Our initial focus will be on `show` commands.

## Learn how to customize SR Linux CLI

For those intereted in learning the process of customizing the SR Linux CLI, refer to the official [SR Linux CLI plug-in guide](https://documentation.nokia.com/srlinux/24-10/title/cli_plugin.html).

For practical experience, start by using the beginner SReXperts hackathon use case [here](https://github.com/nokia/SReXperts/tree/main/hackathon/activities/srlinux-i-cli-plugin-show-version) following by an intermediate use case [here](https://github.com/nokia/SReXperts/tree/main/hackathon/activities/srlinux-i-custom-cli).

## Testing scripts

With the power of [Containerlab](https://containerlab.dev/) and the free SR Linux docker image, testing these custom CLI commands is a simple process. We will also provide sample lab toplogies with startup configs where these custom commands can be tested.

To test these scripts:
- Deploy the SR Linux lab for your choice or the one referenced in the script directory.
- Copy the python script to `/etc/opt/srlinux/cli/plugins` directory on a SR Linux node
- If you are already logged into the node, logout and login again for the custom command to be loaded.

## PolyGlot Scripts

This repo is structured based on the provider/vendor that we try to match in SR Linux CLI.

For this initial release, we are providing scripts for Arista and more providers will follow.

Within each provider's folder, you will find sub-folders with the feature name that we are targeting. This sub-folder will hold the python scripts and references to lab topologies to test these scripts. In this initial release, we have scripts for Arista EVPN show commands.

- [Arista](Arista/)
- Cisco (coming soon)
- Juniper (coming soon)
- SR OS (coming soon)

## Resources for further learning

* [SR Linux documentation](https://documentation.nokia.com/srlinux/)
* [Learn SR Linux](https://learn.srlinux.dev/)
* [YANG Browser](https://yang.srlinux.dev/)
* [gNxI Browser](https://gnxi.srlinux.dev/)
