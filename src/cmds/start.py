import asyncio

from .service_groups import all_groups, services_for_groups

from src.daemon.client import create_start_daemon_connection


def make_parser(parser):

    parser.add_argument(
        "group", choices=all_groups(), type=str, nargs="+",
    )
    parser.add_argument(
        "-r", "--restart", action="store_true", help="Restart of running processes",
    )
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="Restart even if process seems to be running and it can't be stopped",
    )
    parser.set_defaults(function=start)


async def async_start(args, parser):
    daemon = await create_start_daemon_connection(args.root_path)

    for service in services_for_groups(args.group):
        print(f"{service}: ", end="", flush=True)
        if await daemon.is_running(service_name=service):
            if args.restart:
                await daemon.stop_service(service_name=service)
                print(f"stopped\n{service}: ", end="", flush=True)
            else:
                print(
                    f"already running, use `-r` to force restart"
                )
                continue
        msg = await daemon.start_service(service_name=service)
        print(f"{msg}")


def start(args, parser):
    return asyncio.get_event_loop().run_until_complete(async_start(args, parser))
