# Waf environment for C++ projects

This project is an example about how to generate a C++ environment using Waf. In order to this, a calculator source code is used (from https://github.com/MatheusEngel/Calculadora).

# How to use Waf
```sh
waf [commands][options]
```
Where:

 * **Commands**
    * *build*                : command used for building targets. The targets are created in the build directory
    * *clean*              : cleans the project
    * *configure*       : command used to check if the requirements for working on a project are met.
    * *dist*                   : makes a tarball for redistributing the sources
    * *distcheck*       : checks if the project compiles (tarball from 'dist')
    * *distclean*        : removes the build directory

    * *install*              : installs the targets on the system
    * *uninstall*         : removes the targets installed
    * *list*                     : lists the targets to execute
    * *info*  : command to get the project information

 * **Options**
    * *--version*              show program's version number and exit.
    * *-h, --help*             show this help message and exit.
    * *-c COLORS*          whether to use colors (yes/no/auto) [default: auto].
    * *-j, --jobs=JOBS*  amount of parallel jobs (4).
    * *-k, --keep*             continue despite errors (-kk to try harder).
    * *-v, --verbose*       verbosity level -v -vv or -vvv [default: 0].
    * *--notests*             exec no unit tests
    * *--alltests*            exec all unit tests
    * *--testcmd=TESTCMD*     run the unit tests using the test-cmd string example "--test-cmd="valgrind --error-exitcode=1 %s" to run under valgrind
    * *--tests*         explicit run all tests cases
    * *--enable-gcov*       enable code coverage analysis.
    * *--lcov-report*         Generates a code coverage report (use this option at build time, not in configure)

Too see all commands and options run:  **waf -h**

# How to run

 * **Compile**
```sh
waf configure <build_mode>
where build_mode:
- build_release: compile for release mode
- build_debug: compile for debug mode
- build: compile for both modes (only for compilation, don't use this for the following commands).
```

 * **Unit Test Suite**
```sh
waf <build_mode> --<test_opt>
where test_opt:
- notests: exec no unit tests
- alltests: exec all unit tests
- tests: run explicity all test cases throught test exectuble
Tests executable is generated on build/<debug|release>/tests/test_runner
```

 * **coverage**
```sh
waf configure --enable-gcov
waf <build_mode> --lcov-report
Coverage report is generated on reports/lcov-report
```

# How to add third party tools
* 1- Added new option
On the *options* function and new *add_option*. Example:
```python
def options(opt):
    ...
    opt.add_option("--new-tool",
                   help=("..."),
                   action="store_true", default=False,
                   dest="new_tool")
```

* 2- Define new command called *new_tool*
```python
def run_tests(bld):
   ...
   execute new tools
   ...
```

# Waf
Waf is a python-based framework for configuring, compiling and installing applications. For more information visit:

* [Waf project](https://github.com/waf-project/waf)

* [The waf book](https://waf.io/book/)
