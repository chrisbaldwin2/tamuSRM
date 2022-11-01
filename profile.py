"""This is a trivial example of a gitrepo-based profile; The profile source code and other software, documentation, etc. are stored in in a publicly accessible GIT repository (say, github.com). When you instantiate this profile, the repository is cloned to all of the nodes in your experiment, to `/local/repository`. 

This particular profile is a simple example of using a single raw PC. It can be instantiated on any cluster; the node will boot the default operating system, which is typically a recent version of Ubuntu.

Instructions:
Wait for the profile instance to start, then click on the node in the topology and choose the `shell` menu item. 
"""

# Import the Portal object.
import geni.portal as portal
# Import the ProtoGENI library.
import geni.rspec.pg as pg

# Create a portal context.
pc = portal.Context()

# Create a Request object to start building the RSpec.
request = pc.makeRequestRSpec()
 
pc.defineParameter("phystype1", "Switch 1 type",
                   portal.ParameterType.STRING, "mlnx-sn2410",
                   [('mlnx-sn2410', 'Mellanox SN2410'),
                    ('dell-s4048',  'Dell S4048')])

params = pc.bindParameters()

# Add a raw PC to the request.
m1 = request.RawPC("M1")
m1_iface = m1.addInterface()
# M1:192.168.0.11, M2:192.168.0.12
m1_iface.addAddress(pg.IPv4Address("192.168.0.11", "255.255.255.0"))

m2 = request.RawPC("M2")
m2_iface = m2.addInterface()
# M1:192.168.0.11, M2:192.168.0.12
m2_iface.addAddress(pg.IPv4Address("192.168.0.12", "255.255.255.0"))

mysw1 = request.Switch("mysw1")
mysw1.hardware_type = params.phystype1
sw1iface1 = mysw1.addInterface()
sw1iface2 = mysw1.addInterface()

link1 = request.L1Link("link1")
link1.addInterface(m1_iface)
link1.addInterface(sw1iface1)

link2 = request.L1Link("link2")
link2.addInterface(m2_iface)
link2.addInterface(sw1iface2)

# Install and execute a script that is contained in the repository.
# m1.addService(pg.Execute(shell="sh", command="/local/repository/daemon.sh"))
# m2.addService(pg.Execute(shell="sh", command="/local/repository/bd.sh"))

# Print the RSpec to the enclosing page.
pc.printRequestRSpec(request)