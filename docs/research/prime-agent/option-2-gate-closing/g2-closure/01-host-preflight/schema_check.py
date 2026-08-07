import json
import re
import sys
from pathlib import Path

path = Path(sys.argv[1] if len(sys.argv) > 1 else "raw.json")
data = json.loads(path.read_text(encoding="utf-8"))
EXPECTED_COMMANDS = {
    "Get-VM", "New-VM", "Remove-VM", "New-VHD", "Set-VM", "Set-VMMemory", "Set-VMProcessor",
    "Get-VMFirmware", "Set-VMFirmware", "Add-VMDvdDrive", "Remove-VMDvdDrive", "Get-VMDvdDrive",
    "Add-VMHardDiskDrive", "Get-VMHardDiskDrive", "Get-VMNetworkAdapter", "Set-VMNetworkAdapter",
    "Connect-VMNetworkAdapter", "Disconnect-VMNetworkAdapter", "Get-VMSwitch", "New-VMSwitch",
    "Remove-VMSwitch", "Get-VMIntegrationService", "Disable-VMIntegrationService", "Start-VM", "Stop-VM",
    "Get-NetIPAddress", "New-NetIPAddress", "Remove-NetIPAddress", "Get-NetRoute", "Get-DnsClientServerAddress",
    "Get-NetFirewallRule", "New-NetFirewallRule", "Remove-NetFirewallRule",
}
EXPECTED_WSL_NAMES = {"Ubuntu", "docker-desktop"}
SHA256 = re.compile(r"^[0-9a-f]{64}$")
GUID = re.compile(r"^\{[0-9A-Fa-f-]{36}\}$")


def fail(message):
    raise SystemExit("RED " + message)


def is_digest(value):
    return isinstance(value, dict) and isinstance(value.get("bytes"), int) and value["bytes"] >= 0 and isinstance(value.get("sha256"), str) and SHA256.fullmatch(value["sha256"])


def is_query(value):
    return isinstance(value, dict) and isinstance(value.get("exit_code"), (int, type(None))) and isinstance(value.get("stderr"), str) and isinstance(value.get("reason"), (str, type(None))) and isinstance(value.get("source"), str) and value["source"]


for key in ["schema_version", "capture_utc", "mutation_expected", "probes", "ledger"]:
    if key not in data:
        fail("missing top-level field: " + key)
if data["schema_version"] != 3 or data["mutation_expected"] is not False:
    fail("top-level capture contract")
probes = data["probes"]
for key in ["repositories", "powershell_identity", "commands", "secure_boot", "vm_switch_adapter", "network_firewall", "wsl", "executables", "elevation"]:
    if key not in probes:
        fail("missing probes." + key)

roots = {"game": r"C:\Users\egm_8\IdeaProjects\vordar", "nested_claude": r"C:\Users\egm_8\IdeaProjects\vordar\.claude"}
for name, root in roots.items():
    repository = probes["repositories"].get(name)
    if not isinstance(repository, dict) or repository.get("root") != root or not isinstance(repository.get("head"), str) or not repository["head"] or repository["head"] == "UNKNOWN":
        fail("repository identity " + name)
    status = repository.get("status")
    if not is_digest(status) or not isinstance(status.get("exit_code"), int) or not isinstance(status.get("source"), str):
        fail("repository status " + name)
if probes["repositories"]["game"]["head"] == probes["repositories"]["nested_claude"]["head"] and roots["game"] == roots["nested_claude"]:
    fail("repository identities not distinct")

identity = probes["powershell_identity"]
if not isinstance(identity, dict) or not isinstance(identity.get("Path"), str) or not identity["Path"] or not isinstance(identity.get("Elevated"), bool):
    fail("structured PowerShell identity")
if probes["elevation"] is not identity["Elevated"]:
    fail("structured elevation")

commands = probes["commands"]
if not isinstance(commands, list) or {command.get("name") for command in commands if isinstance(command, dict)} != EXPECTED_COMMANDS or len(commands) != len(EXPECTED_COMMANDS):
    fail("exact command set")
for command in commands:
    if not isinstance(command.get("presence"), bool) or not isinstance(command.get("parameters"), list) or command["parameters"] != sorted(command["parameters"], key=str.casefold) or not is_query(command.get("query")):
        fail("command structure " + str(command.get("name")))
    if command["query"]["reason"] == "parse failure" or "EmptyPipeElement" in command["query"]["stderr"]:
        fail("command query parser placeholder " + command["name"])
    if command["presence"]:
        module_file = command.get("module_file")
        if not command["parameters"] or not all(isinstance(parameter, str) and parameter for parameter in command["parameters"]) or not isinstance(command.get("module"), str) or not command["module"] or not isinstance(command.get("version"), str) or not command["version"] or not isinstance(command.get("path"), str) or not command["path"] or not is_digest(module_file) or module_file.get("path") != command["path"]:
            fail("present command metadata " + command["name"])
    elif not isinstance(command.get("reason"), str) or not command["reason"]:
        fail("absent command evidence " + command["name"])

for name in ["secure_boot", "vm_switch_adapter", "network_firewall"]:
    result = probes[name]
    if not isinstance(result, dict) or "facts" not in result or not is_query(result.get("query")):
        fail("explicit query result " + name)
    if result["query"]["reason"] == "parse failure":
        fail("query parser placeholder " + name)

wsl = probes["wsl"]
if not isinstance(wsl, dict) or not isinstance(wsl.get("registrations_text"), str) or not isinstance(wsl.get("registrations"), list) or not is_query((wsl.get("queries") or {}).get("list")) or not is_query((wsl.get("queries") or {}).get("registry")):
    fail("normalized WSL structure")
if {record.get("name") for record in wsl["registrations"] if isinstance(record, dict)} != EXPECTED_WSL_NAMES or len(wsl["registrations"]) != len(EXPECTED_WSL_NAMES):
    fail("normalized WSL registration names")
defaults = []
for record in wsl["registrations"]:
    if not GUID.fullmatch(record.get("guid", "")) or not isinstance(record.get("base_path"), str) or not record["base_path"] or not isinstance(record.get("registry_version"), int) or not isinstance(record.get("wsl_version"), str) or not record["wsl_version"] or not isinstance(record.get("state"), str) or not record["state"] or not isinstance(record.get("default"), bool):
        fail("normalized WSL registration record")
    if record["default"]:
        defaults.append(record)
if len(defaults) != 1 or wsl.get("default_registration_guid") != defaults[0]["guid"] or wsl.get("default_registration_identity") != defaults[0]["name"]:
    fail("WSL default registration")

if not isinstance(probes["executables"], list):
    fail("executable candidates")
for executable in probes["executables"]:
    if not isinstance(executable, dict) or not isinstance(executable.get("name"), str) or not executable["name"] or not isinstance(executable.get("path"), str) or not executable["path"]:
        fail("executable candidate record")
    if executable["path"] != "ABSENT" and (not is_digest(executable.get("file")) or not isinstance(executable.get("version_exit"), int) or not is_query(executable.get("authenticode_query"))):
        fail("present executable candidate record")

if not isinstance(data["ledger"], list) or not data["ledger"]:
    fail("external process ledger")
for index, row in enumerate(data["ledger"]):
    if not isinstance(row, dict) or not isinstance(row.get("executable"), str) or not row["executable"] or not isinstance(row.get("arguments"), list) or not all(isinstance(argument, str) for argument in row["arguments"]) or not isinstance(row.get("start_utc"), str) or not isinstance(row.get("end_utc"), str) or not isinstance(row.get("exit_code"), (int, type(None))) or row.get("mutation_expected") is not False or not isinstance(row.get("capture_destination"), str) or not row["capture_destination"] or not is_digest(row.get("stdout")) or not is_digest(row.get("stderr")):
        fail("ledger[" + str(index) + "]")
for root in roots.values():
    if not any(row["executable"] == "git" and row["arguments"] == ["-C", root, "rev-parse", "HEAD"] for row in data["ledger"]):
        fail("missing rev-parse ledger " + root)
    if not any(row["executable"] == "git" and row["arguments"] == ["-C", root, "status", "--porcelain=v1", "-z", "--untracked-files=all"] for row in data["ledger"]):
        fail("missing exact status ledger " + root)
print("GREEN schema valid:", path)
