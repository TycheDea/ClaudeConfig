#!/usr/bin/env python3
"""Read-only, judgment-free G1 host inventory capture."""

from __future__ import annotations

import copy
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ARTIFACT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = ARTIFACT_DIR.parents[5]
SCHEMA_CHECK = ARTIFACT_DIR / "schema_check.py"
COMMANDS: list[dict[str, Any]] = []


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def decode_output(value: bytes) -> str:
    if not value:
        return ""
    if value.startswith((b"\xff\xfe", b"\xfe\xff")) or value.count(b"\x00") > len(value) // 4:
        try:
            return value.decode("utf-16").replace("\r\n", "\n")
        except UnicodeDecodeError:
            pass
    for encoding in ("utf-8", "cp1252"):
        try:
            return value.decode(encoding).replace("\r\n", "\n")
        except UnicodeDecodeError:
            continue
    return value.decode("utf-8", errors="replace").replace("\r\n", "\n")


def sanitize_stderr(value: str) -> str:
    sanitized = value.replace(str(PROJECT_ROOT), "%PROJECT_ROOT%")
    sanitized = sanitized.replace(str(PROJECT_ROOT).replace("\\", "/"), "%PROJECT_ROOT%")
    sanitized = re.sub(r"(?i)C:\\Users\\[^\\\s]+", "%USER_PROFILE%", sanitized)
    sanitized = re.sub(r"(?i)C:/Users/[^/\s]+", "%USER_PROFILE%", sanitized)
    return sanitized


def run_command(command_id: str, argv: list[str], purpose: str) -> dict[str, Any]:
    started = utc_now()
    try:
        completed = subprocess.run(
            argv,
            cwd=PROJECT_ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            shell=False,
        )
        exit_code = completed.returncode
        stdout = decode_output(completed.stdout)
        stderr = sanitize_stderr(decode_output(completed.stderr))
    except OSError as error:
        exit_code = 127
        stdout = ""
        stderr = sanitize_stderr(f"{type(error).__name__}: {error}\n")
    ended = utc_now()
    entry = {
        "id": command_id,
        "purpose": purpose,
        "argv": argv,
        "command": subprocess.list2cmdline(argv),
        "started_at_utc": started,
        "ended_at_utc": ended,
        "exit_code": exit_code,
        "stdout": stdout,
        "stderr": stderr,
    }
    COMMANDS.append(entry)
    return entry


def powershell(command_id: str, script: str, purpose: str) -> dict[str, Any]:
    prelude = (
        "$ProgressPreference='SilentlyContinue';"
        "$OutputEncoding=[Console]::OutputEncoding=[System.Text.UTF8Encoding]::new($false);"
    )
    return run_command(
        command_id,
        ["powershell.exe", "-NoLogo", "-NoProfile", "-NonInteractive", "-Command", prelude + script],
        purpose,
    )


def parsed_json(entry: dict[str, Any]) -> Any | None:
    if entry["exit_code"] != 0 or not entry["stdout"].strip():
        return None
    try:
        return json.loads(entry["stdout"])
    except json.JSONDecodeError:
        return None


def observed(value: Any, source: str, reason: str | None = None) -> dict[str, Any]:
    result: dict[str, Any] = {"value": value, "source_command_id": source}
    if reason is not None:
        result["reason"] = reason
    return result


def unknown(source: str, reason: str) -> dict[str, Any]:
    return observed("UNKNOWN", source, reason)


def parse_wsl_distributions(entry: dict[str, Any]) -> list[dict[str, Any]] | None:
    if entry["exit_code"] != 0:
        return None
    rows: list[dict[str, Any]] = []
    lines = [line.rstrip() for line in entry["stdout"].splitlines() if line.strip()]
    for line in lines:
        stripped = line.strip()
        if "NAME" in stripped.upper() and "STATE" in stripped.upper() and "VERSION" in stripped.upper():
            continue
        is_default = stripped.startswith("*")
        if is_default:
            stripped = stripped[1:].strip()
        columns = re.split(r"\s{2,}", stripped)
        if len(columns) >= 3:
            rows.append(
                {
                    "name": columns[0],
                    "state": columns[1],
                    "version": columns[2],
                    "default": is_default,
                }
            )
    if rows or not lines:
        return rows
    return None


def remove_path(document: dict[str, Any], dotted_path: str) -> None:
    components = dotted_path.split(".")
    current: dict[str, Any] = document
    for component in components[:-1]:
        current = current[component]
    current.pop(components[-1], None)


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    started_at = utc_now()

    windows_entry = powershell(
        "windows_os",
        "$ErrorActionPreference='Stop';"
        "$cv=Get-ItemProperty -LiteralPath 'HKLM:\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion';"
        "$os=Get-CimInstance -ClassName Win32_OperatingSystem;"
        "[pscustomobject]@{product_name=$cv.ProductName;display_version=$cv.DisplayVersion;"
        "release_id=$cv.ReleaseId;current_build=$cv.CurrentBuild;current_build_number=$cv.CurrentBuildNumber;"
        "ubr=$cv.UBR;build_lab_ex=$cv.BuildLabEx;version=$os.Version;build_number=$os.BuildNumber;"
        "os_architecture=$os.OSArchitecture;caption=$os.Caption}|ConvertTo-Json -Compress -Depth 5",
        "Read Windows build, version, and architecture from the CurrentVersion registry key and Win32_OperatingSystem.",
    )
    cpu_entry = powershell(
        "cpu_memory",
        "$ErrorActionPreference='Stop';"
        "$cs=Get-CimInstance -ClassName Win32_ComputerSystem;"
        "$cpus=@(Get-CimInstance -ClassName Win32_Processor|ForEach-Object{[pscustomobject]@{"
        "name=$_.Name;architecture_code=$_.Architecture;address_width=$_.AddressWidth;"
        "number_of_cores=$_.NumberOfCores;number_of_logical_processors=$_.NumberOfLogicalProcessors}});"
        "[pscustomobject]@{runtime_os_architecture=[Runtime.InteropServices.RuntimeInformation]::OSArchitecture.ToString();"
        "computer_system_logical_processors=$cs.NumberOfLogicalProcessors;total_physical_memory_bytes=$cs.TotalPhysicalMemory;"
        "processors=$cpus}|ConvertTo-Json -Compress -Depth 6",
        "Read CPU architecture/core counts and total physical RAM.",
    )
    storage_entry = powershell(
        "storage_volumes",
        "$ErrorActionPreference='Stop';"
        "function Measure-PathVolume([string]$label,[string]$path){"
        "$full=[IO.Path]::GetFullPath($path);$root=[IO.Path]::GetPathRoot($full);$drive=[IO.DriveInfo]::new($root);"
        "[pscustomobject]@{label=$label;path=$full;volume_root=$root;drive_format=$drive.DriveFormat;"
        "drive_type=$drive.DriveType.ToString();total_bytes=$drive.TotalSize;free_bytes=$drive.AvailableFreeSpace}};"
        "$project=(Get-Location).Path;$local=[Environment]::GetFolderPath([Environment+SpecialFolder]::LocalApplicationData);"
        "[pscustomobject]@{project_volume=(Measure-PathVolume 'project' $project);"
        "candidate_guest_storage_volume=(Measure-PathVolume 'windows_local_application_data' $local)}|ConvertTo-Json -Compress -Depth 6",
        "Read free bytes for the project volume and the Windows LocalApplicationData volume used as the unselected guest-storage candidate location.",
    )
    feature_entry = powershell(
        "windows_virtualization_features",
        "$ErrorActionPreference='Stop';"
        "$names=@('Microsoft-Windows-Subsystem-Linux','VirtualMachinePlatform','HypervisorPlatform','Microsoft-Hyper-V-Hypervisor');"
        "$items=@(foreach($name in $names){$item=Get-CimInstance -ClassName Win32_OptionalFeature -Filter (\"Name='$name'\") -ErrorAction SilentlyContinue;"
        "if($null -eq $item){[pscustomobject]@{name=$name;install_state='UNKNOWN';caption=$null}}"
        "else{[pscustomobject]@{name=$item.Name;install_state=$item.InstallState;caption=$item.Caption}}});"
        "$items|ConvertTo-Json -Compress -Depth 5",
        "Read WSL and virtualization optional-feature states without changing them.",
    )
    wsl_status_entry = run_command("wsl_status", ["wsl.exe", "--status"], "Read WSL status without entering a distribution.")
    wsl_version_entry = run_command("wsl_version", ["wsl.exe", "--version"], "Read WSL component versions without entering a distribution.")
    wsl_list_entry = run_command(
        "wsl_registered_distributions",
        ["wsl.exe", "--list", "--verbose"],
        "List registered distribution names, states, and versions without starting one.",
    )
    wsl_help_entry = run_command(
        "wsl_external_termination_help",
        ["wsl.exe", "--help"],
        "Read wsl.exe help to detect externally invocable termination options without invoking them.",
    )
    virtualization_entry = powershell(
        "virtualization_capability",
        "$ErrorActionPreference='Stop';"
        "$cs=Get-CimInstance -ClassName Win32_ComputerSystem;"
        "$cpus=@(Get-CimInstance -ClassName Win32_Processor|ForEach-Object{[pscustomobject]@{"
        "name=$_.Name;virtualization_firmware_enabled=$_.VirtualizationFirmwareEnabled;"
        "vm_monitor_mode_extensions=$_.VMMonitorModeExtensions;"
        "second_level_address_translation_extensions=$_.SecondLevelAddressTranslationExtensions}});"
        "[pscustomobject]@{hypervisor_present=$cs.HypervisorPresent;processors=$cpus}|ConvertTo-Json -Compress -Depth 6",
        "Read hypervisor presence and processor virtualization capability flags.",
    )
    lxss_entry = powershell(
        "wsl_registration_registry",
        "$ErrorActionPreference='Stop';$root='HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Lxss';"
        "if(-not(Test-Path -LiteralPath $root)){[pscustomobject]@{exists=$false;default_distribution=$null;distributions=@()}|ConvertTo-Json -Compress -Depth 6;exit 0};"
        "$rootItem=Get-ItemProperty -LiteralPath $root;"
        "$distros=@(Get-ChildItem -LiteralPath $root|ForEach-Object{$p=Get-ItemProperty -LiteralPath $_.PSPath;[pscustomobject]@{"
        "registration_id=$_.PSChildName;distribution_name=$p.DistributionName;state=$p.State;version=$p.Version;"
        "base_path=$p.BasePath;flags=$p.Flags;default_uid=$p.DefaultUid;package_family_name=$p.PackageFamilyName}});"
        "[pscustomobject]@{exists=$true;default_distribution=$rootItem.DefaultDistribution;distributions=$distros}|ConvertTo-Json -Compress -Depth 7",
        "Read registered WSL distribution metadata from the host registry without entering or starting a distribution.",
    )
    gpu_entry = powershell(
        "host_graphics_adapters",
        "$ErrorActionPreference='Stop';"
        "$items=@(Get-CimInstance -ClassName Win32_VideoController|ForEach-Object{[pscustomobject]@{"
        "name=$_.Name;adapter_compatibility=$_.AdapterCompatibility;adapter_ram_bytes=$_.AdapterRAM;"
        "driver_version=$_.DriverVersion;driver_date=$_.DriverDate;video_processor=$_.VideoProcessor;"
        "status=$_.Status;pnp_device_id=$_.PNPDeviceID}});$items|ConvertTo-Json -Compress -Depth 6",
        "Read host graphics-adapter identities and driver metadata.",
    )
    gpu_management_entry = powershell(
        "gpu_management_visibility",
        "$cmd=Get-Command nvidia-smi.exe -ErrorAction SilentlyContinue;"
        "if($null -eq $cmd){[pscustomobject]@{installed=$false;executable=$null;query_exit_code=$null;query_output=$null}|ConvertTo-Json -Compress -Depth 5;exit 0};"
        "$output=@(& $cmd.Source --query-gpu=name,driver_version,memory.total --format=csv,noheader,nounits);$code=$LASTEXITCODE;"
        "[pscustomobject]@{installed=$true;executable=$cmd.Source;query_exit_code=$code;query_output=$output}|ConvertTo-Json -Compress -Depth 5;exit $code",
        "Use nvidia-smi only if already installed to read management visibility; no GPU workload is run.",
    )
    pi_identity_entry = powershell(
        "pi_executable_identity",
        "$commands=@(Get-Command pi -All -ErrorAction SilentlyContinue|ForEach-Object{"
        "$hash=$null;if($_.Path -and (Test-Path -LiteralPath $_.Path -PathType Leaf)){$hash=(Get-FileHash -Algorithm SHA256 -LiteralPath $_.Path).Hash};"
        "$version=$null;if($null -ne $_.Version){$version=$_.Version.ToString()};"
        "[pscustomobject]@{name=$_.Name;command_type=$_.CommandType.ToString();source=$_.Source;path=$_.Path;version=$version;sha256=$hash}});"
        "$commands|ConvertTo-Json -Compress -Depth 6",
        "Read installed Pi command identity and executable/shim digest without reading Pi state contents.",
    )
    pi_version_entry = powershell(
        "pi_version",
        "$cmd=Get-Command pi -ErrorAction SilentlyContinue;if($null -eq $cmd){Write-Error 'Pi executable not found';exit 127};& $cmd.Source --version;exit $LASTEXITCODE",
        "Invoke Pi's read-only version option.",
    )
    pi_process_entry = powershell(
        "pi_process_candidates",
        "$items=@(Get-Process -ErrorAction SilentlyContinue|Where-Object{$_.ProcessName -in @('pi','node')}|ForEach-Object{"
        "$path=$null;try{$path=$_.Path}catch{};[pscustomobject]@{process_id=$_.Id;name=$_.ProcessName;executable_path=$path}});"
        "$items|ConvertTo-Json -Compress -Depth 5",
        "Read only IDs, names, and executable paths for Pi/node process candidates; command lines are not requested.",
    )
    pi_state_entry = powershell(
        "pi_state_path_metadata",
        "$profile=[Environment]::GetFolderPath([Environment+SpecialFolder]::UserProfile);"
        "$paths=@([pscustomobject]@{label='user_pi_root';path=(Join-Path $profile '.pi')},"
        "[pscustomobject]@{label='user_pi_agent';path=(Join-Path $profile '.pi\\agent')},"
        "[pscustomobject]@{label='project_pi_root';path=(Join-Path (Get-Location).Path '.pi')});"
        "$results=@(foreach($spec in $paths){$exists=Test-Path -LiteralPath $spec.path;"
        "$self=$null;$children=@();if($exists){$item=Get-Item -LiteralPath $spec.path -Force;"
        "$self=[pscustomobject]@{name=$item.Name;full_name=$item.FullName;is_directory=$item.PSIsContainer;length=$item.Length;"
        "creation_time_utc=$item.CreationTimeUtc.ToString('o');last_write_time_utc=$item.LastWriteTimeUtc.ToString('o');attributes=$item.Attributes.ToString()};"
        "$children=@(Get-ChildItem -LiteralPath $spec.path -Force|ForEach-Object{[pscustomobject]@{name=$_.Name;full_name=$_.FullName;"
        "is_directory=$_.PSIsContainer;length=$_.Length;creation_time_utc=$_.CreationTimeUtc.ToString('o');"
        "last_write_time_utc=$_.LastWriteTimeUtc.ToString('o');attributes=$_.Attributes.ToString()}})};"
        "[pscustomobject]@{label=$spec.label;path=$spec.path;exists=$exists;metadata=$self;children=$children}});"
        "$results|ConvertTo-Json -Compress -Depth 8",
        "Read only Pi state-path names, existence, and filesystem metadata; no state file contents are read.",
    )

    windows = parsed_json(windows_entry)
    cpu = parsed_json(cpu_entry)
    storage = parsed_json(storage_entry)
    features = parsed_json(feature_entry)
    virtualization = parsed_json(virtualization_entry)
    lxss = parsed_json(lxss_entry)
    gpus = parsed_json(gpu_entry)
    gpu_management = parsed_json(gpu_management_entry)
    pi_identity = parsed_json(pi_identity_entry)
    pi_processes = parsed_json(pi_process_entry)
    pi_state = parsed_json(pi_state_entry)
    distributions = parse_wsl_distributions(wsl_list_entry)

    help_text = wsl_help_entry["stdout"]
    termination = None if not help_text.strip() else {
        "help_exit_code": wsl_help_entry["exit_code"],
        "wsl_terminate_option_listed": "--terminate" in help_text,
        "wsl_shutdown_option_listed": "--shutdown" in help_text,
        "commands_not_invoked": ["wsl.exe --terminate <DistributionName>", "wsl.exe --shutdown"],
    }

    raw = {
        "schema_version": "g1-host-platform-inventory-v1",
        "captured_at_utc": utc_now(),
        "capture_started_at_utc": started_at,
        "dependency": {
            "g0_artifact": ".claude/docs/research/prime-agent/option-2-gate-closing/00-evidence-freshness.md",
            "observed_verdict": "FRESH",
        },
        "host": {
            "windows": {
                "build": observed(windows, "windows_os") if windows is not None else unknown("windows_os", "Probe failed or returned non-JSON output."),
                "version": observed(windows, "windows_os") if windows is not None else unknown("windows_os", "Probe failed or returned non-JSON output."),
                "architecture": observed(windows.get("os_architecture"), "windows_os") if isinstance(windows, dict) else unknown("windows_os", "Probe failed or returned non-JSON output."),
            },
            "cpu": {
                "architecture": observed({"runtime_os_architecture": cpu.get("runtime_os_architecture"), "processors": cpu.get("processors")}, "cpu_memory") if isinstance(cpu, dict) else unknown("cpu_memory", "Probe failed or returned non-JSON output."),
                "logical_cores": observed(cpu.get("computer_system_logical_processors"), "cpu_memory") if isinstance(cpu, dict) else unknown("cpu_memory", "Probe failed or returned non-JSON output."),
            },
            "memory": {
                "total_ram_bytes": observed(cpu.get("total_physical_memory_bytes"), "cpu_memory") if isinstance(cpu, dict) else unknown("cpu_memory", "Probe failed or returned non-JSON output."),
            },
            "virtualization": observed(virtualization, "virtualization_capability") if virtualization is not None else unknown("virtualization_capability", "Probe failed or returned non-JSON output."),
            "windows_optional_features": observed(features, "windows_virtualization_features") if features is not None else unknown("windows_virtualization_features", "Probe failed or returned non-JSON output."),
        },
        "storage": {
            "project_volume": {
                "free_bytes": observed(storage["project_volume"]["free_bytes"], "storage_volumes") if isinstance(storage, dict) else unknown("storage_volumes", "Probe failed or returned non-JSON output."),
                "observed": observed(storage.get("project_volume"), "storage_volumes") if isinstance(storage, dict) else unknown("storage_volumes", "Probe failed or returned non-JSON output."),
            },
            "candidate_guest_storage_volume": {
                "free_bytes": observed(storage["candidate_guest_storage_volume"]["free_bytes"], "storage_volumes") if isinstance(storage, dict) else unknown("storage_volumes", "Probe failed or returned non-JSON output."),
                "observed": observed(storage.get("candidate_guest_storage_volume"), "storage_volumes") if isinstance(storage, dict) else unknown("storage_volumes", "Probe failed or returned non-JSON output."),
                "basis": "Windows LocalApplicationData volume; no guest platform or target selected.",
            },
            "registered_distribution_locations": observed(lxss.get("distributions"), "wsl_registration_registry") if isinstance(lxss, dict) else unknown("wsl_registration_registry", "Registry probe failed or returned non-JSON output."),
        },
        "wsl": {
            "state": observed({"status_stdout": wsl_status_entry["stdout"], "status_exit_code": wsl_status_entry["exit_code"], "feature_states": features}, "wsl_status") if wsl_status_entry["exit_code"] == 0 else unknown("wsl_status", "wsl.exe --status did not succeed; feature-state output remains in command transcript."),
            "version": observed(wsl_version_entry["stdout"], "wsl_version") if wsl_version_entry["exit_code"] == 0 else unknown("wsl_version", "wsl.exe --version did not succeed."),
            "registered_distributions": observed(distributions, "wsl_registered_distributions") if distributions is not None else unknown("wsl_registered_distributions", "Distribution output was unavailable or not structurally parseable; exact output is retained in commands.json."),
            "running_distribution_names": observed([row["name"] for row in distributions if row["state"].casefold() == "running"], "wsl_registered_distributions") if distributions is not None else unknown("wsl_registered_distributions", "Distribution output was unavailable or not structurally parseable."),
            "registration_metadata": observed(lxss, "wsl_registration_registry") if lxss is not None else unknown("wsl_registration_registry", "Registry probe failed or returned non-JSON output."),
            "external_guest_termination_capability": observed(termination, "wsl_external_termination_help") if termination is not None else unknown("wsl_external_termination_help", "wsl.exe help was unavailable; no termination command was invoked."),
            "filesystem_mount_defaults": unknown("wsl_registration_registry", "Not established without reading guest configuration or entering a distribution; neither was done."),
            "interop_defaults": unknown("wsl_registration_registry", "Not established without reading guest configuration or entering a distribution; neither was done."),
            "cgroup_capability": unknown("wsl_registered_distributions", "Not established without entering a distribution; no distribution was entered or started."),
            "systemd_capability": unknown("wsl_registered_distributions", "Not established without entering a distribution; no distribution was entered or started."),
        },
        "gpu": {
            "host_adapters": observed(gpus, "host_graphics_adapters") if gpus is not None else unknown("host_graphics_adapters", "Probe failed or returned non-JSON output."),
            "management_visibility": observed(gpu_management, "gpu_management_visibility") if gpu_management is not None else unknown("gpu_management_visibility", "Read-only management query failed or returned non-JSON output."),
            "wsl_guest_visibility": unknown("wsl_registered_distributions", "Not obtainable without entering a distribution; no distribution was entered or started."),
        },
        "pi": {
            "installed_version": observed(pi_version_entry["stdout"].strip(), "pi_version") if pi_version_entry["exit_code"] == 0 else unknown("pi_version", "Pi version probe did not succeed."),
            "executable_identity": observed(pi_identity, "pi_executable_identity") if pi_identity is not None else unknown("pi_executable_identity", "Pi command identity probe failed or returned non-JSON output."),
            "process_ids_names_paths_only": observed(pi_processes, "pi_process_candidates") if pi_processes is not None else unknown("pi_process_candidates", "Process probe failed or returned non-JSON output."),
            "state_path_names_existence_metadata_only": observed(pi_state, "pi_state_path_metadata") if pi_state is not None else unknown("pi_state_path_metadata", "State-path metadata probe failed or returned non-JSON output."),
            "state_file_contents_accessed": False,
            "process_command_lines_accessed": False,
        },
        "capture_constraints": {
            "environment_variable_values_captured": False,
            "distribution_entered_or_started": False,
            "termination_command_invoked": False,
            "configuration_changed": False,
            "gpu_workload_run": False,
            "prime_or_docker_workload_run": False,
            "recommendation_or_target_selection_made": False,
        },
    }

    raw_path = ARTIFACT_DIR / "raw.json"
    write_json(raw_path, raw)

    fixture = copy.deepcopy(raw)
    red_paths = (
        "host.windows.build",
        "wsl.state",
        "wsl.external_guest_termination_capability",
        "storage.project_volume.free_bytes",
        "storage.candidate_guest_storage_volume.free_bytes",
        "pi.executable_identity",
        "gpu.host_adapters",
        "gpu.management_visibility",
        "gpu.wsl_guest_visibility",
    )
    for dotted_path in red_paths:
        remove_path(fixture, dotted_path)
    fixture_path = ARTIFACT_DIR / "_temporary-missing-required-fields.json"
    write_json(fixture_path, fixture)

    red_entry = run_command(
        "schema_red_missing_required_fields",
        [sys.executable, str(SCHEMA_CHECK), str(fixture_path)],
        "Named RED fixture omitting OS build, WSL state, external termination, free disk, Pi identity, and GPU-exposure fields; expected exit code 1.",
    )
    intact_entry = run_command(
        "schema_intact_raw",
        [sys.executable, str(SCHEMA_CHECK), str(raw_path)],
        "Validate the intact retained raw.json; expected exit code 0.",
    )
    fixture_path.unlink()

    expected_names_present = all(path in red_entry["stdout"] for path in red_paths)
    if red_entry["exit_code"] != 1 or not expected_names_present or intact_entry["exit_code"] != 0:
        raise RuntimeError("Schema RED/intact checks did not produce the required results")

    schema_log = (
        "schema_red_missing_required_fields: EXPECTED RED (exit 1)\n"
        + red_entry["stdout"]
        + "schema_intact_raw: PASS (exit 0)\n"
        + intact_entry["stdout"]
    )
    (ARTIFACT_DIR / "schema-check.log").write_text(schema_log, encoding="utf-8")

    commands_document = {
        "schema_version": "g1-command-transcript-v1",
        "generated_at_utc": utc_now(),
        "working_directory": str(PROJECT_ROOT),
        "environment_variable_values_captured": False,
        "commands": COMMANDS,
    }
    write_json(ARTIFACT_DIR / "commands.json", commands_document)

    stderr_sections = []
    for entry in COMMANDS:
        stderr_sections.append(
            f"[{entry['id']}]\n"
            f"started_at_utc={entry['started_at_utc']}\n"
            f"exit_code={entry['exit_code']}\n"
            f"{entry['stderr'] if entry['stderr'] else '<empty>\n'}"
        )
    (ARTIFACT_DIR / "stderr.log").write_text("\n".join(stderr_sections), encoding="utf-8")

    retained = sorted(path for path in ARTIFACT_DIR.iterdir() if path.is_file() and path.name != "sha256.txt")
    hash_lines = []
    for path in retained:
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        hash_lines.append(f"{digest}  {path.name}")
    with (ARTIFACT_DIR / "sha256.txt").open("w", encoding="ascii", newline="\n") as hash_file:
        hash_file.write("\n".join(hash_lines) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
