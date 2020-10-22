from io import StringIO

from fabric import Connection
from invoke.tasks import task

from zerojoy.hid import write_hid_report_desc
from zerojoy.hotaw import hid_report_desc


@task
def build(c):
    c.run("poetry build")
    write_hid_report_desc("usb_gadget/zerojoy/functions/hid.usb0/report_desc", hid_report_desc)
    c.run("tar -C usb_gadget -cf dist/usb_gadget.tar zerojoy/")


@task(pre=[build])
def deploy(c):
    r = Connection("zerojoy")
    r.put("dist/usb_gadget.tar", "zerojoy.tar")
    f = c.run("poetry version -s")
    wheel = f"zerojoy-{f.stdout.strip()}-py3-none-any.whl"
    r.put(f"dist/{wheel}")
    with r.prefix(". .venv/bin/activate"):
        r.run(f"pip install --no-index --force-reinstall {wheel}")
    restart(r)


def restart(c):
    c.sudo('sh -c "echo \\"\\" > /sys/kernel/config/usb_gadget/zerojoy/UDC"', warn=True)
    c.sudo('rm /sys/kernel/config/usb_gadget/zerojoy/configs/c.1/hid.usb0', warn=True)
    c.sudo('tar -C /sys/kernel/config/usb_gadget/ -xf zerojoy.tar --overwrite --no-same-owner')
    c.sudo('ln -s /sys/kernel/config/usb_gadget/zerojoy/functions/hid.usb0 /sys/kernel/config/usb_gadget/zerojoy/configs/c.1/')
    c.sudo('sh -c "ls /sys/class/udc > /sys/kernel/config/usb_gadget/zerojoy/UDC"')
