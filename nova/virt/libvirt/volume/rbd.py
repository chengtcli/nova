#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import os.path

from nova import utils
from nova.virt.libvirt.volume import net
from oslo_log import log as logging

LOG = logging.getLogger(__name__)


class LibvirtRBDVolumeDriver(net.LibvirtNetVolumeDriver):
    """Driver to attach encrypted rbd volumes to libvirt. When the volume is not
       encrypted we fall back to LibvirtNetVolumeDriver as libvirt has native
       support for such volumes.

       For encrypted volumes we need to first map the block device on the
       hypervisor and then pass that to the encryptor. In order for the
       encryptor to properly function however we need to create a symlink,
       as that's the one the encryptors will replace with a link to the
       device-mapper block device.
    """
    def __init__(self, connection):
        super(LibvirtRBDVolumeDriver, self).__init__(connection)

    def get_config(self, connection_info, disk_info):
        if connection_info['data']['encrypted'] is True:
            LOG.debug("Attaching RBD block device on the hypersivor")
            self.is_block_dev = True

            conf = super(net.LibvirtNetVolumeDriver,
                         self).get_config(connection_info, disk_info)
            conf.source_type = "block"
            conf.source_path = connection_info['data']['device_path']
            return conf
        else:
            LOG.debug("RBD block device was not encrypted, let qemu handle it")
            return super(LibvirtRBDVolumeDriver,
                         self).get_config(connection_info, disk_info)

    def connect_volume(self, connection_info, disk_info):
        if connection_info['data']['encrypted'] is True:
            rbd_dev = '/dev/rbd/%s' % connection_info['data']['name']
            symlink_dev = '/dev/rbd-volume-%s' % \
                            connection_info['data']['volume_id']
            if (not os.path.islink(rbd_dev) or
                not os.path.exists(os.path.realpath(rbd_dev))):
                utils.execute('rbd',
                              '--id', connection_info['data']['auth_username'],
                              'map', connection_info['data']['name'],
                               run_as_root=True)
            utils.execute('ln', '--symbolic', '--force',
                          rbd_dev,
                          symlink_dev,
                          run_as_root=True)
            connection_info['data']['device_path'] = symlink_dev
        return super(net.LibvirtNetVolumeDriver,
                     self).connect_volume(connection_info, disk_info)

    def disconnect_volume(self, connection_info, disk_dev):
        super(LibvirtRBDVolumeDriver,
              self).disconnect_volume(connection_info, disk_dev)
        if connection_info['data']['encrypted'] is True:
            symlink_dev = '/dev/rbd-volume-%s' % \
                            connection_info['data']['volume_id']
            utils.execute('rm', '-f', symlink_dev, run_as_root=True)
            rbd_dev = '/dev/rbd/%s' % connection_info['data']['name']
            if os.path.islink(rbd_dev):
                utils.execute('rbd', '--id',
                              connection_info['data']['auth_username'],
                              'unmap', rbd_dev, run_as_root=True)