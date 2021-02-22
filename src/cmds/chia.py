import asyncio
import click

from src import __version__
from src.util.default_root import DEFAULT_ROOT_PATH
from src.daemon.server import async_run_daemon

from src.cmds.init import init_cmd
from src.cmds.keys import keys_cmd
from src.cmds.plots import plots_cmd
from src.cmds.wallet import wallet_cmd
from src.cmds.configure import configure_cmd
from src.cmds.show import show_cmd
from src.cmds.start import start_cmd
from src.cmds.stop import stop_cmd
from src.cmds.netspace import netspace_cmd


@click.group(
    help=f"\n  Manage chia blockchain infrastructure ({__version__})\n",
    epilog="Try 'chia start node', 'chia netspace -d 192', or 'chia show -s'."
)
@click.option("--root-path", default=DEFAULT_ROOT_PATH, help="Config file root.", type=click.Path(), show_default=True)
@click.pass_context
def cli(ctx, root_path):
    ctx.ensure_object(dict)
    ctx.obj['root_path'] = root_path
    pass


@cli.command('version', short_help='show version')
def version_cmd():
    print(__version__)


@cli.command('run_daemon', short_help='runs chia daemon')
@click.pass_context
def run_daemon_cmd(ctx):
    return asyncio.get_event_loop().run_until_complete(async_run_daemon(ctx['root_path']))


cli.add_command(keys_cmd)
cli.add_command(plots_cmd)
cli.add_command(wallet_cmd)
cli.add_command(configure_cmd)
cli.add_command(init_cmd)
cli.add_command(show_cmd)
cli.add_command(start_cmd)
cli.add_command(stop_cmd)
cli.add_command(netspace_cmd)

if __name__ == '__main__':
    cli()
