Velox Repository
Official package repository for Velox Linux — custom tools, wallpapers, and extras built for the Velox ecosystem.


Adding the Repository
Add the following to your /etc/pacman.conf:
ini[velox_repo]
SigLevel = Never
Server = https://thelinutubetltos.github.io/velox_repo/$arch


Then sync:
bashsudo pacman -Sy

Packages
PackageDescriptionvelox-wallpapersOfficial Velox Linux wallpapersvelox-toolsVelox system utilities and scripts
Building Packages

Packages in this repo are built using standard Arch Linux makepkg and added with repo-add.
Links

Velox Linux ISO
The Linux Tube
