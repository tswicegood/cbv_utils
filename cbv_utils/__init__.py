"""
.. todo:: Add module-level documentation
"""

# You can use the following four lines to tweak your version number.
# Following [semantic versioning][1], the `major` variable contains
# major version of your software.  Once users are using your package
# in production, it should be a 1.  The `minor` version is used to
# signify new features being added.  Once the `major` version is at 1
# changes to the minor versions should only add features, never take
# away or break features.
#
# The `third` version should generally be at 0 for released software
# and incremented only when a fix is introduced.  During development,
# this number include an `alpha`, `beta`, or `rc` suffix to denote that
# it is not a full release.
#
# The `extra` number is only taken into account in two scenarios:
#   * The `third` number contains an non-numeric character (such as
#     alpha, or beta).  This is used to show increments in the alpha
#     or beta releases.
#   * The `extra` number is non-zero.  This is not specified by SemVer
#     but can be used to signify changes that do not effect the
#     functioning code.  Examples are documentation changes, additional
#     test cases, and so forth.
#
# [1]: http://semver.org

major = "0"
minor = "1"
third = "2"
extra = "0"

# You should not need to edit anything beyond this point.
__version_parts__ = (major, minor, third)

if not third.isdigit() or extra != "0":
    __version_parts__ += (extra, )
__version__ = ".".join(__version_parts__)

version = "%s version %s" % (__name__, __version__)
