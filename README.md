# python-pacman

Simple Python interface to Arch Linux package manager (pacman).

Requires Python 3.

### Examples

* Refresh master package list: `pacman.refresh()`
* Install a package: `pacman.install("php")`
  * Install multiple packages: `pacman.install(["php", "php-fpm"])`
  * Install a package, and don't install dependencies that are already installed: `pacman.install("php", needed=True)`
* Remove a package: `pacman.remove("php")`
  * Remove multiple packages: `pacman.remove(["php", "php-fpm"])`
  * Remove and purge package: `pacman.remove("php", purge=True)`
* Upgrade all packages: `pacman.upgrade()`
  * Upgrade specific packages: `pacman.upgrade(["php", "php-fpm"])`
* List all installed packages: `pacman.get_installed()` (returns dict of id, version, upgradable status)
* List all available packages: `pacman.get_available()` (returns dict of id, version, repo name)
* Get info for a package: `pacman.get_info("php")` (returns dict, info labels as keys)
* Determine if package came from the AUR or not: `pacman.is_aur("php")`
* Get uninstalled dependencies of a package: `pacman.needs_for("php")` (returns list of package names)
* Get installed packages that depend on this one: `pacman.depends_for("php")` (returns list of package names)
* Check if a package is installed: `pacman.is_installed("php")` (returns bool)
* Use an AUR helper instead of pacman: `pacman.set_bin("yay")`
