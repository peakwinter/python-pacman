# python-pacman

Simple Python interface to Arch Linux package manager (pacman)

### Examples

* Refresh master package list: `pacman.refresh()`
* Install a package: `pacman.install("php")`
* Remove a package: `pacman.remove("php", purge=True)`
* Upgrade all packages: `pacman.upgrade()`
* List all installed packages: `pacman.get_installed()` (returns dict of id, version, upgradable status)
* List all available packages: `pacman.get_available()` (returns dict of id, version, repo name)
* Get info for a package: `pacman.get_info("php")` (returns dict, info labels as keys)
* Get uninstalled dependencies of a package: `pacman.needs_for("php")` (returns list of package names)
* Get installed packages that depend on this one: `pacman.depends_for("php")` (returns list of package names)
* Check if a package is installed: `pacman.is_installed("php")` (returns bool)

All functions that allow a package name as parameter (except `get_info`) will accept either a single package name or a list of multiple names.
