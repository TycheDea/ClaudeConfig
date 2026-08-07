import datetime, hashlib, json, shutil, subprocess
from pathlib import Path

D = Path(__file__).resolve().parent
GAME = Path(r"C:\Users\egm_8\IdeaProjects\vordar")
CLAUDE = GAME / ".claude"
ledger = []
stderrs = []


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")


def digest_bytes(value):
    return {"bytes": len(value), "sha256": hashlib.sha256(value).hexdigest()}


def file_fact(path):
    try:
        data = path.read_bytes()
        return {"path": str(path), **digest_bytes(data)}
    except Exception as exc:
        return {"path": str(path), "value": "UNKNOWN", "reason": str(exc)}


def run(executable, arguments, *, cwd=None, timeout=20, binary=False, destination=None):
    start = now()
    destination = str(destination or D / "raw.json")
    try:
        completed = subprocess.run(
            [executable, *arguments], cwd=cwd, capture_output=True, timeout=timeout, shell=False
        )
        stdout, stderr, code = completed.stdout, completed.stderr, completed.returncode
    except Exception as exc:
        stdout, stderr, code = b"", repr(exc).encode("utf-8"), None
    ledger.append(
        {
            "executable": str(executable),
            "arguments": [str(argument) for argument in arguments],
            "start_utc": start,
            "end_utc": now(),
            "exit_code": code,
            "mutation_expected": False,
            "capture_destination": destination,
            "stdout": digest_bytes(stdout),
            "stderr": digest_bytes(stderr),
        }
    )
    if stderr:
        stderrs.append(f"{executable} {arguments}: {stderr.decode('utf-8', 'replace')}")
    if binary:
        return stdout, stderr, code
    return stdout.decode("utf-8", "replace"), stderr.decode("utf-8", "replace"), code


def ps(script):
    return run(
        "powershell.exe",
        [
            "-NoProfile",
            "-NonInteractive",
            "-ExecutionPolicy",
            "Bypass",
            "-Command",
            "$ErrorActionPreference='Stop'; " + script,
        ],
    )


def json_ps(script):
    stdout, stderr, code = ps(script)
    try:
        return json.loads(stdout), {
            "exit_code": code,
            "stderr": stderr,
            "reason": None if code == 0 else "PowerShell command failed",
            "source": "PowerShell read-only query",
        }
    except json.JSONDecodeError:
        return {"value": "UNKNOWN", "reason": stderr or "non-JSON output"}, {
            "exit_code": code,
            "stderr": stderr,
            "reason": "PowerShell command failed" if code is not None else "PowerShell process could not start",
            "source": "PowerShell read-only query",
        }


def git_repo(root):
    stdout, _stderr, head_code = run("git", ["-C", str(root), "rev-parse", "HEAD"])
    head = stdout.strip() if head_code == 0 else "UNKNOWN"
    raw_status, _stderr, status_code = run(
        "git", ["-C", str(root), "status", "--porcelain=v1", "-z", "--untracked-files=all"], binary=True
    )
    return {
        "root": str(root),
        "head": head,
        "head_source": str(root) + " git rev-parse HEAD",
        "status": {
            **digest_bytes(raw_status),
            "exit_code": status_code,
            "source": str(root) + " exact git status --porcelain=v1 -z --untracked-files=all bytes",
        },
    }


probes = {}
probes["repositories"] = {"game": git_repo(GAME), "nested_claude": git_repo(CLAUDE)}
identity, _identity_query = json_ps(
    "[pscustomobject]@{Path=(Get-Command powershell.exe -ErrorAction Stop).Source;"
    "Version=$PSVersionTable.PSVersion.ToString();Edition=$PSEdition;"
    "LanguageMode=$ExecutionContext.SessionState.LanguageMode.ToString();"
    "Elevated=([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent())."
    "IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)} | ConvertTo-Json -Compress"
)
probes["powershell_identity"] = identity

names = "Get-VM New-VM Remove-VM New-VHD Set-VM Set-VMMemory Set-VMProcessor Get-VMFirmware Set-VMFirmware Add-VMDvdDrive Remove-VMDvdDrive Get-VMDvdDrive Add-VMHardDiskDrive Get-VMHardDiskDrive Get-VMNetworkAdapter Set-VMNetworkAdapter Connect-VMNetworkAdapter Disconnect-VMNetworkAdapter Get-VMSwitch New-VMSwitch Remove-VMSwitch Get-VMIntegrationService Disable-VMIntegrationService Start-VM Stop-VM Get-NetIPAddress New-NetIPAddress Remove-NetIPAddress Get-NetRoute Get-DnsClientServerAddress Get-NetFirewallRule New-NetFirewallRule Remove-NetFirewallRule".split()
commands = []
for name in names:
    script = (
        f"$c=Get-Command -Name '{name}' -ErrorAction SilentlyContinue; "
        "$result=if($null -ne $c){[pscustomobject]@{"
        f"name='{name}';presence=$true;parameters=@($c.Parameters.Keys|Sort-Object);"
        "module=$c.Module.Name;version=$c.Module.Version.ToString();path=$c.Module.Path"
        "}}else{[pscustomobject]@{"
        f"name='{name}';presence=$false;parameters=@();module=$null;version=$null;path=$null;"
        "reason='command absent'}}; $result | ConvertTo-Json -Compress"
    )
    command, query = json_ps(script)
    if not isinstance(command, dict) or command.get("name") != name:
        commands.append(
            {
                "name": name,
                "presence": False,
                "parameters": [],
                "module": None,
                "version": None,
                "path": None,
                "reason": "command query did not return its requested structured result",
                "query": query,
            }
        )
        continue
    command["query"] = query
    if command["presence"]:
        module_file = file_fact(Path(command["path"]))
        if "sha256" not in module_file:
            command.update(
                {
                    "presence": False,
                    "parameters": [],
                    "module": None,
                    "version": None,
                    "path": None,
                    "reason": "command module file could not be read: " + module_file["reason"],
                }
            )
        else:
            command["module_file"] = module_file
    commands.append(command)
probes["commands"] = commands

for key, script in {
    "secure_boot": "Get-VMFirmware -VMName 'VordarPrimeOption2' -ErrorAction Stop | ConvertTo-Json -Compress -Depth 8",
    "vm_switch_adapter": "[pscustomobject]@{vms=@(Get-VM -ErrorAction Stop | Select-Object Name,Id,State);switches=@(Get-VMSwitch -ErrorAction Stop | Select-Object Name,Id,SwitchType);adapters=@(Get-VMNetworkAdapter -VMName * -ErrorAction Stop | Select-Object VMName,MacAddress,Name,SwitchName)} | ConvertTo-Json -Compress -Depth 8",
    "network_firewall": "[pscustomobject]@{addresses=@(Get-NetIPAddress -ErrorAction Stop | Select-Object IPAddress,PrefixLength,InterfaceAlias,AddressFamily,InterfaceIndex,AddressState,PolicyStore);routes=@(Get-NetRoute -ErrorAction Stop | Select-Object DestinationPrefix,NextHop,RouteMetric,InterfaceAlias,InterfaceIndex,AddressFamily,PolicyStore);dns=@(Get-DnsClientServerAddress -ErrorAction Stop | Select-Object InterfaceAlias,InterfaceIndex,AddressFamily,ServerAddresses);firewall=@(Get-NetFirewallRule -ErrorAction Stop | Select-Object Name,DisplayName,InstanceID,Enabled,Direction,Action,Profile,PolicyStoreSourceType)} | ConvertTo-Json -Compress -Depth 12",
}.items():
    facts, query = json_ps(script)
    probes[key] = {"facts": facts, "query": query}

wsl_raw, wsl_stderr, wsl_code = run(
    "wsl.exe", ["--list", "--verbose"], binary=True, destination=D / "wsl-list.raw"
)
(D / "wsl-list.raw").write_bytes(wsl_raw)
wsl_text = wsl_raw.decode("utf-16le", "replace").replace("\x00", "")
registry, registry_query = json_ps(
    "$root=Get-ItemProperty -LiteralPath 'HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Lxss' -ErrorAction Stop; "
    "$records=@(Get-ChildItem -LiteralPath 'HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Lxss' -ErrorAction Stop | "
    "Where-Object {$_.PSChildName -match '^\\{[0-9A-Fa-f-]{36}\\}$'} | ForEach-Object {"
    "$p=Get-ItemProperty -LiteralPath $_.PSPath -ErrorAction Stop; "
    "if($null -ne $p.DistributionName){[pscustomobject]@{guid=$_.PSChildName;name=$p.DistributionName;"
    "base_path=$p.BasePath;registry_version=$p.Version}}}); "
    "[pscustomobject]@{default_guid=$root.DefaultDistribution;records=$records} | ConvertTo-Json -Compress -Depth 6"
)
list_records = {}
for line in wsl_text.splitlines():
    fields = line.strip().lstrip("*").split()
    if len(fields) >= 3 and fields[0].lower() != "name":
        list_records[fields[0]] = {"state": fields[-2], "wsl_version": fields[-1], "default": line.lstrip().startswith("*")}
normalized = []
if isinstance(registry, dict):
    for record in registry.get("records", []) or []:
        listed = list_records.get(record.get("name"), {})
        normalized.append(
            {
                **record,
                "state": listed.get("state"),
                "wsl_version": listed.get("wsl_version"),
                "default": record.get("guid") == registry.get("default_guid"),
            }
        )
probes["wsl"] = {
    "registrations_text": wsl_text,
    "registrations": normalized,
    "default_registration_guid": registry.get("default_guid") if isinstance(registry, dict) else None,
    "default_registration_identity": next((x["name"] for x in normalized if x["default"]), None),
    "queries": {
        "list": {
            "exit_code": wsl_code,
            "stderr": wsl_stderr.decode("utf-8", "replace"),
            "reason": None if wsl_code == 0 else "wsl.exe --list --verbose failed",
            "source": "UTF-16LE wsl.exe --list --verbose",
        },
        "registry": registry_query,
    },
    "lifecycle": "not invoked",
}

for name in ["gpg", "gpgv", "sqop", "tar", "7z"]:
    path = shutil.which(name)
    executable = {"name": name, "path": path or "ABSENT"}
    if path:
        stdout, _stderr, version_code = run(path, ["--version"])
        authenticode, authenticode_query = json_ps(
            f"Get-AuthenticodeSignature -LiteralPath '{path}' -ErrorAction Stop | "
            "Select-Object Status,StatusMessage | ConvertTo-Json -Compress"
        )
        executable.update(
            {
                "file": file_fact(Path(path)),
                "version": stdout.splitlines()[0] if stdout else "UNKNOWN",
                "version_exit": version_code,
                "authenticode": authenticode,
                "authenticode_query": authenticode_query,
                "pe_imports": {"value": "UNKNOWN", "reason": "bounded probe; no PE import tool invoked"},
                "license": {"value": "UNKNOWN", "reason": "no license file selected"},
            }
        )
    probes.setdefault("executables", []).append(executable)

probes["elevation"] = probes["powershell_identity"].get("Elevated", "UNKNOWN")
top = {"schema_version": 3, "capture_utc": now(), "mutation_expected": False, "probes": probes, "ledger": ledger}
(D / "raw.json").write_text(json.dumps(top, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
(D / "commands.json").write_text(json.dumps(ledger, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
stderr_text = "\n".join(stderrs).replace("\r\n", "\n").replace("\r", "\n")
stderr_lines = [line.rstrip(" \t") for line in stderr_text.split("\n")]
while stderr_lines and not stderr_lines[-1]:
    stderr_lines.pop()
(D / "stderr.log").write_text("\n".join(stderr_lines) + "\n", encoding="utf-8", newline="\n")
(D / "red-fixture.json").write_text(json.dumps({"probes": {"wsl": {}}}) + "\n", encoding="utf-8", newline="\n")
manifest = []
for path in sorted(D.iterdir()):
    if path.name != "sha256.txt" and path.is_file():
        manifest.append(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}")
(D / "sha256.txt").write_text("\n".join(manifest) + "\n", encoding="utf-8", newline="\n")
