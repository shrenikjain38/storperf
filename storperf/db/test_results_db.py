##############################################################################
# Copyright (c) 2016 EMC and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import json
import requests
import os


def get_installer_type(logger=None):
    """
    Get installer type (fuel, apex, joid, compass)
    """
    try:
        installer = os.environ['INSTALLER_TYPE']
    except KeyError:
        if logger:
            logger.error("Impossible to retrieve the installer type")
        installer = "Unknown_installer"

    return installer


def push_results_to_db(db_url, project, case_name, logger, pod_name,
                       version, scenario, criteria, build_tag, payload):
    """
    POST results to the Result target DB
    """
    url = db_url + "/results"
    installer = get_installer_type(logger)
    params = {"project_name": project, "case_name": case_name,
              "pod_name": pod_name, "installer": installer,
              "version": version, "scenario": scenario, "criteria": criteria,
              "build_tag": build_tag, "details": payload}

    headers = {'Content-Type': 'application/json'}
    try:
        if logger:
            logger.debug("Pushing results to %s" % (url))
        r = requests.post(url, data=json.dumps(params), headers=headers)
        if logger:
            logger.debug(r)
            logger.debug(r.status_code)
            logger.debug(r.content)
        return True
    except Exception, e:
        logger.error("Error [push_results_to_db('%s', '%s', '%s', " +
                     "'%s', '%s', '%s', '%s', '%s', '%s')]:" %
                     (db_url, project, case_name, pod_name, version,
                      scenario, criteria, build_tag, payload), e)
        return False