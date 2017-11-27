# ------------------------------------------------------------------------------
# ELEVATE PRIVALEDGES
# ------------------------------------------------------------------------------

if [ $EUID != 0 ]; then
    sudo "$0" "$@"
    exit $?
fi

brew install rethinkdb

# ------------------------------------------------------------------------------
# DETECT CURRENT SYSTEM ENVIRONMENT
# ------------------------------------------------------------------------------

SYSTEM_TYPE_UNKNOWN="unknown"
SYSTEM_TYPE_MAC="mac"
SYSTEM_TYPE_LINUX="linux"

CURR_SYSTEM_TYPE="$SYSTEM_TYPE_UNKNOWN"

# Determine current system type

echo ""
echo "---------------------------------------------------"
echo "DETECTING SYSTEM"

if [ "$OSTYPE" =~ "linux"* ]; then
  CURR_SYSTEM_TYPE=$SYSTEM_TYPE_LINUX
  sudo apt-get update;

elif [ "$OSTYPE" == "darwin"* ]; then
  CURR_SYSTEM_TYPE=$SYSTEM_TYPE_MAC

fi

if [ "$CURR_SYSTEM_TYPE" == "$SYSTEM_TYPE_MAC" ]; then
  echo "--Current operating system: macOS"
fi

if [ "$CURR_SYSTEM_TYPE" == "$SYSTEM_TYPE_LINUX" ]; then
  echo "--Current operating system: Linux"
fi


# ------------------------------------------------------------------------------
# INSTALL TURING CLI
# ------------------------------------------------------------------------------

# Set paths for use

PATH_BIN="/usr/local/bin"
PATH_BIN_CLI_ALIAS="$PATH_BIN/turing"

PATH_APP="/etc/turing/framework"
PATH_APP_CLI="$PATH_APP/system/services/cli/cli.py"
PATH_STARTUP_SCRIPT="$PATH_APP/system/run/turing_boot.sh"
PATH_SHUTDOWN_SCRIPT="$PATH_APP/system/run/turing_stop.sh"

# If a file exists at the intended cli alias location,
# remove that file and re-create the alias needed for
# operation.

DOES_ALIAS_REQUIRE_CREATION=false

echo ""
echo "---------------------------------------------------"
echo "INSTALLING CLI"

echo "--Checking integrity of CLI symlink."

if [ -e "$PATH_BIN_CLI_ALIAS" ]; then
  if [ -h "$PATH_BIN_CLI_ALIAS" ]; then
    PATH_BIN_ALIAS_REALPATH=$(readlink "$PATH_BIN_CLI_ALIAS")

    if [ "$PATH_BIN_ALIAS_REALPATH" == "$PATH_APP_CLI" ]; then
      echo "--CLI alias confirmed."
    else
      echo "--Alias is a symlink, but pointing to the wrong location."

      rm "$PATH_BIN_CLI_ALIAS"
      DOES_ALIAS_REQUIRE_CREATION=true

    fi

  else
    echo "--Current CLI alias is an unexpected file. May be a collision with another application."
  fi
else
  DOES_ALIAS_REQUIRE_CREATION=true
fi


if $DOES_ALIAS_REQUIRE_CREATION; then
  echo "--Creating symlink at $PATH_BIN_CLI_ALIAS"

  # Set CLI alias and access permissions for script

  sudo ln -s "$PATH_APP/system/services/cli/cli.py" "$PATH_BIN/turing"
  chmod +x "$PATH_BIN_CLI_ALIAS"
fi

# Set permissions to all for start & shutdown scripts

chmod +x "$PATH_STARTUP_SCRIPT"
chmod +x "$PATH_SHUTDOWN_SCRIPT"

# Output empty lines for visual sanity

echo ""
echo ""
