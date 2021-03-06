.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0

Executing the functest suites (Ubuntu)
======================================

Manual testing
--------------

This section assumes the following:
 * The Functest Docker container is running
 * The docker prompt is shown
 * The Functest environment is ready (Functest CLI command 'functest env prepare'
   has been executed)

If any of the above steps are missing please refer to the Functest Config Guide
as they are a prerequisite and all the commands explained in this section **must** be
performed **inside the container**.

The Functest CLI offers two commands (functest tier ...) and (functest testcase ... )
for the execution of Test Tiers or Test Cases::

  root@22e436918db0:~/repos/functest/ci# functest tier --help
  Usage: functest tier [OPTIONS] COMMAND [ARGS]...

  Options:
    -h, --help  Show this message and exit.

  Commands:
    get-tests  Prints the tests in a tier.
    list       Lists the available tiers.
    run        Executes all the tests within a tier.
    show       Shows information about a tier.
  root@22e436918db0:~/repos/functest/ci# functest testcase --help

  Usage: functest testcase [OPTIONS] COMMAND [ARGS]...

  Options:
    -h, --help  Show this message and exit.

  Commands:
    list  Lists the available testcases.
    run   Executes a test case.
    show  Shows information about a test case.

More details on the existing Tiers and Test Cases can be seen with the 'list'
command::

  root@22e436918db0:~/repos/functest/ci# functest tier list
      - 0. healthcheck:
             ['connection_check', 'api_check', 'snaps_health_check',]
      - 1. smoke:
             ['vping_ssh', 'vping_userdata', 'tempest_smoke_serial', 'odl', 'rally_sanity', 'refstack_defcore', 'snaps_smoke']
      - 2. features:
             ['doctor', 'domino', 'promise', security_scan']
      - 3. components:
             ['tempest_full_parallel', 'rally_full']
      - 4. vnf:
             ['cloudify_ims', 'orchestra_ims', 'vyos_vrouter']

  and

  root@22e436918db0:~/repos/functest/ci# functest testcase list
  api_check
  connection_check
  snaps_health_check
  vping_ssh
  vping_userdata
  snaps_smoke
  refstack_defcore
  tempest_smoke_serial
  rally_sanity
  odl
  tempest_full_parallel
  rally_full
  vyos_vrouter

Note the list of test cases depend on the installer and the scenario.

More specific details on specific Tiers or Test Cases can be seen wih the
'show' command::

  root@22e436918db0:~/repos/functest/ci# functest tier show smoke
  +======================================================================+
  | Tier:  smoke                                                         |
  +======================================================================+
  | Order: 1                                                             |
  | CI Loop: (daily)|(weekly)                                            |
  | Description:                                                         |
  |    Set of basic Functional tests to validate the OpenStack           |
  |    deployment.                                                       |
  | Test cases:                                                          |
  |    - vping_ssh                                                       |
  |    - vping_userdata                                                  |
  |    - tempest_smoke_serial                                            |
  |    - rally_sanity                                                    |
  |                                                                      |
  +----------------------------------------------------------------------+

  and

  root@22e436918db0:~/repos/functest/ci# functest testcase  show tempest_smoke_serial
  +======================================================================+
  | Testcase:  tempest_smoke_serial                                      |
  +======================================================================+
  | Description:                                                         |
  |    This test case runs the smoke subset of the OpenStack Tempest     |
  |    suite. The list of test cases is generated by Tempest             |
  |    automatically and depends on the parameters of the OpenStack      |
  |    deplopyment.                                                      |
  | Dependencies:                                                        |
  |   - Installer:                                                       |
  |   - Scenario :                                                       |
  |                                                                      |
  +----------------------------------------------------------------------+


To execute a Test Tier or Test Case, the 'run' command is used::

  root@22e436918db0:~/repos/functest/ci# functest tier run healthcheck

  2017-08-16 12:35:51,799 - functest.ci.run_tests - INFO - ############################################
  2017-08-16 12:35:51,799 - functest.ci.run_tests - INFO - Running tier 'healthcheck'
  2017-08-16 12:35:51,800 - functest.ci.run_tests - INFO - ############################################
  2017-08-16 12:35:51,800 - functest.ci.run_tests - INFO -
  2017-08-16 12:35:51,800 - functest.ci.run_tests - INFO - ============================================
  2017-08-16 12:35:51,800 - functest.ci.run_tests - INFO - Running test case 'connection_check'...
  2017-08-16 12:35:51,800 - functest.ci.run_tests - INFO - ============================================
  2017-08-16 12:36:00,278 - functest.core.testcase - INFO - The results were successfully pushed to DB
  2017-08-16 12:36:00,279 - functest.ci.run_tests - INFO - Test result:
  +--------------------------+------------------+------------------+----------------+
  |        TEST CASE         |     PROJECT      |     DURATION     |     RESULT     |
  +--------------------------+------------------+------------------+----------------+
  |     connection_check     |     functest     |      00:06       |      PASS      |
  +--------------------------+------------------+------------------+----------------+
  2017-08-16 12:36:00,281 - functest.ci.run_tests - INFO -
  2017-08-16 12:36:00,281 - functest.ci.run_tests - INFO - ============================================
  2017-08-16 12:36:00,281 - functest.ci.run_tests - INFO - Running test case 'api_check'...
  2017-08-16 12:36:00,281 - functest.ci.run_tests - INFO - ============================================
  2017-08-16 12:41:04,088 - functest.core.testcase - INFO - The results were successfully pushed to DB
  2017-08-16 12:41:04,088 - functest.ci.run_tests - INFO - Test result:
  +-------------------+------------------+------------------+----------------+
  |     TEST CASE     |     PROJECT      |     DURATION     |     RESULT     |
  +-------------------+------------------+------------------+----------------+
  |     api_check     |     functest     |      05:03       |      PASS      |
  +-------------------+------------------+------------------+----------------+
  2017-08-16 12:41:04,092 - functest.ci.run_tests - INFO -
  2017-08-16 12:41:04,092 - functest.ci.run_tests - INFO - ============================================
  2017-08-16 12:41:04,092 - functest.ci.run_tests - INFO - Running test case 'snaps_health_check'...
  2017-08-16 12:41:04,092 - functest.ci.run_tests - INFO - ============================================
  2017-08-16 12:41:39,817 - functest.core.testcase - INFO - The results were successfully pushed to DB
  2017-08-16 12:41:39,818 - functest.ci.run_tests - INFO - Test result:
  +----------------------------+------------------+------------------+----------------+
  |         TEST CASE          |     PROJECT      |     DURATION     |     RESULT     |
  +----------------------------+------------------+------------------+----------------+
  |     snaps_health_check     |     functest     |      00:35       |      PASS      |
  +----------------------------+------------------+------------------+----------------+

  and

  root@22e436918db0:~/repos/functest/ci# functest testcase run vping_ssh
  2017-08-16 12:41:39,821 - functest.ci.run_tests - INFO - ============================================
  2017-08-16 12:41:39,821 - functest.ci.run_tests - INFO - Running test case 'vping_ssh'...
  2017-08-16 12:41:39,821 - functest.ci.run_tests - INFO - ============================================
  2017-08-16 12:42:49,861 - functest.core.testcase - INFO - The results were successfully pushed to DB
  2017-08-16 12:42:49,861 - functest.ci.run_tests - INFO - Test result:
  +-------------------+------------------+------------------+----------------+
  |     TEST CASE     |     PROJECT      |     DURATION     |     RESULT     |
  +-------------------+------------------+------------------+----------------+
  |     vping_ssh     |     functest     |      00:47       |      PASS      |
  +-------------------+------------------+------------------+----------------+
  :
  :
  etc.

To list the test cases which are part of a specific Test Tier, the 'get-tests'
command is used with 'functest tier'::

  root@22e436918db0:~/repos/functest/ci# functest tier get-tests healthcheck
  Test cases in tier 'healthcheck':
   ['connection_check', 'api_check', 'snaps_health_check']


Please note that for some scenarios some test cases might not be launched.
For example, the last example displayed only the 'odl' testcase for the given
environment. In this particular system the deployment does not support the 'ocl' SDN
Controller Test Case; for example.

**Important** If you use the command 'functest tier run <tier_name>', then the
Functest CLI utility will call **all valid Test Cases**, which belong to the
specified Test Tier, as relevant to scenarios deployed to the SUT environment.
Thus, the Functest CLI utility calculates automatically which tests can be
executed and which cannot, given the environment variable **DEPLOY_SCENARIO**,
which is passed in to the Functest docker container.

Currently, the Functest CLI command 'functest testcase run <testcase_name>', supports
two possibilities::

 *  Run a single Test Case, specified by a valid choice of <testcase_name>
 *  Run ALL test Test Cases (for all Tiers) by specifying <testcase_name> = 'all'

Functest includes a cleaning mechanism in order to remove all the OpenStack
resources except those present before running any test. The script
*$REPOS_DIR/functest/functest/utils/openstack_snapshot.py* is called once when setting up
the Functest environment (i.e. CLI command 'functest env prepare') to snapshot
all the OpenStack resources (images, networks, volumes, security groups, tenants,
users) so that an eventual cleanup does not remove any of these defaults.

The script **openstack_clean.py** which is located in
*$REPOS_DIR/functest/functest/utils/* is in charge of cleaning the OpenStack resources
that are not specified in the defaults file generated previously which is stored in
*/home/opnfv/functest/conf/openstack_snapshot.yaml* in the Functest docker container.

It is important to mention that if there are new OpenStack resources created
manually after the snapshot done before running the tests, they will be removed,
unless you use the special method of invoking the test case with specific
suppression of clean up. (See the `Troubleshooting`_ section).

The reason to include this cleanup meachanism in Functest is because some
test suites create a lot of resources (users, tenants, networks, volumes etc.)
that are not always properly cleaned, so this function has been set to keep the
system as clean as it was before a full Functest execution.

Although the Functest CLI provides an easy way to run any test, it is possible to
do a direct call to the desired test script. For example:

    python $REPOS_DIR/functest/functest/opnfv_tests/openstack/vping/vping_ssh.py


Automated testing
-----------------

As mentioned previously, the Functest Docker container preparation as well as
invocation of Test Cases can be called within the container from the Jenkins CI
system. There are 3 jobs that automate the whole process. The first job runs all
the tests referenced in the daily loop (i.e. that must been run daily), the second
job runs the tests referenced in the weekly loop (usually long duration tests run
once a week maximum) and the third job allows testing test suite by test suite specifying
the test suite name. The user may also use either of these Jenkins jobs to execute
the desired test suites.

One of the most challenging task in the Danube release consists
in dealing with lots of scenarios and installers. Thus, when the tests are
automatically started from CI, a basic algorithm has been created in order to
detect whether a given test is runnable or not on the given scenario.
Some Functest test suites cannot be systematically run (e.g. ODL suite can not
be run on an ONOS scenario). The daily/weekly notion has been introduces in
Colorado in order to save CI time and avoid running systematically
long duration tests. It was not used in Colorado due to CI resource shortage.
The mechanism remains however as part of the CI evolution.

CI provides some useful information passed to the container as environment
variables:

 * Installer (apex|compass|fuel|joid), stored in INSTALLER_TYPE
 * Installer IP of the engine or VM running the actual deployment, stored in INSTALLER_IP
 * The scenario [controller]-[feature]-[mode], stored in DEPLOY_SCENARIO with

   * controller = (odl|ocl|nosdn)
   * feature = (ovs(dpdk)|kvm|sfc|bgpvpn|ovs_dpdk_bar)
   * mode = (ha|noha)

The constraints per test case are defined in the Functest configuration file
*/usr/local/lib/python2.7/dist-packages/functest/ci/testcases.yaml*::

 tiers:
   -
        name: smoke
        order: 1
        ci_loop: '(daily)|(weekly)'
        description : >-
            Set of basic Functional tests to validate the OpenStack deployment.
        testcases:
            -
                name: vping_ssh
                criteria: 'status == "PASS"'
                blocking: true
                description: >-
                    This test case verifies: 1) SSH to an instance using floating
                    IPs over the public network. 2) Connectivity between 2 instances
                    over a private network.
                dependencies:
                    installer: ''
                    scenario: '^((?!bgpvpn|odl_l3).)*$'
                run:
                    module: 'functest.opnfv_tests.openstack.vping.vping_ssh'
                    class: 'VPingSSH'
        ....

We may distinguish 2 levels in the test case description:
  * Tier level
  * Test case level

At the tier level, we define the following parameters:

 * ci_loop: indicate if in automated mode, the test case must be run in dail and/or weekly jobs
 * description: a high level view of the test case

For a given test case we defined:
  * the name of the test case
  * the criteria (experimental): a criteria used to declare the test case as PASS or FAIL
  * blocking: if set to true, if the test is failed, the execution of the following tests is canceled
  * the description of the test case
  * the dependencies: a combination of 2 regex on the scenario and the installer name
  * run: In Danube we introduced the notion of abstract class in order to harmonize the way to run internal, feature or vnf tests

For further details on abstraction classes, see developper guide.

Additional parameters have been added in the desription in the Database.
The target is to use the configuration stored in the Database and consider the
local file as backup if the Database is not reachable.
The additional fields related to a test case are:
  * trust: we introduced this notion to put in place a mechanism of scenario promotion.
  * Version: it indicates since which version you can run this test
  * domains: the main domain covered by the test suite
  * tags: a list of tags related to the test suite

The order of execution is the one defined in the file if all test cases are selected.

In CI daily job the tests are executed in the following order:

  1) healthcheck (blocking)
  2) smoke: both vPings are blocking
  3) Feature project tests cases

In CI weekly job we add 2 tiers:

  4) VNFs (vIMS)
  5) Components (Rally and Tempest long duration suites)

As explained before, at the end of an automated execution, the OpenStack resources
might be eventually removed.
Please note that a system snapshot is taken before any test case execution.

This testcase.yaml file is used for CI, for the CLI and for the automatic reporting.


Executing Functest suites (Alpine)
==================================

As mentioned in the configuration guide `[1]`_, Alpine docker containers have
been introduced in Euphrates.
Tier containers have been created.
Assuming that you pulled the container and your environement is ready, you can
simply run the tiers by typing (e.g. with functest-healthcheck)::

  sudo docker run --env-file env \
      -v $(pwd)/openstack.creds:/home/opnfv/functest/conf/openstack.creds  \
      -v $(pwd)/images:/home/opnfv/functest/images  \
      opnfv/functest-healthcheck

You should get::

  +----------------------------+------------------+---------------------+------------------+----------------+
  |         TEST CASE          |     PROJECT      |         TIER        |     DURATION     |     RESULT     |
  +----------------------------+------------------+---------------------+------------------+----------------+
  |      connection_check      |     functest     |     healthcheck     |      00:02       |      PASS      |
  |         api_check          |     functest     |     healthcheck     |      03:19       |      PASS      |
  |     snaps_health_check     |     functest     |     healthcheck     |      00:46       |      PASS      |
  +----------------------------+------------------+---------------------+------------------+----------------+

You can run functest-healcheck, functest-smoke, functest-features,
functest-components and functest-vnf.

Please note that you may also use the CLI for manual tests using Alpine
containers.


Functest internal API
=====================

An internal API has been introduced in Euphrates. The goal is to trigger
Functest operations through an API in addition of the CLI.
This could be considered as a first step towards a pseudo micro services
approach where the different test projects could expose and consume APIs to the
other test projects.

In Euphrates the main method of the APIs are:

  * Show environment
  * Prepare Environment
  * Show credentials
  * List all testcases
  * Show a testcase
  * List all tiers
  * Show a tier
  * List all testcases within given tier

The API can be invoked as follows:
  http://<functest_url>:5000/api/v1/functest/envs

TODO

.. _`[1]`: http://artifacts.opnfv.org/functest/colorado/docs/configguide/#
