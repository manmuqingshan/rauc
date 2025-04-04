import json
import shutil

from conftest import have_json, no_service, root
from helper import run


@no_service
def test_status_no_service(rauc_no_service):
    out, err, exitcode = run(f"{rauc_no_service} --override-boot-slot=A status")

    assert exitcode == 0
    assert "=== System Info ===" in out


@no_service
def test_status_no_service_output_readable(rauc_no_service):
    out, err, exitcode = run(f"{rauc_no_service} --override-boot-slot=A status --output-format=readable")

    assert exitcode == 0
    assert "=== System Info ===" in out


@no_service
def test_status_no_service_output_shell(rauc_no_service):
    out, err, exitcode = run(f"{rauc_no_service} --override-boot-slot=A status --output-format=shell")

    assert exitcode == 0
    assert "RAUC_SYSTEM_COMPATIBLE='Test Config'" in out


@no_service
@have_json
def test_status_no_service_output_json(rauc_no_service):
    out, err, exitcode = run(f"{rauc_no_service} --override-boot-slot=A status --output-format=json")

    assert exitcode == 0
    assert '"compatible":"Test Config"' in out


@no_service
@have_json
def test_status_no_service_output_json_pretty(rauc_no_service):
    out, err, exitcode = run(f"{rauc_no_service} --override-boot-slot=A status --output-format=json-pretty")

    assert exitcode == 0
    assert '"compatible" : "Test Config"' in out


@no_service
@have_json
def test_status_no_service_output_invalid(rauc_no_service):
    out, err, exitcode = run(f"{rauc_no_service} --override-boot-slot=A status --output-format=invalid")

    assert exitcode == 1
    assert "Unknown output format: 'invalid'" in err


def test_status(rauc_dbus_service_with_system):
    out, err, exitcode = run("rauc status")

    assert exitcode == 0
    assert out.startswith("=== System Info ===")


def test_status_readable(rauc_dbus_service_with_system):
    out, err, exitcode = run("rauc status --detailed --output-format=readable")

    assert exitcode == 0
    assert out.startswith("=== System Info ===")


def test_status_shell(rauc_dbus_service_with_system):
    out, err, exitcode = run("rauc status --detailed --output-format=shell")

    assert exitcode == 0
    assert out.startswith("RAUC_SYSTEM_COMPATIBLE='Test Config'")


@have_json
def test_status_json(rauc_dbus_service_with_system):
    out, err, exitcode = run("rauc status --detailed --output-format=json")

    assert exitcode == 0
    assert json.loads(out)


@have_json
def test_status_json_pretty(rauc_dbus_service_with_system):
    out, err, exitcode = run("rauc status --detailed --output-format=json-pretty")

    assert exitcode == 0
    assert json.loads(out)


def test_status_invalid(rauc_dbus_service_with_system):
    out, err, exitcode = run("rauc status --detailed --output-format=invalid")

    assert exitcode == 1
    assert "Unknown output format" in err


@root
def test_status_after_install(rauc_dbus_service_with_system, tmp_path):
    # copy to tmp path for safe ownership check
    shutil.copyfile("good-verity-bundle.raucb", tmp_path / "good-verity-bundle.raucb")

    out, err, exitcode = run(f"rauc install {tmp_path}/good-verity-bundle.raucb")
    assert exitcode == 0

    out, err, exitcode = run("rauc status --detailed --output-format=readable")
    assert exitcode == 0

    out, err, exitcode = run("rauc status --detailed --output-format=json")
    assert exitcode == 0
    assert json.loads(out)

    out, err, exitcode = run("rauc status --detailed --output-format=shell")
    assert exitcode == 0
