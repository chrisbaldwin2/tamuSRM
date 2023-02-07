"""This is a trivial example of a gitrepo-based profile; The profile source code and other software, documentation, etc. are stored in in a publicly accessible GIT repository (say, github.com). When you instantiate this profile, the repository is cloned to all of the nodes in your experiment, to `/local/repository`. 

This particular profile is a simple example of using a single raw PC. It can be instantiated on any cluster; the node will boot the default operating system, which is typically a recent version of Ubuntu.

Instructions:
Wait for the profile instance to start, then click on the node in the topology and choose the `shell` menu item. 
"""

# Import the Portal object.
import geni.portal as portal
# Import the ProtoGENI library.
import geni.rspec.pg as pg
# Import the Emulab specific extensions.
import geni.rspec.emulab as emulab

# Create a portal context.
pc = portal.Context()

# Create a Request object to start building the RSpec.
request = pc.makeRequestRSpec()
 
pc.defineParameter("switch_type", "Switch 1 type",
                   portal.ParameterType.STRING, "none",
                   [('mlnx-sn2410', 'Mellanox SN2410'),
                    ('none', 'apt-none'),
                    ('dell-s4048',  'Dell S4048')])

pc.defineParameter("node_type",
                   "Physical node type (m400, c6220, r320, m510, xl170, d6515)",
                   portal.ParameterType.STRING, "r320",
                   [('m400',  'm400:: 8 core 64-bit ARMv8; 64 GB Mem; 10 GB Mellanox'),
                    ('c6220', 'c6220:: 16 core 64-bit x86; 64 GB Mem; 10 GB Mellanox'),
                    ('r320',  'r320:: 8 core 64-bit x86; 16 GB Mem; 10 GB Mellanox'),
                    ('m510',  'm510:: 8 core 64-bit x86; 64 GB Mem; 10 GB Mellanox'),
                    ('xl170', 'xl170:: 10 core 64-bit x86; 64 GB Mem; 25 GB Mellanox'),
                    ('d6515', 'd6515:: 32 core 64-bit x86; 128 GB Mem; 100 GB Mellanox')]
                   )

pc.defineParameter( "n", "Number of Remote Nodes", portal.ParameterType.INTEGER, 1 )

params = pc.bindParameters()

# Add a raw PC to the request.
m1 = request.RawPC("M1")
if params.node_type != "":
    m1.hardware_type = params.node_type
    pass
m1.disk_image = "urn:publicid:IDN+apt.emulab.net+image+tamusrm-PG0:tamuSRM.postIB"
m1_iface = m1.addInterface()
# M1:192.168.0.11
m1_iface.addAddress(pg.IPv4Address("192.168.1.11", "255.255.255.0"))
bs1 = m1.Blockstore("bs1", "/dev/sda4" )
bs1.size = "32GB"

m2 = request.RawPC("M2")
if params.node_type != "":
    m2.hardware_type = params.node_type
    pass
m2.disk_image = "urn:publicid:IDN+apt.emulab.net+image+tamusrm-PG0:tamuSRM.postIB"
m2_iface = m2.addInterface()
# M2:192.168.0.12
m2_iface.addAddress(pg.IPv4Address("192.168.1.12", "255.255.255.0"))
bs2 = m2.Blockstore("bs2", "/dev/sda4" )
bs2.size = "32GB"


if params.switch_type == 'none':

    link1 = request.Link("link1")
    link1.addInterface(m1_iface)
    link1.addInterface(m2_iface)
    pass
else:
    sw1 = request.Switch("Sw1")
    sw1.hardware_type = params.switch_type
    sw1_iface1 = sw1.addInterface()
    sw1_iface1.addAddress(pg.IPv4Address("192.168.1.10", "255.255.255.0"))
    sw1_iface2 = sw1.addInterface()
    sw1_iface2.addAddress(pg.IPv4Address("192.168.1.9", "255.255.255.0"))

    link1 = request.Link("link1")
    link1.addInterface(m1_iface)
    link1.addInterface(sw1_iface1)

    link2 = request.Link("link2")
    link2.addInterface(m2_iface)
    link2.addInterface(sw1_iface2)
    pass

# Install and execute a script that is contained in the repository.
# m1.addService(pg.Execute(shell="sh", command="/local/repository/daemon.sh"))
# m2.addService(pg.Execute(shell="sh", command="/local/repository/bd.sh"))

# print('\n~~~~~~~~~~~Starting Commands~~~~~~~~~~~')
# m1.addService(pg.Install("http://www.mellanox.com/downloads/ofed/MLNX_OFED-4.9-6.0.6.0/MLNX_OFED_LINUX-4.9-6.0.6.0-ubuntu18.04-x86_64.tgz", path="/local"))
# m2.addService(pg.Install("http://www.mellanox.com/downloads/ofed/MLNX_OFED-4.9-6.0.6.0/MLNX_OFED_LINUX-4.9-6.0.6.0-ubuntu18.04-x86_64.tgz", path="/local"))
m1.addService(pg.Execute(shell="bash", command="cd /local/repository/setup ; chmod +x *.sh ; setup/silly.sh"))
m2.addService(pg.Execute(shell="bash", command="cd /local/repository/setup ; chmod +x *.sh ; setup/silly.sh"))

# Print the RSpec to the enclosing page.
pc.printRequestRSpec(request)