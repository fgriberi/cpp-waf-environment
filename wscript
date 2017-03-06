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
RELEASE_CXXFLAGS = CXXFLAGS + ["-O3", "-Wall", "-Wextra", "-Werror", "-Wpedantic"]


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

    conf.setenv(DEBUG, env=conf.env.derive())
    conf.load("compiler_cxx")
    conf.env.CXXFLAGS = DEBUG_CXXFLAGS


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
    conf.set_enviroments()


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
