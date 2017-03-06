#! /usr/bin/env python
# encoding: utf-8

import os
import subprocess
import waftools
import zipfile

from xml.dom import minidom
from waflib.Configure import conf
from waflib.Errors import WafError, ConfigurationError
from waflib import Options
from waflib.Build import BuildContext, CleanContext, InstallContext,\
    UninstallContext
from datetime import datetime

__author__ = "friberi"


# variables used by the target "waf dist"
APPNAME = "cpp-waf-environment"
VERSION = "1.0.0"
REPOSITORY = "https://github.com/fgriberi/cpp-waf-environment"

top = '.'
out = "build"

DEBUG = "debug"
RELEASE = "release"
CXXFLAGS = ["-fPIC", "-Wall", "-Wno-unused-variable", "-std=c++11", "-pthread"]

# Variant specific build flags
DEBUG_CXXFLAGS = CXXFLAGS + ["-Og", "-g"]
RELEASE_CXXFLAGS =\
    CXXFLAGS + ["-O3", "-Wall", "-Wextra", "-Werror", "-Wpedantic"]
TEST_EXTECUTABLE = "test_runner"
REPORTS = "reports"


class BashColor(object):
    """
    Handle the color shell
    """
    OK = '\033[32m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


def info(ctx):
    """
    Command to get the project information
    :param ctx: The configuration context
    :type ctx: waflib.Configure.ConfigurationContext
    """
    print BashColor.OK + "Project name: " + APPNAME + BashColor.ENDC
    print BashColor.OK + "Version: " + VERSION + BashColor.ENDC
    print BashColor.OK + "Repository path: " + REPOSITORY + BashColor.ENDC


def options(opt):
    """
    Responsible to handle the command-line options
    :param opt: the option context
    :type opt: waflib.Options.OptionsContext
    """
    opt.load("compiler_cxx")
    opt.load("cppcheck", tooldir=waftools.location)
    opt.load("doxygen", tooldir=waftools.location)
    opt.load('waf_unittest_gmock')

    opt.add_option("--tests",
                   help=("Runs unit test cases"),
                   action="store_true", default=False,
                   dest="run_tests")

    opt.add_option("--enable-gcov",
                   help=("Enable code coverage analysis."
                         " WARNING: this option only has effect "
                         "with the configure command."),
                   action="store_true", default=False,
                   dest="enable_gcov")
    opt.add_option("--lcov-report",
                   help=("Generates a code coverage report "
                         "(use this option at build time, not in configure)"),
                   action="store_true", default=False,
                   dest="lcov_report")


@conf
def set_lcov(conf):
    """
    Sets the lcov flag if is configurated
    :param config: The configuration context
    :type config: waflib.Configure.ConfigurationContext
    """
    if Options.options.enable_gcov:
        conf.start_msg("Enable code coverage analysis")
        conf.env['GCOV_ENABLED'] = True
        conf.env.append_value('CCFLAGS', '-fprofile-arcs')
        conf.env.append_value('CCFLAGS', '-ftest-coverage')
        conf.env.append_value('CXXFLAGS', '-fprofile-arcs')
        conf.env.append_value('CXXFLAGS', '-ftest-coverage')
        conf.env.append_value('LINKFLAGS', '-lgcov')
        conf.env.append_value('LINKFLAGS', '-coverage')
        conf.end_msg('yes')


@conf
def set_enviroments(conf):
    """
    Sets the following enviroments: debug, release
    :param config: The configuration context
    :type config: waflib.Configure.ConfigurationContext
    """
    conf.setenv(RELEASE)
    conf.load("compiler_cxx")
    conf.env.CXXFLAGS = RELEASE_CXXFLAGS
    conf.set_lcov()

    conf.setenv(DEBUG, env=conf.env.derive())
    conf.load("compiler_cxx")
    conf.env.CXXFLAGS = DEBUG_CXXFLAGS
    conf.set_lcov()


def init(ctx):
    """
    Setup contexts build_debug, build_release, clean_debug, and clean_release
    :param ctx: the general waf context
    :type ctx: waflib.Context.Context
    """
    contexts = (BuildContext, CleanContext, InstallContext, UninstallContext)
    for context in contexts:
        for c_varinat in [DEBUG, RELEASE]:
            class tmp(context):
                variant = c_varinat
                cmd = context.__name__.replace("Context", '').\
                    lower() + '_' + c_varinat


def configure(conf):
    """
    The configuration command is used to check if the requiremements
    for working on a project are met and to store the information.
    :param config: The configuration context
    :type config: waflib.Configure.ConfigurationContext
    """
    conf.load("compiler_cxx")
    conf.load("cppcheck")
    conf.load("doxygen")
    conf.load('waf_unittest_gmock')

    if not conf.env['LIB_PTHREAD']:
        conf.check_cxx(lib='pthread')

    conf.set_enviroments()


def test_summary(bld):
    """
    Reports the tests summary
    :param bld: temporal options context
    :type bld: wscript.tmp
    """
    test_passed = True
    lst = getattr(bld, TEST_EXTECUTABLE, [])
    result_lst = lst[0].split("\n")
    for result in result_lst:
        prefix = result[:12]
        test_failed = "FAILED" in prefix
        if test_failed:
            test_passed = False
            if "[" in prefix:
                print(BashColor.FAIL + prefix + BashColor.ENDC + result[12:])
            else:
                print(result)
        else:
            if "[" in prefix:
                print(BashColor.OK + prefix + BashColor.ENDC + result[12:])
            else:
                print(result)
    return test_passed


def run_tests(bld):
    """
    Runs the unit tests cases
    :param bld: temporal options context
    :type bld: wscript.tmp
    """
    test_exec_path = os.path.join(out, bld.variant, "tests", TEST_EXTECUTABLE)
    print BashColor.WARNING + test_exec_path + BashColor.ENDC
    proc =\
        subprocess.Popen(test_exec_path,
                         stderr=subprocess.STDOUT,
                         stdout=subprocess.PIPE)
    (output, _) = proc.communicate()

    setattr(bld, TEST_EXTECUTABLE, [output])
    test_passed = test_summary(bld)
    if not test_passed:
        raise WafError("Failed unit test cases.")


def lcov_report(bld):
    """
    Generates the coverage report
    :param bld: temporal options context
    :type bld: wscript.tmp
    """
    env = bld.env
    if not env["GCOV_ENABLED"]:
        raise WafError("project not configured for code coverage;"
                       " reconfigure with --enable-gcov")

    run_tests(bld)
    lcov_report_dir = os.path.join(REPORTS, "lcov-report")
    try:
        if not os.path.exists(REPORTS):
            os.mkdir(REPORTS)

        create_dir_command = "rm -rf " + lcov_report_dir
        create_dir_command += " && mkdir " + lcov_report_dir

        print BashColor.WARNING + create_dir_command + BashColor.ENDC
        if subprocess.Popen(create_dir_command, shell=True).wait():
            raise SystemExit(1)

        info_file = os.path.join(lcov_report_dir, "lcov.info")
        lcov_command =\
            "lcov --no-external --capture --directory . -o " + info_file
        lcov_command +=\
            " && lcov --remove " + info_file + " \".waf*\" -o " + info_file

        print BashColor.WARNING + lcov_command + BashColor.ENDC
        if subprocess.Popen(lcov_command, shell=True).wait():
            raise SystemExit(1)

        genhtml_command = "genhtml " + info_file
        genhtml_command += " -o " + lcov_report_dir
        print BashColor.WARNING + genhtml_command + BashColor.ENDC
        if subprocess.Popen(genhtml_command, shell=True).wait():
            raise SystemExit(1)

    except:
        print BashColor.FAIL +\
            "Problems running coverage. Try manually" + BashColor.ENDC

    finally:
        print BashColor.OK +\
            "Coverage successful. Open " + lcov_report_dir +\
            "/index.html" + BashColor.ENDC


def build(bld):
    """
    The build command used for building targets. The targets are created
    in the build directory
    :param bld: The build context
    :type bld: waflib.Build.BuildContext
    """
    if not bld.variant:
        # If no variant was specified then build them all
        for variant in [DEBUG, RELEASE]:
            Options.commands.insert(0, bld.cmd + '_' + variant)
    else:
        bld.recurse("src")
        bld.recurse("tests")
    post_build(bld)


def post_build(bld):
    """
    Responsible to handles the post build actions
    :param bld: The build context
    :type bld: waflib.Build.BuildContext
    """
    if Options.options.run_tests:
        bld.add_post_fun(run_tests)
    if Options.options.lcov_report:
        bld.add_post_fun(lcov_report)
