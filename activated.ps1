$ErrorActionPreference = "Stop"

$script_directory = Split-Path $MyInvocation.MyCommand.Path -Parent

& "$script_directory/venv/Scripts/activate"
& "$args"
