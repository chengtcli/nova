# Copyright 2010 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# Copyright (c) 2010 Citrix Systems, Inc.
# Copyright (c) 2011 Piston Cloud Computing, Inc
# Copyright (c) 2012 University Of Minho
# (c) Copyright 2013 Hewlett-Packard Development Company, L.P.
#
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

"""
A connection to a hypervisor through libvirt.

Supports KVM, LXC, QEMU, UML, XEN and Parallels.

"""

import driver as orglibvdriver

orglibvdriver.libvirt_volume_drivers = [
    'iscsi=nova.virt.libvirt.volume.iscsi.LibvirtISCSIVolumeDriver',
    'iser=nova.virt.libvirt.volume.iser.LibvirtISERVolumeDriver',
    'local=nova.virt.libvirt.volume.volume.LibvirtVolumeDriver',
    'fake=nova.virt.libvirt.volume.volume.LibvirtFakeVolumeDriver',
    'rbd=nova.virt.libvirt.volume.rbd.LibvirtRBDVolumeDriver',
    'sheepdog=nova.virt.libvirt.volume.net.LibvirtNetVolumeDriver',
    'nfs=nova.virt.libvirt.volume.nfs.LibvirtNFSVolumeDriver',
    'smbfs=nova.virt.libvirt.volume.smbfs.LibvirtSMBFSVolumeDriver',
    'aoe=nova.virt.libvirt.volume.aoe.LibvirtAOEVolumeDriver',
    'glusterfs='
        'nova.virt.libvirt.volume.glusterfs.LibvirtGlusterfsVolumeDriver',
    'fibre_channel='
        'nova.virt.libvirt.volume.fibrechannel.'
        'LibvirtFibreChannelVolumeDriver',
    'scality=nova.virt.libvirt.volume.scality.LibvirtScalityVolumeDriver',
    'gpfs=nova.virt.libvirt.volume.gpfs.LibvirtGPFSVolumeDriver',
    'quobyte=nova.virt.libvirt.volume.quobyte.LibvirtQuobyteVolumeDriver',
    'hgst=nova.virt.libvirt.volume.hgst.LibvirtHGSTVolumeDriver',
    'scaleio=nova.virt.libvirt.volume.scaleio.LibvirtScaleIOVolumeDriver',
    'disco=nova.virt.libvirt.volume.disco.LibvirtDISCOVolumeDriver',
    'vzstorage='
        'nova.virt.libvirt.volume.vzstorage.LibvirtVZStorageVolumeDriver',
]

class LibvirtDriver2(orglibvdriver.LibvirtDriver):
    pass