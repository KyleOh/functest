# Copyright (c) 2017 Cable Television Laboratories, Inc. and others.
#
# This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
#
# http://www.apache.org/licenses/LICENSE-2.0

from datetime import datetime
import logging
import os
import time
import uuid

from functest.core import testcase
from functest.utils.constants import CONST

from snaps.openstack import create_flavor
from snaps.openstack.create_flavor import FlavorSettings, OpenStackFlavor
from snaps.openstack.create_network import NetworkSettings, SubnetSettings
from snaps.openstack.tests import openstack_tests
from snaps.openstack.utils import deploy_utils


class VPingBase(testcase.TestCase):

    """
    Base class for vPing tests that check connectivity between two VMs shared
    internal network.
    This class is responsible for creating the image, internal network.
    """

    def __init__(self, **kwargs):
        super(VPingBase, self).__init__(**kwargs)

        # This line is here simply for pep8 as the 'os' package import appears
        # to be required for mock and the unit tests will fail without it
        os.environ

        self.logger = logging.getLogger(__name__)

        if 'os_creds' in kwargs:
            self.os_creds = kwargs['os_creds']
        else:
            creds_override = None
            if hasattr(CONST, 'snaps_os_creds_override'):
                creds_override = CONST.__getattribute__(
                    'snaps_os_creds_override')

            self.os_creds = openstack_tests.get_credentials(
                os_env_file=CONST.__getattribute__('openstack_creds'),
                overrides=creds_override)

        self.creators = list()
        self.image_creator = None
        self.network_creator = None
        self.vm1_creator = None
        self.vm2_creator = None

        # Shared metadata
        self.guid = ''
        if CONST.__getattribute__('vping_unique_names'):
            self.guid = '-' + str(uuid.uuid4())

        self.vm1_name = CONST.__getattribute__('vping_vm_name_1') + self.guid
        self.vm2_name = CONST.__getattribute__('vping_vm_name_2') + self.guid

        self.vm_boot_timeout = CONST.__getattribute__('vping_vm_boot_timeout')
        self.vm_delete_timeout = CONST.__getattribute__(
            'vping_vm_delete_timeout')
        self.vm_ssh_connect_timeout = CONST.vping_vm_ssh_connect_timeout
        self.ping_timeout = CONST.__getattribute__('vping_ping_timeout')
        self.flavor_name = 'vping-flavor' + self.guid

        # Move this configuration option up for all tests to leverage
        if hasattr(CONST, 'snaps_images_cirros'):
            self.cirros_image_config = CONST.__getattribute__(
                'snaps_images_cirros')
        else:
            self.cirros_image_config = None

    def run(self):
        """
        Begins the test execution which should originate from the subclass
        """
        self.logger.info('Begin virtual environment setup')

        self.start_time = time.time()
        self.logger.info("vPing Start Time:'%s'" % (
            datetime.fromtimestamp(self.start_time).strftime(
                '%Y-%m-%d %H:%M:%S')))

        image_base_name = '{}-{}'.format(
            CONST.__getattribute__('vping_image_name'),
            str(self.guid))
        os_image_settings = openstack_tests.cirros_image_settings(
            image_base_name, image_metadata=self.cirros_image_config)
        self.logger.info("Creating image with name: '%s'" % image_base_name)

        self.image_creator = deploy_utils.create_image(
            self.os_creds, os_image_settings)
        self.creators.append(self.image_creator)

        private_net_name = CONST.__getattribute__(
            'vping_private_net_name') + self.guid
        private_subnet_name = CONST.__getattribute__(
            'vping_private_subnet_name') + self.guid
        private_subnet_cidr = CONST.__getattribute__(
            'vping_private_subnet_cidr')

        vping_network_type = None
        vping_physical_network = None
        vping_segmentation_id = None

        if (hasattr(CONST, 'vping_network_type')):
            vping_network_type = CONST.__getattribute__(
                'vping_network_type')
        if (hasattr(CONST, 'vping_physical_network')):
            vping_physical_network = CONST.__getattribute__(
                'vping_physical_network')
        if (hasattr(CONST, 'vping_segmentation_id')):
            vping_segmentation_id = CONST.__getattribute__(
                'vping_segmentation_id')

        self.logger.info(
            "Creating network with name: '%s'" % private_net_name)
        self.network_creator = deploy_utils.create_network(
            self.os_creds,
            NetworkSettings(
                name=private_net_name,
                network_type=vping_network_type,
                physical_network=vping_physical_network,
                segmentation_id=vping_segmentation_id,
                subnet_settings=[SubnetSettings(
                    name=private_subnet_name,
                    cidr=private_subnet_cidr)]))
        self.creators.append(self.network_creator)

        self.logger.info(
            "Creating flavor with name: '%s'" % self.flavor_name)
        scenario = CONST.__getattribute__('DEPLOY_SCENARIO')
        flavor_metadata = None
        if 'ovs' in scenario or 'fdio' in scenario:
            flavor_metadata = create_flavor.MEM_PAGE_SIZE_LARGE
        flavor_creator = OpenStackFlavor(
            self.os_creds,
            FlavorSettings(name=self.flavor_name, ram=512, disk=1, vcpus=1,
                           metadata=flavor_metadata))
        flavor_creator.create()
        self.creators.append(flavor_creator)

    def _execute(self):
        """
        Method called by subclasses after environment has been setup
        :return: the exit code
        """
        self.logger.info('Begin test execution')

        test_ip = self.vm1_creator.get_port_ip(
            self.vm1_creator.instance_settings.port_settings[0].name)

        if self.vm1_creator.vm_active(
                block=True) and self.vm2_creator.vm_active(block=True):
            result = self._do_vping(self.vm2_creator, test_ip)
        else:
            raise Exception('VMs never became active')

        if result == testcase.TestCase.EX_RUN_ERROR:
            return testcase.TestCase.EX_RUN_ERROR

        self.stop_time = time.time()
        self.result = 100
        return testcase.TestCase.EX_OK

    def _cleanup(self):
        """
        Cleanup all OpenStack objects. Should be called on completion
        :return:
        """
        if CONST.__getattribute__('vping_cleanup_objects'):
            for creator in reversed(self.creators):
                try:
                    creator.clean()
                except Exception as e:
                    self.logger.error('Unexpected error cleaning - %s', e)

    def _do_vping(self, vm_creator, test_ip):
        """
        Method to be implemented by subclasses
        Begins the real test after the OpenStack environment has been setup
        :param vm_creator: the SNAPS VM instance creator object
        :param test_ip: the IP to which the VM needs to issue the ping
        :return: T/F
        """
        raise NotImplementedError('vping execution is not implemented')
