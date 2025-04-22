# MultiCLI

Welcome to the MultiCLI project for Nokia SR Linux.

[SR Linux](https://learn.srlinux.dev/) is the industry's most modern Network Operating System (NOS) enabling unmatched automation and programmability features.

One of its capabilities is the ability to customize the CLI on SR Linux.

All SR Linux CLI show commands shipped with the software are written in executable python scripts leveraging the state yang models.

Users are allowed take those python scripts, modify them to fit their use case or build a brand new CLI command leveraging the same state models.

These customized CLI scripts are called **Custom CLI plugins** in SR Linux.

Since everything is modeled in yang from the ground up, this allows the user to use CLI to access any state object or attribute in the system and display it in the format they are familiar with.

Custom CLI commands also provide the same auto-completion and help features that come with native SR Linux commands.

So how does this benefit the user? There are few use cases that we could think of like:
- Use the same MOP and command set that you previously used for another vendor
- Use the same automation or monitoring scripts that was written for another vendor
- allow users to start using SR Linux using the same commands they used for another vendor

All these are CLI heavy use cases. You may have more use cases in your mind.

This is awesome! But how do i put this into action?

## What is MultiCLI about?

The mission of MultiCLI is to get you started with SR Linux CLI customization feature for your environment.

As part of this project, we are publishing custom CLI plugins for `show` commands that will match the command and output of our friends in the industry.

The user community is free to take these scripts, use them as is or modify them based on their end goal. We will also be happy to accept new contributions from the community.

## Learn how to customize SR Linux CLI

For those intereted in learning the process of customizing the SR Linux CLI, refer to the official [SR Linux CLI plug-in guide](https://documentation.nokia.com/srlinux/24-10/title/cli_plugin.html).

For practical experience, start by using the beginner SReXperts hackathon use case [here](https://github.com/nokia/SReXperts/tree/main/hackathon/activities/srlinux-i-cli-plugin-show-version) following by an intermediate use case [here](https://github.com/nokia/SReXperts/tree/main/hackathon/activities/srlinux-i-custom-cli).

Also, check out these blogs on SR Linux CLI customization.

## Testing scripts

With the power of [Containerlab](https://containerlab.dev/) and the free SR Linux docker image, testing these custom CLI commands is a simple process. This repo contains sample lab toplogies with startup configs where these custom commands can be tested.

To test these scripts:
- Clone this repo to your host or use codespaces
- Deploy the SR Linux lab referenced in the lab directory
- All custom CLI plugin files are bound to the nodes using the `bind` function in the topology file
- Login to any node and try these commands

## MultiCLI Scripts

This repo is structured based on the vendor that we try to match in SR Linux CLI.

In this initial release, we have scripts for:

- [Arista EOS](Arista/)
- [Cisco NX-OS]()
- [Juniper JUNOS]()
- [Nokia SR OS]()

## Resources for further learning

* [SR Linux documentation](https://documentation.nokia.com/srlinux/)
* [Learn SR Linux](https://learn.srlinux.dev/)
* [YANG Browser](https://yang.srlinux.dev/)
* [gNxI Browser](https://gnxi.srlinux.dev/)
