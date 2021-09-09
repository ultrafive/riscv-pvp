#!/usr/bin/env python3

import click
import textwrap
import shutil

from rvpvp import generator, runner
from rvpvp.common import Args, parse_config_files, get_package_root

@click.group()
def cli():
    """Create a new target for verification."""
    pass


@cli.command()
@click.argument('dir')
def new(dir):
    """Create a new target for verification."""
    click.echo(f'New target is created in {dir}.')
    shutil.copytree(get_package_root() + '/new', dir)


@cli.command()
@click.option('--config', help='config yaml file', default='target.yml')
@click.option('--nproc', '-n', help='generate elf files on n processes', type=int, default=1)
@click.option('--level', '-l', help='level of cases to compile into one elf file',
                type=click.Choice(['group', 'type', 'case'], case_sensitive=False), default="case")
@click.option('--specs', '-s', help='test case specs')
@click.option('--cases', '-c', help=textwrap.dedent('''\
                             test case list string or file, for example:
                             - vsub_vv,addi/test_imm_op/
                             - cases.list
                             you can find more examples with option --collect'''), default='')
@click.option('--collect', help='just collect the test case to know what cases we can test', default=False)
@click.option('--little', help='only run at most 4 test cases for each test type of each instruction', default=False)
@click.option('--basic', '-b', help='run basic tests of basic_cases test data in yml for regression.', default=False)
@click.option('--random', '-r', help='run random tests of random_cases test data in yml', default=False)
@click.option('--seed', help="set random seed for random functions of each spec yaml", type=int, default=3428)
@click.option('--rtimes', help="set random cases generation times", type=int, default=1)
@click.option('--retry', help='retry last failed cases', default=False)
@click.option('--failing-info', '-fi', help="print the failing info into the screen, rather than into the log/generator_report.log.", default=False)
@click.option('--param-info', '-pi', help="print params information into log/params.yaml of cases collected.", default=False)
def gen(**kwargs):
    """Generate verification cases for current target."""
    kwargs['config'] = parse_config_files(kwargs['config'])
    kwargs['pkgroot'] = get_package_root()
    generator.main(Args(**kwargs))


@ cli.command()
@click.option('--config', help='config yaml file, default config/prod.yml', default='target.yml')
@click.option('--retry', '-r', help='retry last failed cases', default=False)
@click.option('--nproc', '-n', help='runner process number for run cases, default 1', type=int, default=1)
@click.option('--cases', '-c', help=textwrap.dedent('''\
                                    test case list string or file, for example:
                                    - vsub_vv,addi/test_imm_op/
                                    - cases.list'''), default='')
@click.option('--failing-info', '-fi', help="print the failing info into the screen, rather than  in the log/runner_report.log.", default=False)
# options to configure the simulator
@click.option('--lsf', help='run tests on with lsf clusters, if not set, depend on lsf:is_flag in the file set by --config', default=False)
@click.option('--fsdb', '-f', help='generate fsdb waveform file when running vcs simulator, if not set, depend on vcs:fsdb in the file set by --config', default=False)
@click.option('--tsiloadmem', '-tlm', help='Load binary through TSI instead of backdoor, if not set, depend on vcs:tsiloadmem in the file set by --config', default=False)
@click.option('--vcstimeout', '-vto', help='Number of cycles after which VCS stops, if not set, depend on vcs:vcstimeout in the file set by --config', default=-3333, type=int)
def run(**kwargs):
    """Run verification cases for current target."""
    kwargs['config'] = parse_config_files(kwargs['config'])
    kwargs['pkgroot'] = get_package_root()
    runner.main(Args(**kwargs))


if __name__ == '__main__':
    cli()
